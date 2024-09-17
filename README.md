# QR Code Generator

## Descrizione

QR Code Generator è un'applicazione web sviluppata in Django che permette di generare QR code personalizzati. Gli utenti possono specificare colori, caricare immagini e visualizzare un'anteprima del QR code generato. Inoltre, l'applicazione tiene traccia di quante volte il QR code è stato scansionato.

## Caratteristiche

- Generazione di QR code con colori personalizzati per il modulo e lo sfondo.
- Possibilità di caricare un'immagine per essere inclusa nel QR code.
- Anteprima del QR code prima della generazione finale.
- Tracciamento del numero di scansioni per ciascun QR code e progetto.

## Requisiti

- Python 3.8 o superiore
- Django 4.0 o superiore
- [Pillow](https://pillow.readthedocs.io/en/stable/) (per la manipolazione delle immagini)
- [qrcode](https://pypi.org/project/qrcode/) (per la generazione dei QR code)
