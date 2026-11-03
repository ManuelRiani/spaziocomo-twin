# Contratti di servizio con i professionisti

Fonte: cartella Drive **CONTRATTI SERVIZI** (sola lettura), letta il 2026-11-03: 22 contratti firmati, 2 fac-simile, allegati. Le persone compaiono solo con il codice del Google Sheet dei codici; categorie professionali generiche per i terzi.

## Struttura

| Cosa | Dove |
|---|---|
| Testi dei modelli, riscritti in Markdown | [modelli/](modelli/): [fisso a mezza giornata](modelli/fisso-mezza-giornata.md) (testo completo), [spot](modelli/spot.md), [fisso socie](modelli/fisso-socia.md), [speciale stanza 3](modelli/speciale-stanza3.md) |
| Allegati | [A – elenco beni e nomi delle stanze](allegati/A-elenco-beni.md), [B – patto di collaborazione](allegati/B-patto-collaborazione.md); C – modulo privacy: non trascritto |
| Una scheda per contratto | [registro/](registro/) (`C01.md` … `C22.md`) |
| Tabella per analisi | [`dati/contratti.csv`](../dati/contratti.csv) |
| Generatore | `python3 scripts/build_contratti.py` (registro e CSV non si modificano a mano) |

Non entrano nel repo: anagrafiche, codici fiscali, iscrizioni agli albi, polizze, le informative privacy firmate e i documenti d'identità presenti in "INFORMATIVE 2026".

## Le quattro formule, in parole semplici

| Formula | Come funziona | Prezzo (+ IVA) | Esempio |
|---|---|---|---|
| **Fisso socie** | stanza propria, tutto il mese | € 819,67/mese (€ 1.000 lordi) | — |
| **Fisso mezza giornata** | una mezza giornata fissa (es. giovedì dalle 13), pagata in anticipo; ore in più a tariffa oraria | € 195/mese + extra € 10,66 → **€ 14,75/h** da set 2026 | CLI-02 ad aprile: 195 + 2 h × 10,66 = **€ 216,32**, esattamente la fattura n. 24 |
| **Spot** | si prenota l'ora quando serve, si paga a fine mese in base alle ore dichiarate | € 10,66/h → **€ 14,75/h** da set 2026; ora prenotata e non usata € 5,74 → € 7,37 | 10 ore in un mese = € 147,50 |
| **Speciale stanza 3** | spot su una stanza precisa, con esclusiva di categoria | € 25/h; non usata € 12,50 | |

## Cronologia

```
              feb   mar   apr   mag   giu   lug   ago   set   ott   nov  … 2027
SOC-VG/EB/RM  [C01–C03 fisso socie ··················] ? nessun rinnovo scritto
CLI-01/02/04        [C06/07/09 fisso v1 ················][C15–C17 fisso v2, 12 mesi →
CLI-03              [C08 fisso v1 ······················]  scoperto  [C21 spot v2 →
CLI-07, CLI-08      [C10/C11 spot v1 ···················][C18/C19 spot v2, 12 mesi →
CLI-06                          [C13 spot v1 ················][C20 spot v2 →
CLI-09                 [C12 speciale ······][C14 speciale, fino a dic? ····]
CLI-10, CLI-11 [C04/C05 spot v1 ···················]  (non rinnovati)
CLI-12                                                                [C22 spot v2 →
```

## Cosa cambia a settembre 2026

- **Listino nuovo**: ora spot ed extra da € 10,66 a **€ 14,75** (+38%); ora non usata da € 5,74 a € 7,37. Il canone del fisso resta € 195.
- **Durata**: da 6 a 12 mesi.
- **Uso condiviso**: se due professionisti usano insieme la stanza, la tariffa si divide.
- Il cliente CLI-03 passa dal fisso allo spot, con due mesi senza contratto.

## Cosa confermano i contratti (rispetto alle deduzioni precedenti)

- Il cambio di andamento delle fatture di CLI-01…04 a fine marzo 2026 è il **passaggio al contratto fisso** (decorrenza 02/03/2026). Prima era solo **[dedotto]** in [offerta/clienti.md](../offerta/clienti.md); ora è un fatto.
- Il canone delle socie (€ 819,67) è scritto nei contratti.

## Incoerenze e lacune trovate

1. **Socie senza rinnovo**: C01–C03 scadono il 01/08/2026, sono archiviati come "attivi" e non c'è un rinnovo scritto (art. 4.2 lo richiede).
2. **"1 mezza giornata al mese"** nei fissi: è un errore del testo, si intende **una mezza giornata a settimana** (confermato da Manuel Riani il 2026-11-03). Va corretto nei rinnovi (vedi [modello](modelli/fisso-mezza-giornata.md#da-notare)).
3. **C14**: "6 mesi" ma fine al 10/12/**2027**; rimando a un Allegato C inesistente.
4. **Contratti spot senza fatture**: CLI-07, CLI-08, CLI-09, CLI-10 e CLI-11 hanno contratti da febbraio–marzo 2026, ma nei registri IVA fino a giugno 2026 non c'è nessuna fattura a loro nome. **[dedotto]** O non hanno usato le stanze, o le ore non sono state fatturate.
5. **CLI-06**: la fattura di giugno (€ 64,17) non si ricostruisce con le tariffe del contratto C13 (€ 10,66 e € 5,74) con ore intere.
6. **CLI-05** ha una fattura (giugno 2026) ma nessun contratto: è un soggetto societario, uso occasionale.
7. **Stanza 3** condivisa tra la socia SOC-VG (C01) e CLI-09 con esclusiva di categoria (C14): serve una regola sugli orari.
8. Lo spot si fattura sulle **ore dichiarate dal professionista**: non risulta un registro delle prenotazioni da cui controllarle.

Domande corrispondenti in [PUNTI_APERTI.md](../PUNTI_APERTI.md).
