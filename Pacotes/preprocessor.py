import re


class PreProcessor:
    def __init__(self):
        self.text = []

    def filter(self, src):
        self.text = re.sub(r"/\*.*?\*/", r"", src)
        return self.text