#!/usr/bin/env python3
"""Registro dei contratti di servizio con i professionisti.

Trascrizione dei contratti firmati nella cartella Drive "CONTRATTI SERVIZI"
(letti il 2026-11-03). Genera:
  - dati/contratti.csv
  - contratti/registro/<id>.md  (una scheda per contratto)

Privacy: i professionisti compaiono solo con il codice CLI-xx del Google Sheet
"Codici anagrafica - gemello SpazioComo". Non si trascrivono nomi, codici
fiscali, P.IVA, indirizzi, date di nascita, numeri di iscrizione all'albo,
numeri di polizza, né i titoli dei file Drive (contengono il cognome).
La professione dei terzi è ridotta a una categoria generica.

Uso: python3 scripts/build_contratti.py
"""
import csv
import os
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OGGI = date(2026, 11, 3)  # data di lettura dei contratti

# Modelli: tariffe e regole comuni (vedi contratti/modelli/)
MODELLI = {
    "socia": dict(
        nome="Fisso con stanza dedicata (socie)",
        file="modelli/fisso-socia.md",
        canone=819.67, ore=None, extra=None, noshow=None,
        pagamento="anticipato entro il 5 del mese",
        preavviso_mesi=3, patto=True),
    "fisso-v1": dict(
        nome="Fisso mezza giornata, listino feb 2026",
        file="modelli/fisso-mezza-giornata.md",
        canone=195.00, ore=None, extra=10.66, noshow=None,
        pagamento="anticipato entro il 5 del mese",
        preavviso_mesi=3, patto=True),
    "fisso-v2": dict(
        nome="Fisso mezza giornata, listino set 2026",
        file="modelli/fisso-mezza-giornata.md",
        canone=195.00, ore=None, extra=14.75, noshow=None,
        pagamento="anticipato entro il 5 del mese",
        preavviso_mesi=3, patto=True),
    "spot-v1": dict(
        nome="Spot (a ore), listino feb 2026",
        file="modelli/spot.md",
        canone=None, ore=10.66, extra=None, noshow=5.74,
        pagamento="entro 5 giorni dalla fattura",
        preavviso_mesi=3, patto=True),
    "spot-v2": dict(
        nome="Spot (a ore), listino set 2026",
        file="modelli/spot.md",
        canone=None, ore=14.75, extra=None, noshow=7.37,
        pagamento="entro 5 giorni dalla fattura",
        preavviso_mesi=3, patto=True),
    "speciale": dict(
        nome="Spot con stanza 3 ed esclusiva di categoria",
        file="modelli/speciale-stanza3.md",
        canone=None, ore=25.00, extra=None, noshow=12.50,
        pagamento="entro 5 giorni dalla fattura",
        preavviso_mesi=1, patto=False),
}

# id, codice, categoria, modello, inizio, fine, mesi dichiarati, stanza,
# fascia (solo fissi), cartella Drive, ID file Drive, note
C = [
    ("C01", "SOC-VG", "musicoterapia", "socia", "2026-02-01", "2026-08-01", 6,
     "3 Orchestra", "", "1. CONTRATTI ATTIVI", "1hJZDmT26pd62V7utOdoZTpS0jAUe9alw", ""),
    ("C02", "SOC-EB", "logopedia", "socia", "2026-02-01", "2026-08-01", 6,
     "5 Voce", "", "1. CONTRATTI ATTIVI", "1FS089v_OAtaXkTy65xoYHVikvu3pF-34", ""),
    ("C03", "SOC-RM", "neuropsicomotricità (TNPEE)", "socia", "2026-02-01", "2026-08-01", 6,
     "4 Ritmo", "", "1. CONTRATTI ATTIVI", "1DJ5HZDS3XJ7tDAgixJEeaAb5DHoh9luN", ""),
    ("C04", "CLI-10", "area educativa / arti terapie", "spot-v1", "2026-02-01", "2026-08-01", 6,
     "", "", "CONCLUSI", "1exkhsSWBtGiUsc_kha_vTily7DVJgQdN", ""),
    ("C05", "CLI-11", "area educativa / perinatale", "spot-v1", "2026-02-02", "2026-08-02", 6,
     "", "", "CONCLUSI", "1pFEMNl73EIkcjWPTxpjZW2e7zl5CTQRx", ""),
    ("C06", "CLI-01", "area sanitaria (iscritta a ordine)", "fisso-v1", "2026-03-02", "2026-09-02", 6,
     "", "martedì pomeriggio (dalle 13)", "CONCLUSI", "16G7vpjOR3pgUY5O2HlZvbVfmlc-M_fFt", "sostituito da C15"),
    ("C07", "CLI-02", "area educativa / arti terapie", "fisso-v1", "2026-03-02", "2026-09-02", 6,
     "", "giovedì pomeriggio (dalle 13)", "CONCLUSI", "1Fyh2iNhetu5-3t026ImZlJXGAhVR5sMr", "sostituito da C16"),
    ("C08", "CLI-03", "area sanitaria (iscritta a ordine)", "fisso-v1", "2026-03-02", "2026-09-02", 6,
     "", "martedì mattina (fino alle 13)", "CONCLUSI", "1AjeZYkbQJJLFBep3j3xArJiCi-dvijk_", "dal 29/10/2026 passa allo spot (C21)"),
    ("C09", "CLI-04", "area sanitaria (iscritta a ordine)", "fisso-v1", "2026-03-02", "2026-09-02", 6,
     "", "giovedì pomeriggio (dalle 13)", "CONCLUSI", "1OwNpuu4cMUYhiBfhDh1UMxbusDG_rEY5", "sostituito da C17"),
    ("C10", "CLI-07", "area sanitaria (iscritta a ordine)", "spot-v1", "2026-03-02", "2026-09-02", 6,
     "", "", "CONCLUSI", "1hxHCVgrjzFe_CuLPHpUdugilitfsWm0h", "sostituito da C18"),
    ("C11", "CLI-08", "area educativa / famiglia", "spot-v1", "2026-03-02", "2026-09-02", 6,
     "", "", "ALLEGATI CONTRATTO", "11IyKztFhWbIBvT499Vh7ViUp2Cvs_SGb", "sostituito da C19; il PDF è nella cartella degli allegati, non in CONCLUSI"),
    ("C12", "CLI-09", "attività non sanitaria (servizi alle famiglie)", "speciale", "2026-03-09", "2026-06-09", 3,
     "3 Orchestra", "", "CONCLUSI", "1ddiO5vxbfrsmQgY_QPNHR6z7g2iZ6ru1", "sostituito da C14"),
    ("C13", "CLI-06", "area educativa / famiglia", "spot-v1", "2026-05-15", "2026-09-15", 4,
     "", "", "CONCLUSI", "158UXM6b6xVyZkbPXNd1bw6uytReBZ72f", "sostituito da C20"),
    ("C14", "CLI-09", "attività non sanitaria (servizi alle famiglie)", "speciale", "2026-06-10", "2026-12-10", 6,
     "3 Orchestra", "", "1. CONTRATTI ATTIVI", "1hFqCwhs_k1SVdL3YO9UZWVwRaXDuvWBw",
     "nel testo la fine è 10.12.2027, incoerente con '6 mesi': qui 10/12/2026 **[dedotto]**"),
    ("C15", "CLI-01", "area sanitaria (iscritta a ordine)", "fisso-v2", "2026-09-03", "2027-09-03", 12,
     "", "martedì pomeriggio (dalle 13)", "1. CONTRATTI ATTIVI", "1A5gC1WbfGq0QwnNx2qKks5wqg2D1UJQG", ""),
    ("C16", "CLI-02", "area educativa / arti terapie", "fisso-v2", "2026-09-03", "2027-09-03", 12,
     "", "giovedì pomeriggio (dalle 13)", "1. CONTRATTI ATTIVI", "1LWdyRsD7n4sS2VBvir4e6PTfsy7pt4Y7", ""),
    ("C17", "CLI-04", "area sanitaria (iscritta a ordine)", "fisso-v2", "2026-09-03", "2027-09-03", 12,
     "", "giovedì pomeriggio (dalle 13)", "1. CONTRATTI ATTIVI", "1uIofkWiVSadcp_Jxs7b68zfhSvOMF3Yv", ""),
    ("C18", "CLI-07", "area sanitaria (iscritta a ordine)", "spot-v2", "2026-09-03", "2027-09-03", 12,
     "", "", "1. CONTRATTI ATTIVI", "1WoEoR-yJgCKrlkUy_p6Di0vGuk-IfLpD", ""),
    ("C19", "CLI-08", "area educativa / famiglia", "spot-v2", "2026-09-03", "2027-09-03", 12,
     "", "", "1. CONTRATTI ATTIVI", "1lV7AaLPxupjBIShghV9PQsmcrX07M9U2", "senza P.IVA nel contratto"),
    ("C20", "CLI-06", "area educativa / famiglia", "spot-v2", "2026-09-16", "2027-09-16", 12,
     "", "", "1. CONTRATTI ATTIVI", "1-BNwHRuLy7x2I3ZCTGbSdM5csRSe_3zD", "senza P.IVA nel contratto"),
    ("C21", "CLI-03", "area sanitaria (iscritta a ordine)", "spot-v2", "2026-10-29", "2027-10-29", 12,
     "", "", "1. CONTRATTI ATTIVI", "1ZaZDf0PYmhlwj-bLNTSZRiFgZNGKu7ET", "scoperto dal 02/09 al 29/10/2026"),
    ("C22", "CLI-12", "area sanitaria (iscritta a registro)", "spot-v2", "2026-11-04", "2027-05-04", 6,
     "", "", "1. CONTRATTI ATTIVI", "13gNjW72Q2b1bBXzohi4b7gNPQz8eWgkL", "decorre dal giorno dopo la lettura"),
]

FIELDS = ["id", "codice", "categoria", "modello", "inizio", "fine", "mesi",
          "stanza", "fascia_fissa", "canone_mese", "tariffa_ora",
          "extra_ora", "noshow_ora", "preavviso_mesi", "stato_al_2026_11_03",
          "cartella_drive", "drive_id", "note"]


def stato(inizio, fine, cartella):
    i, f = date.fromisoformat(inizio), date.fromisoformat(fine)
    if i > OGGI:
        return "firmato, non ancora iniziato"
    if f >= OGGI:
        return "in corso"
    if cartella == "1. CONTRATTI ATTIVI":
        return "scaduto sulla carta, ma archiviato tra gli attivi"
    return "concluso"


def eur(x):
    return "" if x is None else f"{x:.2f}".replace(".", ",")


def main():
    righe = []
    for (cid, cod, cat, mod, ini, fin, mesi, stz, fascia, cart, did, note) in C:
        m = MODELLI[mod]
        righe.append(dict(
            id=cid, codice=cod, categoria=cat, modello=mod, inizio=ini,
            fine=fin, mesi=mesi, stanza=stz, fascia_fissa=fascia,
            canone_mese=eur(m["canone"]), tariffa_ora=eur(m["ore"]),
            extra_ora=eur(m["extra"]), noshow_ora=eur(m["noshow"]),
            preavviso_mesi=m["preavviso_mesi"],
            stato_al_2026_11_03=stato(ini, fin, cart),
            cartella_drive=cart, drive_id=did, note=note))

    with open(os.path.join(ROOT, "dati", "contratti.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(righe)

    out = os.path.join(ROOT, "contratti", "registro")
    os.makedirs(out, exist_ok=True)
    for r in righe:
        m = MODELLI[r["modello"]]
        prezzo = []
        if r["canone_mese"]:
            prezzo.append(f"- Canone: **€ {r['canone_mese']} + IVA al mese**, {m['pagamento']}")
        if r["tariffa_ora"]:
            prezzo.append(f"- Tariffa: **€ {r['tariffa_ora']} + IVA all'ora** di uso effettivo, {m['pagamento']}")
        if r["extra_ora"]:
            prezzo.append(f"- Ore oltre la mezza giornata inclusa: € {r['extra_ora']} + IVA all'ora")
        if r["noshow_ora"]:
            prezzo.append(f"- Ora prenotata e non usata: € {r['noshow_ora']} + IVA")
        if r["fascia_fissa"]:
            prezzo.append(f"- Uso incluso: 1 mezza giornata **a settimana** (confermato da Manuel Riani il 2026-11-03; il testo firmato dice per errore «al mese»), {r['fascia_fissa']}")
        if r["stanza"]:
            prezzo.append(f"- Stanza: n. {r['stanza']}")
        testo = f"""# {r['id']} – {r['codice']}

Generato da `scripts/build_contratti.py`: non modificare a mano.

| Campo | Valore |
|---|---|
| Utilizzatore | `{r['codice']}` ({r['categoria']}) |
| Modello | [{m['nome']}](../{m['file']}) |
| Durata | {r['mesi']} mesi, dal {r['inizio']} al {r['fine']} |
| Stato al 2026-11-03 | {r['stato_al_2026_11_03']} |
| Preavviso di recesso | {r['preavviso_mesi']} mesi, raccomandata A/R |
| Patto di collaborazione | {'sì (allegato B)' if m['patto'] else 'no'} |
| Fonte | Drive, cartella "CONTRATTI SERVIZI / {r['cartella_drive']}", ID `{r['drive_id']}` |

## Condizioni economiche

{chr(10).join(prezzo)}

## Note

{r['note'] or '—'}

Il testo completo coincide con il modello, salvo i campi sopra. Dati anagrafici, iscrizione all'albo e polizza RC sono nel documento originale e non vengono trascritti.
"""
        with open(os.path.join(out, f"{r['id']}.md"), "w") as fh:
            fh.write(testo)

    print(f"{len(righe)} contratti -> dati/contratti.csv, contratti/registro/")


if __name__ == "__main__":
    main()
