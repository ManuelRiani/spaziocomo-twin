"""Trascrizione dei documenti contabili (Drive) in CSV pseudonimizzati.

Fonti: registri IVA vendite/acquisti Q4-2025, Q1-2026, Q2-2026; liquidazioni IVA;
LIPE Q2-2026; dichiarazione IVA 2026 (anno 2025); foglio "SPESE MENSILI STUDIO.xlsx";
verbali di finanziamento soci. I codici persona sono in privato/anagrafica_codici.csv
(escluso da git).
"""
import csv
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "dati"

# --- Ricavi: fatture emesse (registro IVA vendite, sez. 1) -------------------
# (data, numero, cliente, imponibile, iva)
F = [
    ("2025-11-30", 2, "SOC-VG", 655.00, 144.10),
    ("2025-11-30", 3, "SOC-EB", 655.00, 144.10),
    ("2025-12-01", 4, "SOC-RM", 655.00, 144.10),
    ("2025-12-01", 5, "CLI-01", 29.51, 6.49),
    ("2025-12-01", 6, "CLI-02", 39.35, 8.66),
    ("2025-12-12", 7, "CLI-03", 59.02, 12.98),
    ("2025-12-18", 8, "CLI-04", 81.15, 17.85),
    ("2025-12-19", 9, "SOC-RM", 655.00, 144.10),
    ("2025-12-29", 10, "SOC-EB", 655.00, 144.10),
    ("2025-12-29", 11, "SOC-VG", 655.00, 144.10),
    ("2026-01-18", 1, "SOC-RM", 819.67, 180.33),
    ("2026-01-19", 2, "SOC-VG", 819.67, 180.33),
    ("2026-01-19", 3, "SOC-EB", 819.67, 180.33),
    ("2026-01-19", 4, "CLI-01", 49.18, 10.82),
    ("2026-02-04", 5, "CLI-01", 59.02, 12.98),
    ("2026-02-04", 6, "CLI-02", 29.51, 6.49),
    ("2026-02-27", 7, "SOC-EB", 819.67, 180.33),
    ("2026-02-27", 8, "SOC-VG", 819.67, 180.33),
    ("2026-02-27", 9, "SOC-RM", 819.67, 180.33),
    ("2026-02-27", 10, "CLI-02", 296.72, 65.28),
    ("2026-02-28", 11, "CLI-01", 290.16, 63.84),
    ("2026-03-04", 12, "CLI-03", 216.39, 47.61),
    ("2026-03-09", 13, "CLI-04", 354.10, 77.90),
    ("2026-03-27", 14, "SOC-RM", 819.67, 180.33),
    ("2026-03-27", 15, "SOC-VG", 819.67, 180.33),
    ("2026-03-27", 16, "SOC-EB", 819.67, 180.33),
    ("2026-03-27", 17, "CLI-03", 196.72, 43.28),
    ("2026-03-27", 18, "CLI-02", 196.72, 43.28),
    ("2026-03-27", 19, "CLI-01", 196.72, 43.28),
    ("2026-03-27", 20, "CLI-04", 196.72, 43.28),
    ("2026-04-24", 21, "SOC-EB", 819.67, 180.33),
    ("2026-04-24", 22, "SOC-VG", 819.67, 180.33),
    ("2026-04-24", 23, "SOC-RM", 819.67, 180.33),
    ("2026-04-27", 24, "CLI-02", 216.32, 47.59),
    ("2026-04-27", 25, "CLI-04", 195.00, 42.90),
    ("2026-04-27", 26, "CLI-03", 195.00, 42.90),
    ("2026-04-29", 27, "CLI-01", 195.00, 42.90),
    ("2026-05-25", 28, "SOC-RM", 819.67, 180.33),
    ("2026-05-25", 29, "SOC-EB", 819.67, 180.33),
    ("2026-05-25", 30, "SOC-VG", 819.67, 180.33),
    ("2026-05-25", 31, "CLI-01", 195.00, 42.90),
    ("2026-05-25", 32, "CLI-03", 195.00, 42.90),
    ("2026-05-25", 33, "CLI-04", 195.00, 42.90),
    ("2026-05-25", 34, "CLI-02", 216.32, 47.59),
    ("2026-06-24", 35, "CLI-02", 195.00, 42.90),
    ("2026-06-24", 36, "CLI-04", 195.00, 42.90),
    ("2026-06-24", 37, "CLI-03", 195.00, 42.90),
    ("2026-06-24", 38, "CLI-01", 195.00, 42.90),
    ("2026-06-24", 39, "SOC-VG", 819.67, 180.33),
    ("2026-06-24", 40, "SOC-EB", 819.67, 180.33),
    ("2026-06-24", 41, "SOC-RM", 819.67, 180.33),
    ("2026-06-25", 42, "CLI-05", 81.97, 18.03),
    ("2026-06-27", 43, "CLI-06", 64.17, 14.12),
]

with open(OUT / "ricavi_fatture.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["data", "anno", "numero", "cliente", "tipo_cliente",
                "imponibile", "iva", "totale"])
    for d, n, c, imp, iva in F:
        tipo = "socia" if c.startswith("SOC") else "terzo"
        w.writerow([d, d[:4], n, c, tipo, f"{imp:.2f}", f"{iva:.2f}",
                    f"{imp + iva:.2f}"])

# --- Acquisti (registro IVA acquisti) ----------------------------------------
# (data, fornitore, categoria, imponibile, iva, non_imponibile, note)
# non_imponibile: forfettari, bolli, esclusi art.15. RC = reverse charge edile.
A = [
    # Ottobre 2025
    ("2025-10-01", "LA.SER SRL", "affitto", 2000, 440, 0, ""),
    ("2025-09-30", "Accounting Hub (Fido)", "commercialista", 249.50, 54.89, 0, ""),
    ("2025-09-30", "Google Cloud", "software", 6.80, 1.50, 0, ""),
    ("2025-10-02", "Bricoman", "allestimento", 1739.63, 382.71, 0, ""),
    ("2025-10-03", "Action", "allestimento", 28.48, 6.27, 0, ""),
    ("2025-10-07", "Fisiostore", "allestimento", 500, 110, 0, "attrezzatura sanitaria"),
    ("2025-10-07", "Gruppo Veneziano", "allestimento", 15.50, 3.41, 0, ""),
    ("2025-10-08", "tenulodi", "allestimento", 50.59, 11.13, 0, ""),
    ("2025-10-10", "farma services", "allestimento", 23.27, 5.12, 0, ""),
    ("2025-10-11", "Bricoman", "allestimento", 65.25, 14.36, 0, ""),
    ("2025-10-14", "Accounting Hub (Fido)", "commercialista", 249.50, 54.89, 0, ""),
    ("2025-09-30", "Servizi Innovativi (Fido)", "commercialista", 249.50, 54.89, 0, ""),
    ("2025-10-07", "Amazon", "allestimento", 25.73, 5.66, 0, ""),
    ("2025-10-08", "Amazon", "allestimento", 7.00, 1.54, 0, ""),
    ("2025-10-14", "Servizi Innovativi (Fido)", "commercialista", 249.50, 54.89, 0, ""),
    ("2025-10-17", "Bricoman", "allestimento", 196.07, 43.13, 0, "nota di credito? (NR)"),
    ("2025-10-18", "FOR-P04", "consulenze", 45, 9.90, 0, ""),
    ("2025-10-18", "AD Arte Digitale", "allestimento", 16.27, 3.58, 0, ""),
    ("2025-10-20", "Extra Traslochi", "traslochi", 200, 44, 0, ""),
    ("2025-10-20", "Beper", "allestimento", 57.27, 12.60, 0, ""),
    ("2025-10-23", "tenulodi", "allestimento", 52.23, 11.49, 0, ""),
    ("2025-10-23", "Brico io", "allestimento", 43.44, 9.56, 0, ""),
    ("2025-10-23", "Action", "allestimento", 20.43, 4.49, 0, ""),
    ("2025-10-24", "Ikea", "allestimento", 505.64, 111.24, 0, ""),
    ("2025-10-24", "Brico io", "allestimento", 13.85, 3.05, 0, ""),
    ("2025-10-25", "Leroy Merlin", "allestimento", 75.34, 16.57, 0, ""),
    ("2025-10-28", "Brico io", "allestimento", 38.36, 8.44, 0, ""),
    ("2025-10-30", "Amazon", "allestimento", 11.32, 2.49, 0, ""),
    ("2025-10-30", "Agrifer", "allestimento", 40.91, 9.00, 0, ""),
    ("2025-10-30", "Ikea", "allestimento", 73.65, 16.20, 0, ""),
    ("2025-10-30", "Amazon", "allestimento", 12.64, 2.78, 0, ""),
    ("2025-10-07", "T.N. Costruzioni", "lavori_edili", 10000, 2200, 0, "RC"),
    ("2025-10-21", "T.N. Costruzioni", "lavori_edili", 10000, 2200, 0, "RC"),
    # Novembre 2025
    ("2025-10-31", "Esselunga", "varie", 36.28, 7.06, 0, "aliquote miste"),
    ("2025-10-31", "Google Cloud", "software", 6.80, 1.50, 0, ""),
    ("2025-11-01", "OBI", "allestimento", 62.95, 13.85, 0, ""),
    ("2025-11-02", "Esselunga", "varie", 68.26, 12.59, 0, "aliquote miste"),
    ("2025-10-31", "Ciesseci", "varie", 26.93, 5.92, 0, ""),
    ("2025-11-02", "Esselunga", "varie", -1.27, -0.28, 0, "nota credito"),
    ("2025-11-03", "Extra Traslochi", "traslochi", 490, 107.80, 0, ""),
    ("2025-11-03", "LA.SER SRL", "affitto", 2000, 440, 184, "184 escluso art.15 (registro/bolli?)"),
    ("2025-11-05", "FOR-PUL", "pulizie", 0, 0, 302, ""),
    ("2025-11-07", "Action", "allestimento", 10.02, 2.20, 0, ""),
    ("2025-11-10", "Tipografia Terreni", "varie", 50, 11, 0, ""),
    ("2025-11-06", "FOR-A01", "allestimento", 16.17, 3.56, 0, ""),
    ("2025-11-20", "Amazon", "allestimento", 24.09, 5.30, 0, ""),
    ("2025-11-18", "Eni gas e luce", "energia", 133.40, 29.35, 0, ""),
    ("2025-11-15", "FOR-P03", "consulenze", 0, 0, 1198.08, "forfettario"),
    ("2025-11-07", "T.N. Costruzioni", "lavori_edili", 15400, 3388, 0, "RC"),
    # Dicembre 2025
    ("2025-12-01", "LA.SER SRL", "affitto", 2000, 440, 0, ""),
    ("2025-11-30", "Google Cloud", "software", 6.80, 1.50, 0, ""),
    ("2025-12-01", "FOR-P02", "consulenze", 0, 0, 1892, "forfettario"),
    ("2025-12-03", "FOR-PUL", "pulizie", 0, 0, 452, ""),
    ("2025-12-01", "Fastweb", "internet", 44.91, 9.88, 0, ""),
    ("2025-12-12", "Esselunga", "varie", 60.62, 7.76, 0, "aliquote miste"),
    ("2025-12-12", "Action", "allestimento", 8.51, 1.87, 0, ""),
    ("2025-12-14", "Esselunga", "varie", 47.15, 6.31, 0, "aliquote miste"),
    ("2025-12-12", "Eni gas e luce", "energia", 328.34, 72.23, 0, ""),
    ("2025-12-22", "T.N. Costruzioni", "lavori_edili", 500, 110, 0, "RC"),
    # Gennaio 2026
    ("2025-12-31", "Google Cloud", "software", 6.80, 1.50, 0, ""),
    ("2026-01-01", "Fastweb", "internet", 24.95, 5.49, 0, ""),
    ("2026-01-05", "LA.SER SRL", "affitto", 2000, 440, 0, ""),
    ("2026-01-07", "FOR-PUL", "pulizie", 0, 0, 302, ""),
    ("2026-01-17", "Eni gas e luce", "energia", 340.27, 74.86, 0, ""),
    ("2025-12-01", "FOR-P01", "consulenze", 1768, 388.96, 120, "ritenuta; registrata a gennaio"),
    # Febbraio 2026
    ("2026-01-31", "Google Cloud", "software", 6.80, 1.50, 0, ""),
    ("2026-02-02", "FOR-PUL", "pulizie", 0, 0, 452, ""),
    ("2026-02-02", "LA.SER SRL", "affitto", 2000, 440, 0, ""),
    ("2026-02-01", "Fastweb", "internet", 24.95, 5.49, 0, ""),
    ("2026-02-17", "Eni gas e luce", "energia", 537.09, 118.16, 0, ""),
    # Marzo 2026
    ("2026-03-02", "LA.SER SRL", "affitto", 2000, 440, 0, ""),
    ("2026-02-28", "Accounting Hub (Fido)", "commercialista", 249.50, 54.89, 0, ""),
    ("2026-02-28", "Servizi Innovativi (Fido)", "commercialista", 249.50, 54.89, 0, ""),
    ("2026-02-28", "Google Cloud", "software", 6.80, 1.50, 0, ""),
    ("2026-03-01", "Fastweb", "internet", 24.95, 5.49, 0, ""),
    ("2026-03-03", "FOR-PUL", "pulizie", 0, 0, 452, ""),
    ("2026-03-17", "Eni gas e luce", "energia", 326.58, 71.85, 0, ""),
    ("2026-03-24", "Amazon", "allestimento", 0, 0, 5.60, "fuori campo"),
    # Aprile 2026
    ("2026-03-31", "Google Cloud", "software", 6.80, 1.50, 0, ""),
    ("2026-04-01", "FOR-PUL", "pulizie", 0, 0, 452, ""),
    ("2026-04-01", "Fastweb", "internet", 24.95, 5.49, 0, ""),
    ("2026-04-01", "LA.SER SRL", "affitto", 2000, 440, 0, ""),
    ("2026-04-18", "Eni gas e luce", "energia", 224.97, 49.49, 0, ""),
    # Maggio 2026
    ("2026-04-30", "Google Cloud", "software", 6.80, 1.50, 0, ""),
    ("2026-05-03", "FOR-PUL", "pulizie", 0, 0, 402, ""),
    ("2026-05-01", "Fastweb", "internet", 24.95, 5.49, 0, ""),
    ("2026-05-04", "LA.SER SRL", "affitto", 2000, 440, 0, ""),
    ("2026-05-18", "Amazon", "allestimento", 11.18, 2.46, 0, ""),
    ("2026-05-19", "SA.VI.", "allestimento", 9.68, 2.13, 0, "IVA indetraibile"),
    ("2026-05-19", "Amazon", "allestimento", 16.59, 3.65, 0, "IVA indetraibile"),
    ("2026-05-15", "Eni gas e luce", "energia", 115.37, 25.38, 0, ""),
    ("2026-05-25", "Servizi Innovativi (Fido)", "commercialista", 75, 16.50, 0, ""),
    ("2026-05-25", "Accounting Hub (Fido)", "commercialista", 75, 16.50, 0, ""),
    # Giugno 2026
    ("2026-05-31", "Google Cloud", "software", 6.80, 1.50, 0, ""),
    ("2026-06-01", "Fastweb", "internet", 24.95, 5.49, 0, ""),
    ("2026-06-03", "FOR-PUL", "pulizie", 0, 0, 452, ""),
    ("2026-06-03", "LA.SER SRL", "affitto", 2000, 440, 0, ""),
    ("2026-06-11", "Accounting Hub (Fido)", "commercialista", 249.50, 54.89, 0, ""),
    ("2026-06-11", "Servizi Innovativi (Fido)", "commercialista", 249.50, 54.89, 0, ""),
    ("2026-06-18", "Eni gas e luce", "energia", 139.90, 30.78, 0, ""),
    ("2026-06-15", "Milano Clima", "manutenzione", 480, 105.60, 0, "RC"),
]

INVEST = {"allestimento", "lavori_edili", "traslochi"}

with open(OUT / "acquisti_registro_iva.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["data", "fornitore", "categoria", "natura", "imponibile", "iva",
                "non_imponibile", "reverse_charge", "note"])
    for d, forn, cat, imp, iva, ni, note in A:
        natura = "avvio_investimento" if cat in INVEST else "gestione"
        if cat == "consulenze" and d < "2026-01-01" or forn == "FOR-P01":
            natura = "avvio_investimento"
        w.writerow([d, forn, cat, natura, f"{imp:.2f}", f"{iva:.2f}", f"{ni:.2f}",
                    "si" if "RC" in note else "no", note])

# --- Liquidazioni IVA --------------------------------------------------------
L = [
    ("2025", "anno", 4139.03, 52024.71, 8808.58, 10587.18, -1778.60, -2115.00,
     "dichiarazione IVA 2026; credito annuo 2.115 riportato"),
    ("2026", "T1", 9458.99, 9566.19, 2081.01, 2104.58, -23.57, -2138.57, ""),
    ("2026", "T2", 9905.81, 9041.94, 2284.90, 1697.46, 587.44, -1551.13,
     "vendite al netto del RC Milano Clima (480)"),
]
with open(OUT / "liquidazioni_iva.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["anno", "periodo", "operazioni_attive", "operazioni_passive",
                "iva_esigibile", "iva_detratta", "saldo_periodo",
                "credito_cumulato_fine_periodo", "note"])
    for r in L:
        w.writerow(r)

# --- Spese di cassa dal foglio "SPESE MENSILI STUDIO" (IVA inclusa) -----------
S = {
    "2026-02": [("affitto", 2440.75), ("software", 9), ("energia", 415.83),
                ("pulizie", 452.75), ("internet", 31.14), ("assicurazione", 238.75),
                ("inail", 116.70), ("commercialista", 609.48)],
    "2026-03": [("affitto", 2440.75), ("software", 9), ("energia", 655.25),
                ("pulizie", 452.75), ("internet", 31.14), ("libri_sociali", 309.87)],
    "2026-04": [("affitto", 2440.75), ("software", 9), ("energia", 399),
                ("pulizie", 452.75), ("internet", 31.14), ("inail", 44.98)],
    "2026-05": [("affitto", 2440.75), ("software", 9), ("energia", 275),
                ("pulizie", 402.75), ("internet", 31.14), ("tassa_architetto", 353),
                ("diritti_registro_bilancio", 127.40), ("commercialista", 183),
                ("amministrazione_condominio", 584.14)],
    "2026-06": [("affitto", 2440.75), ("software", 9), ("energia", 141),
                ("pulizie", 452.75), ("internet", 31.14), ("commercialista", 609),
                ("manutenzione", 480)],
    "2026-07": [("affitto", 2440.75), ("software", 9), ("energia", 171),
                ("pulizie", 452.75), ("internet", 31.14),
                ("amministrazione_condominio", 583.98), ("diritto_camerale", 120)],
    "2026-08": [("affitto", 2440.75), ("software", 9), ("energia", 438),
                ("pulizie", 452.75), ("internet", 31.14),
                ("amministrazione_condominio", 583.98)],
    "2026-09": [("affitto", 2440.75), ("software", 9), ("energia", 475),
                ("pulizie", 50), ("internet", 31.14)],
    "2026-10": [("affitto", 2440.75), ("software", 9), ("energia", 452),
                ("pulizie", 452.75), ("internet", 31.14), ("tari", 1211),
                ("commercialista", 609)],
    "2026-11": [("affitto", 2440.75), ("software", 9), ("energia", 442),
                ("pulizie", 452.75), ("internet", 31.14)],
}
with open(OUT / "spese_cassa_mensili.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["mese", "voce", "importo_lordo"])
    for m, rows in S.items():
        for v, x in rows:
            w.writerow([m, v, f"{x:.2f}"])

# --- Finanziamenti soci infruttiferi (delibere) ------------------------------
with open(OUT / "finanziamenti_soci.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["data_delibera", "importo_totale", "per_socia", "rimborso_entro", "fonte"])
    for d, x in [("2025-09-15", 13500), ("2025-10-01", 14700),
                 ("2025-10-15", 14700), ("2025-11-05", 14700)]:
        w.writerow([d, x, x / 3, "2028-12-31", "verbale assemblea"])

print("ok")
