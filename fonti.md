# Fonti (Google Drive)

Versione leggibile. L'elenco usato per il controllo automatico dei percorsi (ID, titolo e cartella attesi) è [`fonti_drive.csv`](fonti_drive.csv): le due liste vanno tenute allineate.

Letti il 2026-11-03. I link funzionano solo per chi ha accesso alle cartelle condivise: nel repo non c'è nessun dato in più rispetto a quanto già trascritto.

## Cartelle condivise da spaziocomosrl@gmail.com (fonte primaria)

| Cartella | Link |
|---|---|
| Spese studio | https://drive.google.com/drive/folders/1lAB2oDpwI6dln9rCWZNQL2jwz1RUDaCE |
| Documenti - IVA | https://drive.google.com/drive/folders/1ZeQf_RrF7FVmkGD93jwoFWG86NsNffJ7 |
| Documenti - IVA / 2025 | https://drive.google.com/drive/folders/1X4LpMhzZrYslkIXgzYoE7gGtp_AYAuTK |
| Documenti - IVA / 2026 | https://drive.google.com/drive/folders/13rggdDLJky40yrcGJYhD4Hb7eYJCUAvg |
| CONTRATTI SERVIZI | https://drive.google.com/drive/folders/1P2bbLTvsXSon1nEKNfe-0VpwEwuMZ9nP |
| CONTRATTI SERVIZI / 1. CONTRATTI ATTIVI | https://drive.google.com/drive/folders/1Djr1vXtbl7lmt9mFrKz5tWCeGIdY6mTO |
| CONTRATTI SERVIZI / 2. FAC SIMILE CONTRATTI | https://drive.google.com/drive/folders/1rRksIcJNlSBSZCegVnCtilFubgpX_LRQ |
| CONTRATTI SERVIZI / CONCLUSI | https://drive.google.com/drive/folders/1NwygU3Oh094iuJ4TCU5vu2Nrb8RR0VWx |
| CONTRATTI SERVIZI / ALLEGATI CONTRATTO | https://drive.google.com/drive/folders/1sqPtCWP0ww5Eg-cGvMWUdSzZGmPQZQB- |
| CONTRATTI SERVIZI / INFORMATIVE 2026 | https://drive.google.com/drive/folders/1rahqZ_mpHysvdPzG7q1yyGjjFDqLcdpT |
| Bilancio e verbali società | https://drive.google.com/drive/folders/1cg_YlwNZE2LloSy0NoB9B_vBIBRYRQBC |
| **spaziocomo-twin** (unica cartella in **scrittura**) | https://drive.google.com/drive/folders/1gTdQ9h4XGkjMWxR6lUfN46sHl7LJZOMB |

Tutte le cartelle sono in sola lettura per Manuel, tranne `spaziocomo-twin`.

## Tabella codici → nomi

**Codici anagrafica - gemello SpazioComo** (Google Sheet nella cartella "spaziocomo-twin", modificabile):
https://docs.google.com/spreadsheets/d/1g1nvYCUQnbIhOzvDHa109JTaauWS5DSPLm6xTCHptds/edit

È l'unico posto in cui i codici `SOC-`, `CLI-` e `FOR-` sono associati ai nomi. Un nuovo cliente o fornitore persona fisica si aggiunge lì e nel repo compare solo il codice.

## Documenti → dati

| Documento | Link | Periodo | Usato per |
|---|---|---|---|
| SPESE MENSILI STUDIO.xlsx | https://drive.google.com/file/d/15TwIRVEJ6SngBkBatwnuCvLELxofgaBA/view | feb–nov 2026 | `dati/spese_cassa_mensili.csv` |
| REGISTRI IVA VENDITE IV TRIM | https://drive.google.com/file/d/1gBm9TkCmTDPUV3TYg3D4tm_o2Xyu9C7s/view | ott–dic 2025 | `dati/ricavi_fatture.csv` |
| REGISTRI IVA ACQUISTI IV TRIM | https://drive.google.com/file/d/1tIl0UinP8gBB7xX1kOIgFRmH2TakE_aq/view | ott–dic 2025 | `dati/acquisti_registro_iva.csv` |
| DICHIARAZIONE IVA 2026 | https://drive.google.com/file/d/1e4XYU6IUsAX3J0DuhbiQxVwsPWtm7k6Y/view | anno 2025 | `dati/liquidazioni_iva.csv`, `fisco/iva.md` |
| REGISTRO IVA I TRIM. VENDITE | https://drive.google.com/file/d/1RYNdYJWjnt59ERulBcwycxwaDTl2qSG1/view | gen–mar 2026 | ricavi |
| REGISTRO IVA I TRIM. ACQUISTI | https://drive.google.com/file/d/1DjxXScU5iEt7ECYlZC8yjwIULCybao-Q/view | gen–mar 2026 | acquisti |
| LIQUIDAZIONE IVA PRIMO TRIMESTRE | https://drive.google.com/file/d/19HCZiAQW-TS--tetU_5KXR-O2Un20Kel/view | T1 2026 | liquidazioni, `scripts/verifica.py` |
| REGISTRI IVA SECONDO TRIMESTRE | https://drive.google.com/file/d/1Ndz_7HRiQaKsLrNt2Tk97rYLiUnxc46N/view | apr–giu 2026 | ricavi, acquisti, liquidazione T2 |
| LIQUIDAZIONE IVA SECONDO TRIMESTRE | https://drive.google.com/file/d/12vjbtswkgBwxQU2KpyN2XLs80aNqyzm9/view | T2 2026 | liquidazioni |
| Lipe II Trimestre | https://drive.google.com/file/d/1_9sg-982oRmvaMVy0I4isWMGF2-Be5Qs/view | T2 2026 | controllo totali |

## Contratti di servizio

| Documento | Link | Usato per |
|---|---|---|
| Fac-simile contratto fisso | https://drive.google.com/file/d/10WFPyZ-DuoBxA4xDFn7TfalRYc0maNAC/view | `contratti/modelli/fisso-mezza-giornata.md` |
| Fac-simile contratto spot ("occasionale") | https://drive.google.com/file/d/12fvTmVb86XGqygzPHctlz1YxXvAgV1uv/view | `contratti/modelli/spot.md` |
| Allegato A – elenco beni | https://drive.google.com/file/d/1NTqCwvUOyR5uXg3jo1gwPIsX7GtwP8ew/view | `contratti/allegati/A-elenco-beni.md` |
| Patto di collaborazione | https://drive.google.com/file/d/1EuWUw7qHzCuVpWyCOPEEOpTBcxGetlKt/view | `contratti/allegati/B-patto-collaborazione.md` |
| Informativa privacy (modello) | https://drive.google.com/file/d/1xWVHe1XfXa4mkHjKRCVB25NGJrsWacxh/view | non trascritta |
| 22 contratti firmati | ID Drive nella colonna `drive_id` di [`dati/contratti.csv`](dati/contratti.csv) | `contratti/registro/` |

I titoli dei contratti firmati e delle informative contengono il cognome del professionista: per questo nel repo compare solo l'ID del file, mai il titolo. "INFORMATIVE 2026" contiene anche documenti d'identità: non si trascrive.

## Bilancio e verbali

| Documento | Link | Usato per |
|---|---|---|
| VISURA DEPOSITO BILANCIO.pdf | https://drive.google.com/file/d/1RCEN8qcl8_kecNkaNmH-srMxMj09M-YV/view | non ancora trascritto |
| Bilancio 2025 micro, XBRL firmato (.p7m) | https://drive.google.com/file/d/1oCyUuqBCcL3lHeK8_IkhOhFKEVx9GSBk/view | non ancora trascritto |
| Verbale di approvazione al 30/04/2026 (.p7m) | https://drive.google.com/file/d/1mG3LzHsawLACIMcz8tJjZN1qmza7203r/view | non ancora trascritto |
| Pratica di deposito (.p7m) | https://drive.google.com/file/d/15BWSaGvCHA4WUhDDt99FlIIkkzDo69AS/view | non ancora trascritto |

## Documenti societari

| Documento | Link | Usato per |
|---|---|---|
| Visura 09.09.2025 | https://drive.google.com/file/d/1NzvuFAr7CAsWCzTSdNEKWA7QVBsO-684/view | `societa/anagrafica.md` |
| Atto costitutivo | https://drive.google.com/file/d/1npaGLLrF2jCAuNLx_AbRRji2N80SDrOa/view | non ancora trascritto |
| Statuto (.doc) | https://drive.google.com/file/d/12KNhlF8sgmU9GVjYhuieRlgqGB6w0HXH/view | non ancora trascritto |
| Contratto locazione via Paoli 3 | https://docs.google.com/document/d/1sK12s9tVoo3U4wsK7yOqBcfWRJCRisLerV7H0WdxkqA/edit | `spazi/immobile.md` |
| Verbali finanziamento soci (cartella) | https://drive.google.com/drive/folders/1d-nArK_ZUWJxvqQmZRxwIZl7I2qA_R6U | `finanza/finanziamenti-soci.md` |
| Libro assemblee | https://drive.google.com/file/d/1UyZ6d8Xz83r4BNDVvhnk_P5Nx1n2ggRw/view | solo frontespizio |
| TARI | https://drive.google.com/file/d/18UPJnvLz8Vz_XDi8pVNHW4F77wdPxvV7/view | non ancora trascritto |
| LIPE III trimestre 2025 | https://drive.google.com/file/d/1sa20dVNLOfiYyTG8lc6ExiR7PTC10T4C/view | non ancora trascritto |

## Non letti / mancanti

Vedi [PUNTI_APERTI.md](PUNTI_APERTI.md) § Dati mancanti.
