"""Grafici del gemello SpazioComo, generati dai CSV di dati/ e contabilita/.

Produce in grafici/:
  README.md                      struttura societaria + panoramica su tutti gli anni + link agli anni
  struttura_societaria.svg       grafo di soci, governance e controparti (richiede Graphviz `dot`)
  panoramica_*.svg               andamenti su tutto il periodo coperto
  <anno>/README.md               tutti i grafici dell'anno in una sola pagina
  <anno>/*.svg                   grafici dell'anno

Va eseguito dopo scripts/partita_doppia.py (legge libro giornale e bilancio di verifica).
Uso: python3 scripts/grafici.py
Dipendenze: matplotlib; Graphviz (`dot`) per il grafo della struttura (se manca, viene scritto solo il .dot).
"""
import csv
import shutil
import subprocess
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import PathPatch, Rectangle  # noqa: E402
from matplotlib.path import Path as MPath  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DATI = ROOT / "dati"
CONT = ROOT / "contabilita"
OUT = ROOT / "grafici"

# SVG riproducibili: stesso input -> stesso file (diff git puliti)
plt.rcParams.update({
    "svg.hashsalt": "spaziocomo",
    "svg.fonttype": "path",
    "font.size": 10,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.3,
    "axes.axisbelow": True,
})

MESI = ["gen", "feb", "mar", "apr", "mag", "giu", "lug", "ago", "set", "ott", "nov", "dic"]

# Socie: dati da societa/anagrafica.md (visura 09/09/2025; professione e regime comunicati il 03/11/2026)
SOCIE = [
    ("SOC-VG", "Valentina Giacosa", "musicoterapista", "33,34%", "€ 1.667"),
    ("SOC-EB", "Erica Bertoni", "logopedista", "33,34%", "€ 1.667"),
    ("SOC-RM", "Roberta Mauri", "psicomotricista", "33,32%", "€ 1.666"),
]
COL_SOCIE = {"SOC-VG": "#4C72B0", "SOC-EB": "#55A868", "SOC-RM": "#C44E52"}
COL_TERZI = "#8C8C8C"

# Raggruppamento dei conti di costo per i grafici
GRUPPI_COSTO = {
    "5000": "Affitto", "5010": "Pulizie", "5020": "Energia",
    "5040": "Commercialista e consulenze", "5100": "Ammortamenti (stima)",
}
COL_COSTI = {
    "Affitto": "#4C72B0", "Pulizie": "#64B5CD", "Energia": "#DD8452",
    "Commercialista e consulenze": "#8172B3", "Altri costi": "#937860",
    "Ammortamenti (stima)": "#CCCCCC",
}


def euro(x, dec=0):
    s = f"{abs(x):,.{dec}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return ("−" if x < 0 else "") + "€ " + s


def leggi(p):
    with open(p, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def salva(fig, path):
    from matplotlib.ticker import FuncFormatter
    for ax in fig.axes:
        if "€" in ax.get_ylabel():
            ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:,.0f}".replace(",", ".")))
    fig.savefig(path, format="svg", bbox_inches="tight", metadata={"Date": None})
    plt.close(fig)


def etichetta_mese(m):
    a, mm = m.split("-")
    return f"{MESI[int(mm) - 1]} {a[2:]}"


def gruppo(conto):
    return GRUPPI_COSTO.get(conto, "Altri costi")


# ---------------------------------------------------------------- dati di base
anni = sorted(int(p.name) for p in CONT.iterdir() if p.is_dir() and p.name.isdigit())
giornale = {a: leggi(CONT / str(a) / "libro_giornale.csv") for a in anni}
bilancio = {a: {r["conto"]: r for r in leggi(CONT / str(a) / "bilancio_verifica.csv")} for a in anni}
ricavi = leggi(DATI / "ricavi_fatture.csv")
acquisti = leggi(DATI / "acquisti_registro_iva.csv")
liquidazioni = leggi(DATI / "liquidazioni_iva.csv")
finanziamenti = leggi(DATI / "finanziamenti_soci.csv")


def saldo(a, conto):
    r = bilancio[a].get(conto)
    return float(r["saldo_dare"]) - float(r["saldo_avere"]) if r else 0.0


def ce_mensile(a):
    """{mese: {'ricavi': x, gruppo: costo}} dal libro giornale (competenza)."""
    out = defaultdict(lambda: defaultdict(float))
    for r in giornale[a]:
        c, m = r["conto"], r["data"][:7]
        d, av = float(r["dare"]), float(r["avere"])
        if c.startswith("4"):
            out[m]["ricavi"] += av - d
        elif c.startswith("5"):
            out[m][gruppo(c)] += d - av
    return out


def periodo(a):
    mesi = sorted(ce_mensile(a))
    return mesi[0], mesi[-1]


def ricavi_anno(a):
    return [r for r in ricavi if r["anno"] == str(a)]


# ---------------------------------------------------------------- grafici per anno
def g_ricavi_costi_mensili(a, path):
    ce = ce_mensile(a)
    mesi = sorted(ce)
    gruppi = [g for g in COL_COSTI if any(ce[m].get(g) for m in mesi)]
    x = range(len(mesi))
    fig, (ax, bx) = plt.subplots(2, 1, figsize=(9, 6.5), height_ratios=[3, 2], sharex=True)
    w = 0.38
    ax.bar([i - w / 2 for i in x], [ce[m]["ricavi"] for m in mesi], w, color="#2E7D32", label="Ricavi")
    base = [0.0] * len(mesi)
    for g in gruppi:
        v = [ce[m].get(g, 0.0) for m in mesi]
        ax.bar([i + w / 2 for i in x], v, w, bottom=base, color=COL_COSTI[g], label=g)
        base = [b + y for b, y in zip(base, v)]
    mens = [ce[m]["ricavi"] - sum(ce[m].get(g, 0.0) for g in gruppi) for m in mesi]
    cum, s = [], 0.0
    for v in mens:
        s += v
        cum.append(s)
    ax.set_xticks(list(x), [etichetta_mese(m) for m in mesi])
    ax.set_ylabel("€ (imponibile)")
    ax.set_title(f"{a} – Ricavi e costi per mese (competenza)")
    ax.legend(fontsize=8, loc="upper left", bbox_to_anchor=(1, 1))
    bx.bar(list(x), mens, 0.6, color=["#2E7D32" if v >= 0 else "#E53935" for v in mens], alpha=0.6,
           label="Risultato del mese")
    bx.plot(list(x), cum, color="black", marker="o", lw=1.5, label="Risultato cumulato")
    for i, v in enumerate(cum):
        bx.annotate(euro(v), (i, v), textcoords="offset points", xytext=(0, -13), ha="center", fontsize=7)
    bx.axhline(0, color="black", lw=0.8)
    bx.set_xticks(list(x), [etichetta_mese(m) for m in mesi])
    bx.set_ylabel("€")
    bx.legend(fontsize=8, loc="upper left", bbox_to_anchor=(1, 1))
    salva(fig, path)


def g_torta_costi(a, path):
    tot = defaultdict(float)
    for c, r in bilancio[a].items():
        if c.startswith("5"):
            tot[gruppo(c)] += float(r["saldo_dare"]) - float(r["saldo_avere"])
    voci = [(g, tot[g]) for g in COL_COSTI if tot.get(g, 0) > 0]
    totale = sum(v for _, v in voci)
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.pie([v for _, v in voci], colors=[COL_COSTI[g] for g, _ in voci], startangle=90, counterclock=False,
           autopct=lambda p: f"{p:.0f}%" if p >= 4 else "", pctdistance=0.75,
           wedgeprops={"width": 0.5, "edgecolor": "white"})
    ax.text(0, 0, f"Totale\n{euro(totale)}", ha="center", va="center", fontsize=11, weight="bold")
    ax.legend([f"{g}  {euro(v)}" for g, v in voci], loc="center left", bbox_to_anchor=(1, 0.5), fontsize=9)
    ax.set_title(f"{a} – Composizione dei costi (conto economico)")
    salva(fig, path)


def g_torta_clienti(a, path):
    per = defaultdict(float)
    for r in ricavi_anno(a):
        per[r["cliente"]] += float(r["imponibile"])
    socie = [(c, per[c]) for c, *_ in SOCIE if per.get(c)]
    terzi = sum(v for c, v in per.items() if not c.startswith("SOC-"))
    voci = socie + ([("Terzi (CLI-xx)", terzi)] if terzi else [])
    colori = [COL_SOCIE.get(c, COL_TERZI) for c, _ in voci]
    tot = sum(v for _, v in voci)
    quota_socie = sum(v for _, v in socie) / tot * 100
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.pie([v for _, v in voci], colors=colori, startangle=90, counterclock=False,
           autopct=lambda p: f"{p:.0f}%", pctdistance=0.75, wedgeprops={"width": 0.5, "edgecolor": "white"})
    ax.text(0, 0, f"Socie\n{quota_socie:.0f}%", ha="center", va="center", fontsize=12, weight="bold")
    ax.legend([f"{c}  {euro(v)}" for c, v in voci], loc="center left", bbox_to_anchor=(1, 0.5), fontsize=9)
    ax.set_title(f"{a} – Ricavi per cliente (imponibile {euro(tot)})")
    salva(fig, path)


def g_ricavi_clienti_mensili(a, path):
    per = defaultdict(lambda: defaultdict(float))
    for r in ricavi_anno(a):
        per[r["data"][:7]][r["cliente"]] += float(r["imponibile"])
    mesi = sorted(per)
    terzi = sorted({c for m in mesi for c in per[m] if not c.startswith("SOC-")})
    serie = [c for c, *_ in SOCIE] + terzi
    grigi = plt.cm.Greys([0.3 + 0.5 * i / max(len(terzi) - 1, 1) for i in range(len(terzi))])
    colori = [COL_SOCIE[c] for c, *_ in SOCIE] + list(grigi)
    fig, ax = plt.subplots(figsize=(9, 4.5))
    base = [0.0] * len(mesi)
    for c, col in zip(serie, colori):
        v = [per[m].get(c, 0.0) for m in mesi]
        if any(v):
            ax.bar(range(len(mesi)), v, 0.6, bottom=base, color=col, label=c, edgecolor="white", lw=0.5)
            base = [b + y for b, y in zip(base, v)]
    ax.set_xticks(range(len(mesi)), [etichetta_mese(m) for m in mesi])
    ax.set_ylabel("€ (imponibile)")
    ax.set_title(f"{a} – Ricavi per mese e per cliente (data fattura)")
    ax.legend(fontsize=8, loc="upper left", bbox_to_anchor=(1, 1))
    salva(fig, path)


def nastro(ax, x0, y0a, y0b, x1, y1a, y1b, colore):
    """Banda curva da (x0, y0a..y0b) a (x1, y1a..y1b)."""
    xm = (x0 + x1) / 2
    verts = [(x0, y0a), (xm, y0a), (xm, y1a), (x1, y1a), (x1, y1b), (xm, y1b), (xm, y0b), (x0, y0b), (x0, y0a)]
    codes = [MPath.MOVETO, MPath.CURVE4, MPath.CURVE4, MPath.CURVE4, MPath.LINETO,
             MPath.CURVE4, MPath.CURVE4, MPath.CURVE4, MPath.CLOSEPOLY]
    ax.add_patch(PathPatch(MPath(verts, codes), facecolor=colore, alpha=0.45, lw=0))


def g_flusso_economico(a, path):
    """Sankey: da dove arrivano i ricavi -> dove vanno (costi) -> risultato."""
    per = defaultdict(float)
    for r in ricavi_anno(a):
        k = r["cliente"] if r["cliente"].startswith("SOC-") else "Terzi (CLI-xx)"
        per[k] += float(r["imponibile"])
    costi = defaultdict(float)
    for c, r in bilancio[a].items():
        if c.startswith("5"):
            costi[gruppo(c)] += float(r["saldo_dare"]) - float(r["saldo_avere"])
    tot_ric = sum(per.values())
    tot_cos = sum(costi.values())
    ris = tot_ric - tot_cos
    sinistra = [(k, per[k], COL_SOCIE.get(k, COL_TERZI)) for k in [c for c, *_ in SOCIE] + ["Terzi (CLI-xx)"] if per.get(k)]
    if ris < 0:
        sinistra.append(("Perdita d'esercizio\n(coperta da mezzi dei soci)", -ris, "#E53935"))
    destra = [(g, costi[g], COL_COSTI[g]) for g in COL_COSTI if costi.get(g, 0) > 0]
    if ris > 0:
        destra.append(("Utile", ris, "#2E7D32"))
    tot = max(tot_ric, tot_cos)
    gap = tot * 0.03
    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.axis("off")
    xl, xc, xr, wb = 0.0, 1.0, 2.0, 0.06

    def colonna(voci, x):
        h = sum(v for _, v, _ in voci) + gap * (len(voci) - 1)
        y = (tot + gap * 5) / 2 + h / 2
        pos = []
        for nome, v, col in voci:
            ax.add_patch(Rectangle((x - wb / 2, y - v), wb, v, color=col))
            pos.append((nome, v, col, y - v, y))
            y -= v + gap
        return pos

    pl = colonna(sinistra, xl)
    pr = colonna(destra, xr)
    ytop = (tot + gap * 5) / 2 + tot / 2
    ax.add_patch(Rectangle((xc - wb / 2, ytop - tot), wb, tot, color="#455A64"))
    y = ytop
    for nome, v, col, ya, yb in pl:
        nastro(ax, xl + wb / 2, yb, ya, xc - wb / 2, y, y - v, col)
        ax.text(xl - wb, (ya + yb) / 2, f"{nome}\n{euro(v)}", ha="right", va="center", fontsize=8)
        y -= v
    y = ytop
    for nome, v, col, ya, yb in pr:
        nastro(ax, xc + wb / 2, y, y - v, xr - wb / 2, yb, ya, col)
        ax.text(xr + wb, (ya + yb) / 2, f"{nome}  {euro(v)}", ha="left", va="center", fontsize=8)
        y -= v
    ax.text(xc, ytop + gap, f"Ricavi {euro(tot_ric)}\nCosti {euro(tot_cos)}", ha="center", va="bottom", fontsize=9)
    ax.set_xlim(-0.9, 3.0)
    ax.set_ylim(-gap, ytop + gap * 6)
    m0, m1 = periodo(a)
    ax.set_title(f"{a} – Flusso economico {etichetta_mese(m0)} – {etichetta_mese(m1)}: "
                 f"risultato {euro(ris)}", fontsize=11)
    salva(fig, path)


def g_iva(a, path):
    righe = [r for r in liquidazioni if r["anno"] == str(a)]
    if not righe:
        return False
    per = [r["periodo"] for r in righe]
    es = [float(r["iva_esigibile"]) for r in righe]
    de = [float(r["iva_detratta"]) for r in righe]
    cr = [-float(r["credito_cumulato_fine_periodo"]) for r in righe]
    x = range(len(per))
    fig, ax = plt.subplots(figsize=(7, 4.2))
    ax.bar([i - 0.2 for i in x], es, 0.4, color="#DD8452", label="IVA a debito (esigibile)")
    ax.bar([i + 0.2 for i in x], de, 0.4, color="#4C72B0", label="IVA detratta")
    ax.plot(list(x), cr, color="black", marker="o", label="Credito IVA cumulato a fine periodo")
    for i, v in enumerate(cr):
        ax.annotate(euro(v), (i, v), textcoords="offset points", xytext=(0, 7), ha="center", fontsize=8)
    ax.set_xticks(list(x), per)
    ax.set_ylabel("€")
    ax.set_title(f"{a} – IVA: liquidazioni e credito")
    ax.legend(fontsize=8, loc="upper left", bbox_to_anchor=(1, 1))
    salva(fig, path)
    return True


def stato_patrimoniale(a):
    imm = saldo(a, "1400") + saldo(a, "1410") + saldo(a, "1490")
    impieghi = [
        ("Immobilizzazioni nette", imm, "#4C72B0"),
        ("Depositi cauzionali", saldo(a, "1300"), "#64B5CD"),
        ("Credito IVA", saldo(a, "1210") + saldo(a, "1200"), "#8172B3"),
        ("Crediti verso clienti", saldo(a, "1100"), "#CCB974"),
        ("Banca [dedotto]", saldo(a, "1010"), "#55A868"),
    ]
    ris_esercizio = -sum(saldo(a, c) for c in bilancio[a] if c[0] in "45")
    pn = -saldo(a, "2000") - saldo(a, "2900") + ris_esercizio
    fonti = [
        ("Finanziamenti soci", -saldo(a, "2100"), "#C44E52"),
        ("Debiti verso fornitori", -saldo(a, "2200"), "#DD8452"),
        ("IVA a debito", -saldo(a, "2300"), "#E5AE38"),
    ]
    return impieghi, fonti, pn, ris_esercizio


def g_stato_patrimoniale(a, path):
    impieghi, fonti, pn, _ = stato_patrimoniale(a)
    fig, ax = plt.subplots(figsize=(8, 5))
    base = 0.0
    for nome, v, col in impieghi:
        if abs(v) > 0.005:
            ax.bar(0, v, 0.55, bottom=base, color=col, label=nome, edgecolor="white")
            base += v
    tot_imp = base
    base = 0.0
    for nome, v, col in fonti:
        if abs(v) > 0.005:
            ax.bar(1, v, 0.55, bottom=base, color=col, label=nome, edgecolor="white")
            base += v
    col_pn = "#2E7D32" if pn >= 0 else "#E53935"
    if pn >= 0:
        ax.bar(1, pn, 0.55, bottom=base, color=col_pn, label="Patrimonio netto")
    else:
        ax.bar(1, pn, 0.55, bottom=0, color=col_pn, hatch="//", label="Patrimonio netto (negativo)")
    ax.axhline(0, color="black", lw=0.8)
    ax.axhline(tot_imp, color="black", lw=0.6, ls=":")
    ax.text(1.32, tot_imp, f"Totale attivo {euro(tot_imp)}", va="center", fontsize=8)
    ax.text(1.32, pn / 2 if pn < 0 else base + pn / 2, f"PN {euro(pn)}", va="center", fontsize=9, weight="bold",
            color=col_pn)
    ax.set_xticks([0, 1], ["Impieghi (attivo)", "Fonti (passivo + netto)"])
    ax.set_xlim(-0.6, 1.9)
    ax.set_ylabel("€")
    _, m1 = periodo(a)
    ax.set_title(f"{a} – Stato patrimoniale a fine {etichetta_mese(m1)}")
    ax.legend(fontsize=8, loc="upper left", bbox_to_anchor=(1, 1))
    salva(fig, path)


def movimenti_banca():
    """Saldo banca giornaliero cumulato su tutti gli anni."""
    mov = []
    for a in anni:
        for r in giornale[a]:
            if r["conto"] == "1010":
                mov.append((r["data"], float(r["dare"]) - float(r["avere"])))
    mov.sort()
    out, s = [], 0.0
    for d, v in mov:
        s += v
        out.append((d, s))
    return out


def g_banca(a, path, dati=None, titolo=None):
    from datetime import date
    serie = dati if dati is not None else [(d, s) for d, s in movimenti_banca() if d.startswith(str(a))]
    if not serie:
        return False
    xs = [date.fromisoformat(d) for d, _ in serie]
    ys = [s for _, s in serie]
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.step(xs, ys, where="post", color="#55A868")
    ax.fill_between(xs, ys, step="post", alpha=0.15, color="#55A868")
    ax.axhline(0, color="black", lw=0.6)
    ax.set_ylabel("€")
    ax.set_title(titolo or f"{a} – Saldo banca ricostruito [dedotto]")
    fig.autofmt_xdate()
    salva(fig, path)
    return True


def g_investimenti_avvio(a, path):
    per = defaultdict(float)
    for r in acquisti:
        if r["natura"] == "avvio_investimento" and r["mese_registro"].startswith(str(a)):
            per[r["categoria"]] += float(r["imponibile"]) + float(r["non_imponibile"])
    if not per:
        return False
    voci = sorted(per.items(), key=lambda kv: -kv[1])
    tot = sum(v for _, v in voci)
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.pie([v for _, v in voci], colors=plt.cm.Set2.colors[:len(voci)], startangle=90, counterclock=False,
           autopct=lambda p: f"{p:.0f}%" if p >= 3 else "", pctdistance=0.75,
           wedgeprops={"width": 0.5, "edgecolor": "white"})
    ax.text(0, 0, f"Totale\n{euro(tot)}", ha="center", va="center", fontsize=11, weight="bold")
    ax.legend([f"{k.replace('_', ' ')}  {euro(v)}" for k, v in voci], loc="center left", bbox_to_anchor=(1, 0.5),
              fontsize=9)
    ax.set_title(f"{a} – Spese di avvio per categoria (registri IVA acquisti)")
    salva(fig, path)
    return True


def g_finanziamenti(a, path):
    righe = [r for r in finanziamenti if r["data_delibera"].startswith(str(a))]
    if not righe:
        return False
    fig, ax = plt.subplots(figsize=(8, 4.2))
    base = [0.0] * len(righe)
    for c, nome, *_ in SOCIE:
        v = [float(r["per_socia"]) for r in righe]
        ax.bar(range(len(righe)), v, 0.55, bottom=base, color=COL_SOCIE[c], label=nome, edgecolor="white")
        base = [b + y for b, y in zip(base, v)]
    cum, s = [], 0.0
    for r in righe:
        s += float(r["importo_totale"])
        cum.append(s)
    ax.plot(range(len(righe)), cum, color="black", marker="o", label="Cumulato")
    for i, v in enumerate(cum):
        ax.annotate(euro(v), (i, v), textcoords="offset points", xytext=(0, 7), ha="center", fontsize=8)
    ax.set_xticks(range(len(righe)), [r["data_delibera"] for r in righe])
    ax.set_ylabel("€")
    ax.set_title(f"{a} – Finanziamenti soci infruttiferi deliberati (rimborso entro 31/12/2028)")
    ax.legend(fontsize=8, loc="upper left", bbox_to_anchor=(1, 1))
    salva(fig, path)
    return True


# ---------------------------------------------------------------- panoramica
def g_panoramica_mensile(path):
    mesi, ric, cos = [], [], []
    for a in anni:
        ce = ce_mensile(a)
        for m in sorted(ce):
            mesi.append(m)
            ric.append(ce[m]["ricavi"])
            cos.append(sum(v for g, v in ce[m].items() if g not in ("ricavi", "Ammortamenti (stima)")))
    x = range(len(mesi))
    fig, ax = plt.subplots(figsize=(10, 4.2))
    ax.plot(list(x), ric, marker="o", color="#2E7D32", label="Ricavi")
    ax.plot(list(x), cos, marker="o", color="#C44E52", label="Costi (esclusi ammortamenti)")
    ax.fill_between(list(x), ric, cos, where=[r >= c for r, c in zip(ric, cos)], color="#2E7D32", alpha=0.12,
                    interpolate=True)
    ax.fill_between(list(x), ric, cos, where=[r < c for r, c in zip(ric, cos)], color="#C44E52", alpha=0.12,
                    interpolate=True)
    ax.set_xticks(list(x), [etichetta_mese(m) for m in mesi], rotation=45)
    ax.set_ylabel("€ (imponibile)")
    ax.set_title("Ricavi e costi per mese, tutto il periodo coperto")
    ax.legend(fontsize=8)
    salva(fig, path)


def g_panoramica_annuale(path):
    etich, ric, cos, ris, pn = [], [], [], [], []
    for a in anni:
        m0, m1 = periodo(a)
        etich.append(f"{a}\n({etichetta_mese(m0)} – {etichetta_mese(m1)})")
        r = -sum(saldo(a, c) for c in bilancio[a] if c.startswith("4"))
        k = sum(saldo(a, c) for c in bilancio[a] if c.startswith("5"))
        ric.append(r)
        cos.append(k)
        ris.append(r - k)
        pn.append(stato_patrimoniale(a)[2])
    x = range(len(anni))
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar([i - 0.27 for i in x], ric, 0.27, color="#2E7D32", label="Ricavi")
    ax.bar(list(x), cos, 0.27, color="#C44E52", label="Costi")
    ax.bar([i + 0.27 for i in x], ris, 0.27, color=["#2E7D32" if v >= 0 else "#E53935" for v in ris],
           hatch="//", label="Risultato")
    ax.plot(list(x), pn, color="black", marker="D", label="Patrimonio netto a fine periodo")
    for i, v in enumerate(pn):
        ax.annotate(euro(v), (i, v), textcoords="offset points", xytext=(0, -14), ha="center", fontsize=8)
    ax.axhline(0, color="black", lw=0.8)
    ax.set_xticks(list(x), etich)
    ax.set_ylabel("€")
    ax.set_title("Sintesi per anno (periodi parziali come indicato)")
    ax.legend(fontsize=8, loc="upper left", bbox_to_anchor=(1, 1))
    salva(fig, path)


# ---------------------------------------------------------------- struttura societaria
def struttura(path_svg):
    fin_per_socia = sum(float(r["per_socia"]) for r in finanziamenti)
    fin_tot = sum(float(r["importo_totale"]) for r in finanziamenti)
    terzi = sorted({r["cliente"] for r in ricavi if not r["cliente"].startswith("SOC-")})
    ultimo = max(anni)
    canone = {}
    for r in ricavi:
        if r["cliente"].startswith("SOC-") and r["anno"] == str(ultimo):
            canone[r["cliente"]] = float(r["imponibile"])
    L = ['digraph G {', 'rankdir=TB; nodesep=0.5; ranksep=0.8;',
         'node [fontname="Helvetica" fontsize=10 shape=box style="rounded,filled" fillcolor="#FFFFFF"];',
         'edge [fontname="Helvetica" fontsize=9];',
         'subgraph cluster_soci { label="Socie (professioniste in regime forfettario)"; fontname="Helvetica"; '
         'style="rounded,dashed"; color="#999999";']
    for c, nome, prof, perc, quota in SOCIE:
        extra = "\\nAmministratrice unica" if c == "SOC-VG" else ""
        if c in canone:
            extra += f"\\ncliente: {euro(canone[c], 2)}/mese + IVA ({ultimo})"
        L.append(f'"{c}" [label="{nome}\\n{prof}{extra}" fillcolor="{COL_SOCIE[c]}22" color="{COL_SOCIE[c]}"];')
    L.append('}')
    L.append('"SC" [label="SpazioComo S.r.l.\\nCapitale € 5.000 · ATECO 68.20.02\\nvia Paoli 3, Como" '
             'fillcolor="#455A64" fontcolor="white" fontsize=12 penwidth=0];')
    for c, nome, prof, perc, quota in SOCIE:
        L.append(f'"{c}" -> "SC" [label="{perc}\\n({quota})" color="{COL_SOCIE[c]}" penwidth=2];')
        L.append(f'"{c}" -> "SC" [label="finanz. soci\\n{euro(fin_per_socia)}" style=dashed color="#C44E52"];')
    L += ['"LASER" [label="LA.SER S.r.l.\\nlocatore (utilizzatore in leasing)" fillcolor="#FFF3E0"];',
          '"SC" -> "LASER" [label="locazione via Paoli 3\\n€ 2.000/mese + IVA" dir=back];',
          f'"TERZI" [label="Professionisti terzi\\n{", ".join(terzi)}" fillcolor="#EEEEEE"];',
          '"SC" -> "TERZI" [label="spazi (coworking)"];',
          '"FIDO" [label="Commercialista\\nFido (Accounting Hub /\\nServizi Innovativi)" fillcolor="#EDE7F6"];',
          '"SC" -> "FIDO" [label="contabilità e dichiarazioni" style=dashed arrowhead=none];',
          f'"NOTE" [shape=note fillcolor="#FFFDE7" fontsize=8 label="Finanziamenti soci deliberati: {euro(fin_tot)}\\n'
          'infruttiferi, rimborso entro 31/12/2028\\nAssemblea: presidente R. Mauri, segretaria E. Bertoni\\n'
          'Organo di controllo: nessuno"];',
          '{rank=same; "LASER"; "TERZI"; "FIDO";}',
          '}']
    dot = "\n".join(L)
    path_dot = path_svg.with_suffix(".dot")
    path_dot.write_text(dot, encoding="utf-8")
    if shutil.which("dot"):
        subprocess.run(["dot", "-Tsvg", str(path_dot), "-o", str(path_svg)], check=True)
        return True
    print("ATTENZIONE: Graphviz `dot` non trovato, struttura_societaria.svg non rigenerata (scritto solo il .dot)")
    return False


# ---------------------------------------------------------------- pagine
def main():
    OUT.mkdir(exist_ok=True)
    for vecchio in OUT.rglob("*.svg"):
        if vecchio.name != "struttura_societaria.svg":
            vecchio.unlink()
    struttura(OUT / "struttura_societaria.svg")
    g_panoramica_annuale(OUT / "panoramica_annuale.svg")
    g_panoramica_mensile(OUT / "panoramica_mensile.svg")
    g_banca(None, OUT / "panoramica_banca.svg", dati=movimenti_banca(),
            titolo="Saldo banca ricostruito, tutto il periodo [dedotto: mancano gli estratti conto]")

    righe_idx = []
    for a in anni:
        d = OUT / str(a)
        d.mkdir(exist_ok=True)
        m0, m1 = periodo(a)
        sez = []  # (titolo, file, nota)
        g_flusso_economico(a, d / "01_flusso_economico.svg")
        sez.append(("Flusso economico", "01_flusso_economico.svg",
                    "Da chi arrivano i ricavi e dove vanno. Se il risultato è negativo, la perdita compare a "
                    "sinistra: è la parte di costi coperta dai mezzi delle socie (capitale e finanziamenti). "
                    "Ammortamenti: **stima**."))
        g_ricavi_costi_mensili(a, d / "02_ricavi_costi_mensili.svg")
        sez.append(("Ricavi e costi per mese", "02_ricavi_costi_mensili.svg",
                    "Per competenza, dal libro giornale. Gli ammortamenti sono registrati in un'unica scrittura "
                    "nell'ultimo mese del periodo."))
        g_torta_costi(a, d / "03_composizione_costi.svg")
        sez.append(("Composizione dei costi", "03_composizione_costi.svg", "Dal bilancio di verifica."))
        g_torta_clienti(a, d / "04_ricavi_per_cliente.svg")
        sez.append(("Ricavi per cliente", "04_ricavi_per_cliente.svg",
                    "Concentrazione: quota dei ricavi che arriva dalle socie."))
        g_ricavi_clienti_mensili(a, d / "05_ricavi_clienti_mensili.svg")
        sez.append(("Ricavi per mese e per cliente", "05_ricavi_clienti_mensili.svg", "Dai registri IVA vendite."))
        g_stato_patrimoniale(a, d / "06_stato_patrimoniale.svg")
        sez.append(("Stato patrimoniale", "06_stato_patrimoniale.svg",
                    "Impieghi contro fonti. Il saldo banca è **[dedotto]** (mancano gli estratti conto)."))
        if g_banca(a, d / "07_saldo_banca.svg"):
            sez.append(("Saldo banca", "07_saldo_banca.svg",
                        "**[dedotto]**: incassi, pagamenti e versamenti ricostruiti dalle fatture, non dagli "
                        "estratti conto."))
        if g_iva(a, d / "08_iva.svg"):
            sez.append(("IVA", "08_iva.svg", "Dalle liquidazioni e dalla dichiarazione IVA."))
        if g_investimenti_avvio(a, d / "09_spese_avvio.svg"):
            sez.append(("Spese di avvio", "09_spese_avvio.svg",
                        "Acquisti con natura `avvio_investimento`; la scelta della categoria è **[dedotto]**."))
        if g_finanziamenti(a, d / "10_finanziamenti_soci.svg"):
            sez.append(("Finanziamenti soci", "10_finanziamenti_soci.svg",
                        "Importi deliberati nei verbali; i versamenti in banca sono **[dedotto]**."))
        testo = [f"# Grafici {a}", "",
                 f"Periodo coperto: {etichetta_mese(m0)} – {etichetta_mese(m1)}"
                 + (" (**parziale**)" if m1[5:] != "12" else "")
                 + ". Generati da `scripts/grafici.py`: non modificare a mano. "
                 f"Grado di evidenza dei movimenti: [contabilita/{a}/README.md](../../contabilita/{a}/README.md).", "",
                 "Indice: " + " · ".join(f"[{t}](#{t.lower().replace(' ', '-')})" for t, _, _ in sez), ""]
        for t, f, nota in sez:
            testo += [f"## {t}", "", f"![{t}]({f})", "", nota, ""]
        (d / "README.md").write_text("\n".join(testo), encoding="utf-8")
        righe_idx.append(f"| [{a}]({a}/README.md) | {etichetta_mese(m0)} – {etichetta_mese(m1)} | {len(sez)} |")

    idx = ["# Grafici", "",
           "Generati da `scripts/grafici.py` dopo `scripts/partita_doppia.py`: non modificare a mano. "
           "Ogni anno ha una pagina con tutti i suoi grafici.", "",
           "| Anno | Periodo | Grafici |", "|---|---|---|", *righe_idx, "",
           "## Struttura societaria", "", "![Struttura societaria](struttura_societaria.svg)", "",
           "Linee piene: quote di capitale. Tratteggio rosso: finanziamenti soci deliberati. Nei riquadri delle "
           "socie, il canone che pagano come clienti nell'ultimo anno coperto.", "",
           "## Sintesi per anno", "", "![Sintesi per anno](panoramica_annuale.svg)", "",
           "## Ricavi e costi per mese", "", "![Ricavi e costi per mese](panoramica_mensile.svg)", "",
           "## Saldo banca", "", "![Saldo banca](panoramica_banca.svg)", "",
           "**[dedotto]**: ricostruito senza estratti conto.", ""]
    (OUT / "README.md").write_text("\n".join(idx), encoding="utf-8")
    print(f"Grafici generati in {OUT.relative_to(ROOT)}/ per gli anni {', '.join(map(str, anni))}")


if __name__ == "__main__":
    main()
