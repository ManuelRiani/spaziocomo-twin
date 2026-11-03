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
