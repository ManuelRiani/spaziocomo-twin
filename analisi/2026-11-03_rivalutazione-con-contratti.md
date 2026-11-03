# Rivalutazione delle analisi con i contratti – 3 novembre 2026

Rilettura di tutte le analisi del repo dopo la trascrizione dei 22 contratti ([contratti/](../contratti/README.md)). Dati contabili invariati: ricavi fino a giugno 2026, spese di cassa fino a novembre 2026; `verifica.py` e `partita_doppia.py` OK.

## In sintesi

1. **Il problema non è il prezzo ma le stanze vuote.** **Stima**: le 3 stanze per i terzi sono occupate dai contratti fissi per circa il **10%** delle mezze giornate. Coprire il buco mensile richiede 2–5 mezze giornate settimanali vendute in più su circa 27 libere.
2. **Da settembre il ricavo sicuro scende**: con i contratti in vigore la base fissa è **€ 3.044/mese** (contro € 3.240 in apr–giu), perché CLI-03 è passato dal fisso allo spot. Il buco rispetto ai costi sale da circa € 680 a circa **€ 940/mese** (**stima**).
3. **L'aumento di listino di settembre (+38%) tocca quasi solo lo spot**, che nel primo semestre ha fatturato € 146 in tutto. Il fisso resta a € 195: **[dedotto]** circa € 9–11 l'ora, sotto il nuovo spot da € 14,75.
4. **Possibili ricavi non fatturati**: 5 professionisti hanno un contratto da feb–mar 2026 e nessuna fattura fino a giugno, tra cui CLI-09 a € 25/h. È la prima cosa da controllare.
5. **Il 76% dei ricavi non ha un contratto scritto valido** dal 01/08/2026 (contratti delle socie scaduti). Il rinnovo è il momento per fissare tariffe, orari e stanza 3, e per metterli a verbale.
6. **Socie e terzi ora si possono confrontare** (**stima**): una socia paga meno di un terzo a mezza giornata se usa la stanza più di circa 4 mezze giornate a settimana. È il numero da portare al commercialista per il valore normale.

## Cosa cambia, analisi per analisi

| Analisi | Prima | Ora | Esito |
|---|---|---|---|
| [Quadro iniziale](2026-11-03_quadro-iniziale.md) – ricavi terzi | "€ 195/mese, tipo di contratto da verificare" | contratto fisso a mezza giornata dal 02/03/2026 (C06–C09) | **confermato** |
| Quadro iniziale – punto di pareggio | buco € 680/mese, occupazione ignota | buco ≈ € 940/mese da settembre; occupazione fissi ≈ 10% | **aggiornato** (sotto) |
| Quadro iniziale – "prezzi o ore?" | domanda aperta | servono ore vendute, non prezzi più alti | **risposto** (**stima**) |
| [Costi](../costi/struttura-costi.md) | | i contratti promettono pulizie, utenze, wi-fi, sito e social: i costi ricorrenti sono il costo del servizio | invariato |
| [IVA](../fisco/iva.md) | 22% su tutte le vendite | i contratti dicono "prestazione di servizi": coerente con il 22% | **confermato** |
| [Parti correlate](../fisco/parti-correlate.md) | ore incluse "da documentare" | socie: stanza propria senza limite di ore; terzi: 1 mezza giornata (al mese o a settimana) | **aggiornato** (sotto) |
| [Immobile](../spazi/immobile.md) – sublocazione | "servizi o sublocazione?" | art. 2.1 dice servizi, ma le premesse parlano di "locazione di spazi" | **rischio più chiaro** (sotto) |
| [Finanziamenti soci](../finanza/finanziamenti-soci.md) | rimborso 2028 improbabile | tradotto in occupazione necessaria: ≈ 65% | **aggiornato** (sotto) |
| [Clienti](../offerta/clienti.md) | 9 clienti | 13 soggetti con contratto o fattura, 5 senza fatture | **aggiornato** in contratti/ |

## 1. Occupazione: quante stanze vendiamo davvero

Ipotesi (**stima**): studio aperto 5 giorni, 2 mezze giornate al giorno (mattina fino alle 13, pomeriggio dalle 13, come scritto nei contratti); "1 mezza giornata" = una a settimana (vedi punto 3).

- Stanze 3, 4 e 5: delle socie (la 3 è condivisa con CLI-09).
- Stanze 1, 2 e 6: per i terzi → **30 mezze giornate a settimana**.

| Periodo | Fissi attivi | Mezze giornate occupate | Occupazione |
|---|---|---|---|
| mar – ago 2026 | CLI-01, 02, 03, 04 | 4 | **13%** |
| da set 2026 | CLI-01, 02, 04 | 3 | **10%** |

Più le ore spot, che però a giugno valevano € 146 (circa 14 ore in un mese, **stima** a € 10,66).

**[dedotto]** Le stanze dei terzi sono quasi vuote. Alzare i prezzi a parità di clienti rende poco; vendere ore rende molto: ogni fisso in più vale € 195/mese, e c'è posto per altri 25–27.

## 2. Punto di pareggio rifatto

| | €/mese |
|---|---|
| Costi di gestione (dal [quadro iniziale](2026-11-03_quadro-iniziale.md)) | 3.400 |
| Ammortamenti (**stima**, 6 anni) | 580 |
| **Costi totali** | **3.980** |
| Socie: 3 × 819,67 (se i contratti proseguono) | 2.459 |
| Fissi C15–C17: 3 × 195 | 585 |
| **Ricavo sicuro da settembre** | **3.044** |
| **Buco** | **≈ 940** |

Come si colma (**stima**, prezzi attuali):

- con soli fissi: **5 contratti in più** (5 mezze giornate a settimana → occupazione dal 10% al 27%);
- con solo spot a € 14,75: **64 ore al mese** in più, circa 15 a settimana;
- senza contare gli ammortamenti (cioè per non perdere cassa): bastano **2 fissi** in più.

Dall'01/10/2026 l'affitto può crescere per l'ISTAT (art. del contratto di locazione): le fatture di ottobre non sono ancora nei dati.

## 3. "1 mezza giornata al mese" o a settimana

Il conto conferma la deduzione già fatta in [modelli/fisso-mezza-giornata.md](../contratti/modelli/fisso-mezza-giornata.md):

| Lettura | Ore al mese (mezza giornata di 4–5 h) | Prezzo orario implicito |
|---|---|---|
| al mese | 4–5 | **€ 39–49/h** (3–4 volte lo spot) |
| a settimana | 17–22 | **€ 9–11/h** (in linea con lo spot di feb 2026, € 10,66) |

**[dedotto]** Il canone è stato calcolato come una mezza giornata **a settimana**. Ma il contratto scritto dice "al mese": letto alla lettera, un cliente potrebbe pretendere ore extra a pagamento invece che comprese, o contestare il canone. Va corretto nei prossimi contratti.

Conseguenza: dopo il listino di settembre il fisso costa **€ 9–11/h contro € 14,75/h dello spot** (sconto 25–40%). Può essere voluto (premio fedeltà), ma va deciso, non subito. Portare il fisso a € 255 (≈ 17,3 h × € 14,75) varrebbe circa € 180/mese sui 3 fissi attuali (**stima**): meno di un solo cliente nuovo.

## 4. Possibili ricavi non fatturati

| Cliente | Contratto | Tariffa | Fatture gen–giu 2026 |
|---|---|---|---|
| CLI-09 | C12 dal 09/03/2026, poi C14 | **€ 25/h**, stanza 3 | nessuna |
| CLI-07, CLI-08 | C10, C11 dal 02/03/2026 | € 10,66/h | nessuna |
| CLI-10, CLI-11 | C04, C05 dal 01–02/02/2026 | € 10,66/h | nessuna |
| CLI-03 | nessun contratto 02/09 – 29/10/2026 | | registri non ancora disponibili |

**[dedotto]** Due spiegazioni possibili: non hanno usato le stanze, oppure le ore non sono state dichiarate o fatturate. Per ordine di grandezza (**stima**): 4 ore a settimana di CLI-09 non fatturate valgono circa **€ 430/mese**, metà del buco.

Il controllo è debole per costruzione: lo spot si fattura sulle ore **dichiarate** dal professionista e non risulta un calendario delle prenotazioni. Un calendario condiviso (anche un Google Calendar per stanza) risolverebbe insieme fatturazione, ore non usate (€ 7,37) e calcolo dell'occupazione.

## 5. Socie: contratti scaduti e confronto con i terzi

**Fatto**: C01–C03 sono scaduti il 01/08/2026; l'art. 4.2 richiede il rinnovo scritto. Le socie generano il 76% dei ricavi.

Confronto (**stima**, stesse ipotesi del punto 1):

- Una stanza piena vale 10 mezze giornate a settimana ≈ 43 al mese.
- Un terzo fisso paga circa **€ 45 a mezza giornata** (€ 195 / 4,33).
- Una socia paga € 819,67 per la stanza intera, cioè **€ 19 a mezza giornata** se la usa sempre.
- Pareggio: la socia paga quanto un terzo se usa **circa 18 mezze giornate al mese (≈ 4 a settimana)**. Sopra, paga meno; sotto, paga di più.

Due letture, entrambe da mettere sul tavolo:

- **A favore delle socie**: stanza dedicata, impegno lungo, nessun rischio di vuoto per la società. Uno sconto "all'ingrosso" è normale. E con l'occupazione reale dei terzi (10%) quella stanza, data ai terzi, renderebbe molto meno di € 819,67.
- **Da documentare**: rispetto al listino, una socia che usa la stanza a tempo pieno paga meno della metà di un terzo. Per il valore normale serve sapere quante mezze giornate usa ciascuna.

Se si sta valutando di **abbassare le tariffe delle socie**: ogni € 100 in meno a testa allarga il buco di € 300/mese e allontana ancora di più il prezzo delle socie da quello dei terzi. Da simulare e da discutere con il commercialista prima del rinnovo.

## 6. Sublocazione: il testo dei contratti non aiuta del tutto

- L'art. 2.1 dice che il contratto è una prestazione di servizi e **non** una sublocazione. Bene.
- Ma le premesse descrivono l'attività come "gestione, organizzazione e **locazione** di spazi professionali" e "conduzione in locazione". **[dedotto]** In una contestazione, questa frase potrebbe essere usata per sostenere che si tratta di sublocazione.
- La stanza 3 è indicata per numero ed esclusiva di categoria (CLI-09); le stanze delle socie sono indicate per numero. Più un contratto assegna una stanza precisa, più assomiglia a una locazione. **[dedotto]**

Domanda per il commercialista o un legale: togliere "locazione" dalle premesse nei rinnovi? E comunque chiedere a LA.SER il consenso scritto (art. 6 del contratto di locazione), che chiude il problema alla radice.

## 7. Finanziamenti soci in termini di stanze

Rimborsare € 57.600 entro il 31/12/2028 (circa 25 mesi) richiede un avanzo di circa € 2.300/mese, più il buco attuale di € 940: circa **€ 3.240/mese** di ricavi in più (**stima**). Sono circa **17 fissi** in più, cioè occupazione delle stanze dei terzi dal 10% a circa il **65%**, mantenuta da subito fino al 2028. **[dedotto]** Conferma che la scadenza 2028 va rivista.

## Cosa resta uguale

Costi, credito IVA, partita doppia, struttura societaria: i contratti non li cambiano.

## Priorità

1. **Ricavi mancanti**: chiedere alle socie se CLI-07…11 e CLI-09 hanno usato le stanze; controllare nei registri T3 2026 (attesi entro il 30/11).
2. **Rinnovo scritto dei contratti delle socie**, con tariffa decisa e messa a verbale in assemblea.
3. **Calendario delle prenotazioni** per stanza: rende controllabili fatture e occupazione.
4. **Correggere i modelli**: "a settimana" invece di "al mese"; togliere "locazione" dalle premesse (dopo parere); refusi di C14.
5. **Commerciale**: 2 fissi in più fermano la perdita di cassa, 5 coprono anche gli ammortamenti.
