# ============================================
# dictionary_menu.rpy — Ren'Py 8.4 compatible
# Layout update:
# - Close button floats/overlaps at top-right (outside main flow)
# - Main content = vbox with 80px internal margin: Title Box + Content Box
# - Title Box: EN/JP centered on same midline; EN grows RIGHT, JP grows LEFT; bottoms aligned
# - Content Box: hbox -> LEFT (Definition, Examples) / RIGHT (POS, Image, Play)
# - Images fit inside 400x400 (keep aspect).
# - If no image → show "No Image"
# - If no audio → disable play button and show AudioOff icon.
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
            renpy.show_screen("dictionary_popup", entry=entry)


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
    style.jp_text.ruby_style = style.ruby_body
    style.jp_text.ruby_line_leading = 22

    style.jp_title = Style(style.default)
    style.jp_title.font = JP_FONT
    style.jp_title.size = 56
    style.jp_title.color = COL_TITLE_JP
    style.jp_title.outlines = [(2, COL_TITLE_OUT, 0, 0)]
    style.jp_title.ruby_style = style.ruby_title
    style.jp_title.ruby_line_leading = 30

    style.dictionary_section = Style(style.default)
    style.dictionary_section.font = JP_FONT
    style.dictionary_section.size = 34
    style.dictionary_section.color = COL_SECTION
    style.dictionary_section.ruby_style = style.ruby_body
    style.dictionary_section.ruby_line_leading = 18

    style.dictionary_title_en = Style(style.default)
    style.dictionary_title_en.size = 48
    style.dictionary_title_en.color = COL_TITLE_EN
    style.dictionary_title_en.outlines = [(2, COL_TITLE_OUT, 0, 0)]

    style.dictionary_text_en = Style(style.default)
    style.dictionary_text_en.size = 26
    style.dictionary_text_en.color = COL_TEXT_MUTED

    # POS label style
    style.dictionary_pos_text = Style(style.default)
    style.dictionary_pos_text.font = JP_FONT
    style.dictionary_pos_text.size = 42
    style.dictionary_pos_text.color = "#FFFFFF"
    style.dictionary_pos_text.ruby_style = style.ruby_body
    style.dictionary_pos_text.ruby_line_leading = 18
    style.dictionary_pos_text.background = Frame(Solid(COL_POS_TAGBG), 8, 8)
    style.dictionary_pos_text.xpadding = 14
    style.dictionary_pos_text.ypadding = 8

    # Panel frame (main container)
    style.dictionary_frame = Style(style.default)
    style.dictionary_frame.background = Frame("gui/dictionary/Box_Square.png")
    style.dictionary_frame.xpadding = 80
    style.dictionary_frame.ypadding = 80

    # Image frame
    style.dictionary_image_frame = Style(style.default)
    style.dictionary_image_frame.background = Frame("gui/dictionary/Box_Blank_Square.png")
    style.dictionary_image_frame.xpadding = 10
    style.dictionary_image_frame.ypadding = 10


# ---------- Hover Zoom (buttons only) ----------
transform btn_zoom:
    zoom 1.0
    on hover:
        ease 0.12 zoom 1.10
    on idle:
        ease 0.12 zoom 1.0

# ---------- Popup Animations ----------
transform dictionary_popup_swipe_in:
    alpha 0.0
    yoffset 400
    easeout_quart 0.3 alpha 1.0 yoffset 0



# ---------- Popup Screen ----------
screen dictionary_popup(entry):
    tag dictionary_popup
    modal True
    zorder 200

    # Scrim (click background to close instantly)
    button:
        background Solid("#0008")
        xfill True
        yfill True
        action [Stop("voice"), Hide("dictionary_popup")]
        focus_mask True

    # Main Panel
    frame:
        style "dictionary_frame"
        at dictionary_popup_swipe_in
        xalign 0.5
        yalign 0.45
        xmaximum 0.92
        ymaximum 0.88

        # --- Close Button (slide-down close animation) ---
        imagebutton:
            idle "gui/dictionary/XButton.png"
            hover "gui/dictionary/XButton.png"
            at btn_zoom
            action [Stop("voice"), Hide("dictionary_popup")]
            xalign 1.0
            yalign 0.0
            xoffset 100
            yoffset -100

        # --- Main Content Layout ---
        vbox:
            style "dbg_vbox"
            spacing 20
            xfill True
            yfill True

            # ===== Title Section =====
            frame:
                background Null()
                xfill True
                yminimum 56
                ymaximum 56
                padding (0, 0, 0, 8)

                fixed:
                    xfill True
                    yfill True
                    $ _title_gap = 40

                    text entry.get("ja", "") style "jp_title":
                        xpos 0.5
                        xanchor 0.0
                        xoffset _title_gap / 2
                        yalign 1.0
                        yoffset 20

                    text entry.get("en", "") style "dictionary_title_en":
                        xpos 0.5
                        xanchor 1.0
                        xoffset -_title_gap / 2
                        yalign 1.0
                        yoffset 20

            # ===== Content Section =====
            hbox:
                style "dbg_hbox"
                spacing 24
                xfill True
                yfill True

                # ---- LEFT COLUMN ----
                vbox:
                    style "dbg_vbox"
                    spacing 14
                    xmaximum 0.62
                    yfill True

                    if entry.get("ja_expl"):
                        text "{rb}説明{/rb}{rt}せつめい{/rt} / Definition:" style "dictionary_section"
                        text entry["ja_expl"] style "jp_text" xoffset 40

                    if entry.get("examples"):
                        text "{rb}用例{/rb}{rt}ようれい{/rt} / Examples:" style "dictionary_section"

                        frame:
                            background Frame("gui/dictionary/Box_Blue_Square.png")
                            padding (30, 20)
                            xfill True
                            yfill True

                            viewport id "examples_vp":
                                mousewheel True
                                draggable True
                                scrollbars "vertical"
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

                # ---- RIGHT COLUMN ----
                vbox:
                    style "dbg_vbox"
                    spacing 16
                    xmaximum 500
                    yfill True
                    xalign 0.5

                    # POS label
                    if entry.get("pos"):
                        $ _pos_key = entry.get("pos", "").lower()
                        $ _pos_label = POS_JA.get(_pos_key, _pos_key)
                        $ _pos_color = POS_COLORS.get(_pos_key, "#FFFFFF")
                        text "[_pos_label]":
                            style "dictionary_pos_text"
                            color _pos_color
                            xalign 0.5

                    # Image / Placeholder logic (fit inside 400x400)
                    if entry.get("image"):
                        frame:
                            style "dictionary_image_frame"
                            xalign 0.5
                            fixed:
                                xsize 400
                                ysize 400
                                xalign 0.5
                                yalign 0.5
                                add Transform("dict_images/%s" % entry["image"], fit="contain", xysize=(400, 400)) xalign 0.5 yalign 0.5
                    else:
                        frame:
                            style "dictionary_image_frame"
                            xalign 0.5
                            has fixed:
                                xsize 400
                                ysize 200
                                xalign 0.5
                                yalign 0.5
                            text "No Image" style "dictionary_text_en" xalign 0.5 yalign 0.5

                    # Audio button logic
                    if entry.get("audio"):
                        imagebutton:
                            idle "gui/dictionary/Icon_Small_Blank_Audio.png"
                            hover "gui/dictionary/Icon_Small_Blank_Audio.png"
                            at btn_zoom
                            action Play("voice", "dict_audio/%s" % entry["audio"])
                            xalign 0.5
                    else:
                        add "gui/dictionary/Icon_Small_Blank_AudioOff.png" xalign 0.5

    key "game_menu" action [Stop("voice"), Hide("dictionary_popup")]
