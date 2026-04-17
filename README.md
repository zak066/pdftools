# PDF Tools

Applicazione desktop Windows per la creazione e manipolazione di file PDF.

![Versione](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.10+-green)
![Licenza](https://img.shields.io/badge/license-MIT-orange)

## Indice

- [Funzionalità](#funzionalità)
- [Requisiti](#requisiti)
- [Installazione](#installazione)
- [Utilizzo](#utilizzo)
- [Shortcut tastiera](#shortcut-tastiera)
- [Configurazione](#configurazione)
- [Struttura progetto](#struttura-progetto)
- [Build exe](#build-exe-opzionale)
- [Note tecniche](#note-tecniche)
- [Licenza](#licenza)

## Funzionalità

### Crea PDF da file

| Formato | Estensioni | Note |
|---------|-----------|------|
| Testo | `.txt` | Supporto multi-encoding (UTF-8, Latin-1, CP1252) |
| Word | `.docx` | Preserva dimensioni font dei paragrafi |
| LibreOffice | `.odt` | Estrazione testo completo |
| Excel | `.xlsx`, `.xls` | Tabelle con bordi e intestazioni |
| CSV | `.csv` | Righe alternate colorate, header evidenziato |

### Manipola PDF esistenti

| Operazione | Descrizione |
|------------|-------------|
| **Merge** | Unisci 2 o più PDF in un unico documento |
| **Estrai pagine** | Estrai pagine specifiche (supporta range: `1,3-5,7`) |
| **Dividi PDF** | Dividi un PDF in file separati per pagina |
| **Elimina pagine** | Rimuovi pagine selezionate |
| **Ruota pagine** | Ruota la pagina corrente di +90° o -90° |
| **Sposta pagine** | Sposta la pagina su o giù nell'ordine |

### Interfaccia

- **Sidebar sinistra**: miniature delle pagine con selezione multipla (Ctrl+Click, Shift+Click)
- **Area centrale**: anteprima della pagina selezionata
- **Drag & Drop**: trascina un PDF sulla finestra per aprirlo
- **Menu e Toolbar**: accesso rapido a tutte le operazioni
- **Barra di stato**: feedback sulle operazioni eseguite

## Requisiti

- Python 3.10+
- Windows 10/11

## Installazione

1. **Clona o scarica il progetto**

2. **Attiva il virtual environment**:
   ```bash
   venv\Scripts\activate.bat
   ```

3. **Installa le dipendenze**:
   ```bash
   pip install -r requirements.txt
   ```

## Utilizzo

Avvia l'applicazione:
```bash
python main.py
```

### Flusso tipico

1. **Apri un PDF**: `File → Apri PDF` (Ctrl+O) oppure trascina il file sulla finestra
2. **Naviga le pagine**: clicca sulle miniature nella sidebar sinistra
3. **Modifica**: usa il menu `Edit` o la toolbar per merge, estrai, dividi, ruota, elimina
4. **Salva**: `File → Salva PDF` (Ctrl+S)

### Creare PDF da altri formati

- **Menu rapido**: `File → Crea PDF da...` e scegli il formato
- **Dialog generale**: `File → Crea PDF da file...` (Ctrl+N) per selezionare qualsiasi formato supportato
- Il PDF viene salvato automaticamente nella stessa cartella del file originale

## Shortcut tastiera

| Tasto | Funzione |
|-------|---------|
| `Ctrl+O` | Apri PDF |
| `Ctrl+N` | Crea PDF da file |
| `Ctrl+S` | Salva PDF |
| `Ctrl+M` | Merge PDF |
| `Ctrl+E` | Estrai pagine |
| `Ctrl+D` | Dividi PDF |
| `Del` | Elimina pagine selezionate |
| `PgUp` | Sposta pagina su |
| `PgDown` | Sposta pagina giù |

## Configurazione

### URL aggiornamenti

L'URL per il controllo aggiornamenti può essere configurato in 3 modi (in ordine di priorità):

1. **Variabile d'ambiente** `PDFTOOLS_UPDATE_URL`
2. **File di configurazione** `config.json`:
   ```json
   {
     "update_url": "https://tuoserver.com/version.json"
   }
   ```
3. **Default**: URL configurato in `config.py`

Il file `config.json` viene cercato in:
- `%APPDATA%\pdftools\config.json`
- Cartella dell'eseguibile (se buildato con PyInstaller)
- Directory corrente

## Struttura progetto

```
pdftools/
├── main.py                  # Entry point
├── app.py                   # Application class (PySide6)
├── config.py                # Costanti dell'applicazione
│
├── gui/
│   ├── __init__.py
│   ├── main_window.py       # Finestra principale (menu, toolbar, azioni)
│   ├── dialogs/
│   │   ├── __init__.py
│   │   ├── create_dialog.py # Dialog: crea PDF da file
│   │   ├── merge_dialog.py  # Dialog: merge PDF multipli
│   │   └── extract_dialog.py# Dialog: estrai pagine
│   └── widgets/
│       ├── __init__.py
│       ├── pdf_sidebar.py   # Sidebar con miniature pagine
│       ├── pdf_preview.py   # Anteprima pagina centrale
│       └── drop_area.py     # Area visualizzazione/drop
│
├── core/
│   ├── __init__.py
│   ├── pdf_merge.py         # Unione PDF multipli
│   ├── pdf_extract.py       # Estrazione pagine (con parsing range)
│   ├── pdf_split.py         # Split PDF in pagine singole
│   └── pdf_edit.py          # Delete, rotate, reorder, move pagine
│
├── converters/
│   ├── __init__.py
│   ├── txt_to_pdf.py        # TXT → PDF (multi-encoding)
│   ├── docx_to_pdf.py       # DOCX → PDF (conserva font size)
│   ├── odt_to_pdf.py        # ODT → PDF
│   ├── xlsx_to_pdf.py       # XLSX → PDF (tabelle)
│   └── csv_to_pdf.py        # CSV → PDF (tabelle con header)
│
├── utils/
│   ├── __init__.py
│   ├── logger.py            # Setup loguru (file + stderr)
│   ├── exceptions.py        # Handler eccezioni globali
│   ├── pdf_utils.py         # Thumbnail, estrazione testo/immagini
│   └── updater.py           # Check/download aggiornamenti
│
├── requirements.txt
└── README.md
```

## Dipendenze

| Libreria | Versione | Scopo |
|----------|----------|-------|
| PySide6 | >= 6.5.0 | GUI (Qt6) |
| pypdf | >= 3.17.0 | Manipolazione PDF (merge, split, extract) |
| PyMuPDF | >= 1.23.0 | Rendering pagine, thumbnail |
| reportlab | >= 4.0.0 | Generazione PDF da zero |
| python-docx | >= 1.0.0 | Lettura file DOCX |
| odfpy | >= 1.0.0 | Lettura file ODT |
| openpyxl | >= 3.1.0 | Lettura file XLSX |
| pandas | >= 2.0.0 | Parsing CSV |
| loguru | >= 0.7.0 | Logging |

## Build exe (opzionale)

Per creare un eseguibile standalone:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed main.py
```

L'eseguibile sarà nella cartella `dist/`.

### Configurazione per build

Se vuoi includere il file di configurazione nell'exe:
```bash
pyinstaller --onefile --windowed --add-data "config.json;." main.py
```

## Note tecniche

### Architettura

L'applicazione segue un'architettura modulare a 4 livelli:

- **GUI** (`gui/`): interfaccia utente con PySide6
- **Core** (`core/`): logica di manipolazione PDF con pypdf
- **Converters** (`converters/`): conversione formati → PDF con reportlab
- **Utils** (`utils/`): servizi trasversali (logging, eccezioni, utility)

### Logging

I log sono scritti in:
- **Console** (stderr): livello INFO, formato compatto
- **File**: `%USERPROFILE%\.pdftools\pdftools.log`, livello DEBUG, rotazione 10MB, retention 7 giorni

Se l'app è buildata con PyInstaller, i log vengono salvati nella stessa cartella dell'exe.

### Gestione encoding

I converter di testo (`txt_to_pdf`, `csv_to_pdf`) provano automaticamente più encoding in ordine: UTF-8 → Latin-1 → CP1252.

### Estrazione pagine

La sintassi per selezionare pagine supporta:
- Pagine singole: `1,3,5`
- Range: `3-7`
- Combinati: `1,3-5,7,10-12`

I numeri pagina sono 1-based (come visualizzati nell'interfaccia).

## Licenza

MIT License
