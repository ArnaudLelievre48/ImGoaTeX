import re
from collections import namedtuple
import sys


Token = namedtuple("Token", ["type", "value", "line"])


# regex patterns
#(r'^\\begin\{frame\}((?:\{[^}]*\})+)', "BEGIN_FRAME"),
# (r'^\\item\{(.+?)\}', "ITEM"),
# (r'^\\subitem\{(.+?)\}', "SUBITEM"),
# (r'^\\textbox\{([^}]*)\}(?:\[([^\]]*)\])?', "TEXTBOX"),
# (r'\\begin\{frame\}\{([^}]*)\}(?:\{([^}]*)\})?(?:\[([^\]]*)\])?', "BEGIN_FRAME"),
TOKEN_PATTERNS = [
    (r'^%(.+?):\s*(.+)$', "META"),
    (r'^\\section\{(.+?)\}', "SECTION"),
    (r'^\\subsection\{(.+?)\}', "SUBSECTION"),
    (r'\\begin\{frame\}\{([^}]*)\}(?:\{([^}]*)\})?(?:\[([^\]]*)\])?(?:\<([^\]]*)\>)?', "BEGIN_FRAME"),
    (r'^\\end\{frame\}', "END_FRAME"),
    (r'\\begin\{code\}\{([^}]*)\}(?:\[([^\]]*)\])?', "BEGIN_CODE"),
    (r'^\\end\{code\}', "END_CODE"),
    (r'^\\video\{([^}]*)\}(?:\[([^\]]*)\])?', "VIDEO"),
    (r'^\\image\{([^}]*)\}(?:\[([^\]]*)\])?', "IMAGE"),
    (r'^\\iframe\{([^}]*)\}(?:\[([^\]]*)\])?', "IFRAME"),
    (r'^\\codeblock\{([^}]*)\}(?:\[([^\]]*)\])?', "CODEBLOCK"),
    (r'^\\codeline\{([^}]*)\}(?:\[([^\]]*)\])?', "CODELINE"),
    (r'^\\textbox\{((?:\$[^$]*\$|[^}])*)\}(?:\[([^\]]*)\])?', "TEXTBOX"),
    (r'\\item\{((?:\$[^$]*\$|[^}])*)\}', "ITEM"),
    (r'\\subitem\{((?:\$[^$]*\$|[^}])*)\}', "SUBITEM"),
    (r'^#\.*', "COMMENT"),
    (r'^\\pause(?:\<([^\]]*)\>)?', "PAUSE"),
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
                frame_title, frame_subtitle, frame_options, frame_animations_list = matching.groups()
                frame_animations = ["FadeIn", "FadeOut"]
                if frame_options is not None:
                    frame_options = frame_options.split(",")
                if frame_animations_list is not None:
                    frame_animations_list = frame_animations_list.split(",")
                    for animation in frame_animations_list:
                        if animation.endswith("In"):
                            frame_animations[0] = animation
                        if animation.endswith("Out"):
                            frame_animations[1] = animation
                if matching.groups():
                    if len(matching.groups()) > 4:
                        print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} {lines[token.line]} \n\n you gave too much argument to the frame '{frame_title}', it only takes 2, a title and a subtitle plus optional options and animations")
                        sys.exit(1)
                    else:
                        return Token(typ, (frame_title, frame_subtitle, frame_options, frame_animations), line_number), rest_expression
                else:
                    print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} {lines[token.line]} \n\n you did not give any argument to the frame '{frame_title}', it takes up to 2 arguments, a title, optional subtitle plus optional options")
                    sys.exit(1)

            elif typ == "BEGIN_CODE":
                code_language, code_options = matching.groups()
                if code_options is not None:
                    code_options = code_options.split(",")
                if matching.groups():
                    if len(matching.groups()) > 2:
                        print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} {lines[token.line]} \n\n you gave too much argument to the code block, it only takes 1, programming language, plus optional options")
                        sys.exit(1)
                    else:
                        return Token(typ, (code_language, code_options), line_number), rest_expression
                else:
                    print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} {lines[token.line]} \n\n you did not give any argument to the code block,  it only takes 1, programming language, plus optional options")
                    sys.exit(1)

            elif typ == "PAUSE":
                pause_animations_list = matching.groups()[0]
                pause_animations =  ["NoneIn", "NoneOut"]
                if pause_animations_list is not None:
                    pause_animations_list = pause_animations_list.split(",")
                    for animation in pause_animations_list:
                        if animation.endswith("In"):
                            pause_animations[0] = animation
                        if animation.endswith("Out"):
                            pause_animations[1] = animation
                return Token(typ, pause_animations, line_number), rest_expression

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

            elif typ == "IFRAME":
                if matching.groups()[1]:
                    website_source, args_web = matching.group(1), matching.group(2).split(",")
                    return Token(typ, tuple([website_source, args_web]), line_number ), rest_expression
                else:
                    return Token(typ, tuple([matching.group(1), None]), line_number), rest_expression

            elif typ == "CODEBLOCK":
                if matching.groups()[1]:
                    codefile, args_code = matching.group(1), matching.group(2).split(",")
                    return Token(typ, tuple([codefile, args_code]), line_number ), rest_expression
                else:
                    return Token(typ, tuple([matching.group(1), None]), line_number), rest_expression

            elif typ == "CODELINE":
                if matching.groups()[1]:
                    code_file, language = matching.group(1), matching.group(2)
                    return Token(typ, tuple([code_file, language]), line_number ), rest_expression
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

            else:
                if matching.groups():
                    return Token(typ, matching.group(1), line_number), rest_expression
                else:
                    return Token(typ, None, line_number), rest_expression
    return Token("TEXT", expression.split('#')[0], line_number), ""
