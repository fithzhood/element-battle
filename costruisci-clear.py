# Genera la versione "clear": stesso gioco, senza l'easter egg delle GIF.
#
#   python costruisci-clear.py
#
# Non e' una copia a mano (divergerebbe alla prima modifica): ritaglia da
# element.js le funzioni che REALIZZANO il segreto e scrive element-clear.js.
# Le due versioni condividono element.css, element-data.js e img/.
#
# Cosa viene tolto:
#   inflateRaw, gifsFromZip   lettura dell'archivio
#   bindEasterEgg             la pressione lunga di 3 secondi sullo stemma
#   askZip, loadZip           scelta del file e attivazione della modalita'
#
# Restano i rami `if (this.gifMode ...)` sparsi nel motore: sono innocui perche'
# gifMode non puo' piu' diventare vero, e toglierli vorrebbe dire riscrivere
# mezzo file rischiando di rompere quello che funziona.

import io
import re
import sys

SORGENTE_JS = 'element.js'
SORGENTE_HTML = 'element.html'
USCITA_JS = 'element-clear.js'
USCITA_HTML = 'element-clear.html'

FUNZIONI_MODULO = ['inflateRaw', 'gifsFromZip']
METODI = ['bindEasterEgg', 'askZip', 'loadZip']

# nessuna di queste parole deve sopravvivere nel file generato
VIETATE = ['DecompressionStream', 'gifsFromZip', 'askZip', 'loadZip',
           'bindEasterEgg', '.zip', 'longPress', '}, 3000)']


def togli_blocco(testo, intestazione, indent):
    """rimuove un blocco che inizia con `intestazione` e finisce con la prima
       graffa chiusa alla stessa indentazione"""
    i = testo.find(intestazione)
    if i < 0:
        return testo, False
    # risale a inizio riga, portandosi via eventuali commenti attaccati sopra
    inizio = testo.rfind('\n', 0, i) + 1
    chiusura = '\n' + ' ' * indent + '}\n'
    fine = testo.find(chiusura, i)
    if fine < 0:
        return testo, False
    return testo[:inizio] + testo[fine + len(chiusura):], True


def main():
    js = io.open(SORGENTE_JS, encoding='utf-8').read()
    tolti = []

    for nome in FUNZIONI_MODULO:
        js, ok = togli_blocco(js, 'async function ' + nome, 0)
        if not ok:
            js, ok = togli_blocco(js, 'function ' + nome, 0)
        tolti.append((nome, ok))

    for nome in METODI:
        js, ok = togli_blocco(js, '    ' + nome + '(', 4)
        if not ok:
            js, ok = togli_blocco(js, '    async ' + nome + '(', 4)
        tolti.append((nome, ok))

    # la chiamata che accendeva l'uovo
    js = js.replace('        this.bindEasterEgg();\n', '')
    # il commento che lo annunciava
    js = re.sub(r'\n */\* -+ modalità GIF \(uovo\) \*/\n', '\n', js)

    js = ("/* Element Battle — versione clear, senza l'easter egg delle GIF.\n"
          "   NON si modifica a mano: si rigenera con costruisci-clear.py. */\n"
          + js)
    io.open(USCITA_JS, 'w', encoding='utf-8').write(js)

    html = io.open(SORGENTE_HTML, encoding='utf-8').read()
    html = html.replace('element.js?v=', 'element-clear.js?v=')
    io.open(USCITA_HTML, 'w', encoding='utf-8').write(html)

    for nome, ok in tolti:
        print(('  tolto  ' if ok else '  NON TROVATO  ') + nome)

    rimaste = [p for p in VIETATE if p in js]
    if rimaste:
        print('\nATTENZIONE, tracce rimaste nel file generato:', rimaste)
        return 1
    if not all(ok for _, ok in tolti):
        print('\nqualcosa non e stato tolto: element.js e cambiato, aggiorna lo script')
        return 1
    print(f'\n{USCITA_JS} e {USCITA_HTML} scritti, nessuna traccia dell uovo')
    return 0


if __name__ == '__main__':
    sys.exit(main())
