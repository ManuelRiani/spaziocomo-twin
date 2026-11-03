"""Partita doppia per anno, ricostruita dai CSV in dati/.

Per ogni anno produce in contabilita/<anno>/:
  - libro_giornale.csv   una riga per movimento (dare o avere) con il grado di evidenza
  - bilancio_verifica.csv saldi per conto
  - README.md            stato patrimoniale, conto economico, controlli

Ogni scrittura ha un campo `evidenza`:
  documento  -> registrata da un documento (fattura, registro, contratto, visura)
  dedotto    -> movimento non documentato, ricostruito per ipotesi (es. incassi e pagamenti
                senza estratto conto, versamento dei finanziamenti deliberati)
  stima      -> importo calcolato (ammortamenti)
  aggregato  -> importo ricavato da un totale di dichiarazione, senza dettaglio

Uso: python3 scripts/partita_doppia.py   (esce con codice 1 se un controllo fallisce)
"""
import csv
import re
from collections import defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATI = ROOT / "dati"
OUT = ROOT / "contabilita"

CONTI = {
    # Stato patrimoniale – attivo
    "1010": ("Banca c/c", "SP"),
    "1100": ("Crediti verso clienti", "SP"),
    "1200": ("IVA a credito (periodo)", "SP"),
    "1210": ("Erario c/IVA (saldo liquidazioni)", "SP"),
    "1300": ("Depositi cauzionali", "SP"),
    "1400": ("Migliorie su beni di terzi", "SP"),
    "1410": ("Mobili, arredi e attrezzature", "SP"),
    "1490": ("Fondo ammortamento", "SP"),
    # Stato patrimoniale – passivo e netto
    "2000": ("Capitale sociale", "SP"),
    "2100": ("Finanziamenti soci infruttiferi", "SP"),
    "2200": ("Debiti verso fornitori", "SP"),
    "2300": ("IVA a debito (periodo)", "SP"),
    "2900": ("Risultato esercizi precedenti", "SP"),
    # Conto economico
    "4000": ("Ricavi da servizi spazi", "CE"),
    "5000": ("Affitto passivo", "CE"),
    "5010": ("Pulizie", "CE"),
    "5020": ("Energia", "CE"),
    "5030": ("Internet e software", "CE"),
    "5040": ("Commercialista e consulenze", "CE"),
    "5050": ("Manutenzioni", "CE"),
    "5060": ("Spese condominiali", "CE"),
    "5070": ("Imposte, tasse e diritti", "CE"),
    "5080": ("Assicurazioni", "CE"),
    "5090": ("Altri costi", "CE"),
    "5100": ("Ammortamenti", "CE"),
}

CAT_CONTO = {
    "affitto": "5000", "pulizie": "5010", "energia": "5020", "internet": "5030",
    "software": "5030", "commercialista": "5040", "consulenze": "5040",
    "manutenzione": "5050", "varie": "5090", "traslochi": "5090",
    "allestimento": "1410", "lavori_edili": "1400",
}
# voci del foglio spese che non passano dai registri IVA (niente doppio conteggio)
SPESE_EXTRA = {
    "assicurazione": "5080", "inail": "5090", "libri_sociali": "5070",
    "tassa_architetto": "5070", "diritti_registro_bilancio": "5070",
    "amministrazione_condominio": "5060", "diritto_camerale": "5070", "tari": "5070",
}
# ammortamento (stima): anni di vita utile
VITA = {"1400": 6, "1410": 6}

righe = []  # (data, n, conto, dare, avere, descrizione, evidenza)
n_scr = 0


def scrittura(d, descr, evid, movimenti):
    """movimenti: lista di (conto, dare, avere). Verifica la quadratura."""
    global n_scr
    n_scr += 1
    tot_d = round(sum(m[1] for m in movimenti), 2)
    tot_a = round(sum(m[2] for m in movimenti), 2)
    assert abs(tot_d - tot_a) < 0.005, (d, descr, tot_d, tot_a)
    for conto, dare, avere in movimenti:
        if dare or avere:
            righe.append((d, n_scr, conto, round(dare, 2), round(avere, 2), descr, evid))


def f(x):
    return float(x or 0)


# --- costituzione e rapporti con le socie ------------------------------------
scrittura("2025-08-05", "Capitale sociale versato (visura)", "documento",
          [("1010", 5000, 0), ("2000", 0, 5000)])
scrittura("2025-09-25", "Cauzione locazione LA.SER (contratto art. 7)", "documento",
          [("1300", 6000, 0), ("1010", 0, 6000)])
for r in csv.DictReader(open(DATI / "finanziamenti_soci.csv")):
    x = f(r["importo_totale"])
    scrittura(r["data_delibera"],
              "Finanziamento soci deliberato; versamento in banca non documentato",
              "dedotto", [("1010", x, 0), ("2100", 0, x)])

# --- acquisti 2025 non dettagliati (settembre): dalla dichiarazione IVA ------
# credito annuo dichiarato 2.115,00 - credito dei registri Q4 1.778,60 = 336,40
iva_agg = 336.40
imp_agg = round(iva_agg / 0.22, 2)
scrittura("2025-09-30", "Acquisti Q3 2025 non dettagliati (da dichiarazione IVA, natura non nota)",
          "aggregato", [("5090", imp_agg, 0), ("1200", iva_agg, 0), ("2200", 0, imp_agg + iva_agg)])
scrittura("2025-09-30", "Pagamento acquisti Q3 2025", "dedotto",
          [("2200", imp_agg + iva_agg, 0), ("1010", 0, imp_agg + iva_agg)])
IVA_TRIM = defaultdict(lambda: [0.0, 0.0])  # trimestre -> [debito, credito]
IVA_TRIM["2025T3"][1] += iva_agg

# --- acquisti dai registri ---------------------------------------------------
cespiti = []  # (data, conto, costo)
for r in csv.DictReader(open(DATI / "acquisti_registro_iva.csv")):
    imp, iva, ni = f(r["imponibile"]), f(r["iva"]), f(r["non_imponibile"])
    conto = CAT_CONTO[r["categoria"]]
    m = r["mese_registro"]
    d = r["data"] if r["data"][:7] == m else f"{m}-01"
    trim = f"{m[:4]}T{(int(m[5:]) - 1) // 3 + 1}"
    indetr = "indetraibile" in r["note"].lower()
    costo = imp + ni + (iva if indetr else 0)
    tot = imp + iva + ni
    descr = f"Fattura {r['fornitore']} ({r['categoria']})"
    if r["reverse_charge"] == "si":
        scrittura(d, descr + " – reverse charge", "documento",
                  [(conto, imp, 0), ("1200", iva, 0), ("2200", 0, imp), ("2300", 0, iva)])
        IVA_TRIM[trim][0] += iva
        IVA_TRIM[trim][1] += iva
        pag = imp
    else:
        mov = [(conto, costo, 0), ("2200", 0, tot)]
        if not indetr:
            mov.append(("1200", iva, 0))
            IVA_TRIM[trim][1] += iva
        scrittura(d, descr, "documento", mov)
        pag = tot
    if conto in VITA:
        cespiti.append((d, conto, costo))
    scrittura(d, f"Pagamento {r['fornitore']}", "dedotto",
              [("2200", pag, 0), ("1010", 0, pag)])

# --- ricavi ------------------------------------------------------------------
for r in csv.DictReader(open(DATI / "ricavi_fatture.csv")):
    imp, iva = f(r["imponibile"]), f(r["iva"])
    d = r["data"]
    trim = f"{d[:4]}T{(int(d[5:7]) - 1) // 3 + 1}"
    scrittura(d, f"Fattura n. {r['numero']}/{d[:4]} a {r['cliente']}", "documento",
              [("1100", imp + iva, 0), ("4000", 0, imp), ("2300", 0, iva)])
    IVA_TRIM[trim][0] += iva
    scrittura(d, f"Incasso da {r['cliente']}", "dedotto",
              [("1010", imp + iva, 0), ("1100", 0, imp + iva)])

# --- periodo coperto dai registri -------------------------------------------
fine_registri = max(r[0] for r in righe if r[6] == "documento" and r[5].startswith("Fattura"))
ultimo_mese = fine_registri[:7]

# --- spese di cassa non fatturate (foglio spese), entro il periodo coperto ---
for r in csv.DictReader(open(DATI / "spese_cassa_mensili.csv")):
    if r["voce"] in SPESE_EXTRA and r["mese"] <= ultimo_mese:
        x = f(r["importo_lordo"])
        scrittura(f"{r['mese']}-15", f"{r['voce']} (foglio spese)", "documento",
                  [(SPESE_EXTRA[r["voce"]], x, 0), ("1010", 0, x)])

# --- liquidazioni IVA trimestrali --------------------------------------------
for trim in sorted(IVA_TRIM):
    deb, cred = (round(v, 2) for v in IVA_TRIM[trim])
    y, q = int(trim[:4]), int(trim[-1])
    d = date(y, q * 3, [31, 30, 30, 31][q - 1]).isoformat()
    if d[:7] > ultimo_mese:
        continue
    saldo = round(cred - deb, 2)
    mov = [("2300", deb, 0), ("1200", 0, cred)]
    mov.append(("1210", saldo, 0) if saldo > 0 else ("1210", 0, -saldo))
    scrittura(d, f"Liquidazione IVA {trim}", "documento", mov)

# --- ammortamenti (stima), pro rata mensile fino alla fine del periodo --------
anni = sorted({r[0][:4] for r in righe})
for anno in anni:
    fine = f"{anno}-12" if f"{anno}-12" <= ultimo_mese else ultimo_mese
    quota = defaultdict(float)
    for d, conto, costo in cespiti:
        inizio = max(d[:7], f"{anno}-01")
        if inizio > fine:
            continue
        mesi = (int(fine[:4]) - int(inizio[:4])) * 12 + int(fine[5:]) - int(inizio[5:]) + 1
        quota[conto] += costo / (VITA[conto] * 12) * mesi
    tot = round(sum(quota.values()), 2)
    if tot:
        scrittura(f"{fine}-28" if fine[5:] == "02" else f"{fine}-30",
                  f"Ammortamento {anno} (vita utile {VITA['1400']} anni, pro rata mensile)",
                  "stima", [("5100", tot, 0), ("1490", 0, tot)])

righe.sort(key=lambda r: (r[0], r[1]))

# --- output per anno ---------------------------------------------------------
LIQ = {(r["anno"], r["periodo"]): f(r["credito_cumulato_fine_periodo"])
       for r in csv.DictReader(open(DATI / "liquidazioni_iva.csv"))}
RIC_ATTESI = defaultdict(float)  # operazioni attive dalle liquidazioni (al netto reverse charge)
for r in csv.DictReader(open(DATI / "liquidazioni_iva.csv")):
    RIC_ATTESI[r["anno"]] += f(r["operazioni_attive"])

esito_ok = True
risultato_prec = 0.0
for anno in anni:
    dir_ = OUT / anno
    dir_.mkdir(parents=True, exist_ok=True)
    gio = [r for r in righe if r[0][:4] == anno]
    with open(dir_ / "libro_giornale.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["data", "scrittura", "conto", "nome_conto", "dare", "avere",
                    "descrizione", "evidenza"])
        for d, n, c, da, av, ds, ev in gio:
            w.writerow([d, n, c, CONTI[c][0], f"{da:.2f}", f"{av:.2f}", ds, ev])

    saldi = defaultdict(float)
    for d, n, c, da, av, ds, ev in righe:
        if CONTI[c][1] == "SP" and d[:4] <= anno or CONTI[c][1] == "CE" and d[:4] == anno:
            saldi[c] += da - av
    saldi["2900"] -= risultato_prec  # perdita = saldo dare
    ricavi = -saldi["4000"]
    costi = sum(v for c, v in saldi.items() if CONTI[c][1] == "CE" and c != "4000")
    risultato = round(ricavi - costi, 2)

    with open(dir_ / "bilancio_verifica.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["conto", "nome", "sezione", "saldo_dare", "saldo_avere"])
        for c in sorted(saldi):
            v = round(saldi[c], 2)
            if abs(v) >= 0.005:
                w.writerow([c, CONTI[c][0], CONTI[c][1], f"{max(v, 0):.2f}", f"{max(-v, 0):.2f}"])

    # controlli
    ctrl = []
    tot_d = round(sum(r[3] for r in gio), 2)
    tot_a = round(sum(r[4] for r in gio), 2)
    ctrl.append(("Totale dare = totale avere", f"{tot_d:,.2f} / {tot_a:,.2f}", tot_d == tot_a))
    sp = round(sum(v for c, v in saldi.items() if CONTI[c][1] == "SP"), 2)
    ctrl.append(("Attivo − passivo = risultato d'esercizio", f"{sp:,.2f} / {risultato:,.2f}",
                 abs(sp - risultato) < 0.01))
    atteso = RIC_ATTESI.get(anno)
    if atteso is not None:
        ctrl.append(("Ricavi = registri IVA vendite", f"{ricavi:,.2f} / {atteso:,.2f}",
                     abs(ricavi - atteso) < 0.01))
    cum = 0.0
    for trim in sorted(IVA_TRIM):
        deb, cred = IVA_TRIM[trim]
        cum += cred - deb
        y, q = trim[:4], trim[-1]
        chiave = (y, "anno") if y == "2025" and q == "4" else (y, f"T{q}")
        if y == anno and chiave in LIQ:
            ctrl.append((f"Credito IVA cumulato a fine {trim} = liquidazione",
                         f"{cum:,.2f} / {-LIQ[chiave]:,.2f}", abs(cum + LIQ[chiave]) < 0.01))
    esito_ok &= all(c[2] for c in ctrl)

    per_evid = defaultdict(float)
    for r in gio:
        per_evid[r[6]] += r[3]

    def riga(c):
        return f"| {c} {CONTI[c][0]} | {abs(saldi[c]):,.2f} |"

    att = [c for c in sorted(saldi) if CONTI[c][1] == "SP" and saldi[c] > 0.005]
    pas = [c for c in sorted(saldi) if CONTI[c][1] == "SP" and saldi[c] < -0.005]
    ce_c = [c for c in sorted(saldi) if CONTI[c][1] == "CE" and c != "4000" and abs(saldi[c]) > 0.005]
    periodo = f"01/01/{anno} – 31/12/{anno}" if f"{anno}-12" <= ultimo_mese else \
        f"01/01/{anno} – fine {ultimo_mese} (**periodo parziale**: ultimi registri IVA disponibili)"

    md = [f"# Partita doppia {anno}", "",
          f"Periodo: {periodo}. Generato da `scripts/partita_doppia.py` sui CSV di `dati/`.", "",
          "> Ricostruzione gestionale, **non** è la contabilità ufficiale del commercialista. "
          "Ogni movimento in `libro_giornale.csv` ha il suo grado di evidenza.", "",
          "## Evidenza dei movimenti (totale dare)", "",
          "| Evidenza | € | Significato |", "|---|---|---|"]
    signif = {"documento": "da fattura, registro, contratto, visura o foglio spese",
              "dedotto": "**[dedotto]** incassi, pagamenti e versamenti senza estratto conto",
              "stima": "**stima** ammortamenti",
              "aggregato": "totale da dichiarazione IVA senza dettaglio"}
    for e in ["documento", "dedotto", "stima", "aggregato"]:
        if per_evid.get(e):
            md.append(f"| {e} | {per_evid[e]:,.2f} | {signif[e]} |")
    md += ["", "## Stato patrimoniale", "", "| Attivo | € |", "|---|---|"]
    md += [riga(c) for c in att]
    md += ["", "| Passivo e netto | € |", "|---|---|"]
    md += [riga(c) for c in pas]
    md += [f"| Risultato dell'esercizio | {risultato:,.2f} |", "",
           "Il fondo ammortamento è una rettifica dell'attivo: compare tra le voci in avere. "
           "Il risultato degli esercizi precedenti, se negativo, compare in attivo.", "",
           "## Conto economico", "", "| Voce | € |", "|---|---|",
           f"| 4000 Ricavi da servizi spazi | {ricavi:,.2f} |"]
    md += [f"| {c} {CONTI[c][0]} | −{saldi[c]:,.2f} |" for c in ce_c]
    md += [f"| **Risultato** | **{risultato:,.2f}** |", "",
           "## Controlli", "", "| Controllo | Valori | Esito |", "|---|---|---|"]
    md += [f"| {a} | {b} | {'OK' if ok else '**ERRORE**'} |" for a, b, ok in ctrl]
    md += ["", "## Limiti noti", "",
           "- **[dedotto]** Saldo banca: incassi e pagamenti sono registrati alla data della fattura "
           "e i finanziamenti soci alla data della delibera, senza estratto conto. "
           "Crediti e debiti commerciali risultano quindi a zero per costruzione.",
           "- Le fatture sono imputate al mese del **registro IVA**, non alla competenza economica.",
           "- **[dedotto]** Classificazione dei costi e capitalizzazione di lavori e allestimento: vedi `dati/README.md`.",
           "- **stima** Ammortamento a quote costanti su 6 anni (durata della locazione), pro rata mensile.",
           "- Ritenute d'acconto sui professionisti, imposte sul reddito (IRES/IRAP) e ratei/risconti non sono rilevati.",
           "- Le spese del foglio non fatturate sono registrate al giorno 15 del mese indicato.", ""]
    if anno == "2025":
        md.insert(-1, "- **aggregato** Acquisti di settembre 2025 (€ "
                  f"{imp_agg:,.2f} + IVA {iva_agg:,.2f}): ricavati dalla differenza tra credito IVA "
                  "dichiarato e registri Q4; registro Q3 2025 non disponibile.")
    testo = re.sub(r"-?\d{1,3}(?:,\d{3})*\.\d{2}",
                   lambda m: m.group(0).replace(",", "_").replace(".", ",").replace("_", "."),
                   "\n".join(md))
    (dir_ / "README.md").write_text(testo)
    risultato_prec += risultato
    print(f"{anno}: risultato {risultato:,.2f}; controlli "
          + ", ".join("OK" if c[2] else "ERRORE" for c in ctrl))

raise SystemExit(0 if esito_ok else 1)
