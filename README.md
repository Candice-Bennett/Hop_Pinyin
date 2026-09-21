# Hop Pinyin

Connects to Anki via AnkiConnect and adds spaces between the syllables of an
existing Pinyin field, e.g. `nǐhǎo` becomes `nǐ hǎo`. The
entry point is [main.py](main.py), and the pipeline steps live under
[src](src).

## What it does

- Finds every note of the note type set in [config.json](config.json).
- Reads the Hanzi field and Pinyin field off each note.
- Splits the pinyin to have spaces.
- Already-spaced Pinyin is left untouched.

## Prerequisites

- **Python** - get it from [python.org/downloads](https://www.python.org/downloads/). On Windows,
  tick "Add python.exe to PATH" during install, then confirm it worked with `python --version`
  in a new terminal.
- **AnkiConnect** - in Anki go to Tools > Add-ons > Get Add-ons,
  paste in code `2055492159`, and restart Anki. More info at
  [ankiweb.net/shared/info/2055492159](https://ankiweb.net/shared/info/2055492159).

## Downloading Hop Pinyin

Click the green "Code" button near the top of this page, then "Download ZIP",
and extract it somewhere.

You'll then need a terminal open *in that folder* to run the commands below. On Windows,
open the extracted folder in File Explorer, click the address bar, type `cmd`, and hit Enter.

## Running Hop Pinyin

With Anki open, set `note_type`, `hanzi_field` and `pinyin_field` in
[config.json](config.json) to match your note type, then:

```
pip install -r requirements.txt
python main.py
```

It'll print how many notes need spacing and ask you to confirm before
updating anything.

## Config ([config.json](config.json))

| Flag | What it does |
|---|---|
| `note_type` | the Anki note type to update |
| `hanzi_field` | field holding the Hanzi word |
| `pinyin_field` | field holding the Pinyin reading to space out |
| `ankiconnect_url` | default `http://127.0.0.1:8765` |
