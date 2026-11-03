# Istruzioni per Claude

Questo repo è il gemello digitale di SpazioComo S.r.l. Lo usa Manuel Riani per supportare le socie su gestione e fisco.

## Regole

- Rispondi in italiano, conciso, senza preamboli.
- **Fonte di verità**: i documenti nel Drive condiviso (`spaziocomosrl@gmail.com`, cartelle "Spese studio" e "Documenti - IVA"). Questo repo ne è una trascrizione: se un numero qui contraddice un registro IVA, vince il registro.
- Ogni cifra nuova deve citare il documento di origine (vedi `fonti.md`). Le stime vanno marcate come **stima** con l'ipotesi usata.
- Non scrivere mai nomi di clienti terzi o fornitori persona fisica: usa i codici. Non committare nulla da `privato/`.
- Distingui sempre: **imponibile** (competenza, al netto IVA) vs **lordo** (cassa, IVA inclusa). Il foglio spese delle socie è lordo; i registri IVA sono al netto.
- Nelle vendite, le righe di reverse charge (T.N. Costruzioni, Milano Clima) **non sono ricavi**: sono autofatture. Già escluse da `dati/ricavi_fatture.csv`.
- Su temi fiscali dai il quadro e le domande da porre al commercialista; non presentare conclusioni come parere professionale.
- Nuove analisi: file in `analisi/AAAA-MM-GG_titolo.md`. Decisioni prese dalle socie: `decisioni/`.
- Aggiorna `PUNTI_APERTI.md` quando una domanda viene risolta o ne nasce una nuova.
