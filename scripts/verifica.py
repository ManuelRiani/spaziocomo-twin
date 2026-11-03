"""Controlla che i CSV quadrino con i totali dei registri IVA."""
import csv
from collections import defaultdict
from pathlib import Path

D = Path(__file__).resolve().parent.parent / "dati"


def q(data):
    y, m = int(data[:4]), int(data[5:7])
    return f"{y}T{(m - 1) // 3 + 1}"


ric = defaultdict(float)
for r in csv.DictReader(open(D / "ricavi_fatture.csv")):
    ric[q(r["data"])] += float(r["imponibile"])

ATTESI = {"2025T4": 4139.03, "2026T1": 9458.99, "2026T2": 9905.81}
ok = True
for k, v in ATTESI.items():
    got = round(ric[k], 2)
    flag = "OK" if abs(got - v) < 0.01 else "ERRORE"
    ok &= flag == "OK"
    print(f"ricavi {k}: {got:>10.2f} atteso {v:>10.2f}  {flag}")

# acquisti T1 2026 per mese di registrazione: FOR-P01 (data 2025-12-01) e' registrata a gennaio
imp = iva = ni = 0.0
for r in csv.DictReader(open(D / "acquisti_registro_iva.csv")):
    in_t1 = ("2025-12-31" <= r["data"] < "2026-03-31") or r["fornitore"] == "FOR-P01"
    if in_t1:
        imp += float(r["imponibile"]); iva += float(r["iva"]); ni += float(r["non_imponibile"])
for nome, got, v in [("imponibile", imp, 9566.19), ("iva", iva, 2104.58), ("non sogg.", ni, 1331.60)]:
    flag = "OK" if abs(round(got, 2) - v) < 0.01 else "ERRORE"
    ok &= flag == "OK"
    print(f"acquisti T1 2026 {nome}: {got:>10.2f} atteso {v:>10.2f}  {flag}")

raise SystemExit(0 if ok else 1)
