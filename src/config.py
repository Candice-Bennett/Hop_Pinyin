from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from console import warn


@dataclass
class Config:

    note_type: str = ""
    hanzi_field: str = "Hanzi"
    pinyin_field: str = "Pinyin"
    ankiconnect_url: str = "http://127.0.0.1:8765"

    @classmethod
    def load(cls, path: str | Path) -> "Config":
        try:
            raw = json.loads(Path(path).read_text(encoding="utf-8"))
            raw = {k: v for k, v in raw.items() if v != ""}
            return cls(**raw)
        except FileNotFoundError:
            warn(f"Config: couldn't find {str(path)!r}, using default settings")
        except (json.JSONDecodeError, TypeError) as e:
            warn(f"Config: {str(path)!r} is malformed ({e}), using default settings")
        return cls()
