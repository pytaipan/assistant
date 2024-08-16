from collections import UserDict
from typing import List
from record.note import Note
from search.engine import Engine


class Notebook(UserDict):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.index = 0
        self.search = Engine(["text"])

    def add_note(self, note: str) -> str:
        note_id = f'note-{self.index}'
        self.data[note_id] = Note(note)
        self.search.add_to_index(note_id, self.data[note_id])
        self.index += 1

        return note_id

    def get_note(self, key: str) -> Note:
        return self.data[key]

    def delete_note(self, key: str) -> None:
        del self.data[key]
        self.search.remove_from_index(key)

    def find_notes(self, search_text: str) -> List[Note]:
        return self.search.find(search_text)
