from record.tag import Tag

class Note:
    def __init__(self, value: str):
        self.value = value
        self.tags = []

    def edit(self, value: str):
        self.value = value

    def add_tag(self, tag: str):
        self.tags.append(Tag(tag))

    def __str__(self) -> str:
        return self.value
