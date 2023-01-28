from pathlib import Path
from .content import Content
from typing import List, Union


class Report:
    """
    Wrapper class for collecting content and exporting to various formats.
    """

    def __init__(self, title: str):
        self.title = title
        self.content: List[Content] = []

    def add_content(self, content: Content):
        self.content.append(content)

    def remove_content(self, key: str):
        for i, c in enumerate(self.content):
            if c.key == key:
                self.content.pop(i)
                break

    def export_to_pdf(self, file_name: Union[str, Path]):
        pass

    def export_to_html(self, file_name: Union[str, Path]):
        pass

    def export_to_latex(self, file_name: Union[str, Path]):
        pass
