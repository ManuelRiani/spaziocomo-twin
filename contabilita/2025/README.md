# Partita doppia 2025

Periodo: 01/01/2025 – 31/12/2025. Generato da `scripts/partita_doppia.py` sui CSV di `dati/`.

> Ricostruzione gestionale, **non** è la contabilità ufficiale del commercialista. Ogni movimento in `libro_giornale.csv` ha il suo grado di evidenza.

## Evidenza dei movimenti (totale dare)

| Evidenza | € | Significato |
|---|---|---|
| documento | 89.771,08 | da fattura, registro, contratto, visura o foglio spese |
| dedotto | 119.414,99 | **[dedotto]** incassi, pagamenti e versamenti senza estratto conto |
| stima | 1.421,86 | **stima** ammortamenti |
| aggregato | 1.865,49 | totale da dichiarazione IVA senza dettaglio |

## Stato patrimoniale

| Attivo | € |
|---|---|
| 1010 Banca c/c | 4.884,23 |
| 1210 Erario c/IVA (saldo liquidazioni) | 2.115,00 |
| 1300 Depositi cauzionali | 6.000,00 |
| 1400 Migliorie su beni di terzi | 35.900,00 |
| 1410 Mobili, arredi e attrezzature | 3.734,61 |

| Passivo e netto | € |
|---|---|
| 1490 Fondo ammortamento | 1.421,86 |
| 2000 Capitale sociale | 5.000,00 |
| 2100 Finanziamenti soci infruttiferi | 57.600,00 |
| Risultato dell'esercizio | -11.388,02 |

Il fondo ammortamento è una rettifica dell'attivo: compare tra le voci in avere. Il risultato degli esercizi precedenti, se negativo, compare in attivo.

## Conto economico

| Voce | € |
|---|---|
| 4000 Ricavi da servizi spazi | 4.139,03 |
| 5000 Affitto passivo | −6.184,00 |
| 5010 Pulizie | −754,00 |
| 5020 Energia | −461,74 |
| 5030 Internet e software | −65,31 |
| 5040 Commercialista e consulenze | −4.133,08 |
| 5090 Altri costi | −2.507,06 |
| 5100 Ammortamenti | −1.421,86 |
| **Risultato** | **-11.388,02** |

## Controlli

| Controllo | Valori | Esito |
|---|---|---|
| Totale dare = totale avere | 212.473,42 / 212.473,42 | OK |
| Attivo − passivo = risultato d'esercizio | -11.388,02 / -11.388,02 | OK |
| Ricavi = registri IVA vendite | 4.139,03 / 4.139,03 | OK |
| Credito IVA cumulato a fine 2025T4 = liquidazione | 2.115,00 / 2.115,00 | OK |

## Limiti noti

- **[dedotto]** Saldo banca: incassi e pagamenti sono registrati alla data della fattura e i finanziamenti soci alla data della delibera, senza estratto conto. Crediti e debiti commerciali risultano quindi a zero per costruzione.
- Le fatture sono imputate al mese del **registro IVA**, non alla competenza economica.
- **[dedotto]** Classificazione dei costi e capitalizzazione di lavori e allestimento: vedi `dati/README.md`.
- **stima** Ammortamento a quote costanti su 6 anni (durata della locazione), pro rata mensile.
- Ritenute d'acconto sui professionisti, imposte sul reddito (IRES/IRAP) e ratei/risconti non sono rilevati.
- Le spese del foglio non fatturate sono registrate al giorno 15 del mese indicato.
- **aggregato** Acquisti di settembre 2025 (€ 1.529,09 + IVA 336,40): ricavati dalla differenza tra credito IVA dichiarato e registri Q4; registro Q3 2025 non disponibile.
