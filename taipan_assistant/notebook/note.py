from datetime import datetime

from taipan_assistant.notebook.tag import Tag


class Note:
    def __init__(self, title: str, text: str):
        self.title = title
        self.text = text
        self.tags = set()
        self.updated_at = datetime.now()

    def edit_title(self, title: str):
        self.title = title
        self.updated_at = datetime.now()

    def edit_note(self, text: str):
        self.text = text
        self.updated_at = datetime.now()

    def add_tag(self, tag: str):
        self.tags.add(Tag(tag))
        self.updated_at = datetime.now()

    def __str__(self) -> str:
        return f'''{'-' * 10}
Title: \n{self.title}
{'-' * 10}
Text: \n{self.text}
{'-' * 10}
Tags: \n{', '.join(map(lambda tag: str(tag), self.tags))}
{'-' * 10}
Last changed:
{self.updated_at.strftime("%Y-%m-%d %H:%M:%S")}
'''
