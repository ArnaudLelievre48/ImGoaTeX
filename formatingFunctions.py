import re

#split text to avoid splittin \\ inside $...$ or $$...$$
def split_outside_math(text):
    parts = []
    buf = ""
    i = 0
    n = len(text)
    in_inline = False  # inside $...$
    in_display = False  # inside $$...$$

    while i < n:
        # Detect start/end of $$...$$
        if text[i:i+2] == "$$":
            if in_display:
                in_display = False
            elif not in_inline:
                in_display = True
            buf += "$$"
            i += 2
            continue

        # Detect start/end of $...$ (but skip if in display math)
        if text[i] == "$" and not in_display:
            in_inline = not in_inline
            buf += "$"
            i += 1
            continue

        # Only split if we are **outside all math**
        if not in_inline and not in_display and text[i] in ['\n']:
            parts.append(buf)
            buf = ""
            i += 1
            continue

        if (i+1) < len(text):
            if not in_inline and not in_display and text[i:i+2] in [r'\\', r'\n']:
                parts.append(buf)
                buf = ""
                i += 2
                continue

        # Otherwise, just append the character
        buf += text[i]
        i += 1

    # Add the last buffer
    if buf:
        parts.append(buf)
    return parts




# parse text in html format
def parse_text_to_html(text, fontsize):
    #parts = re.split(r'(\\\\|\\n|\$)', text)
    #parts = re.split(r'(?:\\\\|\n)(?=(?:[^$]*\$[^$]*\$)*[^$]*$)', text)
    parts = split_outside_math(text)
    bad = {r'\\', r"\n"}
    for i in range(len(parts)):
        # ** ... ** to <b> ... </b>
        parts[i] = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', parts[i])
        # * ... * or _ ... _ to <i> ... </i>
        parts[i] = re.sub(r'\*(.+?)\*', r'<i>\1</i>', parts[i])
        # !htab to <span class="hspace" style="width=calc(...*var(--unit_x))"></span>
        parts[i] = re.sub(r'!htab', r'<span class="hspace"></span>', parts[i])
        # \textbf{...} to <b> ... </b>
        parts[i] = re.sub(r'\\textbf\{(.+?)\}', r'<b>\1</b>', parts[i])
        # \textit{...} to <i> ... </i>
        parts[i] = re.sub(r'\\textit\{(.+?)\}', r'<i>\1</i>', parts[i])
        # \link{...}{...} to <a href='...'> ... </a>
        parts[i] = re.sub(r'\\link\{(.+?)\}\[(.+?)\]', r'<a href="\2">\1</a>', parts[i])

    outText = ''
    for part in parts:
        if part not in bad:
            outText = outText + f"<p style='font-size: calc({fontsize}*var(--basefontsize))'>{part}</p>"
        else:
            outText = outText + "<span style='height: calc(1* var(--unit_y))'></span>"

    return(outText)



# return the root_css code
def root_css(as_w=16, as_h=9, bgcolor="#faf3e1", color1="#6b3016", color2="#783a1f", color3="#ad5e3b", color4="#362821", basefontsize=1.5, font="Noto Serif"):
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
        --basefontsize: calc({basefontsize}*var(--unit_x));
        --font: {font};
"""
    css_root = ":root {\n" + var + "}"
    return css_root


# return the root_css code for fullscreen
def root_css_fullscreen(as_w=16, as_h=9, bgcolor="#faf3e1", color1="#6b3016", color2="#783a1f", color3="#ad5e3b", color4="#362821", basefontsize=1.5, font="Noto Serif"):
    var = f"""
        --ar_width: {as_w};
        --ar_height: {as_h};
        --unit_x: calc( min(100vw, calc( ( var(--ar_width) / var(--ar_height) ) * 100vh) )/100 );
        --unit_y: calc( min(100vh, calc( ( var(--ar_height) / var(--ar_width) ) * 100vw) )/100 );
        --bgcolor: {bgcolor};
        --color1: {color1};
        --color2: {color2};
        --color3: {color3};
        --color4: {color4};
        --basefontsize: calc({basefontsize}*var(--unit_x));
        --font: {font};
"""

    css_root = ":root.presentation {\n" + var + "}"
    return css_root


