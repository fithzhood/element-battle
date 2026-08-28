# Genera la versione "clear": stesso gioco, senza l'easter egg.
#
#   python costruisci-clear.py
#
# Non e' una copia a mano (divergerebbe alla prima modifica): ritaglia dai file
# originali tutto quello che riguarda il segreto e scrive element-clear.html,
# element-clear.js, element-clear.css. Le due versioni condividono solo
# element-data.js (che non ne parla) e le immagini.
#
# Non basta togliere il meccanismo: se resta un `gifMode` o un `#gif-slot`,
# chi apre il sorgente capisce lo stesso che esiste una modalita' nascosta.
# Per questo alla fine lo script cerca le parole proibite e si rifiuta di
# scrivere se ne trova anche una.

import io
import re
import sys

# `(?<!strin)` perche' JSON.stringify contiene "gif" e farebbe scattare
# l'allarme su codice che non c'entra niente
VIETATE = [r'(?<!strin)gif', 'zip', 'easter', 'DecompressionStream',
           'longPress', r', 3000\)']
# per togliere righe di commento e regole css basta la parola nuda
VIETATE_RIGHE = ['gif', 'zip', 'easter', 'DecompressionStream', 'longPress']

FUNZIONI_MODULO = ['inflateRaw', 'gifsFromZip']
METODI = ['bindEasterEgg', 'askZip', 'loadZip', 'assignGif', 'gifNodes',
          'switchToNormal', 'playGifBurst', 'showFrozenGif', 'playVictoryGif']

# sostituzioni puntuali nei punti dove il motore consulta la modalita' nascosta
SOSTITUZIONI = [
    ("            gifSlot:   $('#gif-slot'),\n", ''),
    ("            gifshow:   $('#gifshow'),\n", ''),
    (",\n            changeBtn: $('#btn-change')", ''),
    ("        this.gifMode  = false;\n        this.gifs     = [];\n"
     "        this.usedGifs = new Set();\n", ''),
    ("        return { normal: 10, gif: 10 };", "        return { normal: 10 };"),
    ("        if (this.gifMode && this.gifs.length) this.assignGif();\n", ''),
    ("        if (this.gifMode && this.enemy.gif) await this.playGifBurst(dmg);\n\n", ''),
    ("        const key = this.gifMode ? 'gif' : 'normal';",
     "        const key = 'normal';"),
    ("        await this.playVictoryGif();\n", ''),
    ("(this.gifMode ? this.best.gif : this.best.normal)", "this.best.normal"),
    ("this.dom.best.textContent = this.gifMode ? this.best.gif : this.best.normal;",
     "this.dom.best.textContent = this.best.normal;"),
    ("        this.dom.gifSlot.innerHTML = '';\n"
     "        this.dom.gifSlot.hidden = !(this.gifMode && e.gif);\n"
     "        this.dom.art.hidden = !!(this.gifMode && e.gif);\n"
     "        if (this.gifMode && e.gif) this.showFrozenGif();\n", ''),
    ("        this.dom.changeBtn.onclick = () => this.switchToNormal();\n", ''),
]

INTESTAZIONE = ("/* Element Battle — motore.\n"
                "   File generato: non si modifica a mano. */\n")


def togli_blocco(testo, intestazione, indent):
    """rimuove il blocco che inizia con `intestazione`, insieme al commento
       che lo precede, fino alla graffa chiusa alla stessa indentazione"""
    i = testo.find(intestazione)
    if i < 0:
        return testo, False
    inizio = testo.rfind('\n', 0, i) + 1
    # Si porta via anche il commento che sta sopra. Non basta guardare se la
    # riga comincia con `*`: un commento di piu' righe scritto in prosa ha le
    # righe di mezzo che cominciano con una parola qualsiasi, e restavano li'
    # (28 ago 2026: una riga sfuggita cosi' ha fatto scattare il guardiano).
    # Quando si incontra una riga che CHIUDE un commento, si risale fino al `/*`.
    dentro = False
    while True:
        prec = testo.rfind('\n', 0, inizio - 1) + 1
        riga = testo[prec:inizio].strip()
        if dentro:
            inizio = prec
            if '/*' in riga:
                dentro = False
            continue
        if riga.startswith('/*') or riga.startswith('*') or riga.startswith('//'):
            inizio = prec
        elif riga.endswith('*/'):
            inizio = prec
            dentro = '/*' not in riga
        else:
            break
    chiusura = '\n' + ' ' * indent + '}\n'
    fine = testo.find(chiusura, i)
    if fine < 0:
        return testo, False
    return testo[:inizio] + testo[fine + len(chiusura):], True


def pulisci_js():
    js = io.open('element.js', encoding='utf-8').read()
    esiti = []
    for nome in FUNZIONI_MODULO:
        js, ok = togli_blocco(js, 'async function ' + nome, 0)
        if not ok:
            js, ok = togli_blocco(js, 'function ' + nome, 0)
        esiti.append((nome, ok))
    for nome in METODI:
        js, ok = togli_blocco(js, '    ' + nome + '(', 4)
        if not ok:
            js, ok = togli_blocco(js, '    async ' + nome + '(', 4)
        esiti.append((nome, ok))
    for cerca, metti in SOSTITUZIONI:
        if cerca not in js:
            esiti.append((cerca.strip()[:44], False))
        js = js.replace(cerca, metti)
    js = js.replace('        this.bindEasterEgg();\n', '')
    # righe di commento che nominano il segreto
    js = '\n'.join(r for r in js.split('\n')
                   if not (r.strip().startswith('/*') and re.search('|'.join(VIETATE), r, re.I)))
    js = re.sub(r'\n{3,}', '\n\n', js)
    # via l'intestazione originale INTERA: e' un commento su piu' righe, e
    # togliendone solo la prima resta una riga orfana e il file non compila
    if js.lstrip().startswith('/*'):
        js = js[js.index('*/') + 2:].lstrip()
    return INTESTAZIONE + js, esiti


def pulisci_css():
    righe = io.open('element.css', encoding='utf-8').read().split('\n')
    tenute = [r for r in righe if not re.search('|'.join(VIETATE_RIGHE), r, re.I)]
    testo = '\n'.join(tenute)
    if testo.count('{') != testo.count('}'):
        raise SystemExit('lo stacco nel css ha lasciato graffe scompagnate: '
                         'una regola sulle gif non e piu su una riga sola')
    return re.sub(r'\n{3,}', '\n\n', testo)


def togli_elemento(html, ident):
    """toglie l'elemento con quell'id, anche se sta su piu' righe

       Prima si andava per stringa esatta, e bastava riscrivere un pulsante su
       tre righe invece che su una perche' restasse dentro (28 ago 2026)."""
    i = html.find('id="%s"' % ident)
    if i < 0:
        return html, False
    apertura = html.rfind('<', 0, i)
    tag = re.match(r'<([a-zA-Z0-9]+)', html[apertura:]).group(1)
    fine = html.find('</%s>' % tag, i)
    if fine < 0:
        return html, False
    fine += len(tag) + 3
    riga = html.rfind('\n', 0, apertura) + 1      # via anche l'indentazione
    if html[fine:fine + 1] == '\n':
        fine += 1
    return html[:riga] + html[fine:], True


def pulisci_html():
    html = io.open('element.html', encoding='utf-8').read()
    for ident in ('btn-change', 'gif-slot', 'gifshow'):
        html, tolto = togli_elemento(html, ident)
        # fatale, non un avviso: un avviso scorre via e la clear esce sporca
        if not tolto:
            raise SystemExit('elemento html non trovato: ' + ident)
    html = html.replace('element.js?v=', 'element-clear.js?v=')
    html = html.replace('element.css?v=', 'element-clear.css?v=')
    return html


def main():
    js, esiti = pulisci_js()
    css = pulisci_css()
    html = pulisci_html()

    for nome, ok in esiti:
        print(('  tolto  ' if ok else '  NON TROVATO  ') + nome)

    guai = []
    for nome, testo in (('element-clear.js', js), ('element-clear.css', css),
                        ('element-clear.html', html)):
        for parola in VIETATE:
            n = len(re.findall(parola, testo, re.I))
            if n:
                guai.append(f'{nome}: "{parola}" x{n}')
    if guai:
        print('\nNIENTE SCRITTO, sono rimaste tracce:')
        for g in guai:
            print('   ', g)
        return 1
    if not all(ok for _, ok in esiti):
        print('\nqualcosa non e stato tolto: element.js e cambiato, aggiorna lo script')
        return 1

    io.open('element-clear.js', 'w', encoding='utf-8').write(js)
    io.open('element-clear.css', 'w', encoding='utf-8').write(css)
    io.open('element-clear.html', 'w', encoding='utf-8').write(html)
    print('\nscritti element-clear.html/.js/.css — nessuna delle parole proibite')
    return 0


if __name__ == '__main__':
    sys.exit(main())
