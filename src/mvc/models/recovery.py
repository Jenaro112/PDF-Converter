"""Crash-recovery snapshots kept outside user documents."""
import hashlib
import json
import os
import tempfile
from pathlib import Path


class RecoveryManager:
    def __init__(self):
        self.directory = Path(tempfile.gettempdir()) / 'pdf_converter_recovery'
        self.directory.mkdir(parents=True, exist_ok=True)

    def _path(self, source_path: str) -> Path:
        key = hashlib.sha256(os.path.abspath(source_path or 'unsaved').encode()).hexdigest()[:24]
        return self.directory / f'{key}.json'

    def save(self, source_path: str, text: str):
        path = self._path(source_path)
        with path.open('w', encoding='utf-8') as handle:
            json.dump({'source_path': source_path, 'text': text, 'saved_at': __import__('time').time()}, handle)

    def load_if_newer(self, source_path: str):
        path = self._path(source_path)
        if not path.exists(): return None
        try:
            data = json.loads(path.read_text(encoding='utf-8'))
            original_mtime = os.path.getmtime(source_path) if source_path and os.path.exists(source_path) else 0
            return data if data.get('saved_at', 0) > original_mtime else None
        except (OSError, json.JSONDecodeError):
            return None

    def clear(self, source_path: str):
        try: self._path(source_path).unlink()
        except FileNotFoundError: pass
