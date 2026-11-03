# SpazioComo – gemello digitale

Modello in Markdown + CSV di **SpazioComo S.r.l.** (Como, via Pasquale Paoli 3): chi è, come guadagna, quanto spende, che vincoli fiscali e contrattuali ha. Serve a fare controllo di gestione, simulazioni e a preparare domande per il commercialista.

> **Non** sostituisce la contabilità ufficiale né il commercialista (Fido / Accounting Hub). Le cifre sono trascritte dai documenti nel Drive condiviso; le deduzioni sono marcate **[dedotto]** e le stime **stima**.

## Mappa

| Cartella | Contenuto |
|---|---|
| [societa/](societa/) | anagrafica, soci, governance |
| [spazi/](spazi/) | immobile, contratto di locazione passivo, stanze |
| [offerta/](offerta/) | formule contrattuali, tariffe osservate, clienti |
| [costi/](costi/) | struttura dei costi |
| [fisco/](fisco/) | IVA, parti correlate, scadenze |
| [finanza/](finanza/) | finanziamenti soci, cassa |
| [dati/](dati/) | CSV trascritti dai documenti (vedi [dati/README.md](dati/README.md)) |
| [analisi/](analisi/) | analisi datate |
| [decisioni/](decisioni/) | registro decisioni |
| [PUNTI_APERTI.md](PUNTI_APERTI.md) | domande e verifiche in sospeso |
| [fonti.md](fonti.md) | documenti del Drive da cui viene ogni dato |

## Privacy

- Repo **privato**. Accesso: Manuel Riani + le tre socie.
- I clienti terzi e i fornitori persona fisica compaiono solo con codici (`CLI-xx`, `FOR-xx`). La tabella di corrispondenza è il Google Sheet "Codici anagrafica - gemello SpazioComo" nella cartella Drive "Documenti - IVA" (link in [fonti.md](fonti.md)); la copia locale in `privato/` è esclusa da git.
- Le socie compaiono con i codici `SOC-VG`, `SOC-EB`, `SOC-RM` nei dati e per nome nei documenti di governance.

## Aggiornare i dati

1. Trascrivere i nuovi registri IVA / spese in `scripts/build_dati.py`.
2. `python3 scripts/build_dati.py`
3. Verificare i totali con quelli dei registri (vedi [dati/README.md](dati/README.md)).
