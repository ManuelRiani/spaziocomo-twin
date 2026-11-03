# Partita doppia 2026

Periodo: 01/01/2026 – fine 2026-06 (**periodo parziale**: ultimi registri IVA disponibili). Generato da `scripts/partita_doppia.py` sui CSV di `dati/`.

> Ricostruzione gestionale, **non** è la contabilità ufficiale del commercialista. Ogni movimento in `libro_giornale.csv` ha il suo grado di evidenza.

## Evidenza dei movimenti (totale dare)

| Evidenza | € | Significato |
|---|---|---|
| documento | 53.542,98 | da fattura, registro, contratto, visura o foglio spese |
| dedotto | 47.273,06 | **[dedotto]** incassi, pagamenti e versamenti senza estratto conto |
| stima | 3.304,40 | **stima** ammortamenti |

## Stato patrimoniale

| Attivo | € |
|---|---|
| 1010 Banca c/c | 3.086,55 |
| 1210 Erario c/IVA (saldo liquidazioni) | 1.551,13 |
| 1300 Depositi cauzionali | 6.000,00 |
| 1400 Migliorie su beni di terzi | 35.900,00 |
| 1410 Mobili, arredi e attrezzature | 3.783,44 |
| 2900 Risultato esercizi precedenti | 11.388,02 |

| Passivo e netto | € |
|---|---|
| 1490 Fondo ammortamento | 4.726,26 |
| 2000 Capitale sociale | 5.000,00 |
| 2100 Finanziamenti soci infruttiferi | 57.600,00 |
| Risultato dell'esercizio | -5.617,12 |

Il fondo ammortamento è una rettifica dell'attivo: compare tra le voci in avere. Il risultato degli esercizi precedenti, se negativo, compare in attivo.

## Conto economico

| Voce | € |
|---|---|
| 4000 Ricavi da servizi spazi | 19.364,80 |
| 5000 Affitto passivo | −12.000,00 |
| 5010 Pulizie | −2.512,00 |
| 5020 Energia | −1.684,18 |
| 5030 Internet e software | −190,50 |
| 5040 Commercialista e consulenze | −3.036,00 |
| 5050 Manutenzioni | −480,00 |
| 5060 Spese condominiali | −584,14 |
| 5070 Imposte, tasse e diritti | −790,27 |
| 5080 Assicurazioni | −238,75 |
| 5090 Altri costi | −161,68 |
| 5100 Ammortamenti | −3.304,40 |
| **Risultato** | **-5.617,12** |

## Controlli

| Controllo | Valori | Esito |
|---|---|---|
| Totale dare = totale avere | 104.120,44 / 104.120,44 | OK |
| Attivo − passivo = risultato d'esercizio | -5.617,12 / -5.617,12 | OK |
| Ricavi = registri IVA vendite | 19.364,80 / 19.364,80 | OK |
| Credito IVA cumulato a fine 2026T1 = liquidazione | 2.138,57 / 2.138,57 | OK |
| Credito IVA cumulato a fine 2026T2 = liquidazione | 1.551,13 / 1.551,13 | OK |

## Limiti noti

- **[dedotto]** Saldo banca: incassi e pagamenti sono registrati alla data della fattura e i finanziamenti soci alla data della delibera, senza estratto conto. Crediti e debiti commerciali risultano quindi a zero per costruzione.
- Le fatture sono imputate al mese del **registro IVA**, non alla competenza economica.
- **[dedotto]** Classificazione dei costi e capitalizzazione di lavori e allestimento: vedi `dati/README.md`.
- **stima** Ammortamento a quote costanti su 6 anni (durata della locazione), pro rata mensile.
- Ritenute d'acconto sui professionisti, imposte sul reddito (IRES/IRAP) e ratei/risconti non sono rilevati.
- Le spese del foglio non fatturate sono registrate al giorno 15 del mese indicato.
