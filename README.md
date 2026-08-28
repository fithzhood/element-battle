# Element Battle

Un mostro alla volta. Cinque elementi in mano, contati: ogni colpo che tiri è un
colpo in meno. Quando finiscono, finisce la partita.

**Gioca:** https://fithzhood.github.io/element-battle/element.html
**Versione clear** (senza easter egg): https://fithzhood.github.io/element-battle/element-clear.html

## Come funziona

- Il nemico ha punti vita pari all'onda: 10 alla prima, 100 alla novantunesima.
- Fuoco > natura > acqua > fuoco. La luce fa poco male ma **regala un attacco**
  a ogni colpo, il buio ne fa tanto ma **te ne toglie uno**; due colpi di buio
  di fila fanno 14.
- Ogni vittoria dà un pacchetto di attacchi da scegliere fra quattro, uno dei
  quali è coperto.
- Ogni onda ha una **quest** che, se rispettata, paga.
- A ogni cambio di illustrazione (onde 11, 21, … 91) arriva un **boss** con una
  delle quattro sfide, e paga in **artefatti**: armi (+danno) e scudi (attacchi
  che ricrescono a ogni combattimento).
- Onda 91, l'ultimo boss: finisce la campagna. Poi si può proseguire all'infinito.

## Le due versioni

`element.html` e' il gioco completo. `element-clear.html` e' lo stesso gioco
**senza l'easter egg**: non e' una copia a mano, si rigenera con
`python costruisci-clear.py`, che ritaglia da `element.js` le funzioni che
realizzano il segreto e controlla che nel file prodotto non ne resti traccia.
Le due versioni condividono `element.css`, `element-data.js` e `img/`, quindi
ogni modifica al gioco vale per entrambe: va solo rilanciato lo script.

Il banco di prova gira su tutte e due: `_test.html` per quella completa,
`_test.html?target=clear` per l'altra, che al posto delle prove sull'uovo
verifica che non ne sia rimasto niente.

## Easter egg

Tieni premuto **tre secondi sullo stemma dell'elemento** (in alto a sinistra del
ritratto) e scegli uno **zip di GIF**: i mostri diventano quelle. Il premio per
ogni vittoria è la GIF a pieno schermo, per tanti secondi quanti erano i punti
vita del mostro. Il record della modalità GIF è separato da quello normale.
Il pulsante **Art** in alto riporta alle illustrazioni.

Lo zip viene letto in casa, senza librerie esterne (`DecompressionStream`), così
funziona anche offline dentro l'APK.

## File

| file | cosa c'è dentro |
|---|---|
| `element.html` | struttura e sigilli SVG |
| `element.css` | tutto lo stile, tema per elemento |
| `element-data.js` | tabelle: danni, mostri, quest, boss, artefatti, manopole del bilanciamento |
| `element.js` | motore, effetti, salvataggi, lettura zip |
| `img/` | illustrazioni ridotte in WebP (le originali 2048² stanno in OneDrive) |
| `element-clear.html` / `element-clear.js` | versione senza easter egg, generata |
| `costruisci-clear.py` | la genera e verifica che l'uovo sia sparito |
| `_test.html` | banco di prova: 81 verifiche, `?target=clear` per l'altra versione |
| `_bot.html` | bot che gioca da solo e misura il bilanciamento |
| `_shot.html` | ponte per gli screenshot a misura di telefono |

Sorgente di verità: `OneDrive\Documenti\app\Element`. Questo repo è la copia che
va online — le immagini si rigenerano con `costruisci-immagini.py`.

## Parametri per il collaudo

`?debug` tasti scorciatoia e `window.__el` · `?auto` parte subito ·
`?fast` azzera le attese · `?wave=N` · `?el=fire` · `?boss=<tipo>`
