# Dati

Generati da `scripts/build_dati.py`, trascrizione manuale dei documenti del Drive. Importi in euro.

| File | Contenuto | Base | Periodo |
|---|---|---|---|
| `ricavi_fatture.csv` | una riga per fattura emessa | imponibile + IVA | nov 2025 – giu 2026 |
| `acquisti_registro_iva.csv` | una riga per fattura ricevuta, con categoria e natura (gestione / avvio) | imponibile + IVA + non imponibile | ott 2025 – giu 2026 |
| `spese_cassa_mensili.csv` | foglio spese delle socie | **lordo** (IVA inclusa) | feb – nov 2026 |
| `liquidazioni_iva.csv` | liquidazioni periodiche | | 2025, T1-T2 2026 |
| `finanziamenti_soci.csv` | delibere di finanziamento | | set – nov 2025 |

## Controlli di quadratura

Totali ricavi che devono coincidere con i registri:

| Periodo | Imponibile atteso | Fonte |
|---|---|---|
| Q4 2025 | 4.139,03 | volume d'affari dichiarazione IVA 2026 |
| T1 2026 | 9.458,99 | liquidazione T1 |
| T2 2026 | 9.905,81 | LIPE T2 (vendite al netto del reverse charge) |

Acquisti T1 2026: imponibile 9.566,19 / IVA 2.104,58 / non soggetto 1.331,60 (liquidazione T1).

## Convenzioni

- Le autofatture in reverse charge **non** sono nei ricavi.
- `non_imponibile` comprende i compensi dei forfettari, i bolli e gli importi esclusi art. 15.
- `natura = avvio_investimento` comprende lavori, allestimento, traslochi e consulenze del 2025 (più FOR-P01, registrata a gennaio).
- Esselunga con aliquote miste: imponibile e IVA sommati sulle diverse aliquote.
