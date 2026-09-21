from __future__ import annotations

import re
from dataclasses import dataclass

from ankiconnect_client import AnkiConnectClient
from console import warn
from pinyin_spacing import space_pinyin


@dataclass
class PinyinUpdate:
    note_id: int
    hanzi: str
    before: str
    after: str


def strip_html(text: str) -> str:
    return re.sub(r"<[^>]+>", "", text).strip()


class PinyinUpdater:
    def __init__(self, client: AnkiConnectClient, note_type: str, hanzi_field: str, pinyin_field: str):
        self.client = client
        self.note_type = note_type
        self.hanzi_field = hanzi_field
        self.pinyin_field = pinyin_field

    def _resolve_field(self, actual_fields: list[str], field_name: str) -> str | None:
        if field_name in actual_fields:
            return field_name
        match = next((a for a in actual_fields if a.lower() == field_name.lower()), None)
        if match:
            warn(f"Pinyin: field {field_name!r} not found on {self.note_type!r}, using {match!r} instead")
            return match
        warn(f"Pinyin: field {field_name!r} not found on {self.note_type!r} (fields: {actual_fields})")
        return None

    def compute_updates(self) -> list[PinyinUpdate]:
        note_ids = self.client.invoke("findNotes", {"query": f'note:"{self.note_type}"'})
        if not note_ids:
            warn(f"Pinyin: no notes found for note type {self.note_type!r}, check the spelling in Anki")
            return []

        actual_fields = self.client.invoke("modelFieldNames", {"modelName": self.note_type})
        hanzi_field = self._resolve_field(actual_fields, self.hanzi_field)
        pinyin_field = self._resolve_field(actual_fields, self.pinyin_field)
        if hanzi_field is None or pinyin_field is None:
            return []

        infos = self.client.invoke("notesInfo", {"notes": note_ids})
        updates = []
        for info in infos:
            hanzi = strip_html(info.get("fields", {}).get(hanzi_field, {}).get("value", ""))
            pinyin = info.get("fields", {}).get(pinyin_field, {}).get("value", "")
            if not hanzi or not pinyin:
                continue
            spaced = space_pinyin(hanzi, pinyin)
            if spaced == pinyin:
                continue
            updates.append(PinyinUpdate(info["noteId"], hanzi, pinyin, spaced))
        return updates

    def apply(self, updates: list[PinyinUpdate]) -> None:
        if not updates:
            return
        actions = [
            {
                "action": "updateNoteFields",
                "params": {"note": {"id": u.note_id, "fields": {self.pinyin_field: u.after}}},
            }
            for u in updates
        ]
        results = self.client.invoke("multi", {"actions": actions})
        for u, result in zip(updates, results):
            if result and result.get("error"):
                warn(f"Pinyin: failed to update note {u.note_id} ({u.hanzi}): {result['error']}")
