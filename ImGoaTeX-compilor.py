#!/usr/bin/env python3


import re
from collections import namedtuple
import argparse
from pathlib import Path
import os, sys
import time

import formatingFunctions
import lexer
import parseAST



time_compile = time.time()
ABS_COMPILOR_PATH = os.path.dirname(os.path.realpath(__file__))+"/"
Token = namedtuple("Token", ["type", "value", "line"])



# tokenize each lines
def tokenize_lines(lines):
    tokens = []
    line_number = 0
    for line in lines:
        line_number += 1
        line = line.strip()
        if not line:
            continue
        else:
            token, after_expression = lexer.tokenize_expression(line, line_number, lines)
            if token != None:
                tokens.append(token)
            else:
                continue
            while after_expression.lstrip(" ") != "":
                token, after_expression = lexer.tokenize_expression(after_expression.lstrip(" "), line_number, lines)
                tokens.append(token)
    return(tokens)



# creates the presentation object (AST) from the tokens
def parse(tokens, folder, lines, CSSVARS, PORTABLE_MEDIAS=True):
    presentation = parseAST.Presentation()
    current_frame = None
    for token in tokens:
        current_frame = parseAST.parse_filtering(token, presentation, PORTABLE_MEDIAS, current_frame ,folder, CSSVARS, lines)
    return(presentation)



# takes the presentation data and generate the output file/files
def write_output_html_file(presentation, css_variable, css_variable_fullscreen, folder, name="output.html", CSS_FILE_GENERATION=False, SECTIONS=True, OUTLINE=True):
    PRESENTATION_FRAME = f"<div id='0'class='frame FadeIn FadeOut'><h1>{presentation.title}</h1><h2>{presentation.subtitle}</h2><h3>author : {presentation.author}</h3><h3>date : {presentation.date}</h3></div>"

    INDEXES = {}
    if OUTLINE:
        frame_number_indexing = 2
    else:
        frame_number_indexing = 1

    for k in range(len(presentation.sections)):
        INDEXES[(k,-1)] = frame_number_indexing
        if SECTIONS:
            frame_number_indexing += 1
        for l in range(len(presentation.sections[k].subsections)):
            INDEXES[(k,l)] = frame_number_indexing
            frame_number_indexing += len(presentation.sections[k].subsections[l].frames)

    FRAMES = ""
    if OUTLINE:
        frame_number = 2
    else:
        frame_number = 1

    for k in range(len(presentation.sections)):
        if SECTIONS:
            SUBSECTIONS_HTML = ""
            for l in range(len(presentation.sections[k].subsections)):
                SUBSECTIONS_HTML = SUBSECTIONS_HTML + f"<h3 onclick='goToSlide({INDEXES[(k,l)]})'>● {presentation.sections[k].subsections[l].title}</h3>"
            SECTION_FRAME = f"<div id='{frame_number}' class='frame ZoomIn RotateOut'><h1 style='padding-top: calc(10*var(--uniit_y))'>{presentation.sections[k].title}</h1><div class='subsectionsOfSection'>{SUBSECTIONS_HTML}</div></div>"
            FRAMES = FRAMES + SECTION_FRAME
            frame_number += 1
        for l in range(len(presentation.sections[k].subsections)):
            for m in range(len(presentation.sections[k].subsections[l].frames)):
                classes = ""
                classes_animations = ""
                for arg in presentation.sections[k].subsections[l].frames[m].options:
                    arg = arg.replace(" ", "")
                    arg = arg.replace("=", "_")
                    classes += arg + " "
                for arg in presentation.sections[k].subsections[l].frames[m].animations:
                    classes_animations += arg + " "
                if presentation.sections[k].subsections[l].frames[m].subtitle is not None:
                    FRAME_BODY = f"<div class='frameTitle'><h2>{k+1}.{l+1}-{m+1} : {presentation.sections[k].subsections[l].frames[m].title}</h2><h3 class='frameNumber'>{frame_number}</h3></div><div class='frameSubtitle'><h3>{presentation.sections[k].subsections[l].frames[m].subtitle}</h3></div>"
                else:
                    FRAME_BODY = f"<div class='frameTitle'><h2>{k+1}.{l+1}-{m+1} : {presentation.sections[k].subsections[l].frames[m].title}</h2><h3 class='frameNumber'>{frame_number}</h3></div>"
                if presentation.sections[k].subsections[l].frames[m].subtitle:
                    FRAME_BODY = FRAME_BODY + f"<div class='frameContentSub {classes}'>"
                else:
                    FRAME_BODY = FRAME_BODY + f"<div class='frameContent {classes}'>"
                for content in presentation.sections[k].subsections[l].frames[m].contents:
                    FRAME_BODY = FRAME_BODY + content
                FRAME_BODY = FRAME_BODY + "</div>"
                FRAME_BODY = f"<div id='{frame_number}' class='frame {classes_animations}'>{FRAME_BODY}</div>"
                frame_number+=1
                FRAMES = FRAMES + FRAME_BODY


    OUTLINE_HTML_FRAME = ""
    for k in range(len(presentation.sections)):
        OUTLINE_HTML_FRAME = OUTLINE_HTML_FRAME + f"<h2 onclick='goToSlide({INDEXES[(k,-1)]})'>{k+1} ) {presentation.sections[k].title}</h2>\n"
        for l in range(len(presentation.sections[k].subsections)):
            OUTLINE_HTML_FRAME = OUTLINE_HTML_FRAME + f"<h3 onclick='goToSlide({INDEXES[(k,l)]})' style='margin-left:5vw'>{k+1}.{l+1} ) {presentation.sections[k].subsections[l].title}</h3>\n"

    if OUTLINE:
        OUTLINE_HTML_FRAME = f"<div id='1' class='frame FadeIn FadeOut'><div class='outline'><div>{OUTLINE_HTML_FRAME}</div></div></div>"
        body = PRESENTATION_FRAME + OUTLINE_HTML_FRAME + FRAMES
    else:
        body = PRESENTATION_FRAME + FRAMES

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

    try:
        with open(ABS_COMPILOR_PATH + "highlights/highlight.min.js", 'r') as highlight_min_js_file:
            highlight_min_js = f"<script>{highlight_min_js_file.read()}</script>"
        with open(ABS_COMPILOR_PATH + "highlights/atom-one-dark.css", 'r') as atom_one_dark_file:
            atom_one_dark_css = f"<style>{atom_one_dark_file.read()}</style>" + "<style>.hljs {background: transparent !important;}</style>"
    except:
        print("HighlightsJS files not found, please run `install.sh`")
        sys.exit(1)

    with open(folder+name, "w+") as outfile:
        if CSS_FILE_GENERATION:
            outfile.write(f"""<!DOCTYPE html><html><head>{katex_min_css}{katex_min_js}{katex_render_min_js}{atom_one_dark_css}{highlight_min_js}<script>hljs.highlightAll();</script><style>{css_variable}</style><style>{css_variable_fullscreen}</style><link rel="stylesheet" href="static/styles.css"><meta charset="UTF-8"><title>{presentation.title}</title></head><body><div class="overlay-menu"><button id="start">↑↑</button><button id="up">↑</button><input type="number" id="slideNumber" min="0" value="0"><button id="down">↓</button><button id="end">↓↓</button><button id="fullscreen">⛶</button></div><div class="loading" id="loading"><p class="loading-text">loading...</p></div>"{body}</body>{javascript}</html>""")
        else:
            outfile.write(f"""<!DOCTYPE html><html><head>{katex_min_css}{katex_min_js}{katex_render_min_js}{atom_one_dark_css}{highlight_min_js} <script>hljs.highlightAll();</script> <style>{css_variable}</style> <style>{css_variable_fullscreen}</style> <style>{style_code}</style> <meta charset="UTF-8"><title>{presentation.title}</title></head> <body><div class="overlay-menu"><button id="start">↑↑</button><button id="up">↑</button><input type="number" id="slideNumber" min="0" value="0"><button id="down">↓</button><button id="end">↓↓</button><button id="fullscreen">⛶</button></div><div class="loading" id="loading"><p class="loading-text">loading...</p></div>{body}</body>{javascript}</html>""")




if __name__ == "__main__" :
    arguments_parser = argparse.ArgumentParser()
    arguments_parser.add_argument("filename", help="The file to compile")
    args = arguments_parser.parse_args()

    CSSVARS= [
        16,
        9,
        "#faf3e1", #bgcolor
        "#6b3016", #color1
        "#783a1f", #color2
        "#ad5e3b", #color3
        "#362821", #color4
        1.5, #basefontsize
        "Noto Serif", #font
    ]

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
        presentation = parse(tokens, folder, lines, CSSVARS)
        css_variable = formatingFunctions.root_css(CSSVARS[0], CSSVARS[1], CSSVARS[2], CSSVARS[3], CSSVARS[4], CSSVARS[5], CSSVARS[6], CSSVARS[7], CSSVARS[8])
        css_variable_fullscreen = formatingFunctions.root_css_fullscreen(CSSVARS[0], CSSVARS[1], CSSVARS[2], CSSVARS[3], CSSVARS[4], CSSVARS[5], CSSVARS[6], CSSVARS[7], CSSVARS[8])
        write_output_html_file(presentation, css_variable, css_variable_fullscreen, folder)
        print(f"\n >> ImGoaTeX ~~~~ The file : `{file}` compiled to `./output.html` in {(time.time() - time_compile):.3f} seconds \n")
