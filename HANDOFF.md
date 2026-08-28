# Element Battle — punto della situazione

Ultimo aggiornamento: **28 agosto 2026**. Leggi questo prima di toccare il gioco.

---

## Dove sta cosa

| | |
|---|---|
| **Sorgente (verità)** | `OneDrive\Documenti\app\Element` — si lavora qui |
| **Repo completo** | `WebApps\element-battle` → https://fithzhood.github.io/element-battle/element.html |
| **Repo clear** | `WebApps\element-clear` → https://fithzhood.github.io/element-clear/element-clear.html |
| **APK** | `G:\Il mio Drive\ElementBattle-debug.apk` · progetto `CapacitorApps\element` |
| **Vecchio gioco** | `legacy/` — la versione del 2025, tenuta come riferimento |

I repo sono **copie**: si modifica in OneDrive, si copia, si fa push.

L'**APK carica l'URL remoto**: le modifiche al web arrivano sul telefono senza
ricostruirlo. Va ricostruito solo per cose native (icona, nome, permessi,
orientamento) — vedi la skill `webapp-deploy-apk`.

---

## Com'è fatto

- `element.html` struttura e sigilli SVG · `element.css` stile · `element.js`
  motore · `element-data.js` **tutte le tabelle** (danni, mostri, quest, boss,
  artefatti, e le manopole `BAL` del bilanciamento)
- `img/` è quello che il gioco carica davvero: WebP ridotte, 3,5 MB. Gli
  originali 2048² stanno in `pic2/` (mostri), `armi/` (artefatti), `pics/`
  (sfondi) e **il gioco non li apre mai**.

### Il gioco in due righe

Un mostro alla volta, PV = 10 + (onda − 1). Attacchi contati: quando finiscono,
finisce la partita. Boss ogni 10 onde (PV multipli di 10 da 20 in su), che
pagano in artefatti invece che in attacchi. **Onda 91** = ultimo boss, 100 PV,
finale della campagna, poi corsa infinita.

---

## Comandi

```bash
cd C:\Users\lfili\OneDrive\Documenti\app\Element

python -m http.server 8158 --directory .     # server locale (o preview_start "element")
python costruisci-immagini.py                # rigenera img/ dagli originali
python costruisci-clear.py                   # rigenera i tre element-clear.*
```

Collaudo, con Chrome headless (`--dump-dom` e si leggono i PASS/FAIL):

```
http://localhost:8158/_test.html                  81 verifiche, versione completa
http://localhost:8158/_test.html?target=clear     86 verifiche, versione clear
http://localhost:8158/_bot.html?runs=100          bot che gioca e misura il bilanciamento
http://localhost:8158/_shot.html?w=384&h=800&...  screenshot a misura di telefono
```

**Vanno tenute verdi tutte e due.** Se tocchi `element.js`, rilancia
`costruisci-clear.py` e ricopia i tre file nel repo `element-clear`, altrimenti
le due versioni divergono.

Deploy: copia in `WebApps\<repo>`, `git push`, e **incrementa `?v=N`** sui
riferimenti a css e js dentro l'html (adesso `v=4`).

---

## Cosa c'è dentro, già fatto

- 91 onde, 50 illustrazioni di mostri su 10 livelli, tutti i nomi rivisti
  guardando le immagini
- 13 quest, 4 sfide dei boss, **32 artefatti tutti illustrati** (i 12 che
  mancavano generati con Gemini il 28 ago)
- finale della campagna + corsa infinita
- schermata delle ricompense con il prossimo nemico in grande, la sua onda/PV,
  la fascia BOSS e la tabella di quanto fa ogni attacco contro di lui
- aura pesante sui boss, scaffale degli artefatti, effetti a particelle,
  suoni sintetizzati (nessun file audio)
- **easter egg**: pressione lunga 3 secondi sullo stemma dell'elemento → zip di
  GIF → i mostri diventano quelle, premio a pieno schermo lungo quanto i PV.
  Solo nella versione completa.

---

## Trappole, tutte pagate almeno una volta

**Le due versioni.** La clear sta in un repo **separato** apposta: il repo del
gioco completo è pubblico e il suo README descrive l'easter egg. Togliere il
solo meccanismo non basta — restavano `gifMode`, `#gif-slot` e un'intestazione
che lo annunciava. `costruisci-clear.py` si rifiuta di scrivere se trova una
parola proibita. **`JSON.stringify` contiene "gif"** e fa scattare falsi allarmi.

**Screenshot headless.** `--window-size` non viene rispettato: la pagina si
impagina a 526×700 e lo scatto ritaglia. Per questo c'è `_shot.html`, che mette
il gioco in un iframe di misura data. Con `--blink-settings=accessibilityFontScaleFactor=1.3`
si riproducono le misure vere del telefono (384×800, vedi [[telefono-metriche-reali]]).

**Cache della CDN.** Dopo un push, per ~10 minuti il sito può servire ancora i
file vecchi. È già successo di leggere un risultato e crederlo un deploy
fallito: verifica con `?cb=$RANDOM` e guarda il `Last-Modified`.

**Capacitor 8.** Le barre di sistema si tolgono dalla configurazione
(`SystemBars: {hidden, insetsHandling:"disable"}`), non da `MainActivity`:
`setSystemUiVisibility` su Android 15 non fa più niente. Sta nella skill.

**L'icona.** Per ritagliare il disco da `Element.png` non usare il rettangolo
dei pixel diversi dal fondo: l'**ombra sotto** ci finisce dentro e sposta il
centro di 26 px. Centro vero (508, 497), raggio 457 su 1024.

---

## Aperto, in ordine di quanto conta

**1. Il bilanciamento è a due gobbe.** Il bot dice: gioco forte → mediana onda
13, ma **una corsa su tre arriva in fondo**; e chi passa il boss dell'onda 21
non muore più — le ultime 60 onde non hanno attrito. La causa non sono i
pacchetti (mettere un tetto alle ricompense non sposta niente): sono **gli
scudi**, +2 attacchi per onda a testa, per sempre. Se si vuole un finale teso,
la leva è quella. È una scelta di design, non un bug: le manopole sono in `BAL`
dentro `element-data.js`.

**2. Illustrazioni che mancherebbero** (nessuna blocca niente): versioni
"sovrano" dei boss, una schermata del finale e una di fine partita, l'icona a
1024×1024 invece dei 256 attuali. Dettagli in `ASSET-MANCANTI.md`.

**3. Il nome del repo clear.** `element-clear` lascia intuire che esista una
versione non-clear. Se dà fastidio si rinomina, cambia solo l'indirizzo.

**4. Quest della luce.** Esiste `darknessSpecialist` ma non `lightSpecialist`:
era così anche nell'originale, l'ho lasciato. Se si aggiunge, va aggiornato il
banco di prova.

---

## Cose che il vecchio gioco sbagliava, da non reintrodurre

Il game over non scattava mai (`checkGameOver` non era chiamato da nessuna
parte), il livello 3 delle illustrazioni non usciva mai, la sfida *Elemental
Armor* non faceva nulla, *Conversion Aura* convertiva nell'elemento **forte**
contro il boss invece che in quello resistito, la benedizione del saggio non
saltava niente, i record non contavano i boss, e ricaricando la partita su un
boss la sfida rimangiava gli attacchi. Sono tutti coperti dal banco di prova:
se una di queste torna, `_test.html` diventa rosso.
