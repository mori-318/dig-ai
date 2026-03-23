from threading import Lock
from typing import Any, Dict, Optional


class AppraisalStateStore:
    def __init__(self) -> None:
        self._data: Dict[str, Dict[str, Any]] = {}
        self._lock = Lock()

    def set(self, thread_id: str, payload: Dict[str, Any]) -> None:
        with self._lock:
            self._data[thread_id] = payload

    def update(self, thread_id: str, changes: Dict[str, Any]) -> None:
        with self._lock:
            current = self._data.get(thread_id, {})
            if not isinstance(current, dict):
                current = {}
            current.update(changes)
            self._data[thread_id] = current

    def get(self, thread_id: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            return self._data.get(thread_id)

    def delete(self, thread_id: str) -> None:
        with self._lock:
            self._data.pop(thread_id, None)
