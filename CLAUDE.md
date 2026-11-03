# Istruzioni per Claude

Questo repo è il **gemello digitale di SpazioComo S.r.l.** (Como, P.IVA 04244840130). È una società che concede a professionisti, soprattutto sanitari, l'uso di 6 stanze con contratti di servizio. Le tre socie sono anche clienti. Il repo è usato da Manuel Riani per supportare le socie su gestione, fisco e finanza.

Rispondi in italiano, conciso, senza preamboli.

## All'inizio di ogni sessione

Prima di rispondere alla prima richiesta:

1. Leggi [`STATO.md`](STATO.md): copertura dei dati, ultimo aggiornamento, documenti attesi.
2. Leggi [`PUNTI_APERTI.md`](PUNTI_APERTI.md): domande in sospeso.
3. Se la richiesta tocca dati o numeri, esegui `python3 scripts/verifica.py` e `python3 scripts/partita_doppia.py`: confermano che il repo è coerente. Usano solo la libreria standard di Python (`scripts/grafici.py` invece richiede `matplotlib` e Graphviz).
4. Se la sessione ha il connettore Google Drive, esegui il **controllo dei percorsi Drive** (vedi sotto).
5. Se la richiesta è "aggiorna", "ci sono novità", "riprendiamo" o simili, controlla se nel Drive ci sono documenti nuovi e segui la **procedura di aggiornamento**.

## Dove stanno le fonti

La **fonte di verità** sono i documenti nel Google Drive delle socie. Il repo ne è una trascrizione verificata: se un numero qui contraddice un registro IVA, vince il registro.

- Link a ogni cartella e file, con il dato che alimenta: [`fonti.md`](fonti.md) per chi legge, [`fonti_drive.csv`](fonti_drive.csv) per i controlli (ID, titolo atteso, cartella padre attesa).
- Accesso: tramite il **connettore Google Drive**. Se non è disponibile nella sessione, dillo all'utente e chiedi di attivarlo; senza connettore si possono fare solo analisi sui dati già nel repo.
- Cartelle da controllare per i documenti nuovi (ID Drive):

| Cartella | ID |
|---|---|
| Spese studio | `1lAB2oDpwI6dln9rCWZNQL2jwz1RUDaCE` |
| Documenti - IVA | `1ZeQf_RrF7FVmkGD93jwoFWG86NsNffJ7` |
| Documenti - IVA / 2025 | `1X4LpMhzZrYslkIXgzYoE7gGtp_AYAuTK` |
| Documenti - IVA / 2026 | `13rggdDLJky40yrcGJYhD4Hb7eYJCUAvg` |
| CONTRATTI SERVIZI (e sottocartelle "1. CONTRATTI ATTIVI", "2. FAC SIMILE CONTRATTI", "CONCLUSI", "ALLEGATI CONTRATTO") | `1P2bbLTvsXSon1nEKNfe-0VpwEwuMZ9nP` |
| Bilancio e verbali società | `1cg_YlwNZE2LloSy0NoB9B_vBIBRYRQBC` |
| spaziocomo-twin (**l'unica in scrittura**) | `1gTdQ9h4XGkjMWxR6lUfN46sHl7LJZOMB` |

  Tutte le cartelle sono in sola lettura tranne `spaziocomo-twin`, dove sta il foglio codici e dove si possono salvare file di lavoro per le socie. La sottocartella "INFORMATIVE 2026" contiene informative firmate e documenti d'identità: non si legge e non si trascrive.

  Ricerca dei file nuovi: `search_files` con `parentId = '<ID>' and modifiedTime > '<data ultimo aggiornamento in STATO.md>'`, per ciascuna cartella (comprese eventuali nuove sottocartelle, per esempio un anno nuovo). Il foglio "SPESE MENSILI STUDIO.xlsx" viene **modificato** e non sostituito: controllane `modifiedTime`.
- Tabella codici → nomi: Google Sheet "Codici anagrafica - gemello SpazioComo" nella cartella "spaziocomo-twin" (link in `fonti.md`). Si **legge** dal Drive quando serve; non se ne fa mai una copia nel repo, neanche in cartelle ignorate da git.

### Controllo dei percorsi Drive (obbligatorio)

Gli ID dei file Drive restano validi anche se un file viene rinominato o spostato, ma titoli e cartelle scritti nel repo diventano sbagliati. A ogni inizio sessione con il connettore Drive, e comunque prima di ogni aggiornamento dei dati:

1. Per ogni riga di `fonti_drive.csv` (e, per i contratti firmati, per ogni `drive_id` di `dati/contratti.csv`: lì si controlla solo che il file esista e non sia nel cestino, perché il titolo contiene il cognome e non va scritto nel repo), leggi i metadati del file con `get_file_metadata` (con `excludeContentSnippets: true`) e confronta `title` e `parentId` con `titolo` e `parent_id`.
2. **Rinominato o spostato**: aggiorna `fonti_drive.csv`, la riga corrispondente di `fonti.md`, la tabella delle cartelle qui sotto (se è una cartella) e ogni altro riferimento nel repo (`grep -r` sul vecchio titolo). Commit con messaggio `Fonti Drive: <vecchio> → <nuovo>`.
3. **Non trovato o nel cestino**: cerca per titolo con `search_files`. Se lo trovi con un altro ID, aggiorna come sopra; se non lo trovi, **non** cancellare il riferimento: segnalalo all'utente e aggiungilo a `PUNTI_APERTI.md`.
4. **Nuova cartella** (per esempio `Documenti - IVA / 2027`): aggiungila a `fonti_drive.csv`, `fonti.md` e alla tabella qui sotto.
5. Riporta all'utente in una riga cosa è cambiato, oppure che i percorsi sono invariati.

## Regole

- Ogni cifra nuova deve citare il documento di origine (aggiungilo a `fonti.md` se è nuovo).
- **Fatti, deduzioni e stime vanno sempre distinti.** Un fatto è scritto in un documento. Una deduzione (interpretazione di un andamento, attribuzione di una categoria, causa probabile) va marcata `**[dedotto]**` con il ragionamento. Una stima numerica va marcata `**stima**` con l'ipotesi usata. Una deduzione resta tale finché non è confermata da un documento o dalle socie; quando viene confermata si toglie il marcatore e si cita la conferma. Vale anche nelle risposte in chat.
- **Privacy (regola assoluta)**: nel repo, **compresa la storia dei commit**, non deve mai esserci un'informazione personale non anonimizzata, salvo quelle delle tre socie.
  - Vietati: nomi e cognomi di persone diverse dalle socie (clienti, fornitori, professionisti, amministratori di altre società, parenti), anche dentro la ragione sociale di una ditta o società (per esempio una SRL o una SAS col nome del titolare), codici fiscali, indirizzi, telefoni, email, IBAN, legami di parentela con persone identificabili.
  - Le persone si indicano solo con un codice: `CLI-xx` clienti, `FOR-Pxx` professionisti, `FOR-PUL` pulizie, `FOR-Axx` altri fornitori con nome personale. Un soggetto nuovo riceve il primo codice libero e va aggiunto **prima** al Google Sheet dei codici.
  - La tabella di conversione codici → nomi **non** va mai nel repo, né come file né in cartelle ignorate (`privato/` non deve esistere nella cartella del repo).
  - I **titoli dei file Drive** dei contratti e delle informative contengono il cognome: nel repo si scrive solo l'ID del file.
  - Dai contratti non si trascrivono professione esatta dei terzi (solo una categoria generica), iscrizione all'albo, polizza RC, P.IVA. L'IBAN della società si omette.
  - Le società senza nome personale nella ragione sociale (es. LA.SER S.r.l., Eni, Fastweb) si possono nominare.
  - Prima di ogni commit: controllo privacy (passo 8 della procedura). Se un dato personale è finito in un commit già pubblicato, va rimosso anche dalla storia (riscrittura e push forzato), avvisando l'utente.
- Distingui sempre **imponibile** (al netto IVA, dai registri) e **lordo** (IVA inclusa, dal foglio spese).
- Nelle vendite, le righe di reverse charge (T.N. Costruzioni, Milano Clima) **non sono ricavi**: sono autofatture. Vanno negli acquisti con `RC` nelle note.
- Su temi fiscali e legali dai il quadro e le domande da porre al commercialista (Fido / Accounting Hub). Non presentare conclusioni come parere professionale.
- Nuove analisi: `analisi/AAAA-MM-GG_titolo.md`. Decisioni delle socie: `decisioni/`.
- Non modificare file nel Drive delle socie, tranne il Google Sheet dei codici, senza una richiesta esplicita.

## Procedura di aggiornamento dei dati (obbligatoria)

Ogni volta che si chiede di aggiornare i dati, esegui **tutti** questi passi, nell'ordine:

1. Esegui il **controllo dei percorsi Drive**, poi **cerca i documenti nuovi** nelle cartelle Drive (vedi sopra) dalla data in `STATO.md`. Elencali all'utente prima di trascriverli.
2. **Trascrivi** i nuovi contratti in `scripts/build_contratti.py` e i nuovi documenti contabili in `scripts/build_dati.py`:
   - ricavi: lista `F` (data, numero, cliente, imponibile, iva), una riga per fattura del registro vendite, esclusi i reverse charge;
   - acquisti: lista `A`, aprendo ogni mese di registro con il marcatore `("@", "AAAA-MM")`; categoria tra quelle già usate (la scelta della categoria è **[dedotto]**);
   - liquidazioni: lista `L`; spese di cassa: dizionario `S`; finanziamenti soci: in fondo.
3. `python3 scripts/build_contratti.py` e `python3 scripts/build_dati.py`
4. `python3 scripts/verifica.py`: aggiorna i totali attesi con quelli delle nuove liquidazioni o LIPE.
5. **`python3 scripts/partita_doppia.py`**: rigenera la partita doppia di **ogni** anno in `contabilita/<anno>/`. Va sempre rieseguita, anche se l'aggiornamento riguarda un solo anno: i saldi patrimoniali passano da un anno all'altro.
6. Se un controllo fallisce (lo script esce con codice 1), **non committare**: trova la causa e correggi i dati.
   Se i controlli sono OK: **`python3 scripts/grafici.py`** rigenera tutti i grafici in `grafici/` (struttura societaria, panoramica, una pagina per anno). Va rieseguito a ogni aggiornamento, dopo la partita doppia. Richiede `matplotlib` e Graphviz (`dot`); se un nuovo grafico usa una deduzione o una stima, il titolo o la nota lo devono dire.
7. Aggiorna `STATO.md`, le analisi interessate e `PUNTI_APERTI.md` (chiudi le domande risolte, aggiungi le nuove).
8. Controllo privacy: leggi la colonna `nome` del Google Sheet dei codici e verifica con `grep -ri` che nessun nome di `CLI-` o `FOR-` compaia nei file del repo. Controlla anche a vista i nomi di fornitori e controparti nuovi trascritti in `build_dati.py`. Poi commit con un messaggio che dica quali documenti sono stati trascritti, e push.

Nella partita doppia ogni movimento ha un campo `evidenza` (`documento`, `dedotto`, `stima`, `aggregato`). Quando arrivano documenti che confermano un movimento dedotto (per esempio gli estratti conto per incassi, pagamenti e versamenti dei soci), sostituisci la scrittura dedotta con quella documentata in `scripts/partita_doppia.py`.

## Richieste tipiche

| Richiesta | Cosa fare |
|---|---|
| "Aggiorna i dati" / "ci sono novità?" | Procedura di aggiornamento completa |
| "Fammi vedere i grafici" / nuovo grafico | `grafici/README.md` e `grafici/<anno>/README.md`; un grafico nuovo si aggiunge in `scripts/grafici.py`, non a mano |
| "Come va la società?" | Leggi `contabilita/<anno>/README.md` e l'ultima analisi; rispondi con numeri citati, e date di copertura |
| Domanda su IVA, scadenze | `fisco/`, `spazi/immobile.md`; per i dettagli torna al documento in `fonti.md` |
| Domanda sui contratti con i professionisti | `contratti/README.md`, `contratti/modelli/`, `dati/contratti.csv` |
| Nuovo contratto firmato nel Drive | aggiungi una riga in `C` di `scripts/build_contratti.py` (codice dal foglio codici, prima libero se nuovo), poi `python3 scripts/build_contratti.py`; aggiorna `contratti/README.md` se cambia il listino |
| Simulazione (prezzi, nuovi clienti, costi) | Nuovo file in `analisi/`, con ipotesi esplicite e marcate **stima** |
| Preparare domande per commercialista o socie | Parti da `PUNTI_APERTI.md` |
| Una socia conferma un'informazione | Togli il marcatore **[dedotto]** dove serve, cita la conferma (chi, quando), aggiorna `PUNTI_APERTI.md` |

## Mappa del repo

Vedi [`README.md`](README.md). In breve: `societa/`, `spazi/`, `offerta/`, `costi/`, `fisco/`, `finanza/` descrivono la società; `dati/` contiene i CSV; `contabilita/` la partita doppia; `grafici/` i grafici generati; `scripts/` genera e verifica; `analisi/` e `decisioni/` sono datati.
