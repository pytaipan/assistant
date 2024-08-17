from taipan_assistant.contacts.record.tag import Tag


class Note:
    def __init__(self, text: str):
        self.text = text
        self.tags = []

    def edit(self, text: str):
        self.text = text

    def add_tag(self, tag: str):
        self.tags.append(Tag(tag))

    def __str__(self) -> str:
        return self.text
