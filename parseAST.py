import datetime
import copy
import urllib.request
import sys
import base64
import textwrap
import html

import formatingFunctions



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
    def __init__(self, title=None, subtitle=None, contents=None, options=None, animations=None):
        self.title = title
        self.subtitle = subtitle
        if options is None:
            self.options = []
        else:
            self.options = copy.deepcopy(options)
        if animations is None:
            self.animations = ["FadeIn","FadeOut"]
        else:
            self.animations = copy.deepcopy(animations)
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
def parse_filtering(token, presentation, PORTABLE_MEDIAS, current_frame, folder, CSSVARS, lines):
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
        if key == "as_w":
            CSSVARS[0] = val
        if key == "as_h":
            CSSVARS[1] = val
        if key == "bgcolor":
            CSSVARS[2] = val
        if key == "color1":
            CSSVARS[3] = val
        if key == "color2":
            CSSVARS[4] = val
        if key == "color3":
            CSSVARS[5] = val
        if key == "color4":
            CSSVARS[6] = val
        if key == "basefontsize":
            CSSVARS[7] = val
        if key == "font":
            CSSVARS[8] = val


    if token.type == "SECTION":
        if token.value: # if the section has a title
            presentation.sections.append( Section(token.value) ) # create a section with the title : token.value
        else:
            if 0 <= token.line-1 <= len(lines)-2:
                print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} -- {lines[token.line]} \n\n No name were given for the section")
            elif 0 > token.line-1:
                print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {token.line} >> {lines[token.line-1]} {token.line+1} -- {lines[token.line]} \n\n No name were given for the section")
            elif token.line-1 > len(lines)-2:
                print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} -- \n\n No name were given for the section")
            sys.exit(1)

    if token.type == "SUBSECTION":
        if token.value: # if the subsection has a title
            if presentation.sections != []: # if the presentation has a section
                presentation.sections[-1].subsections.append( Subsection(token.value) ) # adds the subsection to the last section created
            else:
                if 0 <= token.line-1 <= len(lines)-2:
                    print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} --  {lines[token.line]} \n\n the subsection '{token.value}' could not be created : no sections were declared beforehand")
                elif 0 > token.line-1:
                    print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {token.line} >> {lines[token.line-1]} {token.line+1} --  {lines[token.line]} \n\n the subsection '{token.value}' could not be created : no sections were declared beforehand")
                elif token.line-1 > len(lines)-2:
                    print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} -- \n\n the subsection '{token.value}' could not be created : no sections were declared beforehand")
                sys.exit(1)
        else:
            if 0 <= token.line-1 <= len(lines)-2:
                print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} {lines[token.line]} \n\n No name were given for the subsection")
            elif 0 > token.line-1:
                print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {token.line} >> {lines[token.line-1]} {token.line+1} {lines[token.line]} \n\n No name were given for the subsection")
            elif token.line-1 > len(lines)-2:
                print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} \n\n No name were given for the subsection")
            sys.exit(1)

    if token.type == "BEGIN_FRAME":
        if current_frame is not None:
            if 0 <= token.line-1 <= len(lines)-2:
                print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} -- {lines[token.line]} \n\n the frame '{token.value[0]}' could not be created, the frame '{presentation.sections[-1].subsections[-1].frames[-1].title}' has not been ended.")
            elif 0 > token.line-1:
                print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {token.line} >> {lines[token.line-1]} {token.line+1} -- {lines[token.line]} \n\n the frame '{token.value[0]}' could not be created, the frame '{presentation.sections[-1].subsections[-1].frames[-1].title}' has not been ended.")
            elif token.line-1 > len(lines)-2:
                print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} -- \n\n the frame '{token.value[0]}' could not be created, the frame '{presentation.sections[-1].subsections[-1].frames[-1].title}' has not been ended.")
            sys.exit(1)
        if presentation.sections != []:
            if presentation.sections[-1].subsections != []:
                frame_title, frame_subtitle, frame_options, frame_animations = token.value
                presentation.sections[-1].subsections[-1].frames.append( Frame(frame_title, frame_subtitle, None, frame_options, frame_animations) )
                current_frame = presentation.sections[-1].subsections[-1].frames[-1]
            else:
                if 0 <= token.line-1 <= len(lines)-2:
                    print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} -- {lines[token.line]} \n\n The frame '{token.value[0]}' could not be created : no subsections were declared beforehand")
                elif 0 > token.line-1:
                    print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {token.line} >> {lines[token.line-1]} {token.line+1} -- {lines[token.line]} \n\n The frame '{token.value[0]}' could not be created : no subsections were declared beforehand")
                elif token.line-1 > len(lines)-2:
                    print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} -- \n\n The frame '{token.value[0]}' could not be created : no subsections were declared beforehand")
                sys.exit(1)
        else:
            if 0 <= token.line-1 <= len(lines)-2:
                print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} -- {lines[token.line]} \n\n The frame '{token.value[0]}' could not be created : no sections were declared beforehand")
            elif 0 > token.line-1:
                print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {token.line} >> {lines[token.line-1]} {token.line+1} -- {lines[token.line]} \n\n The frame '{token.value[0]}' could not be created : no sections were declared beforehand")
            elif token.line-1 > len(lines)-2:
                print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} -- \n\n The frame '{token.value[0]}' could not be created : no sections were declared beforehand")
            sys.exit(1)

    if token.type == "END_FRAME":
        if current_frame is not None:
            current_frame = None
        else:
            if 0 <= token.line-1 <= len(lines)-2:
                print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} -- {lines[token.line]} \n\n You are not in a frame, you thus cannot end a frame")
            elif 0 > token.line-1:
                print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {token.line} >> {lines[token.line-1]} {token.line+1} -- {lines[token.line]} \n\n You are not in a frame, you thus cannot end a frame")
            elif token.line-1 > len(lines)-2:
                print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} -- \n\n You are not in a frame, you thus cannot end a frame")
            sys.exit(1)

    if token.type == "PAUSE":
        if current_frame is not None:
            pause_animations = token.value
            animation_in, animation_out = current_frame.animations
            animations = [animation_in, pause_animations[1]]
            animations_next = [pause_animations[0], animation_out]
            presentation.sections[-1].subsections[-1].frames[-1] = ( Frame(current_frame.title, current_frame.subtitle, current_frame.contents, current_frame.options, animations) )
            current_frame.animations  = animations_next
            presentation.sections[-1].subsections[-1].frames.append( current_frame  )
        else:
            if 0 <= token.line-1 <= len(lines)-2:
                print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} -- {lines[token.line]} \n\n You tried to pause, but you were not in a frame.")
            elif 0 > token.line-1:
                print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {token.line} >> {lines[token.line-1]} {token.line+1} -- {lines[token.line]} \n\n You tried to pause, but you were not in a frame.")
            elif token.line-1 > len(lines)-2:
                print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} -- \n\n You tried to pause, but you were not in a frame.")

    if token.type == "ITEM":
        inside_token = token.value
        if current_frame:
            current_frame.contents.append( "<div class='item'>" )
            current_frame = parse_filtering(inside_token, presentation, PORTABLE_MEDIAS, current_frame, folder, CSSVARS, lines)
            current_frame.contents.append( "</div>" )

    if token.type == "SUBITEM":
        inside_token = token.value
        if current_frame:
            current_frame.contents.append( "<div class='subitem'>" )
            current_frame = parse_filtering(inside_token, presentation,PORTABLE_MEDIAS, current_frame, folder, CSSVARS, lines)
            current_frame.contents.append( "</div>" )

    if token.type == "TEXT":
        if current_frame:
            current_frame.contents.append( formatingFunctions.parse_text_to_html( token.value, 1 ) )
            #print(presentation.sections[-1].subsections[-1].frames[-1].contents)
        else:
            if 0 <= token.line-1 <= len(lines)-2:
                print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} -- {lines[token.line]} \n\n You are not in a frame, you thus cannot add text to a frame")
            elif 0 > token.line-1:
                print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {token.line} >> {lines[token.line-1]} {token.line+1} -- {lines[token.line]} \n\n You are not in a frame, you thus cannot add text to a frame")
            elif token.line-1 > len(lines)-2:
                print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} -- \n\n You are not in a frame, you thus cannot add text to a frame")
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
                                    if 0 <= token.line-1 <= len(lines)-2:
                                        print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} -- {lines[token.line]} \n\n The value given to rotate is incorrect, please use a float (deg)")
                                    elif 0 > token.line-1:
                                        print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {token.line} >> {lines[token.line-1]} {token.line+1} -- {lines[token.line]} \n\n The value given to rotate is incorrect, please use a float (deg)")
                                    elif token.line-1 > len(lines)-2:
                                        print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} -- \n\n The value given to rotate is incorrect, please use a float (deg)")
                                    sys.exit(1)
                            if arg[:5] == "shift":
                                arg = arg.split("_")[1]
                                if len(arg.split('+')) != 4:
                                    if 0 <= token.line-1 <= len(lines)-2:
                                        print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} -- {lines[token.line]} \n\n You tried to use shift, but the syntax was wrong, the right syntax is : shift=[top]+[right]+[bottom]+[left], the shift option is adding padding to the oposite direction to place the media, with paging unit")
                                    elif 0 > token.line-1:
                                        print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {token.line} >> {lines[token.line-1]} {token.line+1} -- {lines[token.line]} \n\n You tried to use shift, but the syntax was wrong, the right syntax is : shift=[top]+[right]+[bottom]+[left], the shift option is adding padding to the oposite direction to place the media, with paging unit")
                                    elif token.line-1 > len(lines)-2:
                                        print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} -- \n\n You tried to use shift, but the syntax was wrong, the right syntax is : shift=[top]+[right]+[bottom]+[left], the shift option is adding padding to the oposite direction to place the media, with paging unit")
                                    sys.exit(1)

                                shift_top = f"calc( {arg.split('+')[2]}*var(--unit_y) )"
                                shift_right = f"calc( {arg.split('+')[3]}*var(--unit_x) )"
                                shift_bottom = f"calc( {arg.split('+')[0]}*var(--unit_y) )"
                                shift_left  = f"calc( {arg.split('+')[1]}*var(--unit_x) )"

                            else:
                                classes = classes + arg + " "

                    if PORTABLE_MEDIAS:
                        if inline:
                            video_html = f"""<video style='width: calc(20*var(--unit_x)); padding: {shift_top} {shift_right} {shift_bottom} {shift_left}; transform: rotate({degre})' class='{classes}' src='data:video/mp4;base64,{base64.b64encode(vid.read()).decode("utf-8")}' controls autoplay loop muted></video>"""
                        else:
                            video_html = f"""<div class='{imgclass} {classes_pos}'><video style='width: calc(20*var(--unit_x)); padding: {shift_top} {shift_right} {shift_bottom} {shift_left}; transform: rotate({degre})' class='{classes}' src='data:video/mp4;base64,{base64.b64encode(vid.read()).decode("utf-8")}' controls autoplay loop muted></video></div>"""
                    else:
                        if inline:
                            video_html = f"<video style='width: calc(20*var(--unit_x)); padding: {shift_top} {shift_right} {shift_bottom} {shift_left}; transform: rotate({degre})' class='{classes}' src='{folder}medias/{token.value[0]}' controls autoplay loop muted></video>"
                        else:
                            video_html = f"<div class='{imgclass} {classes_pos}'><video style='width: calc(20*var(--unit_x)); padding: {shift_top} {shift_right} {shift_bottom} {shift_left}; transform: rotate({degre})' class='{classes}' src='{folder}medias/{token.value[0]}' controls autoplay loop muted></video></div>"
                    current_frame.contents.append( video_html )
            except:
                current_frame.contents.append( f"<div class='{imgclass}'><p style='border: solid 2px var(--color1); padding: 5em'> Cannot find the file : '{folder}medias/{token.value[0]} '</p></div>" )
        else:
            if 0 <= token.line-1 <= len(lines)-2:
                print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} -- {lines[token.line]} \n\n You are not in a frame, you thus cannot add a video to a frame")
            elif 0 > token.line-1:
                print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {token.line} >> {lines[token.line-1]} {token.line+1} -- {lines[token.line]} \n\n You are not in a frame, you thus cannot add a video to a frame")
            elif token.line-1 > len(lines)-2:
                print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} -- \n\n You are not in a frame, you thus cannot add a video to a frame")
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
                                    if 0 <= token.line-1 <= len(lines)-2:
                                        print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} -- {lines[token.line]} \n\n The value given to rotate is incorrect, please use a float (deg)")
                                    elif 0 > token.line-1:
                                        print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {token.line} >> {lines[token.line-1]} {token.line+1} -- {lines[token.line]} \n\n The value given to rotate is incorrect, please use a float (deg)")
                                    elif token.line-1 > len(lines)-2:
                                        print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} -- \n\n The value given to rotate is incorrect, please use a float (deg)")
                                    sys.exit(1)
                            if arg[:5] == "shift":
                                arg = arg.split("_")[1]
                                if len(arg.split('+')) != 4:
                                    if 0 <= token.line-1 <= len(lines)-2:
                                        print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} -- {lines[token.line]} \n\n You tried to use shift, but the syntax was wrong, the right syntax is : shift=[top]+[right]+[bottom]+[left], the shift option is adding padding to the oposite direction to place the media, with paging unit")
                                    elif 0 > token.line-1:
                                        print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {token.line} >> {lines[token.line-1]} {token.line+1} -- {lines[token.line]} \n\n You tried to use shift, but the syntax was wrong, the right syntax is : shift=[top]+[right]+[bottom]+[left], the shift option is adding padding to the oposite direction to place the media, with paging unit")
                                    elif token.line-1 > len(lines)-2:
                                        print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} -- \n\n You tried to use shift, but the syntax was wrong, the right syntax is : shift=[top]+[right]+[bottom]+[left], the shift option is adding padding to the oposite direction to place the media, with paging unit")
                                    sys.exit(1)

                                shift_top = f"calc( {arg.split('+')[2]}*var(--unit_y) )"
                                shift_right = f"calc( {arg.split('+')[3]}*var(--unit_x) )"
                                shift_bottom = f"calc( {arg.split('+')[0]}*var(--unit_y) )"
                                shift_left  = f"calc( {arg.split('+')[1]}*var(--unit_x) )"
                            else:
                                classes = classes + arg + " "

                    if PORTABLE_MEDIAS:
                        if inline:
                            image_html = f"""<img style='width: calc(20*var(--unit_x)); padding: {shift_top} {shift_right} {shift_bottom} {shift_left}; transform: rotate({degre})' class='{classes}' src='data:image/png;base64,{base64.b64encode(img.read()).decode("utf-8")}'></img>"""
                        else:
                            image_html = f"""<div class='{imgclass} {classes_pos}'><img style='width: calc(20*var(--unit_x)); padding: {shift_top} {shift_right} {shift_bottom} {shift_left}; transform: rotate({degre})' class='{classes}' src='data:image/png;base64,{base64.b64encode(img.read()).decode("utf-8")}'></img></div>"""
                    else:
                        if inline:
                            image_html = f"<img style='width: calc(20*var(--unit_x)); padding: {shift_top} {shift_right} {shift_bottom} {shift_left}; transform: rotate({degre})' class='{classes}' src='{folder}medias/{token.value[1]}'></img>"
                        else:
                            image_html = f"<div class='{imgclass} {imgclass_pos}'><img style='width: calc(20*var(--unit_x)); padding: {shift_top} {shift_right} {shift_bottom} {shift_left}; transform: rotate({degre})' class='{classes}' src='{folder}medias/{token.value[1]}'></img></div>"

                current_frame.contents.append( image_html )
            except:
                current_frame.contents.append( f"<div class='{imgclass}'><p style='border: solid 2px var(--color1); padding: 5em'> Cannot find the file : '{folder}medias/{token.value[0]} '</p></div>" )
        else:
            if 0 <= token.line-1 <= len(lines)-2:
                print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} -- {lines[token.line]} \n\n You are not in a frame, you thus cannot add an image to a frame")
            elif 0 > token.line-1:
                print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {token.line} >> {lines[token.line-1]} {token.line+1} -- {lines[token.line]} \n\n You are not in a frame, you thus cannot add an image to a frame")
            elif token.line-1 > len(lines)-2:
                print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} -- \n\n You are not in a frame, you thus cannot add an image to a frame")
            sys.exit(1)

    if token.type == "IFRAME":
        if current_frame:
            iframeclass = "mediaoverlay"
            if current_frame.subtitle is not None:
                iframeclass = "mediaoverlaySub"
            inline = False

            try:
                if urllib.request.urlopen(token.value[0]).getcode() == 200:
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
                                    if 0 <= token.line-1 <= len(lines)-2:
                                        print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} -- {lines[token.line]} \n\n The value given to rotate is incorrect, please use a float (deg)")
                                    elif 0 > token.line-1:
                                        print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {token.line} >> {lines[token.line-1]} {token.line+1} -- {lines[token.line]} \n\n The value given to rotate is incorrect, please use a float (deg)")
                                    elif token.line-1 > len(lines)-2:
                                        print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} -- \n\n The value given to rotate is incorrect, please use a float (deg)")
                                    sys.exit(1)
                            if arg[:5] == "shift":
                                arg = arg.split("_")[1]
                                if len(arg.split('+')) != 4:
                                    if 0 <= token.line-1 <= len(lines)-2:
                                        print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} -- {lines[token.line]} \n\n You tried to use shift, but the syntax was wrong, the right syntax is : shift=[top]+[right]+[bottom]+[left], the shift option is adding padding to the oposite direction to place the media, with paging unit")
                                    elif 0 > token.line-1:
                                        print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {token.line} >> {lines[token.line-1]} {token.line+1} -- {lines[token.line]} \n\n You tried to use shift, but the syntax was wrong, the right syntax is : shift=[top]+[right]+[bottom]+[left], the shift option is adding padding to the oposite direction to place the media, with paging unit")
                                    elif token.line-1 > len(lines)-2:
                                        print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} -- \n\n You tried to use shift, but the syntax was wrong, the right syntax is : shift=[top]+[right]+[bottom]+[left], the shift option is adding padding to the oposite direction to place the media, with paging unit")
                                    sys.exit(1)

                                shift_top = f"calc( {arg.split('+')[2]}*var(--unit_y) )"
                                shift_right = f"calc( {arg.split('+')[3]}*var(--unit_x) )"
                                shift_bottom = f"calc( {arg.split('+')[0]}*var(--unit_y) )"
                                shift_left  = f"calc( {arg.split('+')[1]}*var(--unit_x) )"
                            else:
                                classes = classes + arg + " "

                    if inline:
                        iframe_html = f"<iframe style='width: calc(20*var(--unit_x)); padding: {shift_top} {shift_right} {shift_bottom} {shift_left}; transform: rotate({degre}); overflow:hidden; border:0;' class='{classes}' overflow='hidden' scrolling='no' frameBorder='0' class='{classes}' border='0' src='{token.value[0]}?widget=false&amp;headers=false&amp;chrome=false&amp;rm=minimal;frameborder=0'></iframe>"
                    else:
                        iframe_html = f"<div class='{iframeclass} {classes_pos}'><iframe style='width: calc(20*var(--unit_x)); padding: {shift_top} {shift_right} {shift_bottom} {shift_left}; transform: rotate({degre}); overflow:hidden; border:0;' class='{classes}' overflow='hidden' scrolling='no' frameBorder='0' class='{classes}' border='0' src='{token.value[0]}?widget=false&amp;headers=false&amp;chrome=false&amp;rm=minimal;frameborder=0'></iframe></div>"

                current_frame.contents.append( iframe_html )
            except:
                current_frame.contents.append( f"<div class='{iframeclass}'><p style='border: solid 2px var(--color1); padding: 5em'> Cannot find the website : '{token.value[0]} '</p></div>" )
        else:
            if 0 <= token.line-1 <= len(lines)-2:
                print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} -- {lines[token.line]} \n\n You are not in a frame, you thus cannot add an iframe to a frame")
            elif 0 > token.line-1:
                print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {token.line} >> {lines[token.line-1]} {token.line+1} -- {lines[token.line]} \n\n You are not in a frame, you thus cannot add an iframe to a frame")
            elif token.line-1 > len(lines)-2:
                print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} -- \n\n You are not in a frame, you thus cannot add an iframe to a frame")
            sys.exit(1)

    if token.type == "CODEBLOCK":
        if current_frame:
            codeblockclass = "mediaoverlay"
            if current_frame.subtitle is not None:
                codeblockclass = "mediaoverlaySub"
            inline = False

            try:
                with open(folder+"medias/"+token.value[0], 'rb') as codefile:
                    code_raw = codefile.read()
                    code_utf8= code_raw.decode("utf-8")
                    code_text = textwrap.dedent(code_utf8)
                    code = html.escape(code_text)
                    classes = ""
                    classes_pos = ""
                    shift_top = "0px"
                    shift_right = "0px"
                    shift_bottom = "0px"
                    shift_left = "0px"
                    degre="0deg"
                    # treat options
                    language = ""
                    if token.value[1] is not None:
                        for arg in token.value[1]:
                            arg = arg.replace(" ", "")
                            arg = arg.replace("=", "_")
                            if arg.startswith("language"):
                                language = arg.replace("_","-")
                            if arg == "inline":
                                inline = True
                            if arg[:8] == "position":
                                classes_pos = classes_pos + arg + " "
                            if arg[:6] == "rotate":
                                try:
                                    degre = f"{ str(float(arg.split('_')[1])) }deg"
                                except:
                                    if 0 <= token.line-1 <= len(lines)-2:
                                        print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} -- {lines[token.line]} \n\n The value given to rotate is incorrect, please use a float (deg)")
                                    elif 0 > token.line-1:
                                        print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {token.line} >> {lines[token.line-1]} {token.line+1} -- {lines[token.line]} \n\n The value given to rotate is incorrect, please use a float (deg)")
                                    elif token.line-1 > len(lines)-2:
                                        print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} -- \n\n The value given to rotate is incorrect, please use a float (deg)")
                                    sys.exit(1)
                            if arg[:5] == "shift":
                                arg = arg.split("_")[1]
                                if len(arg.split('+')) != 4:
                                    if 0 <= token.line-1 <= len(lines)-2:
                                        print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} -- {lines[token.line]} \n\n You tried to use shift, but the syntax was wrong, the right syntax is : shift=[top]+[right]+[bottom]+[left], the shift option is adding padding to the oposite direction to place the media, with paging unit")
                                    elif 0 > token.line-1:
                                        print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {token.line} >> {lines[token.line-1]} {token.line+1} -- {lines[token.line]} \n\n You tried to use shift, but the syntax was wrong, the right syntax is : shift=[top]+[right]+[bottom]+[left], the shift option is adding padding to the oposite direction to place the media, with paging unit")
                                    elif token.line-1 > len(lines)-2:
                                        print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} -- \n\n You tried to use shift, but the syntax was wrong, the right syntax is : shift=[top]+[right]+[bottom]+[left], the shift option is adding padding to the oposite direction to place the media, with paging unit")
                                    sys.exit(1)

                                shift_top = f"calc( {arg.split('+')[2]}*var(--unit_y) )"
                                shift_right = f"calc( {arg.split('+')[3]}*var(--unit_x) )"
                                shift_bottom = f"calc( {arg.split('+')[0]}*var(--unit_y) )"
                                shift_left  = f"calc( {arg.split('+')[1]}*var(--unit_x) )"
                            else:
                                classes = classes + arg + " "

                    if inline:
                        codeblock_html = f"<div style='width: calc(20*var(--unit_x)); padding: {shift_top} {shift_right} {shift_bottom} {shift_left}; transform: rotate({degre}); overflow:hidden; border:0;' class='wrapper {classes}' overflow='scroll'><div class='codewrapper'><pre><code class='{language}'>{code}</code></pre></div></div>"
                    else:
                        codeblock_html = f"<div class='{codeblockclass} {classes_pos}'><div class='wrapper {classes}' style='padding: {shift_top} {shift_right} {shift_bottom} {shift_left}; transform: rotate({degre})'><div class='codewrapper'><pre><code class='{language}'>{ code }</code></pre></div></div></div>"

                current_frame.contents.append( codeblock_html )
            except:
                current_frame.contents.append( f"<div class='{codeblockclass}'><p style='border: solid 2px var(--color1); padding: 5em'> Cannot find the website : '{token.value[0]} '</p></div>" )
        else:
            if 0 <= token.line-1 <= len(lines)-2:
                print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} -- {lines[token.line]} \n\n You are not in a frame, you thus cannot add an iframe to a frame")
            elif 0 > token.line-1:
                print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {token.line} >> {lines[token.line-1]} {token.line+1} -- {lines[token.line]} \n\n You are not in a frame, you thus cannot add an iframe to a frame")
            elif token.line-1 > len(lines)-2:
                print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} -- \n\n You are not in a frame, you thus cannot add an iframe to a frame")
            sys.exit(1)



    if token.type == "CODELINE":
        if current_frame:
            codelineclass = "mediaoverlay"
            if current_frame.subtitle is not None:
                codelineclass = "mediaoverlaySub"
            try:
                codeline_html = f"""<div class='codeline' overflow='scroll'><div class='codewrapper'><pre><code class='{token.value[1].replace("=","-")}'>{textwrap.dedent(token.value[0])}</code></pre></div></div>"""
                current_frame.contents.append( codeline_html )
            except:
                current_frame.contents.append( f"<div class='{codelineclass}'><p style='border: solid 2px var(--color1); padding: 5em'> Cannot find the website : '{token.value[0]} '</p></div>" )
        else:
            if 0 <= token.line-1 <= len(lines)-2:
                print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} -- {lines[token.line]} \n\n You are not in a frame, you thus cannot add an codeline to a frame")
            elif 0 > token.line-1:
                print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {token.line} >> {lines[token.line-1]} {token.line+1} -- {lines[token.line]} \n\n You are not in a frame, you thus cannot add an codeline to a frame")
            elif token.line-1 > len(lines)-2:
                print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} -- \n\n You are not in a frame, you thus cannot add an codeline to a frame")
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
                            if 0 <= token.line-1 <= len(lines)-2:
                                print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} -- {lines[token.line]} \n\n The value given to rotate is incorrect, please use a float (paging unit x)")
                            elif 0 > token.line-1:
                                print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {token.line} >> {lines[token.line-1]} {token.line+1} -- {lines[token.line]} \n\n The value given to rotate is incorrect, please use a float (paging unit x)")
                            elif token.line-1 > len(lines)-2:
                                print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} -- \n\n The value given to rotate is incorrect, please use a float (paging unit x)")

                    elif arg[:6] == "rotate":
                        try:
                            degre = f"{ str(float(arg.split('_')[1])) }deg"
                        except:
                            if 0 <= token.line-1 <= len(lines)-2:
                                print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} -- {lines[token.line]} \n\n The value given to rotate is incorrect, please use a float (deg)")
                            elif 0 > token.line-1:
                                print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {token.line} >> {lines[token.line-1]} {token.line+1} -- {lines[token.line]} \n\n The value given to rotate is incorrect, please use a float (deg)")
                            elif token.line-1 > len(lines)-2:
                                print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} -- \n\n The value given to rotate is incorrect, please use a float (deg)")
                            sys.exit(1)
                    elif arg[:5] == "shift":
                        arg = arg.split("_")[1]
                        if len(arg.split('+')) != 4:
                            if 0 <= token.line-1 <= len(lines)-2:
                                print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} -- {lines[token.line]} \n\n You tried to use shift, but the syntax was wrong, the right syntax is : shift=[top]+[right]+[bottom]+[left], the shift option is adding padding to the oposite direction to place the media, with paging unit")
                            elif 0 > token.line-1:
                                print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {token.line} >> {lines[token.line-1]} {token.line+1} -- {lines[token.line]} \n\n You tried to use shift, but the syntax was wrong, the right syntax is : shift=[top]+[right]+[bottom]+[left], the shift option is adding padding to the oposite direction to place the media, with paging unit")
                            elif token.line-1 > len(lines)-2:
                                print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} -- \n\n You tried to use shift, but the syntax was wrong, the right syntax is : shift=[top]+[right]+[bottom]+[left], the shift option is adding padding to the oposite direction to place the media, with paging unit")
                            sys.exit(1)

                        shift_top = f"calc( {arg.split('+')[2]}*var(--unit_y) )"
                        shift_right = f"calc( {arg.split('+')[3]}*var(--unit_x) )"
                        shift_bottom = f"calc( {arg.split('+')[0]}*var(--unit_y) )"
                        shift_left  = f"calc( {arg.split('+')[1]}*var(--unit_x) )"

                    else:
                        classes = classes + arg + " "

            if inline:
                text_inside_html = f"<div class='wrapper {classes}' style='padding: {shift_top} {shift_right} {shift_bottom} {shift_left}; transform: rotate({degre});'><div>{ formatingFunctions.parse_text_to_html( token.value[0].value, fontsize ) }</div></div>"
            else:
                text_inside_html = f"<div class='{imgclass} {classes_pos}'><div class='wrapper {classes}' style='padding: {shift_top} {shift_right} {shift_bottom} {shift_left}; transform: rotate({degre})'><div>{ formatingFunctions.parse_text_to_html( token.value[0].value, fontsize ) }</div></div></div>"
            current_frame.contents.append( text_inside_html )
        else:
            if 0 <= token.line-1 <= len(lines)-2:
                print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} -- {lines[token.line]} \n\n You are not in a frame, you thus cannot add a textbox to a frame")
            elif 0 > token.line-1:
                print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {token.line} >> {lines[token.line-1]} {token.line+1} -- {lines[token.line]} \n\n You are not in a frame, you thus cannot add a textbox to a frame")
            elif token.line-1 > len(lines)-2:
                print(f"ERROR AT LINE {token.line} : \n\n {token.line-1} -- {lines[token.line-2]} {token.line} >> {lines[token.line-1]} {token.line+1} -- \n\n You are not in a frame, you thus cannot add a textbox to a frame")
            sys.exit(1)

    return(current_frame)
