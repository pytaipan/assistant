from collections import UserList
from typing import List
from record.note import Note

class Notebook(UserList):
    def add_note(self, note: str) -> int:
        self.data.append(Note(note))
        return len(self.data) - 1

    def get_note(self, key: int) -> Note:
        return self.data[key]

    def delete_note(self, key: int) -> None:
        if key > len(self.data) - 1:
            raise IndexError

        del self.data[key]

    def find_notes(self, search_text: str) -> List[Note]:
        pass
