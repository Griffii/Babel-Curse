# ============================================
# dictionary_menu.rpy — Ren'Py 8.5 compatible
# Smaller centered popup version:
# - Fixed popup size: 1250 x 800
# - Centered on screen
# - Definition section removed
# - EN/JP main titles moved to left side above example box
# - Titles stacked vertically:
#     School
#     学校
# - Example section label changed to 例文 / Examples
# - No furigana shown for Japanese text in this screen
# - Example box enlarged
# - Audio icon reduced in size
# - Left column uses fixed positioning for tighter vertical control
# - Placeholder back button added top-left
# - Missing image falls back to dict_images/question-mark.png
# - Tooltip button wrapped in white frame and fully clickable
# - Close button renders above tooltip button
# ============================================


init -10 python:

    JP_FONT = "fonts/NotoSansJP/NotoSansJP-Bold.ttf"

    # Base ruby (fallback)
    style.ruby_style = Style(style.default)
    style.ruby_style.font = JP_FONT
    style.ruby_style.size = 18
    style.ruby_style.yoffset = -34
    style.ruby_style.color = None

    # Title ruby (larger)
    style.ruby_title = Style(style.ruby_style)
    style.ruby_title.size = 24
    style.ruby_title.yoffset = -55

    # Body ruby
    style.ruby_body = Style(style.ruby_style)
    style.ruby_body.size = 20
    style.ruby_body.yoffset = -36

    try:
        style.say_dialogue.ruby_style = style.ruby_body
        style.say_dialogue.ruby_line_leading = 22
    except Exception:
        pass
    try:
        style.history_text.ruby_style = style.ruby_body
        style.history_text.ruby_line_leading = 22
    except Exception:
        pass


init -1 python:
    import json

    POS_JA = {
        "noun": "名詞", "verb": "動詞", "adjective": "形容詞", "adverb": "副詞",
        "pronoun": "代名詞", "preposition": "前置詞", "conjunction": "接続詞",
        "interjection": "間投詞", "determiner": "限定詞", "phrase": "表現",
    }

    POS_COLORS = {
        "noun": "#4CAF50",
        "verb": "#2196F3",
        "adjective": "#E91E63",
        "adverb": "#9C27B0",
        "pronoun": "#FF9800",
        "preposition": "#009688",
        "conjunction": "#3F51B5",
        "interjection": "#F44336",
        "determiner": "#795548",
        "phrase": "#607D8B",
    }

    DICTIONARY_DATA = {}
    DICTIONARY_IDS = []

    def load_full_dictionary(path="dictionary.json"):
        global DICTIONARY_DATA, DICTIONARY_IDS
        try:
            with renpy.file(path) as f:
                DICTIONARY_DATA = json.load(f) or {}
        except Exception:
            DICTIONARY_DATA = {}
        DICTIONARY_IDS = sorted(DICTIONARY_DATA.keys(), key=lambda x: x.lower())

    load_full_dictionary("dictionary.json")

    def open_dict_popup_by_key(key):
        entry = DICTIONARY_DATA.get(key)
        if entry:
            renpy.show_screen("dictionary_popup", entry=entry, entry_key=key)


init python:

    # ---------- Color Tokens ----------
    COL_BG_PANEL = "#14161aF0"
    COL_TEXT_MAIN = "#ffffff"
    COL_TEXT_MUTED = "#CFD7DE"
    COL_TITLE_EN = "#ffe6b4"
    COL_TITLE_JP = "#ffe6b4"
    COL_TITLE_OUT = "#000000d0"
    COL_SECTION = "#3abaf5"
    COL_POS_TAGBG = "#3e2244"

    # Drop shadow color
    COL_TEXT_SHADOW = "#000000cc"

    # Shadow definition
    TEXT_SHADOW = [(3, COL_TEXT_SHADOW, 2, 2)]

    # ---------- Debug Layout Styles ----------
    style.dbg_vbox = Style(style.default)
    style.dbg_vbox.background = Null()

    style.dbg_hbox = Style(style.default)
    style.dbg_hbox.background = Null()

    # ---------- Text Styles ----------
    style.jp_text = Style(style.default)
    style.jp_text.font = JP_FONT
    style.jp_text.size = 32
    style.jp_text.color = COL_TEXT_MAIN
    style.jp_text.line_spacing = 2
    style.jp_text.ruby_style = None
    style.jp_text.outlines = TEXT_SHADOW

    style.jp_title = Style(style.default)
    style.jp_title.font = JP_FONT
    style.jp_title.size = 70
    style.jp_title.color = COL_TITLE_JP
    style.jp_title.outlines = [
        (2, COL_TITLE_OUT, 0, 0),
        (1, COL_TEXT_SHADOW, 2, 2)
    ]
    style.jp_title.ruby_style = None

    style.dictionary_section = Style(style.default)
    style.dictionary_section.font = JP_FONT
    style.dictionary_section.size = 32
    style.dictionary_section.color = COL_SECTION
    style.dictionary_section.ruby_style = None
    style.dictionary_section.outlines = TEXT_SHADOW

    style.dictionary_title_en = Style(style.default)
    style.dictionary_title_en.size = 70
    style.dictionary_title_en.color = COL_TITLE_EN
    style.dictionary_title_en.outlines = [
        (2, COL_TITLE_OUT, 0, 0),
        (1, COL_TEXT_SHADOW, 2, 2)
    ]

    style.dictionary_text_en = Style(style.default)
    style.dictionary_text_en.size = 32
    style.dictionary_text_en.color = COL_TEXT_MUTED
    style.dictionary_text_en.outlines = TEXT_SHADOW

    # POS label style
    style.dictionary_pos_text = Style(style.default)
    style.dictionary_pos_text.font = JP_FONT
    style.dictionary_pos_text.size = 42
    style.dictionary_pos_text.color = "#FFFFFF"
    style.dictionary_pos_text.ruby_style = None
    style.dictionary_pos_text.background = Frame(Solid(COL_POS_TAGBG), 8, 8)
    style.dictionary_pos_text.xpadding = 14
    style.dictionary_pos_text.ypadding = 8
    style.dictionary_pos_text.outlines = TEXT_SHADOW

    # Top bar label style
    style.dictionary_toggle_label = Style(style.default)
    style.dictionary_toggle_label.font = JP_FONT
    style.dictionary_toggle_label.size = 28
    style.dictionary_toggle_label.color = "#FFFFFF"
    style.dictionary_toggle_label.outlines = TEXT_SHADOW

    # Panel frame (main container)
    style.dictionary_frame = Style(style.default)
    style.dictionary_frame.background = Frame("gui/dictionary/Box_Square.png", 32, 32)
    style.dictionary_frame.xpadding = 32
    style.dictionary_frame.ypadding = 32

    # Image frame
    style.dictionary_image_frame = Style(style.default)
    style.dictionary_image_frame.background = Frame("gui/dictionary/button_square_line_white.png", 32, 32)
    style.dictionary_image_frame.xpadding = 16
    style.dictionary_image_frame.ypadding = 16


# ---------- Hover Zoom ----------
transform btn_zoom:
    zoom 1.0
    on hover:
        ease 0.12 zoom 1.10
    on idle:
        ease 0.12 zoom 1.0


# ---------- Hover + Click Animation ----------
# Use `activate` instead of mousedown/mouseup so the click bounce works reliably on Ren'Py buttons.
transform btn_interactive:
    zoom 1.0
    on hover:
        ease 0.12 zoom 1.08
    on idle:
        ease 0.12 zoom 1.0
    on activate:
        ease 0.04 zoom 0.94
        ease 0.08 zoom 1.08


# ---------- Smaller Audio Icon ----------
transform dictionary_audio_small:
    zoom 0.72


# ---------- Popup Animations ----------
transform dictionary_popup_swipe_in:
    alpha 0.0
    yoffset 400
    easeout_quart 0.3 alpha 1.0 yoffset 0


# ---------- Popup Screen ----------
screen dictionary_popup(entry, entry_key=None):

    tag dictionary_popup
    modal True
    zorder 200

    button:
        background Solid("#0008")
        xfill True
        yfill True
        action [Stop("voice"), Hide("dictionary_popup")]
        focus_mask True

    frame:
        style "dictionary_frame"
        at dictionary_popup_swipe_in
        xalign 0.5
        yalign 0.5
        yoffset -100
        xsize 1250
        ysize 800

        vbox:
            style "dbg_vbox"
            spacing 16
            xfill True
            yfill True

            # Top bar row
            frame:
                background Null()
                xfill True
                yminimum 52
                ymaximum 52
                padding (0, 0, 0, 0)

                fixed:
                    xfill True
                    yfill True

                    # ---------- Back Button ----------
                    imagebutton:
                        idle "gui/dictionary/arrow_left.png"
                        hover "gui/dictionary/arrow_left.png"
                        at btn_interactive
                        action NullAction()
                        xalign 0.0
                        yalign 0.5
                        focus_mask True

                    # ---------- Tooltip Toggle ----------
                    if entry_key and entry_key in _DICTIONARY:

                        $ _tooltip_enabled = bool(entry.get("tooltip_on", True))
                        $ _tooltip_icon = "gui/dictionary/check_square_color_checkmark.png" if _tooltip_enabled else "gui/dictionary/check_square_color.png"

                        button:
                            background Frame("gui/dictionary/button_square_line_white.png", 32, 32)
                            at btn_interactive
                            xalign 1.0
                            yalign 0.5
                            xsize 250
                            ysize 56
                            action Function(toggle_dictionary_tooltip_for_entry, entry_key)

                            fixed:
                                xfill True
                                yfill True

                                text "Tooltip":
                                    style "dictionary_toggle_label"
                                    xpos 22
                                    yalign 0.5

                                add _tooltip_icon:
                                    xpos 182
                                    yalign 0.5

            hbox:
                style "dbg_hbox"
                spacing 8
                xfill True
                yfill True

                # ---------- LEFT COLUMN ----------
                fixed:
                    xmaximum 0.68
                    yfill True

                    if entry.get("en"):
                        text entry.get("en", "") style "dictionary_title_en":
                            xpos 0
                            ypos 0

                    if entry.get("ja"):
                        text entry.get("ja", "") style "jp_title":
                            xpos 0
                            ypos 96

                    if entry.get("examples"):

                        text "例文 / Examples:" style "dictionary_section":
                            xpos 0
                            ypos 192

                        frame:
                            background Frame("gui/dictionary/button_square_flat_blue.png", 32, 32)
                            padding (20, 14)
                            xfill True
                            ypos 240
                            ysize 400

                            viewport id "examples_vp":
                                mousewheel True
                                draggable True
                                scrollbars "vertical"
                                side_yfill True
                                xfill True
                                yfill True

                                vbox:
                                    spacing 10

                                    for ex in entry["examples"]:

                                        frame:
                                            background Null()
                                            padding (10, 8)

                                            vbox:
                                                spacing 4

                                                if ex.get("ja"):
                                                    text ex["ja"] style "jp_text"

                                                if ex.get("en"):
                                                    text "{i}%s{/i}" % ex["en"] style "dictionary_text_en"

                # ---------- RIGHT COLUMN ----------
                vbox:
                    style "dbg_vbox"
                    spacing 14
                    xmaximum 360
                    yfill True
                    xalign 0.5

                    if entry.get("pos"):

                        $ _pos_key = entry.get("pos", "").lower()
                        $ _pos_label = POS_JA.get(_pos_key, _pos_key)
                        $ _pos_color = POS_COLORS.get(_pos_key, "#FFFFFF")

                        text "[_pos_label]":
                            style "dictionary_pos_text"
                            color _pos_color
                            xalign 0.5

                    $ _image_file = entry.get("image", "")
                    $ _image_path = "dict_images/%s" % _image_file if _image_file else ""
                    $ _has_image = bool(_image_file) and renpy.loadable(_image_path)
                    $ _display_image_path = _image_path if _has_image else "dict_images/question-mark.png"

                    frame:
                        style "dictionary_image_frame"
                        xalign 0.5

                        fixed:
                            xsize 300
                            ysize 300
                            xalign 0.5
                            yalign 0.5

                            add Transform(
                                _display_image_path,
                                fit="contain",
                                xysize=(300, 300)
                            ) xalign 0.5 yalign 0.5

                    fixed:
                        xalign 0.5
                        ysize 64

                        $ _audio_file = entry.get("audio", "")
                        $ _audio_path = "dict_audio/%s" % _audio_file if _audio_file else ""
                        $ _has_audio = bool(_audio_file) and renpy.loadable(_audio_path)

                        if _has_audio:

                            imagebutton:
                                idle "gui/dictionary/Icon_Small_Blank_Audio.png"
                                hover "gui/dictionary/Icon_Small_Blank_Audio.png"
                                at btn_zoom, dictionary_audio_small
                                action Play("voice", _audio_path)
                                xalign 0.5
                                yalign 0.5
                                focus_mask True

                        else:

                            add "gui/dictionary/Icon_Small_Blank_AudioOff.png" at dictionary_audio_small:
                                xalign 0.5
                                yalign 0.5

        # ---------- CLOSE BUTTON ----------
        fixed:
            xfill True
            yfill True

            imagebutton:
                idle "gui/dictionary/XButton.png"
                hover "gui/dictionary/XButton.png"
                at btn_interactive
                action [Stop("voice"), Hide("dictionary_popup")]
                xalign 1.0
                yalign 0.0
                xoffset 52
                yoffset -60
                focus_mask True

    key "game_menu" action [Stop("voice"), Hide("dictionary_popup")]