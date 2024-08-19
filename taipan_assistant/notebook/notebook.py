from collections import UserDict, defaultdict
from typing import List, Dict

from taipan_assistant.notebook.note import Note
from taipan_assistant.search.engine import Engine


class Notebook(UserDict):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.index = 0
        self.search = Engine(["title", "text", "tags"])

    def add_note(self, title: str, note: str) -> str:
        note_id = f'note-{self.index}'
        self.data[note_id] = Note(title, note)
        self.search.add_to_index(note_id, self.data[note_id])
        self.index += 1

        return note_id

    def get_note(self, key: str) -> Note:
        return self.data[key]

    def edit_note(self, note_id: str, new_text) -> None:
        note = self.data[note_id]
        note.edit_note(new_text)
        self.search.add_to_index(note_id, note)

    def delete_note(self, key: str) -> None:
        del self.data[key]
        self.search.remove_from_index(key)

    def find_notes(self, search_text: str) -> List[Note]:
        return self.search.find(search_text)

    def add_tag(self, note_id: str, tag: str) -> None:
        note = self.data[note_id]
        note.add_tag(tag)
        self.search.add_to_index(note_id, note)

    def sort_notes_by_tags(self) -> Dict[str, Dict[str, Note]]:
        tags = defaultdict(dict)
        for note_id, note in self.data.items():
            for tag in note.tags:
                tags[str(tag).lower().capitalize()].update({note_id: note})

        return dict(sorted(tags.items()))
