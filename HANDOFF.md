# Element Battle — punto della situazione

Ultimo aggiornamento: **28 agosto 2026** (sera: colonna sonora vera). Leggi questo prima di toccare il gioco.

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
http://localhost:8158/_test.html                 119 verifiche, versione completa
http://localhost:8158/_test.html?target=clear    124 verifiche, versione clear
http://localhost:8158/_bot.html?runs=100&variant=W   solo spade (S: scudi, M: misto,
                                                     B*: prende sempre la calma del saggio)
http://localhost:8158/_bot.html?runs=100          bot che gioca e misura il bilanciamento
http://localhost:8158/_shot.html?w=384&h=800&...  screenshot a misura di telefono
   ...&drive=report|mystery|nerfed|artshow        le schermate nuove
http://localhost:8158/_musica.html                collauda i due brani: che il
   browser decodifichi l'Opus, che la durata torni esatta, che la giunta
   del loop non scatti. Va aperto in un browser VERO (vedi trappole).
   ...&freeze=1400                                congela le animazioni a un istante
```

**Vanno tenute verdi tutte e due.** Se tocchi `element.js`, rilancia
`costruisci-clear.py` e ricopia i tre file nel repo `element-clear`, altrimenti
le due versioni divergono.

Deploy: copia in `WebApps\<repo>`, `git push`, e **incrementa `?v=N`** sui
riferimenti a css e js dentro l'html (adesso `v=10`). La stessa marca finisce
da sola sugli URL dei brani: `element.js` la legge dal proprio tag `<script>`
(`const VER`), quindi **non va aggiornata a mano in due posti**.

---

## Cosa c'è dentro, già fatto

- 91 onde, 50 illustrazioni di mostri su 10 livelli, tutti i nomi rivisti
  guardando le immagini
- 13 quest, 4 sfide dei boss, **32 artefatti tutti illustrati** (i 12 che
  mancavano generati con Gemini il 28 ago)
- finale della campagna + corsa infinita
- schermata delle ricompense con il prossimo nemico in grande, la sua onda/PV,
  la fascia BOSS e la tabella di quanto fa ogni attacco contro di lui
- aura pesante sui boss + **i colori del mostro che pulsano** (`bossColors`,
  ripresa dal `bossBorderPulse` del gioco del 2025: brightness 1 -> 1,4 e
  alone bianco sul bordo, ma sul tempo dell'aura, 2,8s), scaffale degli
  artefatti, effetti a particelle,
  suoni sintetizzati (nessun file audio)
- **precarico delle figure** (`Preload` in `element.js`): le velature e i mostri
  scendono in sottofondo appena si apre la pagina, due per volta e a bassa
  priorita'; la figura del prossimo nemico — che si conosce un'onda prima —
  scavalca la coda. Se una figura non e' ancora intera il ritratto resta spento
  (`#portrait-art.waiting`) invece di mostrarla arrivare a fasce. Il sottofondo
  non parte con `?fast` (il bot farebbe 87 richieste per partita) ne' quando il
  telefono chiede di risparmiare dati.
- **resoconto dell'onda** (`showReport`): prima della schermata del bottino si
  legge fermo com'e' finita la quest (bollo `complete`/`failed`), che premio ha
  pagato, e quanti attacchi ha restituito ogni scudo, uno per uno. Sul boss al
  posto della quest c'e' la sfida, e il pulsante manda agli artefatti. Se non
  c'e' niente da raccontare (nessuna quest, nessuno scudo, nessuna sfida) la
  schermata si salta: nessun tocco a vuoto.
- **il punto interrogativo si spiega** (`revealMystery`): scelto il pacchetto
  misterioso, un pannello dice cosa era rispetto ai pacchetti che si vedevano
  (`Empty hands` / `Thin` / `Fair` / `Rich` / `Double pack`) ed elenca gli
  attacchi presi. Prima era un bollino da 750 ms sulla carta.
- **musica** (`Music` in `element.js`): **due brani veri**, generati con Suno
  il 28 ago e chiusi su se stessi con ffmpeg. `musica/tema.ogg` (52,020 s,
  533 KB) sulle onde normali, `musica/boss.ogg` (84,000 s, 808 KB) sui boss:
  **1,31 MB in tutto**. Stessa tonalita' (Re minore) e stesso livello
  (−18,0 LUFS), cosi' il passaggio e' una **dissolvenza incrociata a potenza
  costante** invece di un cambio di tempo. Il boss si scarica solo quando
  serve. Pulsante suo nella barra in alto, separato dagli effetti; si ferma
  col telefono in tasca e sul game over. Il sintetizzatore di prima e' in
  `_musica_vecchia.js.bak`, se un giorno servisse rileggerlo.
- **l'artefatto raccolto si vede in grande** (`showArtifactCard`): 272 px,
  nome, descrizione e famiglia. Le illustrazioni sono 320² e nello scaffale si
  vedono da 46: era l'unico modo di guardarle davvero. Vale anche per le
  benedizioni, che nello scaffale non ci finiscono nemmeno.
- **prontuario degli attacchi**: pulsante `?` nella barra in alto → tabella dei
  cinque attacchi contro il mostro in scena, piu' le quattro regole che prima
  si potevano solo dedurre (la ruota, la luce, il buio, e che gli attacchi sono
  l'orologio). Le righe le costruisce `legendRow`, la stessa della legenda delle
  ricompense: cosi' le due non possono raccontare cose diverse.
- **la collezione resta sotto gli occhi** mentre si sceglie l'artefatto del
  boss (`renderOwned`): senza, per sapere se un doppione conviene bisognava
  ricordarselo.
- **easter egg**: **tre tocchi sul titolo** → zip di GIF → i mostri diventano
  quelle, premio a pieno schermo lungo quanto i PV. Solo nella versione
  completa. I titoli sono due, uno per schermata: `#start h1` sulla schermata
  iniziale e `#enemy-name` durante la partita, cosi' si accende anche a corsa
  avviata. L'archivio si legge **in sottofondo**: alla ventesima GIF il mostro
  in scena ne prende una e si gioca, il resto continua a scendere. Le GIF gia'
  caricate non si buttano finche' non ne arriva almeno una nuova, se no uno zip
  sbagliato lasciava a mani vuote.

---

## Trappole, tutte pagate almeno una volta

**Le due versioni.** La clear sta in un repo **separato** apposta: il repo del
gioco completo è pubblico e il suo README descrive l'easter egg. Togliere il
solo meccanismo non basta — restavano `gifMode`, `#gif-slot` e un'intestazione
che lo annunciava. `costruisci-clear.py` si rifiuta di scrivere se trova una
parola proibita. **`JSON.stringify` contiene "gif"** e fa scattare falsi allarmi.

**Le prove si sporcano fra loro.** La calma del saggio raccolta in una prova
disarmava il boss della prova dopo, e il banco falliva una volta su quattro
senza motivo apparente. Adesso `setup()` azzera anche `skipChallenge`;
`setupRaw()` no, perche' e' proprio quello che serve alla prova del saggio.
Quando una verifica fallisce a intermittenza, il primo sospetto e' uno stato
lasciato indietro, non il caso.

**L'audio non si collauda in headless col tempo finto.** Con
`--virtual-time-budget` il thread audio non si muove: un `OfflineAudioContext`
resta a renderizzare per sempre e le rampe di guadagno non avanzano di un
millesimo. `_musica.html` va aperto in un **browser vero** (`preview_start`), e
lo stesso vale per qualunque verifica sulla dissolvenza. Le prove sui *file*
(durata, livello, giunta) si fanno invece fuori dal browser, con
`audio/verifica-loop.py`, che non ha questo problema.

**L'AAC riapre la giunta del loop.** Misurato: un m4a restituisce **512
campioni piu'** di quelli che gli sono entrati (riempimento in testa
dell'encoder). Sono 11 ms, e bastano a far sentire lo scatto a ogni giro.
Opus e Vorbis rendono la lunghezza esatta al campione. I brani del gioco sono
**Ogg Opus** per questo, non per la dimensione.

**`cancelScheduledValues` non ferma una rampa gia' partita**, toglie solo gli
appuntamenti futuri. Per interrompere una dissolvenza a meta' serve
`cancelAndHoldAtTime`. E una voce che sta sfumando **non va tolta subito** dal
registro: se la scena torna indietro (boss → normale → boss in fretta), senza
quella voce `accendi` ne accendeva una seconda sovrapposta alla prima. Adesso
resta li' con un appuntamento di chiusura che `accendi` sa disdire.

**Due rampe lineari incrociate fanno un buco.** I due brani sono materiale
scorrelato: si sommano in **potenza**, non in ampiezza, quindi a meta'
dissolvenza la somma cala di 3 dB. Le rampe seguono una curva a seno (la
stessa che ffmpeg chiama `qsin`), cosi' sin² + cos² = 1 e il livello non si
muove — verificato in Chrome, potenza 1,000 a ogni istante del passaggio.

**I pannelli che aspettano un tocco.** Il resoconto dell'onda e il pacchetto
misterioso si fermano finche' non si tocca il pulsante. Con `?fast` no: il
pannello viene **costruito ma non mostrato**, e il gioco tira dritto. Senza
questa scorciatoia il bot resterebbe piantato per sempre, e ogni verifica che
uccide un nemico andrebbe riscritta. Le verifiche leggono `#report-body` e
`#mystery-*` proprio cosi', a pannello costruito.

**Le GIF non si ricreano a ogni colpo.** Prima ogni colpo buttava via l'`<img>`
e ne creava un'altra con lo stesso `src`: per il browser e' una GIF nuova da
decodificare da capo, ed e' li' che l'animazione arrancava — non nel resto del
gioco. Adesso `gifNodes()` tiene **gli stessi due nodi** (immagine viva e canvas
del fotogramma fermo) e scambia solo quale si vede; il fermo lo disegna
dall'immagine che sta gia' girando. In piu' la GIF sta su un piano suo
(`translateZ(0)`) e sui boss non le passa piu' sopra il filtro animato di
`bossColors`: un `filter` che cambia a ogni fotogramma sopra un'immagine animata
e' la ricetta per farla scattare.

**In headless le immagini non si decodificano.** Con `--virtual-time-budget`
un'`<img>` arriva a `complete = true` ma `naturalWidth = 0`: il tempo finto non
muove il decodificatore, come non muove il thread audio del render della musica
(`_musica.html` va aperta nel browser vero). Quindi il banco **non puo'**
verificare che il fotogramma finisca sul canvas: verifica invece che, non
potendo posare, il gioco lasci viva l'animazione e si prenoti per quando
l'immagine arriva.

**La barra in alto sta in piedi per un pelo.** Ci devono stare `best`, `wave`,
`next` e i pulsanti **col numero piu' lungo che i contatori raggiungono** (tre
cifre) e con Art acceso, su 360 px. Con tre pulsanti icona traboccava di 34 px e
il chip `next` finiva fuori schermo. Ora gli interruttori di suoni e musica
stanno **dentro il pannello `?`** e Art e' un'icona: restano 44 px di margine a
360 e 68 a 384. `_shot.html?drive=barra` lo misura e lo scrive nel titolo.

**Alla clear non deve interessare NIENTE dell'uovo.** Non una parola, non una
riga, nemmeno una che ne descriva il meccanismo con altri nomi. Il guardiano
adesso controlla tre cose invece di una:

1. le **parole** del segreto, piu' quelle degli attrezzi che servono solo a lui
   (`inflate`, `ObjectURL`, `frozen`, `usedGif`, `blob:`);
2. che **nessuno dei nomi tolti** sopravviva da nessuna parte — un metodo puo'
   chiamarsi in modo innocente e restare citato in un commento o in una chiamata
   orfana, e le parole da sole non lo prendono;
3. le **cicatrici del taglio**: una riga vuota appiccicata a una graffa chiusa,
   e codice che nessuno scriverebbe. Il record passava per
   `const key = 'normal'` usato come indice: un indice che non varia dice che
   li' c'era un ramo in piu'. Ora la sostituzione riscrive la riga intera.

Le stesse tre cose le ricontrolla `_test.html?target=clear`, che legge i file
generati: cosi' non ci si affida solo allo strumento che li ha scritti.

**Il generatore della clear va tenuto al passo.** Due difetti trovati insieme il
28 ago: ritagliava l'html per **stringa esatta** (un pulsante riscritto su tre
righe restava dentro) e quando non trovava un pezzo si limitava a stampare un
avviso, che scorre via. Ora ritaglia per **id**, la mancanza e' **fatale**, e
`togli_blocco` sa risalire anche i commenti scritti in prosa. Se aggiungi un
metodo che nomina il segreto, mettilo in `METODI`.

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

**0. Spade e scudi, sistemato il 28 ago 2026.** Il bot che raccoglie *una sola
famiglia* di artefatti diceva: solo scudi **34%** di campagne chiuse, solo spade
**4%**. Le spade erano una carta morta. La causa non era il danno — a +4 e a +6
la campagna resta al 4-5%, misurato due volte — ma la valuta: la partita finisce
quando finiscono gli **attacchi**, e le spade non ne danno. Ora ogni spada
arriva con una **dotazione** di 6 attacchi del suo tipo (3+3 per le doppie) e
il bonus di danno e' salito a +3 (+2 per le doppie): `BAL.weapon1`,
`BAL.weapon2`, `BAL.weaponGrant`. Rimisurato: **34% contro 34%**, con curve
diverse (le spade alzano la mediana a 21, gli scudi vincono di rendita) e il
gioco misto passa dal 33% al 37%.

**Trappola del banco:** `_bot.html` ripartiva da una copia di `BAL` scritta a
mano, e dopo il cambio misurava un gioco che non esisteva piu' (spade al 3%
invece che al 34%). Adesso `BASE` si prende a caldo da `D.BAL` dopo il boot.
Le varianti `M`/`S`/`W` del bot servono proprio a questo confronto.

**0-bis. Benedizioni e sfide dei boss (28 ago 2026, sera).** La prosperita'
ancestrale paga **4 per tipo** invece di 3 (`BAL.blessingGrant`), le sfide dei
boss mordono di piu' (`chConvert` 3→5, `chReflect` 8→5, e la corazza elementale
toglie `chArmor` = 1 danno **a ogni colpo**, non solo al super), e un boss che
arriva **senza sfida** paga `BAL.nerfedPicks` = 3 artefatti su un'offerta di 6
carte invece di 1 su 4.

Cosa dicono i numeri, onestamente:
- le sfide piu' cattive si sentono: campagna completata **37% → 30%**;
- il pagamento maggiorato del boss disarmato **non sposta la percentuale**. Un
  bot che prende sempre la calma del saggio chiude il 27% sia col vecchio
  pagamento (1 artefatto) sia col nuovo (3). Il motivo e' la struttura a due
  gobbe: **la partita si decide all'onda 21**, e quello che il boss paga dopo
  arriva quando il verdetto c'e' gia'. Resta perche' e' vistoso e non
  sbilancia niente, non perche' abbia raddrizzato la carta.
- Se un giorno si vuole che la calma del saggio conti davvero, la leva non e'
  quanto paga il boss dopo: e' **non far pagare la scelta** (la si prende
  *oltre* all'artefatto, non al posto suo). Da misurare.

**0-ter. La mano di partenza (28 ago 2026, sera).** Si comincia con 5 di fuoco,
acqua e natura e **2 di luce e buio** (prima erano 0). Misurato, 100 partite col
gioco forte:

| luce/buio iniziali | campagna completata |
|---|---|
| 0 (com'era) | 30% |
| **2 (adesso)** | **73%** |
| 5 | 99% |

Non e' lineare: bastano due luci per accendere il motore, perche' la luce costa
quasi zero (spendi 1, ne torna 1 a caso) e da li' si autoalimenta coi pacchetti.
Il gioco distratto invece quasi non se ne accorge (3% → 4%): questa mano aiuta
chi sa giocare.

Se un giorno si vuole restringere di nuovo senza togliere luce e buio dalla
mano, le leve: **1 a testa**, oppure rendere la luce meno gratuita (il rimborso
non a colpo sicuro).

**0-quater. La luce non e' piu' un motore (28 ago 2026, sera).** Rendeva un
attacco **a caso** a ogni colpo, sempre: chi partiva bene non si fermava piu'.
Adesso rende solo se la mano e' sotto **onda / `BAL.lightRefundDiv`** attacchi
in tutto, e rende il tipo di cui si e' **piu' poveri** (a parita', il primo
nell'ordine degli elementi: deve essere prevedibile). Da fonte inesauribile a
rete di sicurezza — per riaccenderla bisogna essersi svuotati la mano.

**Seconda versione, la sera stessa.** La regola sul totale della mano e' stata
sostituita da una che guarda **solo il tipo di cui si ha di meno**: se ne
restano meno di `BAL.lightRefundMax`, la luce ne rende uno. Si legge guardando i
pulsanti, senza sommare niente — ma **non frena quasi nulla**, perche' con
cinque tipi e pacchetti casuali un buco c'e' quasi sempre:

| regola | campagna completata |
|---|---|
| sempre (com'era all'inizio) | 73% |
| totale sotto onda/1.5 | 40% |
| totale sotto onda/2 | 23% |
| totale sotto onda/3 | 13% |
| un tipo sotto 1 · 2 · 3 · 5 (soglia fissa) | 63% · 70% · 73% · 75% |
| un tipo sotto onda/2 · /3 · **/4 (adesso)** · /6 · /8 | 76% · 71% · **~70%** · 65% · 62% |

**La soglia sul tipo piu' scarso non frena, qualunque numero le si dia.** Da 1 a
onda/8 il gioco resta fra il 62% e il 76%, cioe' dov'era senza freno: con
quattro tipi e pacchetti casuali **un buco c'e' quasi sempre**, quindi la
condizione e' quasi sempre vera. Attenzione a leggere una sola misura da 100
partite: `onda/4` era uscito all'81%, ripetuto a 200 ha dato 75% e 66%. Su una
distribuzione a due gobbe servono almeno 200 partite, e meglio due giri.

**Se si vuole il freno tenendo questa forma**, c'e' il secondo lucchetto
`BAL.lightRefundTotal` (spento di serie, 0): pretende che *anche* la mano
intera stia sotto `onda / questo`. Misurato con `lightRefundDiv: 4`:

| secondo lucchetto | campagna completata |
|---|---|
| spento (adesso) | ~70% |
| mano sotto onda/1 | 63% |
| mano sotto onda/1.5 | 40% |
| mano sotto onda/2 | 33% |

Il pulsante della luce si accende (bollino `+1` dorato, classe `charged`)
quando il rimborso e' armato: senza, sarebbe una regola invisibile.

**TRAPPOLA, la seconda della stessa famiglia.** `_bot.html` ha un **modello di
costo** che diceva `cost('light') = 0.02` — "spendi 1, ne torna 1". Dopo la
modifica quel modello era falso: il bot spendeva luce aspettando rimborsi che
non arrivavano, e ha misurato **5%** invece del 23% vero. Il modello di costo
del bot fa parte del bilanciamento quanto le manopole: **se cambi una regola,
guarda se il banco la conosce.**

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
