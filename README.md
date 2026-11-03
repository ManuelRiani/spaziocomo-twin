# SpazioComo – gemello digitale

Modello in Markdown + CSV di **SpazioComo S.r.l.** (Como, via Pasquale Paoli 3): chi è, come guadagna, quanto spende, che vincoli fiscali e contrattuali ha. Serve a fare controllo di gestione, simulazioni e a preparare domande per il commercialista.

> **Non** sostituisce la contabilità ufficiale né il commercialista (Fido / Accounting Hub). Le cifre sono trascritte dai documenti nel Drive condiviso; le deduzioni sono marcate **[dedotto]** e le stime **stima**.

## Mappa

| Cartella | Contenuto |
|---|---|
| [societa/](societa/) | anagrafica, soci, governance |
| [spazi/](spazi/) | immobile, contratto di locazione passivo, stanze |
| [offerta/](offerta/) | formule contrattuali, tariffe osservate, clienti |
| [contratti/](contratti/README.md) | contratti con i professionisti: modelli riscritti in Markdown, allegati, registro (generato da `scripts/build_contratti.py`) |
| [costi/](costi/) | struttura dei costi |
| [fisco/](fisco/) | IVA, parti correlate, scadenze |
| [finanza/](finanza/) | finanziamenti soci, cassa |
| [contabilita/](contabilita/) | partita doppia per anno: libro giornale, bilancio di verifica, SP e CE (generata da `scripts/partita_doppia.py`) |
| [grafici/](grafici/) | struttura societaria e grafici economico-finanziari, una pagina per anno (generati da `scripts/grafici.py`) |
| [dati/](dati/) | CSV trascritti dai documenti (vedi [dati/README.md](dati/README.md)) |
| [analisi/](analisi/) | analisi datate |
| [decisioni/](decisioni/) | registro decisioni |
| [STATO.md](STATO.md) | copertura dei dati, ultimo aggiornamento, documenti attesi |
| [PUNTI_APERTI.md](PUNTI_APERTI.md) | domande e verifiche in sospeso |
| [CLAUDE.md](CLAUDE.md) | istruzioni operative per le sessioni di Claude |
| [fonti.md](fonti.md) | documenti del Drive da cui viene ogni dato |
| [fonti_drive.csv](fonti_drive.csv) | ID, titolo e cartella attesi di ogni fonte Drive, per il controllo dei percorsi |

## Privacy

- Repo **privato**. Accesso: Manuel Riani + le tre socie.
- I clienti terzi e i fornitori persona fisica compaiono solo con codici (`CLI-xx`, `FOR-xx`). La tabella di corrispondenza esiste **solo** come Google Sheet "Codici anagrafica - gemello SpazioComo" nella cartella Drive "spaziocomo-twin" (link in [fonti.md](fonti.md)); non viene mai copiata nel repo.
- Nessun'altra informazione personale non anonimizzata, a parte quelle delle socie, entra nel repo (regola completa in [CLAUDE.md](CLAUDE.md)).
- Le socie compaiono con i codici `SOC-VG`, `SOC-EB`, `SOC-RM` nei dati e per nome nei documenti di governance.

## Aggiornare i dati

Procedura completa in [CLAUDE.md](CLAUDE.md#aggiornamento-dei-dati-procedura-obbligatoria). In breve:

```bash
python3 scripts/build_dati.py      # CSV dai documenti trascritti
python3 scripts/verifica.py        # quadratura con i registri IVA
python3 scripts/partita_doppia.py  # partita doppia di ogni anno (sempre)
python3 scripts/grafici.py         # grafici in grafici/ (matplotlib + Graphviz)
```
