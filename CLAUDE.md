# Istruzioni per Claude

Questo repo è il gemello digitale di SpazioComo S.r.l. Lo usa Manuel Riani per supportare le socie su gestione e fisco.

## Regole

- Rispondi in italiano, conciso, senza preamboli.
- **Fonte di verità**: i documenti nel Drive condiviso (`spaziocomosrl@gmail.com`, cartelle "Spese studio" e "Documenti - IVA"). Questo repo ne è una trascrizione: se un numero qui contraddice un registro IVA, vince il registro.
- Ogni cifra nuova deve citare il documento di origine (vedi `fonti.md`).
- **Fatti, deduzioni e stime vanno sempre distinti.** Un fatto è scritto in un documento. Una deduzione (interpretazione di un andamento, attribuzione di una categoria, causa probabile) va marcata `**[dedotto]**` con il ragionamento. Una stima numerica va marcata `**stima**` con l'ipotesi usata. Una deduzione resta tale finché non è confermata da un documento o dalle socie; quando viene confermata si toglie il marcatore e si cita la conferma.
- Non scrivere mai nomi di clienti terzi o fornitori persona fisica: usa i codici. La corrispondenza codice → nome sta solo nel Google Sheet "Codici anagrafica - gemello SpazioComo" (link in `fonti.md`); un nuovo soggetto va aggiunto lì. Non committare nulla da `privato/`.
- I link a tutte le cartelle e i file Drive usati sono in `fonti.md`.
- Distingui sempre: **imponibile** (competenza, al netto IVA) vs **lordo** (cassa, IVA inclusa). Il foglio spese delle socie è lordo; i registri IVA sono al netto.
- Nelle vendite, le righe di reverse charge (T.N. Costruzioni, Milano Clima) **non sono ricavi**: sono autofatture. Già escluse da `dati/ricavi_fatture.csv`.
- Su temi fiscali dai il quadro e le domande da porre al commercialista; non presentare conclusioni come parere professionale.
- Nuove analisi: file in `analisi/AAAA-MM-GG_titolo.md`. Decisioni prese dalle socie: `decisioni/`.
- Aggiorna `PUNTI_APERTI.md` quando una domanda viene risolta o ne nasce una nuova.

## Aggiornamento dei dati (procedura obbligatoria)

Ogni volta che si chiede di aggiornare i dati, esegui **tutti** questi passi, nell'ordine:

1. Trascrivi i nuovi documenti in `scripts/build_dati.py` (acquisti: indica il mese del registro IVA con il marcatore `("@", "AAAA-MM")`). Aggiungi le nuove liquidazioni in `dati/liquidazioni_iva.csv` tramite lo script.
2. `python3 scripts/build_dati.py`
3. `python3 scripts/verifica.py` (aggiorna i totali attesi con quelli dei nuovi registri).
4. **`python3 scripts/partita_doppia.py`**: rigenera la partita doppia di **ogni** anno in `contabilita/<anno>/` (libro giornale, bilancio di verifica, stato patrimoniale, conto economico, controlli). La partita doppia va sempre rieseguita, anche se l'aggiornamento riguarda un solo anno: i saldi patrimoniali si trascinano da un anno all'altro.
5. Se un controllo fallisce (lo script esce con codice 1), **non committare**: trova la causa e correggi i dati.
6. Aggiorna analisi e `PUNTI_APERTI.md`, poi commit e push.

Nella partita doppia ogni movimento ha un campo `evidenza` (`documento`, `dedotto`, `stima`, `aggregato`). Quando arrivano documenti che confermano un movimento dedotto (per esempio gli estratti conto per incassi e pagamenti), sostituisci la scrittura dedotta con quella documentata.
