import re
from collections import namedtuple
import datetime
from dataclasses import dataclass, field
import argparse
from pathlib import Path
import base64



Token = namedtuple("Token", ["type", "value"])

# regex patterns
# (r'^\\begin\{frame\}\{([^}]*)\}', "BEGIN_FRAME"),
# (r'^%*(.+?):\s*(.+)$', "META"),
# (r'^\\begin\{frame\}\{(.+?)\}', "BEGIN_FRAME"),
# (r'^\\begin\{frame\}((?:\{[^}]*\})+)', "BEGIN_FRAME"),
# (r'^\\image\{(.+?)\}', "IMAGE"),
TOKEN_PATTERNS = [
    (r'^%(.+?):\s*(.+)$', "META"),
    (r'^\\section\{(.+?)\}', "SECTION"),
    (r'^\\subsection\{(.+?)\}', "SUBSECTION"),
    (r'^\\begin\{frame\}((?:\{[^}]*\})+)', "BEGIN_FRAME"),
    (r'^\\end\{frame\}', "END_FRAME"),
    (r'^\\video\{([^}]*)\}(?:\[([^\]]*)\])?', "VIDEO"),
    (r'^\\image\{([^}]*)\}(?:\[([^\]]*)\])?', "IMAGE"),
    (r'^\\item\{(.+?)\}', "ITEM"),
    (r'^\\subitem\{(.+?)\}', "SUBITEM"),
    (r'^\\note\{(.+?)\}', "NOTE"),
]


# tokenization
def tokenize_expression(expression):
    for pattern, typ in TOKEN_PATTERNS:
        matching = re.match(pattern, expression)
        if matching:

            if typ == "META":
                key, val = matching.groups()
                return Token("META", (key.strip(), val.strip()))

            elif typ == "BEGIN_FRAME":
                args_frame = re.findall(r'\{([^}]*)\}', matching.group(1))
                if matching.groups():
                    if len(args_frame) > 2:
                        raise Exception(f"you gave too much argument to the frame '{args_frame[1]}', it only takes 2")
                    else:
                        return Token(typ, tuple(args_frame))
                else:
                    return Token(typ, None)

            elif typ == "IMAGE":
                if matching.groups()[1]:
                    image_source, args_img = matching.group(1), matching.group(2).split(",")
                    return Token(typ, tuple([image_source, args_img]) )
                else:
                    return Token(typ, matching.group(1))

            elif typ == "VIDEO":
                if matching.groups()[1]:
                    video_source, args_vid = matching.group(1), matching.group(2).split(",")
                    return Token(typ, tuple([video_source, args_vid]))
                else:
                    return Token(typ, matching.group(1))

            elif typ == "ITEM":
                if matching.group(1):
                    token_inside = tokenize_expression(matching.group(1))
                    print(token_inside)
                return ( Token(typ, token_inside) )

            elif typ == "SUBITEM":
                if matching.group(1):
                    token_inside = tokenize_expression(matching.group(1))
                    print(token_inside)
                return ( Token(typ, token_inside) )


            else:
                if matching.groups():
                    return Token(typ, matching.group(1))
                else:
                    return Token(typ, None)
    return Token("TEXT", expression)

def tokenize_lines(lines):
    tokens = []
    for line in lines:
        line = line.strip()
        if not line or line[0] == '#':
            continue
        else:
            token = tokenize_expression(line)
            tokens.append(token)
    return(tokens)




# data structure
class Presentation:
    def __init__(self, title=None, subtitle=None, author=None, date=None):
        self.title = title
        self.subtitle = subtitle
        self.author = author
        self.date = datetime.datetime.now().strftime("%a %d %b %Y")
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
    def __init__(self, title=None, subtitle=None):
        self.title = title
        self.subtitle = subtitle
        self.contents = []

class Item:
    def __init__(self, contents):
        self.contents = contents

class Subitem:
    def __init__(self, contents):
        self.contents = contents

class Text:
    def __init__(self, text):
        self.text = text

class Video:
    def __init__(self, url):
        self.url = url


def parse_filtering(token, presentation, PORTABLE_MEDIAS, current_frame):
    if token.type == "META":
        key, val = token.value
        if key == "title":
            presentation.title = val
        if key == "subtitle":
            presentation.subtitle = val
        if key == "author":
            presentation.author = val
        if key == "date":
            try_date = tuple(key.split("-")) # day-month-year
            try:
                presentaton.date = datetime.strptime(try_date)
            except:
                None # default date with datetime.datetime -> see the presentation class

    if token.type == "SECTION":
        if token.value: # if the section has a title
            presentation.sections.append( Section(token.value) ) # create a section with the title : token.value
        else:
            raise Exception("No name were given for the section")

    if token.type == "SUBSECTION":
        if token.value: # if the subsection has a title
            if presentation.sections != []: # if the presentation has a section
                presentation.sections[-1].subsections.append( Subsection(token.value) ) # adds the subsection to the last section created
            else:
                raise Exception("A subsection has been tried to be created, but no sections were declared beforehand")
        else:
            raise Exception("No name were given for the subsection")


    if token.type == "BEGIN_FRAME":
        if current_frame is not None:
            raise Exception(f"the frame {current_frame.title} has not been close, you cannot begin another one")
        if presentation.sections != []:
            if presentation.sections[-1] != []:
                if len(token.value) == 2:
                    frame_title, frame_subtitle = token.value
                    presentation.sections[-1].subsections[-1].frames.append( Frame(frame_title, frame_subtitle) )
                else:
                    frame_title = token.value[0]
                    presentation.sections[-1].subsections[-1].frames.append( Frame(frame_title) )
                current_frame = presentation.sections[-1].subsections[-1].frames[-1]
            else:
                raise Exception("A frame has been tried to be created, but no subsection were declared beforehand")
        else:
            raise Exception("A frame has been tried to be created, but no section nor subsection were declared beforehand")

    if token.type == "END_FRAME":
        if current_frame is not None:
            current_frame = None
        else:
            raise Exception("You are not in a frame, you thus cannot end a frame")

    if token.type == "ITEM":
        print(token.value)
        if current_frame:
            current_frame = parse_filtering(token.value, presentation, PORTABLE_MEDIAS, current_frame)
    if token.type == "SUBITEM":
        #print(token.value)
        if current_frame:
            current_frame = parse_filtering(token.value, presentation,PORTABLE_MEDIAS, current_frame)



    if token.type == "TEXT":
        if current_frame:
            current_frame.contents.append( parse_text_to_html( token.value ) )
            #print(presentation.sections[-1].subsections[-1].frames[-1].contents)
        else:
            raise Exception("You are not in a frame, you thus cannot add text to a frame")

    if token.type == "VIDEO":
        if current_frame:
            if type(token.value) != type( tuple() ):
                try:
                    with open("medias/"+token.value, 'rb') as vid:
                        if PORTABLE_MEDIAS:
                            video_html = f"<video style='width: calc(20*var(--unit_x))' src='data:video/mp4;base64,{base64.b64encode(vid.read()).decode("utf-8")}' controls autoplay loop muted></video>"
                        else:
                            video_html = f"<video style='width: calc(20*var(--unit_x))' src='medias/{token.value}' controls autoplay loop muted></video>"
                        current_frame.contents.append( video_html )
                except:
                    current_frame.contents.append( f"<p> empty video pane, cannot find the file : ' medias/{token.value} '</p>" )
            else:
                try:
                    with open("medias/"+token.value[0], 'rb') as vid:
                        #print("VIDEO OPTIONS : ", token.value[1])
                        classes = ""
                        for arg in token.value[1]:
                            arg = arg.replace(" ", "")
                            arg = arg.replace("=", "_")
                            classes = classes + arg + " "
                        if PORTABLE_MEDIAS:
                            video_html = f"<video style='width: calc(20*var(--unit_x))' class='{classes}' src='data:video/mp4;base64,{base64.b64encode(vid.read()).decode("utf-8")}' controls autoplay loop muted></video>"
                        else:
                            video_html = f"<video style='width: calc(20*var(--unit_x))' class='{classes}' src='medias/{token.value[0]}' controls autoplay loop muted></video>"
                        current_frame.contents.append( video_html )
                except:
                    current_frame.contents.append( f"<p> empty video pane, cannot find the file : ' medias/{token.value[0]} '</p>" )
        else:
            raise Exception("You are not in a frame, you thus cannot add text to a frame")

    if token.type == "IMAGE":
        if current_frame:
            if type(token.value) != type( tuple() ):
                try:
                    with open("medias/"+token.value, 'rb') as img:
                        if PORTABLE_MEDIAS:
                            image_html = f"<img style='width: calc(20*var(--unit_x))' src='data:image/png;base64,{base64.b64encode(img.read()).decode("utf-8")}'</img>"
                        else:
                            image_html = f"<img style='width: calc(20*var(--unit_x))' src='medias/{token.value}'</img>"
                    current_frame.contents.append( image_html )
                except:
                    current_frame.contents.append( f"<p> empty image pane, cannot find the file : ' medias/{token.value} '</p>" )
            else:
                try:
                    with open("medias/"+token.value[0], 'rb') as img:
                        #print("IMAGE OPTIONS : ", token.value[1])
                        classes = ""
                        for arg in token.value[1]:
                            arg = arg.replace(" ", "")
                            arg = arg.replace("=", "_")
                            classes = classes + arg + " "
                        if PORTABLE_MEDIAS:
                            image_html = f"<img style='width: calc(20*var(--unit_x))' class='{classes}' src='data:image/png;base64,{base64.b64encode(img.read()).decode("utf-8")}'></img>"
                        else:
                            image_html = f"<img style='width: calc(20*var(--unit_x))' class='{classes}' src='medias/{token.value[1]}'></img>"
                    current_frame.contents.append( image_html )
                except:
                    current_frame.contents.append( f"<p> empty image pane, cannot find the file : ' medias/{token.value[0]} '</p>" )
        else:
            raise Exception("You are not in a frame, you thus cannot add text to a frame")
    return(current_frame)





def parse(tokens, PORTABLE_MEDIAS=True):
    presentation = Presentation()
    current_frame = None

    for token in tokens:
        current_frame = parse_filtering(token, presentation, PORTABLE_MEDIAS, current_frame)
    return(presentation)


# parse text in html format
def parse_text_to_html(text):
    parts = re.split(r'(\\\\|\\n)', text)
    bad = {r"\\", r"\n", r""}
    for i in range(len(parts)):
        # ** ... ** to <b> ... </b>
        parts[i] = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', parts[i])
        # * ... * or _ ... _ to <i> ... </i>
        parts[i] = re.sub(r'\*(.+?)\*', r'<i>\1</i>', parts[i])
        # \textbf{...} to <b> ... </b>
        parts[i] = re.sub(r'\\textbf\{(.+?)\}', r'<b>\1</b>', parts[i])
        # \textit{...} to <i> ... </i>
        parts[i] = re.sub(r'\\textit\{(.+?)\}', r'<i>\1</i>', parts[i])

    outText = ''
    for part in parts:
        if part not in bad:
            outText = outText + f"<p>{part}</p>"
    return(outText)



# takes the presentation data and generate the output file/files
def write_output_html_file(presentation, name="output.html", CSS_FILE_GENERATION=False):
    PRESENTATION_FRAME = f"<div id='0'class='frame'><h1>{presentation.title}</h1><h2>{presentation.subtitle}</h2><h3>author : {presentation.author}</h3><h3>date : {presentation.date}</h3></div>"

    OUTLINE_HTML_FRAME = ""
    for k in range(len(presentation.sections)):
        OUTLINE_HTML_FRAME = OUTLINE_HTML_FRAME + f"<h2>{k+1} ) {presentation.sections[k].title}</h2>\n"
        for l in range(len(presentation.sections[k].subsections)):
            OUTLINE_HTML_FRAME = OUTLINE_HTML_FRAME + f"<h3 style='margin-left:5vw'>{k+1}.{l+1} ) {presentation.sections[k].subsections[l].title}</h3>\n"

    FRAMES = ""
    frame_number = 2
    for k in range(len(presentation.sections)):
        for l in range(len(presentation.sections[k].subsections)):
            for m in range(len(presentation.sections[k].subsections[l].frames)):
                if presentation.sections[k].subsections[l].frames[m].subtitle:
                    FRAME_BODY = f"<div class='frameTitle'><h2>{k+1}.{l+1}-{m+1} : {presentation.sections[k].subsections[l].frames[m].title}</h2></div><div class='frameSubtitle'><h3>{presentation.sections[k].subsections[l].frames[m].subtitle}</h3></div>"
                else:
                    FRAME_BODY = f"<div class='frameTitle'><h2>{k+1}.{l+1}-{m+1} : {presentation.sections[k].subsections[l].frames[m].title}</h2></div>"
                if presentation.sections[k].subsections[l].frames[m].subtitle:
                    FRAME_BODY = FRAME_BODY + "<div class='frameContentSub'>"
                else:
                    FRAME_BODY = FRAME_BODY + "<div class='frameContent'>"
                for content in presentation.sections[k].subsections[l].frames[m].contents:
                    FRAME_BODY = FRAME_BODY + content
                FRAME_BODY = FRAME_BODY + "</div>"
                FRAME_BODY = f"<div id='{frame_number}' class='frame'>{FRAME_BODY}</div>"
                frame_number+=1
                FRAMES = FRAMES + FRAME_BODY

    OUTLINE_HTML_FRAME = f"<div>{OUTLINE_HTML_FRAME}</div>"
    OUTLINE_HTML_FRAME = f"<div id='1' class='frame'><div class='outline'>{OUTLINE_HTML_FRAME}</div></div>"

    body = PRESENTATION_FRAME + OUTLINE_HTML_FRAME + FRAMES

    javascript = """
<script>
let currentSlide = 0;
const slideInput = document.getElementById("slideNumber");

// Find all slides with numeric IDs and sort them
const slides = Array.from(document.querySelectorAll("div[id]"))
  .filter(div => !isNaN(div.id))
  .sort((a, b) => Number(a.id) - Number(b.id));

// Function to go to a slide
const goToSlide = n => {
  const slide = slides.find(s => Number(s.id) === n);
  if (!slide) return;
  slide.scrollIntoView({ behavior: "smooth", block: "center" });
  currentSlide = n;
  slideInput.value = currentSlide;
};

// On page load, go to slide 0
goToSlide(0);

// Up/Down buttons
document.getElementById("up").addEventListener("click", () => goToSlide(currentSlide - 1));
document.getElementById("down").addEventListener("click", () => goToSlide(currentSlide + 1));

// Input events
slideInput.addEventListener("change", () => goToSlide(Number(slideInput.value)));
slideInput.addEventListener("keydown", e => {
  if (e.key === "ArrowUp") goToSlide(currentSlide + 1);
  if (e.key === "ArrowDown") goToSlide(currentSlide - 1);
});
</script>
            """
    with open("styles.css", 'r') as style:
        style_code = style.read()

    css_variable = """
:root {
        --ar_width: 16;
        --ar_height: 9;
        --unit_x: calc( min(90vw, calc( ( var(--ar_width) / var(--ar_height) ) * 90vh) )/100 );
        --unit_y: calc( min(90vh, calc( ( var(--ar_height) / var(--ar_width) ) * 90vw) )/100 );
        --bgcolor: #faf3e1;
        --color1: #6b3016;
        --color2: #783a1f;
        --color3: #ad5e3b;
        --color4: #362821;
}
    """
    with open("katex/katex_min.css", 'r') as katex_min_css_file:
        katex_min_css = f"<style>{katex_min_css_file.read()}</style>"
    with open("katex/katex_min.js", 'r') as katex_min_js_file:
        katex_min_js = f"<script defer>{katex_min_js_file.read()}</script>"
    with open("katex/auto_render_min.js", 'r') as katex_render_min_js_file:
        katex_render_min_js = f"<script defer>{katex_render_min_js_file.read()}</script>"
        katex_render_min_js += """
<script>
    document.addEventListener("DOMContentLoaded", function() {
        renderMathInElement(document.body, {
            delimiters: [
                { left: "$$", right: "$$", display: true },
                { left: "$", right: "$",  display: false }
            ]
        });
    });
</script>
        """
    try:
        with open("katex/katex_min.css", 'r') as katex_min_css_file:
            katex_min_css = f"<style>{katex_min_css_file.read()}</style>"
        with open("katex/katex_min.js", 'r') as katex_min_js_file:
            katex_min_js = f"<script defer>{katex_min_js_file.read()}</script>"
        with open("katex/auto_render_min.js", 'r') as katex_render_min_js_file:
            katex_render_min_js = f"<script defer>{katex_render_min_js_file.read()}</script>"
            katex_render_min_js += """
                <script>
        document.addEventListener("DOMContentLoaded", function() {
            renderMathInElement(document.body, {
                delimiters: [
                    { left: "$$", right: "$$", display: true },
                    { left: "$", right: "$",  display: false }
                ]
            });
        });
    </script>
            """
    except:
        raise Exception("KaTeX files not found, you may run `install.sh`")

    with open(name, "w+") as outfile:
        if CSS_FILE_GENERATION:
            outfile.write(f"""<!DOCTYPE html><html><head>{katex_min_css}{katex_min_js}{katex_render_min_js}<style>{css_variable}</style><link rel="stylesheet" href="styles.css"><meta charset="UTF-8"><title>{presentation.title}</title></head><body><div class="overlay-menu"><button id="up">↑</button><input type="number" id="slideNumber" min="0" value="0"><button id="down">↓</button></div>{body}</body>{javascript}</html>""")
        else:
            outfile.write(f"""<!DOCTYPE html><html><head>{katex_min_css}{katex_min_js}{katex_render_min_js}<style>{css_variable}</style><style>{style_code}</style><meta charset="UTF-8"><title>{presentation.title}</title></head><body><div class="overlay-menu"><button id="up">↑</button><input type="number" id="slideNumber" min="0" value="0"><button id="down">↓</button></div>{body}</body>{javascript}</html>""")


if __name__ == "__main__" :
    arguments_parser = argparse.ArgumentParser()
    arguments_parser.add_argument("filename", help="The file to compile")
    args = arguments_parser.parse_args()

    if args.filename:
        file_path = Path(args.filename)
        if not file_path.is_file():
            raise Exception(f"Error: '{args.filename}' does not exist or is not a file.")
            exit(1)
        else:
            file = args.filename

    file = "main.igtex"
    with open(file, 'r') as igtexFile:
        lines = igtexFile.readlines()
        #tokens = tokenize(lines)
        tokens = tokenize_lines(lines)
        #print(tokens)
        presentation = parse(tokens)
        #write_output_html_file(presentation, CSS_FILE_GENERATION=True)
        write_output_html_file(presentation)
