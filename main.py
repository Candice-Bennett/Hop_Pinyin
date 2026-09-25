from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

import requests

from ankiconnect_client import AnkiConnectClient
from config import Config
from console import fatal, warn
from pinyin_updater import PinyinUpdater


def ask_confirm(count: int) -> bool:
    while True:
        answer = input(f"Update {count} note(s)? [y/N]: ")
        answer = answer.strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("", "n", "no"):
            return False
        print("Please answer y or n.")


def main() -> None:
    cfg = Config.load("config.json")
    if not cfg.note_type:
        fatal("Usage: set note_type in config.json to the Anki note type holding the pinyin field")

    client = AnkiConnectClient(cfg.ankiconnect_url)
    try:
        client.invoke("version")
    except requests.exceptions.ConnectionError:
        fatal(
            "Couldn't connect to AnkiConnect.\n"
            "  - Make sure Anki is open\n"
            "  - Make sure the AnkiConnect add-on is installed (code 2055492159) and Anki was restarted after installing it\n"
            f"  - Check that ankiconnect_url in config.json matches AnkiConnect's address (currently {cfg.ankiconnect_url!r})"
        )
    except requests.exceptions.Timeout:
        fatal(
            "AnkiConnect took too long to respond.\n"
            "  - Anki might be showing a popup asking to allow this app, check Anki and click yes then run this again\n"
            "  - Otherwise Anki might just be busy (e.g. syncing), try again in a bit"
        )

    updater = PinyinUpdater(client, cfg.note_type, cfg.hanzi_field, cfg.pinyin_field)
    updates = updater.compute_updates(cfg.add_spaces)
    print(f"Pinyin: {len(updates)} note(s) need {'spacing' if cfg.add_spaces else 'spaces removed'}")

    if not updates:
        return

    if not ask_confirm(len(updates)):
        warn("Cancelled, no changes made")
        return

    updater.apply(updates)
    print(f"Done: updated {len(updates)} note(s)")


if __name__ == "__main__":
    main()
