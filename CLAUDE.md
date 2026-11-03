# Istruzioni per Claude

Questo repo è il **gemello digitale di SpazioComo S.r.l.** (Como, P.IVA 04244840130). È una società che concede a professionisti, soprattutto sanitari, l'uso di 6 stanze con contratti di servizio. Le tre socie sono anche clienti. Il repo è usato da Manuel Riani per supportare le socie su gestione, fisco e finanza.

Rispondi in italiano, conciso, senza preamboli.

## All'inizio di ogni sessione

Prima di rispondere alla prima richiesta:

1. Leggi [`STATO.md`](STATO.md): copertura dei dati, ultimo aggiornamento, documenti attesi.
2. Leggi [`PUNTI_APERTI.md`](PUNTI_APERTI.md): domande in sospeso.
3. Se la richiesta tocca dati o numeri, esegui `python3 scripts/verifica.py` e `python3 scripts/partita_doppia.py`: confermano che il repo è coerente. Usano solo la libreria standard di Python.
4. Se la richiesta è "aggiorna", "ci sono novità", "riprendiamo" o simili, controlla se nel Drive ci sono documenti nuovi (vedi sotto) e segui la **procedura di aggiornamento**.

## Dove stanno le fonti

La **fonte di verità** sono i documenti nel Google Drive delle socie. Il repo ne è una trascrizione verificata: se un numero qui contraddice un registro IVA, vince il registro.

- Link a ogni cartella e file, con il dato che alimenta: [`fonti.md`](fonti.md).
- Accesso: tramite il **connettore Google Drive**. Se non è disponibile nella sessione, dillo all'utente e chiedi di attivarlo; senza connettore si possono fare solo analisi sui dati già nel repo.
- Cartelle da controllare per i documenti nuovi (ID Drive):

| Cartella | ID |
|---|---|
| Spese studio | `1lAB2oDpwI6dln9rCWZNQL2jwz1RUDaCE` |
| Documenti - IVA | `1ZeQf_RrF7FVmkGD93jwoFWG86NsNffJ7` |
| Documenti - IVA / 2025 | `1X4LpMhzZrYslkIXgzYoE7gGtp_AYAuTK` |
| Documenti - IVA / 2026 | `13rggdDLJky40yrcGJYhD4Hb7eYJCUAvg` |

  Ricerca dei file nuovi: `search_files` con `parentId = '<ID>' and modifiedTime > '<data ultimo aggiornamento in STATO.md>'`, per ciascuna cartella (comprese eventuali nuove sottocartelle, per esempio un anno nuovo). Il foglio "SPESE MENSILI STUDIO.xlsx" viene **modificato** e non sostituito: controllane `modifiedTime`.
- Tabella codici → nomi: Google Sheet "Codici anagrafica - gemello SpazioComo" in "Documenti - IVA" (link in `fonti.md`).

## Regole

- Ogni cifra nuova deve citare il documento di origine (aggiungilo a `fonti.md` se è nuovo).
- **Fatti, deduzioni e stime vanno sempre distinti.** Un fatto è scritto in un documento. Una deduzione (interpretazione di un andamento, attribuzione di una categoria, causa probabile) va marcata `**[dedotto]**` con il ragionamento. Una stima numerica va marcata `**stima**` con l'ipotesi usata. Una deduzione resta tale finché non è confermata da un documento o dalle socie; quando viene confermata si toglie il marcatore e si cita la conferma. Vale anche nelle risposte in chat.
- **Privacy**: mai nomi di clienti terzi o fornitori persona fisica nel repo; usa i codici (`CLI-xx`, `FOR-xx`). Un soggetto nuovo riceve il primo codice libero e va aggiunto **prima** al Google Sheet dei codici. Prima di ogni commit verifica che nessun nome sia finito nei file. Non committare nulla da `privato/`.
- Distingui sempre **imponibile** (al netto IVA, dai registri) e **lordo** (IVA inclusa, dal foglio spese).
- Nelle vendite, le righe di reverse charge (T.N. Costruzioni, Milano Clima) **non sono ricavi**: sono autofatture. Vanno negli acquisti con `RC` nelle note.
- Su temi fiscali e legali dai il quadro e le domande da porre al commercialista (Fido / Accounting Hub). Non presentare conclusioni come parere professionale.
- Nuove analisi: `analisi/AAAA-MM-GG_titolo.md`. Decisioni delle socie: `decisioni/`.
- Non modificare file nel Drive delle socie, tranne il Google Sheet dei codici, senza una richiesta esplicita.

## Procedura di aggiornamento dei dati (obbligatoria)

Ogni volta che si chiede di aggiornare i dati, esegui **tutti** questi passi, nell'ordine:

1. **Cerca i documenti nuovi** nelle cartelle Drive (vedi sopra) dalla data in `STATO.md`. Elencali all'utente prima di trascriverli.
2. **Trascrivi** i nuovi documenti in `scripts/build_dati.py`:
   - ricavi: lista `F` (data, numero, cliente, imponibile, iva), una riga per fattura del registro vendite, esclusi i reverse charge;
   - acquisti: lista `A`, aprendo ogni mese di registro con il marcatore `("@", "AAAA-MM")`; categoria tra quelle già usate (la scelta della categoria è **[dedotto]**);
   - liquidazioni: lista `L`; spese di cassa: dizionario `S`; finanziamenti soci: in fondo.
3. `python3 scripts/build_dati.py`
4. `python3 scripts/verifica.py`: aggiorna i totali attesi con quelli delle nuove liquidazioni o LIPE.
5. **`python3 scripts/partita_doppia.py`**: rigenera la partita doppia di **ogni** anno in `contabilita/<anno>/`. Va sempre rieseguita, anche se l'aggiornamento riguarda un solo anno: i saldi patrimoniali passano da un anno all'altro.
6. Se un controllo fallisce (lo script esce con codice 1), **non committare**: trova la causa e correggi i dati.
7. Aggiorna `STATO.md`, le analisi interessate e `PUNTI_APERTI.md` (chiudi le domande risolte, aggiungi le nuove).
8. Controllo privacy: leggi la colonna `nome` del Google Sheet dei codici e verifica con `grep -ri` che nessun nome di `CLI-` o `FOR-` compaia nei file del repo. Poi commit con un messaggio che dica quali documenti sono stati trascritti, e push.

Nella partita doppia ogni movimento ha un campo `evidenza` (`documento`, `dedotto`, `stima`, `aggregato`). Quando arrivano documenti che confermano un movimento dedotto (per esempio gli estratti conto per incassi, pagamenti e versamenti dei soci), sostituisci la scrittura dedotta con quella documentata in `scripts/partita_doppia.py`.

## Richieste tipiche

| Richiesta | Cosa fare |
|---|---|
| "Aggiorna i dati" / "ci sono novità?" | Procedura di aggiornamento completa |
| "Come va la società?" | Leggi `contabilita/<anno>/README.md` e l'ultima analisi; rispondi con numeri citati, e date di copertura |
| Domanda su IVA, scadenze, contratti | `fisco/`, `spazi/immobile.md`, `offerta/contratti.md`; per i dettagli torna al documento in `fonti.md` |
| Simulazione (prezzi, nuovi clienti, costi) | Nuovo file in `analisi/`, con ipotesi esplicite e marcate **stima** |
| Preparare domande per commercialista o socie | Parti da `PUNTI_APERTI.md` |
| Una socia conferma un'informazione | Togli il marcatore **[dedotto]** dove serve, cita la conferma (chi, quando), aggiorna `PUNTI_APERTI.md` |

## Mappa del repo

Vedi [`README.md`](README.md). In breve: `societa/`, `spazi/`, `offerta/`, `costi/`, `fisco/`, `finanza/` descrivono la società; `dati/` contiene i CSV; `contabilita/` la partita doppia; `scripts/` genera e verifica; `analisi/` e `decisioni/` sono datati.
