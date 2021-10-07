import re

class Block:
    def __init__(self):
        pass

class QuoteBlock:
    pass

class ListBlock:
    pass

class CodeFence(Block):
    def __init__(self, text: list, level: int, lang=None):
        self.level = level
        self.lang = lang
        self.text = text
        self.char = '`'

    def __iter__(self):
        return iter(self.text)

    def __repr__(self):
        rtn = [self.char*self.level + '\n']
        rtn = rtn + self.text
        rtn.append(self.char*self.level)
        return ''.join(t for t in rtn)

class Paragraph(Block):
    # https://spec.commonmark.org/0.30/#paragraph
    def __init__(self, text: list):
        self.text = text

class Heading:
    def __init__(self, text: str, source_file='', lineno=-0):
        self.text = text
        self.source_file = source_file
        self.code_fences = []
        self.paragraphs = []

    def __repr__(self):
        return ''.join(f"{self.text}({self.level})")
    
    def add_codefence(self, cf):
        self.code_fences.append(cf)
    def add_paragraph(self, paragraph: Paragraph):
        self.paragraphs.append(paragraph)

class HashtagHeading(Heading):
    def __init__(self, level, text, source_file='', lineno=-0):
        super().__init__(text=text, source_file=source_file, lineno=lineno)
        self.level = level
        #print(self.text, self.level)
    

class BlockQuote:
    pass
class MDList:
    pass

class Entry:
    """A heading and the stuff init"""
    def __init__(self):
        self.level = level
        self.text = text
        self.block = None

    def _load_block(self, mdstring):
        pass
    
