import re
from collections import namedtuple
import sys
import datetime
from dataclasses import dataclass, field

Token = namedtuple("Token", ["type", "value"])

# regex patterns
TOKEN_PATTERNS = [
    (r'^%*(.+?):\s*(.+)$', "META"),
    (r'^\\section\{(.+?)\}', "SECTION"),
    (r'^\\subsection\{(.+?)\}', "SUBSECTION"),
    (r'^\\begin\{frame\}\{(.+?)\}', "BEGIN_FRAME"),
    (r'^\\end\{frame\}', "END_FRAME"),
    (r'^\\video\{(.+?)\}', "VIDEO"),
    (r'^\\image\{(.+?)\}', "IMAGE"),
    (r'^\\note\{(.+?)\}', "NOTE"),
]

def tokenize(lines):
    tokens = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        matched = False
        for pattern, typ in TOKEN_PATTERNS:
            m = re.match(pattern, line)
            if m:
                if typ == "META":
                    key, val = m.groups()
                    tokens.append(Token("META", (key.strip(), val.strip())))
                else:
                    if m.groups():
                        tokens.append(Token(typ, m.group(1)))
                    else:
                        tokens.append(Token(typ, None))
                matched = True
                break
        if not matched:
            tokens.append(Token("TEXT", line))
    return(tokens)



class Presentation:
    def __init__(self, title=None, author=None, date=None):
        self.title = title
        self.author = author
        self.date = datetime.datetime.now()
        self.sections = []

class Section:
    def __init__(self, title=None):
        self.title = title
        self.subsections = []

class Subsection:
    def __init__(self, title=None):
        self.title = title
        self.frames = []

class Frame:
    def __init__(self, title=None):
        self.title = title
        self.contents = []

class Text:
    def __init__(self, text):
        self.text = text

class Video:
    def __init__(self, url):
        self.url = url


def parse(tokens):
    presentation = Presentation()
    current_frame = None

    for token in tokens:

        if token.type == "META":
            key, val =token.value
            if key == "title":
                presentation.title = val
                print("title :", val)
            if key == "author":
                presentation.author = val
                print("author :", val)
            if key == "date":
                try:
                    presentaton.date = datetime.strptime(val)
                    print("date:", datetime.strptime(val))
                except:
                    print("date:", presentation.date)
                    continue

        if token.type == "SECTION":
            if token.value:
                presentation.sections.append( Section(token.value) )
                print("section :", token.value)
            else:
                raise("No name were given for the section")

        if token.type == "SUBSECTION":
            if token.value:
                if presentation.sections != []:
                    presentation.sections[-1].subsections.append( Subsection(token.value) )
                    print("subsection :", token.value)
                else:
                    raise("A subsection has been tried to be created, but no sections were declared beforehand")
            else:
                raise("No name were given for the subsection")

        if token.type == "BEGIN_FRAME":
            if presentation.sections != []:
                if presentation.sections[-1] != []:
                    presentation.sections[-1].subsections[-1].frames.append( Frame(token.value) )
                    print("frame :", token.value)
                    current_frame = presentation.sections[-1].subsections[-1].frames[-1]
                else:
                    raise("A frame has been tried to be created, but no subsection were declared beforehand")
            else:
                raise("A frame has been tried to be created, but no section nor subsection were declared beforehand")

        if token.type == "END_FRAME":
            if current_frame:
                current_frame = None
            else:
                raise("You are not in a frame, you thus cannot end a frame")

        if token.type == "TEXT":
            if current_frame:
                current_frame.contents.append( parse_text_to_html( token.value ) )
                print(presentation.sections[-1].subsections[-1].frames[-1].contents)
            else:
                raise("You are not in a frame, you thus cannot add text to a frame")

def parse_text_to_html(content):
    return(f"<p>{content}</p>")


if __name__ == "__main__" :
    file = "main.igtex"
    with open(file, 'r') as igtexFile:
        lines = igtexFile.readlines()
        print(lines)
        print()
        tokens = tokenize(lines)
        print(tokens)
        parse(tokens)
