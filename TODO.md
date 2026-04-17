# PDF Tools - Piano di Sviluppo

## Panoramica Progetto

**Nome**: PDF Tools
**Tipo**: Applicazione desktop Windows
**Licenza**: Open Source (MIT)
**Python**: 3.10+

## Stack Tecnologico

| Componente | Libreria | Versione |
|------------|----------|----------|
| GUI | PySide6 | ^6.5.0 |
| PDF manipolazione | pypdf | ^3.17.0 |
| PDF analisi/modifica | PyMuPDF | ^1.23.0 |
| PDF creazione | reportlab | ^4.0.0 |
| DOCX | python-docx | ^1.0.0 |
| ODT | odfpy | ^1.0.0 |
| Excel | openpyxl | ^3.1.0 |
| CSV | pandas | ^2.0.0 |
| Logging | loguru | ^0.7.0 |

## Funzionalità

### 1. Crea PDF da file ✅

| # | Input | Output | Priorità |
|---|------|--------|----------|
| 1.1 | .txt → PDF | ✅ Alta |
| 1.2 | .docx → PDF | ✅ Alta |
| 1.3 | .odt → PDF | ✅ Media |
| 1.4 | .xlsx, .xls → PDF | ✅ Alta |
| 1.5 | .csv → PDF | ✅ Alta |

### 2. Manipola PDF ✅

| # | Funzionalità | Descrizione | Priorità |
|---|--------------|-------------|----------|
| 2.1 | Merge PDF | Combina 2+ PDF in uno | ✅ Alta |
| 2.2 | Estrai pagine | Estrai pagine specifiche | ✅ Alta |
| 2.3 | Dividi PDF | Dividi PDF in file separati | ✅ Alta |
| 2.4 | Elimina pagine | Rimuovi pagine selezionate | ✅ Alta |
| 2.5 | Ruota pagine | Ruota +/-90 gradi | ✅ Alta |
| 2.6 | Sposta pagine | Sposta su/giù | ✅ Media |

### 3. Interfaccia ✅

| # | Funzionalità | Priorità |
|---|--------------|----------|
| 3.1 | Sidebar con miniature pagine | ✅ Alta |
| 3.2 | Anteprima pagina nel centro | ✅ Alta |
| 3.3 | Selezione multipla pagine (Ctrl/Shift+Click) | ✅ Alta |
| 3.4 | Toolbar | ✅ Media |
| 3.5 | Menu | ✅ Alta |
| 3.6 | Shortcut tastiera | ✅ Alta |

## Fasi di Sviluppo Completate

### Fase 1: Setup e GUI Base ✅
- [x] Setup progetto Python
- [x] Configura environment virtuale
- [x] Installa dipendenze
- [x] Crea main window PySide6
- [x] Menu bar e toolbar
- [x] Logger configurato

### Fase 2: Crea PDF da file ✅
- [x] Implementa txt → PDF
- [x] Implementa docx → PDF
- [x] Implementa odt → PDF
- [x] Implementa xlsx → PDF
- [x] Implementa csv → PDF

### Fase 3: Manipola PDF ✅
- [x] Merge PDF
- [x] Estrai pagine
- [x] Dividi PDF
- [x] Elimina pagine
- [x] Ruota pagine
- [x] Sposta pagine

### Fase 4: Interfaccia Utente ✅
- [x] Sidebar con miniature
- [x] Preview centro
- [x] Selezione multipla
- [x] Status bar

##Struttura Progetto

```
pdftools/
├── main.py                    # Entry point
├── app.py                   # Application class
├── gui/
│   ├── main_window.py       # Main window
│   ├── dialogs/
│   │   ├── create_dialog.py
│   │   ├── merge_dialog.py
│   │   └── extract_dialog.py
│   └── widgets/
│       ├── pdf_sidebar.py
│       ├── pdf_preview.py
│       └── drop_area.py
├── core/
│   ├── pdf_merge.py
│   ├── pdf_extract.py
│   ├── pdf_split.py
│   └── pdf_edit.py
├── converters/
│   ├── txt_to_pdf.py
│   ├── docx_to_pdf.py
│   ├── odt_to_pdf.py
│   ├── xlsx_to_pdf.py
│   └── csv_to_pdf.py
├── utils/
│   ├── logger.py
│   ├── exceptions.py
│   └── pdf_utils.py
├── requirements.txt
├── README.md
├── TODO.md
└── .gitignore
```

## Funzionalità Future (v1.1)

- [ ] Estrai immagini da PDF
- [ ] Estrai testo da PDF
- [ ] Aggiungi filigrana/watermark
- [ ] Comprimi PDF
- [ ] PDF viewer integrato più avanzato
- [ ] Tema UI scuro

---

## Fase 5: Generazione EXE ✅

### 5.1 Build eseguibile
- [x] Installa PyInstaller
- [x] Esegui: `pyinstaller --onefile --windowed main.py`
- [x] Testa eseguibile in `dist/`
- [x] Fix: logger.py per stderr=None (app windowed)
- [x] Fix: converter imports espliciti per PyInstaller

### 5.2 Istruzioni build
```bash
pip install pyinstaller
pyinstaller --onefile --windowed main.py
# Output: dist/pdftools.exe
```

---

## Fase 6: Auto-Update ✅ COMPLETO

### 6.1 Configurazione server

Sul server Linux interno configurare:

```
http://www.pdftools.local/pdftools/
├── version.json        # Info versione
├── pdftools.exe     # Eseguibile corrente
└── pdftools.exe.sig # Firma (opzionale)
```

### 6.2 File version.json (sul server)
```json
{
  "version": "1.0.1",
  "url": "http://www.pdftools.local/pdftools/pdftools.exe",
  "changelog": "- Bug fix\n- Nuove funzionalità",
  "mandatory": false,
  "released": "2026-04-16"
}
```

### 6.3 Codice Python

File: `utils/updater.py` ✅
- [x] Funzione `check_for_updates()` - contatta server
- [x] Funzione `download_update()` - scarica nuovo .exe
- [x] Dialog per notifica/download

### 6.4 Configurazione con fallback
Priorità ricerca URL:
1. `%APPDATA%/pdftools/config.json` (utente configura)
2. `./config.json` (portatile, accanto exe)
3. Valore di default nel codice

### 6.5 Menu Help
- [x] Help → Controlla aggiornamenti
- [x] Help → Informazioni su PDF Tools

### 6.6 File config.json default
File: `config.json` ✅
```json
{
  "version": "1.0.0",
  "check_on_start": true,
  "update_url": "http://www.pdftools.local/pdftools/version.json"
}
```

---

## Struttura Progetto Aggiornata

```
pdftools/
├── main.py                    # Entry point
├── app.py                   # Application class
├── config.json              # Configurazione (opzionale)
├── gui/
│   ├── main_window.py
│   ├── dialogs/
│   └── widgets/
├── core/
├── converters/
├── utils/
│   ├── logger.py
│   ├── exceptions.py
│   ├── pdf_utils.py
│   └── updater.py          # <- NUOVO
├── requirements.txt
├── README.md
└── TODO.md
```

## Note Tecniche

### Conversione Text to PDF
- Usa `reportlab` per generazione PDF
- Supporta UTF-8

### Conversione Office
- DOCX: `python-docx` → estrai testo
- ODT: `odfpy` → estrai testo
- Excel: `openpyxl` → estrai dati in tabella
- CSV: `pandas` → estrai dati in tabella

### PDF Editing
- Per modifiche: crea nuova copia con modifiche
- Non modifica il file originale

## Build

Per creare un eseguibile standalone:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed main.py
```

L'eseguibile sarà nella cartella `dist/`.