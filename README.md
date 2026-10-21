# whatsapp_data_mining

Python script that analyzes an exported WhatsApp chat (`.txt`) and generates statistics per contact: messages per hour and per month, yearly totals and most-used words. The charts go to a PDF.

## What it does (`whatsap_miningV2.py`)

- Parses lines in the WhatsApp export format `DD/MM/YY HH:MM - Name: message` (skipping media placeholders such as `<Arquivo ...>`).
- For each contact, counts:
  - messages per hour of the day (one chart per month)
  - messages per month (one chart per year)
  - most frequent words (words longer than 4 letters, ignoring laughter like `kkkk`/`ahah`)
- Saves every chart to `<chat file>_graficos.pdf` (matplotlib `PdfPages`) and prints a text report with each contact's most-used words per month.

## Usage

```bash
pip install pandas numpy matplotlib
python3 whatsap_miningV2.py "Conversa do WhatsApp com Fulano.txt"
# -> "Conversa do WhatsApp com Fulano.txt_graficos.pdf"
```

Export the chat from WhatsApp ("Export chat" → without media). The parser expects the Brazilian date format (`DD/MM/YY`) and 24-hour times.

## Documentation

The module is documented with Sphinx (`conf.py`, `index.rst`, `Makefile`/`make.bat`):

```bash
pip install sphinx
make html      # output in _build/html
```
