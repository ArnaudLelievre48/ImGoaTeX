import re
from collections import namedtuple
import datetime
from dataclasses import dataclass, field
import argparse
from pathlib import Path
import base64
import os, sys, copy
import time

time_compile = time.time()

ABS_COMPILOR_PATH = os.path.dirname(os.path.abspath(__file__))+"/"

Token = namedtuple("Token", ["type", "value", "line"])

# regex patterns
#(r'^\\begin\{frame\}((?:\{[^}]*\})+)', "BEGIN_FRAME"),
# (r'^\\item\{(.+?)\}', "ITEM"),
# (r'^\\subitem\{(.+?)\}', "SUBITEM"),
# (r'^\\textbox\{([^}]*)\}(?:\[([^\]]*)\])?', "TEXTBOX"),
TOKEN_PATTERNS = [
    (r'^%(.+?):\s*(.+)$', "META"),
    (r'^\\section\{(.+?)\}', "SECTION"),
    (r'^\\subsection\{(.+?)\}', "SUBSECTION"),
    (r'\\begin\{frame\}\{([^}]*)\}(?:\{([^}]*)\})?(?:\[([^\]]*)\])?', "BEGIN_FRAME"),
    (r'^\\end\{frame\}', "END_FRAME"),
    (r'^\\video\{([^}]*)\}(?:\[([^\]]*)\])?', "VIDEO"),
    (r'^\\image\{([^}]*)\}(?:\[([^\]]*)\])?', "IMAGE"),
    (r'^\\textbox\{((?:\$[^$]*\$|[^}])*)\}(?:\[([^\]]*)\])?', "TEXTBOX"),
    (r'\\item\{((?:\$[^$]*\$|[^}])*)\}', "ITEM"),
    (r'\\subitem\{((?:\$[^$]*\$|[^}])*)\}', "SUBSUBITEM"),
    (r'^#\.*', "COMMENT"),
    (r'^\\pause', "PAUSE"),
]


# tokenization
def tokenize_expression(expression, line_number):
    for pattern, typ in TOKEN_PATTERNS:
        matching = re.match(pattern, expression)
        if matching: # if a certain pattern has been recognized, then it's not plain text -> we treat it
            rest_expression = expression[matching.end():]

            if typ == "COMMENT":
                return None, ""

            elif typ == "META":
                key, val = matching.groups()
                return Token("META", (key.strip(), val.strip()), line_number), rest_expression

            elif typ == "BEGIN_FRAME":
                frame_title, frame_subtitle, frame_options = matching.groups()
                if frame_options is not None:
                    frame_options = frame_options.split(",")
                if matching.groups():
                    if len(matching.groups()) > 3:
                        print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} {lines[token.line]} \n\n you gave too much argument to the frame '{frame_title}', it only takes 2, a title and a subtitle plus optional options")
                        sys.exit(1)
                    else:
                        return Token(typ, (frame_title, frame_subtitle, frame_options), line_number), rest_expression
                else:
                    print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} {lines[token.line]} \n\n you did not give any argument to the frame '{frame_title}', it takes up to 2 arguments, a title, optional subtitle plus optional options")
                    sys.exit(1)

            elif typ == "PAUSE":
                return Token(typ, None, line_number), rest_expression


            elif typ == "IMAGE":
                if matching.groups()[1]:
                    image_source, args_img = matching.group(1), matching.group(2).split(",")
                    return Token(typ, tuple([image_source, args_img]), line_number ), rest_expression
                else:
                    return Token(typ, tuple([matching.group(1), None]), line_number), rest_expression

            elif typ == "VIDEO":
                if matching.groups()[1]:
                    video_source, args_vid = matching.group(1), matching.group(2).split(",")
                    return Token(typ, tuple([video_source, args_vid]), line_number), rest_expression
                else:
                    return Token(typ, tuple([matching.group(1), None]), line_number), rest_expression

            elif typ == "TEXTBOX":
                if matching.groups()[1]:
                    text_inside_token, args_text = Token("TEXT", matching.group(1), line_number), matching.group(2).split(",")
                    return Token(typ, tuple([text_inside_token, args_text]), line_number ), rest_expression
                else:
                    return Token(typ, tuple([Token("TEXT", matching.group(1), line_number), None]), line_number), rest_expression

            elif typ == "ITEM":
                if matching.group(1):
                    token_inside, _ = tokenize_expression("● " + matching.group(1), line_number)
                return ( Token(typ, token_inside, line_number) ), rest_expression

            elif typ == "SUBITEM":
                if matching.group(1):
                    token_inside, _ = tokenize_expression("○ " + matching.group(1), line_number)
                return ( Token(typ, token_inside, line_number) ), rest_expression

            elif typ == "SUBSUBITEM":
                if matching.group(1):
                    token_inside, _ = tokenize_expression("◌ " + matching.group(1), line_number)
                return ( Token(typ, token_inside, line_number) ), rest_expression


            else:
                if matching.groups():
                    return Token(typ, matching.group(1), line_number), rest_expression
                else:
                    return Token(typ, None, line_number), rest_expression
    return Token("TEXT", expression.split('#')[0], line_number), ""

def tokenize_lines(lines):
    tokens = []
    line_number = 0
    for line in lines:
        line_number += 1
        line = line.strip()
        if not line:
            continue
        else:
            token, rest_expression = tokenize_expression(line, line_number)
            if token != None:
                tokens.append(token)
            else:
                continue
            while rest_expression != "":
                token, rest_expression = tokenize_expression(rest_expression.lstrip(" "), line_number)
                tokens.append(token)
    return(tokens)




# data structure for each token type
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
    def __init__(self, title=None, subtitle=None, contents=None, options=None):
        self.title = title
        self.subtitle = subtitle
        if options is None:
            self.options = []
        else:
            self.options = copy.deepcopy(options)
        if contents is None:
            self.contents = []
        else:
            self.contents = copy.deepcopy(contents)

class Pause:
    def __init__(self, frame=None):
        self.frame = frame

class Item:
    def __init__(self, contents):
        self.contents = contents

class Subitem:
    def __init__(self, contents):
        self.contents = contents

class SubSubitem:
    def __init__(self, contents):
        self.contents = contents

class Text:
    def __init__(self, text):
        self.text = text

class Video:
    def __init__(self, url):
        self.url = url


# treat a token and how it is added to the presentation. The function returns current_frame, which is - so far - all that is necessary - besides presetation - to describe the state of the presentation being build 
def parse_filtering(token, presentation, PORTABLE_MEDIAS, current_frame, folder):
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
            print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} -- {lines[token.line]} \n\n No name were given for the section")
            sys.exit(1)

    if token.type == "SUBSECTION":
        if token.value: # if the subsection has a title
            if presentation.sections != []: # if the presentation has a section
                presentation.sections[-1].subsections.append( Subsection(token.value) ) # adds the subsection to the last section created
            else:
                print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} --  {lines[token.line]} \n\n the subsection '{token.value}' could not be created : no sections were declared beforehand")
                sys.exit(1)
        else:
            print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} {lines[token.line]} \n\n No name were given for the subsection")
            sys.exit(1)

    if token.type == "BEGIN_FRAME":
        if current_frame is not None:
            print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} -- {lines[token.line]} \n\n the frame '{current_frame.title}' could not be created, the frame '{presentation.sections[-1].subsections[-1].frames[-1].title}' has not been ended.")
            sys.exit(1)
        if presentation.sections != []:
            if presentation.sections[-1].subsections != []:
                frame_title, frame_subtitle, frame_options = token.value
                presentation.sections[-1].subsections[-1].frames.append( Frame(frame_title, frame_subtitle, None, frame_options) )
                current_frame = presentation.sections[-1].subsections[-1].frames[-1]
            else:
                print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} -- {lines[token.line]} \n\n The frame '{token.value[0]}' could not be created : no subsections were declared beforehand")
                sys.exit(1)
        else:
            print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} -- {lines[token.line]} \n\n The frame '{token.value[0]}' could not be created : no sections were declared beforehand")
            sys.exit(1)

    if token.type == "END_FRAME":
        if current_frame is not None:
            current_frame = None
        else:
            print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} -- {lines[token.line]} \n\n You are not in a frame, you thus cannot end a frame")
            sys.exit(1)

    if token.type == "PAUSE":
        if current_frame is not None:
            presentation.sections[-1].subsections[-1].frames[-1] = ( Frame(current_frame.title, current_frame.subtitle, current_frame.contents, current_frame.options) )
            presentation.sections[-1].subsections[-1].frames.append( current_frame  )
        else:
            print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} -- {lines[token.line]} \n\n You tried to pause, but you were not in a frame.")

    if token.type == "ITEM":
        inside_token = token.value
        if current_frame:
            current_frame.contents.append( "<div class='item'>" )
            current_frame = parse_filtering(inside_token, presentation, PORTABLE_MEDIAS, current_frame, folder)
            current_frame.contents.append( "</div>" )

    if token.type == "SUBITEM":
        inside_token = token.value
        if current_frame:
            current_frame.contents.append( "<div class='subitem'>" )
            current_frame = parse_filtering(inside_token, presentation,PORTABLE_MEDIAS, current_frame, folder)
            current_frame.contents.append( "</div>" )

    if token.type == "SUBSUBITEM":
        inside_token = token.value
        if current_frame:
            current_frame.contents.append( "<div class='subsubitem'>" )
            current_frame = parse_filtering(inside_token, presentation,PORTABLE_MEDIAS, current_frame, folder)
            current_frame.contents.append( "</div>" )


    if token.type == "TEXT":
        if current_frame:
            current_frame.contents.append( parse_text_to_html( token.value ) )
            #print(presentation.sections[-1].subsections[-1].frames[-1].contents)
        else:
            print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} -- {lines[token.line]} \n\n You are not in a frame, you thus cannot add text to a frame")
            sys.exit(1)

    if token.type == "VIDEO":
        if current_frame:
            imgclass = "mediaoverlay"
            inline = False
            if current_frame.subtitle is not None:
                imgclass = "mediaoverlaySub"

            try:
                with open(folder+"medias/"+token.value[0], 'rb') as vid:
                    #print("VIDEO OPTIONS : ", token.value[1])
                    classes = ""
                    classes_pos = ""
                    shift_top = "0px"
                    shift_right = "0px"
                    shift_bottom = "0px"
                    shift_left = "0px"
                    degre="0deg"
                # treat options
                    if token.value[1] is not None:
                        for arg in token.value[1]:
                            arg = arg.replace(" ", "")
                            arg = arg.replace("=", "_")

                            if arg == "inline":
                                inline = True
                            if arg[:8] == "position":
                                classes_pos = classes_pos + arg + " "
                            if arg[:6] == "rotate":
                                try:
                                    degre = f"{ str(float(arg.split('_')[1])) }deg"
                                except:
                                    print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} -- {lines[token.line]} \n\n The value given to rotate is incorrect, please use a float (deg)")
                                    sys.exit(1)
                            if arg[:5] == "shift":
                                arg = arg.split("_")[1]
                                if len(arg.split('+')) != 4:
                                    print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} -- {lines[token.line]} \n\n You tried to use shift, but the syntax was wrong, the right syntax is : shift=[top]+[right]+[bottom]+[left], the shift option is adding padding to the oposite direction to place the media, with paging unit")
                                    sys.exit(1)

                                shift_top = f"calc( {arg.split('+')[2]}*var(--unit_y) )"
                                shift_right = f"calc( {arg.split('+')[3]}*var(--unit_x) )"
                                shift_bottom = f"calc( {arg.split('+')[0]}*var(--unit_y) )"
                                shift_left  = f"calc( {arg.split('+')[1]}*var(--unit_x) )"

                            else:
                                classes = classes + arg + " "

                    if PORTABLE_MEDIAS:
                        if inline:
                            video_html = f"<video style='width: calc(20*var(--unit_x)); padding: {shift_top} {shift_right} {shift_bottom} {shift_left}; transform: rotate({degre})' class='{classes}' src='data:video/mp4;base64,{base64.b64encode(vid.read()).decode("utf-8")}' controls autoplay loop muted></video>"
                        else:
                            video_html = f"<div class='{imgclass} {classes_pos}'><video style='width: calc(20*var(--unit_x)); padding: {shift_top} {shift_right} {shift_bottom} {shift_left}; transform: rotate({degre})' class='{classes}' src='data:video/mp4;base64,{base64.b64encode(vid.read()).decode("utf-8")}' controls autoplay loop muted></video></div>"
                    else:
                        if inline:
                            video_html = f"<video style='width: calc(20*var(--unit_x)); padding: {shift_top} {shift_right} {shift_bottom} {shift_left}; transform: rotate({degre})' class='{classes}' src='{folder}medias/{token.value[0]}' controls autoplay loop muted></video>"
                        else:
                            video_html = f"<div class='{imgclass} {classes_pos}'><video style='width: calc(20*var(--unit_x)); padding: {shift_top} {shift_right} {shift_bottom} {shift_left}; transform: rotate({degre})' class='{classes}' src='{folder}medias/{token.value[0]}' controls autoplay loop muted></video></div>"
                    current_frame.contents.append( video_html )
            except:
                current_frame.contents.append( f"<div class='{imgclass}'><p style='border: solid 2px var(--color1); padding: 5em'> Cannot find the file : '{folder}medias/{token.value[0]} '</p></div>" )
        else:
            print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} -- {lines[token.line]} \n\n You are not in a frame, you thus cannot add a video to a frame")
            sys.exit(1)

    if token.type == "IMAGE":
        if current_frame:
            imgclass = "mediaoverlay"
            if current_frame.subtitle is not None:
                imgclass = "mediaoverlaySub"
            inline = False

            try:
                with open(folder+"medias/"+token.value[0], 'rb') as img:
                    classes = ""
                    classes_pos = ""
                    shift_top = "0px"
                    shift_right = "0px"
                    shift_bottom = "0px"
                    shift_left = "0px"
                    degre="0deg"
                    # treat options
                    if token.value[1] is not None:
                        for arg in token.value[1]:
                            arg = arg.replace(" ", "")
                            arg = arg.replace("=", "_")
                            if arg == "inline":
                                inline = True
                            if arg[:8] == "position":
                                classes_pos = classes_pos + arg + " "
                            if arg[:6] == "rotate":
                                try:
                                    degre = f"{ str(float(arg.split('_')[1])) }deg"
                                except:
                                    print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} -- {lines[token.line]} \n\n The value given to rotate is incorrect, please use a float (deg)")
                                    sys.exit(1)
                            if arg[:5] == "shift":
                                arg = arg.split("_")[1]
                                if len(arg.split('+')) != 4:
                                    print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} -- {lines[token.line]} \n\n You tried to use shift, but the syntax was wrong, the right syntax is : shift=[top]+[right]+[bottom]+[left], the shift option is adding padding to the oposite direction to place the media, with paging unit")
                                    sys.exit(1)

                                shift_top = f"calc( {arg.split('+')[2]}*var(--unit_y) )"
                                shift_right = f"calc( {arg.split('+')[3]}*var(--unit_x) )"
                                shift_bottom = f"calc( {arg.split('+')[0]}*var(--unit_y) )"
                                shift_left  = f"calc( {arg.split('+')[1]}*var(--unit_x) )"
                            else:
                                classes = classes + arg + " "

                    if PORTABLE_MEDIAS:
                        if inline:
                            image_html = f"<img style='width: calc(20*var(--unit_x)); padding: {shift_top} {shift_right} {shift_bottom} {shift_left}; transform: rotate({degre})' class='{classes}' src='data:image/png;base64,{base64.b64encode(img.read()).decode("utf-8")}'></img>"
                        else:
                            image_html = f"<div class='{imgclass} {classes_pos}'><img style='width: calc(20*var(--unit_x)); padding: {shift_top} {shift_right} {shift_bottom} {shift_left}; transform: rotate({degre})' class='{classes}' src='data:image/png;base64,{base64.b64encode(img.read()).decode("utf-8")}'></img></div>"
                    else:
                        if inline:
                            image_html = f"<img style='width: calc(20*var(--unit_x)); padding: {shift_top} {shift_right} {shift_bottom} {shift_left}; transform: rotate({degre})' class='{classes}' src='{folder}medias/{token.value[1]}'></img>"
                        else:
                            image_html = f"<div class='{imgclass} {imgclass_pos}'><img style='width: calc(20*var(--unit_x)); padding: {shift_top} {shift_right} {shift_bottom} {shift_left}; transform: rotate({degre})' class='{classes}' src='{folder}medias/{token.value[1]}'></img></div>"

                current_frame.contents.append( image_html )
            except:
                current_frame.contents.append( f"<div class='{imgclass}'><p style='border: solid 2px var(--color1); padding: 5em'> Cannot find the file : '{folder}medias/{token.value[0]} '</p></div>" )
        else:
            print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} -- {lines[token.line]} \n\n You are not in a frame, you thus cannot add an image to a frame")
            sys.exit(1)

    if token.type == "TEXTBOX":
        if current_frame:
            imgclass = "mediaoverlay"
            inline = False
            if current_frame.subtitle is not None:
                imgclass = "mediaoverlaySub"

            classes = ""
            classes_pos = ""
            fontsize = 1
            shift_top = "0px"
            shift_right = "0px"
            shift_bottom = "0px"
            shift_left = "0px"
            degre="0deg"
            # treat options
            if token.value[1] is not None:
                for arg in token.value[1]:
                    arg = arg.replace(" ", "")
                    arg = arg.replace("=", "_")

                    if arg == "inline":
                        inline = True
                    elif arg[:8] == "position":
                        classes_pos = classes_pos + arg + " "
                    elif arg[:8] == "fontsize":
                        try:
                            fontsize = float(arg.split('_')[1])
                        except:
                            print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} -- {lines[token.line]} \n\n The value given to rotate is incorrect, please use a float (paging unit x)")

                    elif arg[:6] == "rotate":
                        try:
                            degre = f"{ str(float(arg.split('_')[1])) }deg"
                        except:
                            print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} -- {lines[token.line]} \n\n The value given to rotate is incorrect, please use a float (deg)")
                            sys.exit(1)
                    elif arg[:5] == "shift":
                        arg = arg.split("_")[1]
                        if len(arg.split('+')) != 4:
                            print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} -- {lines[token.line]} \n\n You tried to use shift, but the syntax was wrong, the right syntax is : shift=[top]+[right]+[bottom]+[left], the shift option is adding padding to the oposite direction to place the media, with paging unit")
                            sys.exit(1)

                        shift_top = f"calc( {arg.split('+')[2]}*var(--unit_y) )"
                        shift_right = f"calc( {arg.split('+')[3]}*var(--unit_x) )"
                        shift_bottom = f"calc( {arg.split('+')[0]}*var(--unit_y) )"
                        shift_left  = f"calc( {arg.split('+')[1]}*var(--unit_x) )"

                    else:
                        classes = classes + arg + " "

            if inline:
                text_inside_html = f"<div class='wrapper {classes}' style='padding: {shift_top} {shift_right} {shift_bottom} {shift_left}; transform: rotate({degre});'><div>{ parse_text_to_html( token.value[0].value, fontsize ) }</div></div>"
            else:
                text_inside_html = f"<div class='{imgclass} {classes_pos}'><div class='wrapper {classes}' style='padding: {shift_top} {shift_right} {shift_bottom} {shift_left}; transform: rotate({degre})'><div>{ parse_text_to_html( token.value[0].value, fontsize ) }</div></div></div>"
            current_frame.contents.append( text_inside_html )
        else:
            print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} -- {lines[token.line]} \n\n You are not in a frame, you thus cannot add a textbox to a frame")
            sys.exit(1)

    return(current_frame)





# creates the presentation from the tokens
def parse(tokens, folder, PORTABLE_MEDIAS=True):
    presentation = Presentation()
    current_frame = None
    for token in tokens:
        current_frame = parse_filtering(token, presentation, PORTABLE_MEDIAS, current_frame ,folder)
    return(presentation)


# parse text in html format
def parse_text_to_html(text, fontsize=1):
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
            outText = outText + f"<p style='font-size: calc({fontsize}*var(--unit_x))'>{part}</p>"
    return(outText)


def root_css(as_w=16, as_h=9, bgcolor="#faf3e1", color1="#6b3016", color2="#783a1f", color3="#ad5e3b", color4="#362821"):
    var = f"""
        --ar_width: {as_w};
        --ar_height: {as_h};
        --unit_x: calc( min(90vw, calc( ( var(--ar_width) / var(--ar_height) ) * 90vh) )/100 );
        --unit_y: calc( min(90vh, calc( ( var(--ar_height) / var(--ar_width) ) * 90vw) )/100 );
        --bgcolor: {bgcolor};
        --color1: {color1};
        --color2: {color2};
        --color3: {color3};
        --color4: {color4};
"""

    css_root = ":root {\n" + var + "}"
    return css_root


# takes the presentation data and generate the output file/files
def write_output_html_file(presentation, css_variable, folder, name="output.html", CSS_FILE_GENERATION=False):
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
                classes = ""
                for arg in presentation.sections[k].subsections[l].frames[m].options:
                    arg = arg.replace(" ", "")
                    arg = arg.replace("=", "_")
                    classes += arg + " "
                if presentation.sections[k].subsections[l].frames[m].subtitle is not None:
                    FRAME_BODY = f"<div class='frameTitle'><h2>{k+1}.{l+1}-{m+1} : {presentation.sections[k].subsections[l].frames[m].title}</h2></div><div class='frameSubtitle'><h3>{presentation.sections[k].subsections[l].frames[m].subtitle}</h3></div>"
                else:
                    FRAME_BODY = f"<div class='frameTitle'><h2>{k+1}.{l+1}-{m+1} : {presentation.sections[k].subsections[l].frames[m].title}</h2></div>"
                if presentation.sections[k].subsections[l].frames[m].subtitle:
                    FRAME_BODY = FRAME_BODY + f"<div class='frameContentSub {classes}'>"
                else:
                    FRAME_BODY = FRAME_BODY + f"<div class='frameContent {classes}'>"
                for content in presentation.sections[k].subsections[l].frames[m].contents:
                    FRAME_BODY = FRAME_BODY + content
                FRAME_BODY = FRAME_BODY + "</div>"
                FRAME_BODY = f"<div id='{frame_number}' class='frame'>{FRAME_BODY}</div>"
                frame_number+=1
                FRAMES = FRAMES + FRAME_BODY

    OUTLINE_HTML_FRAME = f"<div>{OUTLINE_HTML_FRAME}</div>"
    OUTLINE_HTML_FRAME = f"<div id='1' class='frame'><div class='outline'>{OUTLINE_HTML_FRAME}</div></div>"

    body = PRESENTATION_FRAME + OUTLINE_HTML_FRAME + FRAMES

    # loads the differents script/style files inside variables
    with open(ABS_COMPILOR_PATH + "static/script.js", 'r') as script:
        javascript = script.read()
    with open(ABS_COMPILOR_PATH + "static/styles.css", 'r') as style:
        style_code = style.read()

    try:
        # loads katex's script/style files inside variables
        with open(ABS_COMPILOR_PATH + "katex/katex_min.css", 'r') as katex_min_css_file:
            katex_min_css = f"<style>{katex_min_css_file.read()}</style>"
        with open(ABS_COMPILOR_PATH + "katex/katex_min.js", 'r') as katex_min_js_file:
            katex_min_js = f"<script defer>{katex_min_js_file.read()}</script>"
        with open(ABS_COMPILOR_PATH + "katex/auto_render_min.js", 'r') as katex_render_min_js_file:
            katex_render_min_js = f"<script defer>{katex_render_min_js_file.read()}</script>"
            katex_render_min_js += """<script> document.addEventListener("DOMContentLoaded", function() { renderMathInElement(document.body, { delimiters: [ { left: "$$", right: "$$", display: true }, { left: "$", right: "$",  display: false } ] }); }); </script>"""

    except:
        print("KaTeX files not found, please run `install.sh`")
        sys.exit(1)

    with open(folder+name, "w+") as outfile:
        if CSS_FILE_GENERATION:
            outfile.write(f"""<!DOCTYPE html><html><head>{katex_min_css}{katex_min_js}{katex_render_min_js}<style>{css_variable}</style><link rel="stylesheet" href="static/styles.css"><meta charset="UTF-8"><title>{presentation.title}</title></head><body><div class="overlay-menu"><button id="up">↑</button><input type="number" id="slideNumber" min="0" value="0"><button id="down">↓</button></div>{body}</body>{javascript}</html>""")
        else:
            outfile.write(f"""<!DOCTYPE html><html><head>{katex_min_css}{katex_min_js}{katex_render_min_js}<style>{css_variable}</style><style>{style_code}</style><meta charset="UTF-8"><title>{presentation.title}</title></head><body><div class="overlay-menu"><button id="up">↑</button><input type="number" id="slideNumber" min="0" value="0"><button id="down">↓</button></div>{body}</body>{javascript}</html>""")



if __name__ == "__main__" :
    arguments_parser = argparse.ArgumentParser()
    arguments_parser.add_argument("filename", help="The file to compile")
    args = arguments_parser.parse_args()

    if args.filename:
        file_path = Path(args.filename)
        if not file_path.is_file():
            print(f"Error: '{args.filename}' does not exist or is not a file.")
            sys.exit(1)
        else:
            file = os.path.abspath(args.filename)
            folder = os.path.dirname(file)
            if folder:
                folder += "/"

    with open(file, 'r') as igtexFile:
        lines = igtexFile.readlines()
        tokens = tokenize_lines(lines)
        presentation = parse(tokens, folder)
        css_variable = root_css()
        write_output_html_file(presentation, css_variable, folder)
        print(f"\n >> ImGoaTeX ~~~~ The file : `{file}` compiled to `./output.html` in {(time.time() - time_compile):.3f} seconds \n")
