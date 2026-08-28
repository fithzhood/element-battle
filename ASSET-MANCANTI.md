# Element Battle — asset mancanti

Stato al 28 agosto 2026, dopo la ricostruzione del gioco.

Le illustrazioni originali stanno in `pic2/` (mostri), `armi/` (artefatti) e `pics/` (sfondi),
tutte 2048×2048. Il gioco **non le carica**: usa le copie ridotte in `img/`, generate da quelle
(36,3 MB → 3,2 MB). Se aggiungi un'illustrazione nuova, mettila nella cartella originale e
rilancia `costruisci-immagini.py`.

---

## 1. Mancano davvero — 12 illustrazioni di artefatti

Sono gli unici buchi veri: il gioco li mostra con uno stemma disegnato al volo
(sfondo a due colori + i sigilli degli elementi) al posto dell'immagine.
Si vede che è un segnaposto, ma non sembra rotto.

### Scudi doppi (10) — `armi/s2XY.jpg`, 2048×2048

Servono nello stesso stile dei cinque scudi singoli già presenti (`s1f`, `s1w`, `s1n`, `s1l`, `s1d`):
uno scudo al centro, ambientato nell'elemento. Qui però l'elemento è doppio.

| file | artefatto | elementi |
|---|---|---|
| `s2df.jpg` | Fire and Darkness Shield | buio + fuoco |
| `s2dl.jpg` | Light and Darkness Shield | buio + luce |
| `s2dn.jpg` | Nature and Darkness Shield | buio + natura |
| `s2dw.jpg` | Water and Darkness Shield | buio + acqua |
| `s2fl.jpg` | Flame and Light Shield | fuoco + luce |
| `s2fn.jpg` | Fire and Nature Shield | fuoco + natura |
| `s2fw.jpg` | Fire and Water Shield | fuoco + acqua |
| `s2ln.jpg` | Nature and Light Shield | luce + natura |
| `s2lw.jpg` | Water and Light Shield | luce + acqua |
| `s2nw.jpg` | Water and Nature Shield | natura + acqua |

Le lettere sono `f` fuoco, `w` acqua, `n` natura, `l` luce, `d` buio, **in ordine alfabetico**
(come le armi doppie `w2df`, `w2dl`, … che sono già tutte lì).

### Benedizioni (2) — `armi/b1.jpg`, `armi/b2.jpg`, 2048×2048

Non sono armi né scudi: sono effetti magici a uso singolo. Un oggetto rituale, non un'arma.

| file | artefatto | cosa fa |
|---|---|---|
| `b1.jpg` | Ancestral Mage Prosperity | dà subito 3 attacchi di ogni tipo — un tesoro, cinque gemme, un'offerta |
| `b2.jpg` | Sage's Absolute Calm | annulla la sfida del boss successivo — un saggio, un sigillo di quiete |

---

## 2. Non mancano, ma se ci fossero il gioco guadagnerebbe

Nessuno di questi blocca niente: sono migliorie.

- **Illustrazioni dei boss.** Il boss dell'onda 11, 21, … usa la stessa illustrazione dei
  mostri normali del suo livello, con cornice e aura diverse. Cinque illustrazioni dedicate
  (una per elemento, versione "sovrano") si vedrebbero.
- **Schermata del finale.** Ora usa l'icona `Element.png` ingrandita. Un'illustrazione
  larga (1024×1536, verticale) renderebbe la fine della campagna un momento vero.
- **Schermata di fine partita.** Stessa cosa, in negativo.
- **Icona dell'app a risoluzione piena.** `Element.png` è 256×256: basta per l'APK
  (viene scalata), ma una 1024×1024 darebbe un'icona più pulita sul telefono.
- **Effetti sonori.** Non ce n'è nessuno su disco: il gioco li **sintetizza** con WebAudio
  (colpo, guadagno, perdita, morte, boss, premio). Funzionano e non pesano niente.
  Dei suoni veri sarebbero meglio, ma non è un buco.

---

## 3. Cosa c'è già e ora viene usato

Roba che era sul disco e il vecchio gioco non mostrava mai:

- **`armi/` — 20 illustrazioni.** Non erano referenziate da nessuna riga di codice.
  Ora sono le figure degli artefatti: 5 armi singole, 10 armi doppie, 5 scudi singoli.
- **`pic2/` livello 3 — 5 illustrazioni** (`fire3`, `water3`, `nature3`, `light3`, `darkness3`).
  Il vecchio calcolo del livello saltava il 3: non uscivano mai. Ora sì.
- **`pics/*bg.png` — 5 sfondi.** Prima erano lo sfondo pieno della pagina; ora sono una
  velatura che ruota lentamente dietro al ritratto.

Restano inutilizzati, ma per scelta: `pics/background.png`, `pics/background2.png`,
`pics/pergamena*.png` (la pergamena della vecchia carta delle quest).
