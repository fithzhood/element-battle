# Element Battle — stato degli asset

Aggiornato il 28 agosto 2026.

## Non manca più niente di obbligatorio

Tutti e **32 gli artefatti hanno la loro illustrazione**. I 12 che mancavano —
i 10 scudi doppi e le 2 benedizioni — sono stati generati con **Gemini
(Nano Banana 2)** il 28 agosto 2026, nello stile degli altri: oggetto grande e
centrato, illustrazione fantasy dipinta, lo sfondo è l'elemento stesso, 1:1.

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
| `b1.jpg` | Ancestral Mage Prosperity | tutti e cinque |
| `b2.jpg` | Sage's Absolute Calm | luce |

Sono 1024×1024 (le vecchie sono 2048²): il gioco le riduce comunque a 320,
quindi la differenza non si vede.

### La regola imparata generandole

Su una coppia di elementi il rischio è che **uno si mangi l'altro**. Alla prima
passata `s2dn` e `s2dw` erano solo viola — di verde e di azzurro non c'era
traccia — e `s2fn` aveva foglie rosso-autunno invece che verdi. Rifatti
chiedendo esplicitamente il **colore tipico di ciascuno dei due**, ben presente e
riconoscibile al primo colpo d'occhio. Le versioni scartate stanno in
`armi/_scarti/`, che il generatore ignora perché guarda solo dentro `armi/`.

## Se un giorno si vuole alzare l'asticella

Niente di questo blocca qualcosa:

- **Illustrazioni dedicate ai boss.** Il boss usa l'illustrazione dei mostri
  normali del suo livello, con cornice e aura diverse. Cinque versioni
  "sovrano", una per elemento, si vedrebbero.
- **Schermata del finale e di fine partita.** Ora usano l'icona `Element.png`
  ingrandita; un'illustrazione verticale (1024×1536) renderebbe di più.
- **Icona a risoluzione piena.** `Element.png` è 256×256 e per l'APK viene
  scalata; una 1024×1024 sarebbe più pulita sul telefono.
- **Effetti sonori veri.** Ora sono sintetizzati con WebAudio (colpo, guadagno,
  perdita, morte, boss, premio): funzionano e non pesano niente.

## Come sono fatte le cartelle

`pic2/` (mostri), `armi/` (artefatti) e `pics/` (sfondi) tengono gli originali.
Il gioco **non li apre**: carica solo `img/`, che sono le copie ridotte in WebP
(40,1 MB → 3,5 MB). Dopo aver aggiunto o rifatto un'illustrazione va rilanciato:

```bash
python costruisci-immagini.py
```

Restano inutilizzati per scelta: `pics/background.png`, `pics/background2.png`,
`pics/pergamena*.png`.
