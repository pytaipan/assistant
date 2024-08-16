from collections import UserDict
from typing import List
from record.note import Note

class Notebook(UserDict):
    index = 0

    def add_note(self, note: str) -> str:
        self.data[f'note-{self.index}'] = Note(note)
        self.index += 1

        return f'note-{self.index}'

    def get_note(self, key: str) -> Note:
        return self.data[key]

    def delete_note(self, key: str) -> None:
        del self.data[key]

    def find_notes(self, search_text: str) -> List[Note]:
        pass
