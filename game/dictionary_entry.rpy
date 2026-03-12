# ============================================
# dictionary_menu.rpy — Ren'Py 8.5 compatible
# Compact dictionary entry popup:
# - Fixed popup size: 1250 x 800
# - Centered on screen
# - No image section
# - Top row: Back button (left), Tooltip toggle (right)
# - Row 2: English word (left), Audio icon (right)
# - Row 3: Japanese word (left), POS label (right)
# - Bottom: Example sentence box fills remaining space
# - No furigana shown in this screen
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
    COL_TITLE_EN = "#FFB347"
    COL_TITLE_JP = "#FFB347"
    COL_TITLE_OUT = "#1F1F1F"
    COL_SECTION = "#3abaf5"
    COL_POS_TAGBG = "#3e2244"

    COL_TEXT_OUTLINE = "#1F1F1F"
    TEXT_OUTLINE = [(2, COL_TEXT_OUTLINE, 0, 0)]

    style.dbg_vbox = Style(style.default)
    style.dbg_vbox.background = Null()

    style.dbg_hbox = Style(style.default)
    style.dbg_hbox.background = Null()

    style.jp_text = Style(style.default)
    style.jp_text.font = JP_FONT
    style.jp_text.size = 32
    style.jp_text.color = COL_TEXT_MAIN
    style.jp_text.line_spacing = 2
    style.jp_text.ruby_style = None
    style.jp_text.outlines = TEXT_OUTLINE

    style.jp_title = Style(style.default)
    style.jp_title.font = JP_FONT
    style.jp_title.size = 52
    style.jp_title.color = COL_TITLE_JP
    style.jp_title.outlines = [
        (3, COL_TITLE_OUT, 0, 0)
    ]
    style.jp_title.ruby_style = None

    style.dictionary_section = Style(style.default)
    style.dictionary_section.font = JP_FONT
    style.dictionary_section.size = 32
    style.dictionary_section.color = COL_SECTION
    style.dictionary_section.ruby_style = None
    style.dictionary_section.outlines = TEXT_OUTLINE

    style.dictionary_title_en = Style(style.default)
    style.dictionary_title_en.size = 52
    style.dictionary_title_en.color = COL_TITLE_EN
    style.dictionary_title_en.outlines = [
        (3, COL_TITLE_OUT, 0, 0)
    ]

    style.dictionary_text_en = Style(style.default)
    style.dictionary_text_en.size = 32
    style.dictionary_text_en.color = COL_TEXT_MUTED
    style.dictionary_text_en.outlines = TEXT_OUTLINE

    style.dictionary_pos_text = Style(style.default)
    style.dictionary_pos_text.font = JP_FONT
    style.dictionary_pos_text.size = 38
    style.dictionary_pos_text.color = "#FFFFFF"
    style.dictionary_pos_text.ruby_style = None
    style.dictionary_pos_text.background = Frame(Solid(COL_POS_TAGBG), 8, 8)
    style.dictionary_pos_text.xpadding = 14
    style.dictionary_pos_text.ypadding = 8
    style.dictionary_pos_text.outlines = TEXT_OUTLINE

    style.dictionary_toggle_label = Style(style.default)
    style.dictionary_toggle_label.font = JP_FONT
    style.dictionary_toggle_label.size = 28
    style.dictionary_toggle_label.color = "#FFFFFF"
    style.dictionary_toggle_label.outlines = TEXT_OUTLINE

    style.dictionary_frame = Style(style.default)
    style.dictionary_frame.background = Frame("gui/dictionary/Box_Square.png", 32, 32)
    style.dictionary_frame.xpadding = 32
    style.dictionary_frame.ypadding = 32

    # ---------- Example Scrollbar Styles ----------
    style.dictionary_vscrollbar = Style(style.vscrollbar)
    style.dictionary_vscrollbar.xmaximum = 26
    style.dictionary_vscrollbar.xminimum = 26
    style.dictionary_vscrollbar.top_bar = Frame("gui/dictionary/slide_vertical.png", 0, 0)
    style.dictionary_vscrollbar.bottom_bar = Frame("gui/dictionary/slide_vertical.png", 0, 0)
    style.dictionary_vscrollbar.thumb = Frame("gui/dictionary/slide_grabber.png", 3, 3)
    style.dictionary_vscrollbar.unscrollable = "hide"


transform btn_zoom:
    zoom 1.0
    on hover:
        ease 0.12 zoom 1.10
    on idle:
        ease 0.12 zoom 1.0


transform btn_interactive:
    zoom 1.0
    on hover:
        ease 0.12 zoom 1.08
    on idle:
        ease 0.12 zoom 1.0
    on activate:
        ease 0.04 zoom 0.94
        ease 0.08 zoom 1.08


transform dictionary_audio_small:
    zoom 0.5


transform dictionary_popup_swipe_in:
    alpha 0.0
    yoffset 400
    easeout_quart 0.3 alpha 1.0 yoffset 0


screen dictionary_popup(entry, entry_key=None):

    # Disable mouse wheel advancing dialogue while this menu is open
    key "mousedown_4" action NullAction()
    key "mousedown_5" action NullAction()

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
        xsize 900
        ysize 700

        vbox:
            style "dbg_vbox"
            spacing 18
            xfill True
            yfill True

            # ---------- TOP ROW ----------
            fixed:
                xfill True
                ysize 56

                imagebutton:
                    idle "gui/dictionary/arrow_left.png"
                    hover "gui/dictionary/arrow_left.png"
                    at btn_interactive
                    action [Hide("dictionary_popup"), Show("dictionary_list_screen")]
                    xalign 0.0
                    yalign 0.5
                    focus_mask True

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

                            text "ヒント表示":
                                style "dictionary_toggle_label"
                                xpos 22
                                yalign 0.5

                            add _tooltip_icon:
                                xpos 182
                                yalign 0.5

            # ---------- EN / AUDIO ----------
            fixed:
                xfill True
                ysize 84

                if entry.get("en"):
                    text entry.get("en", "") style "dictionary_title_en":
                        xpos 0
                        yalign 0.5

                $ _audio_file = entry.get("audio", "")
                $ _audio_path = "dict_audio/%s" % _audio_file if _audio_file else ""
                $ _has_audio = bool(_audio_file) and renpy.loadable(_audio_path)

                if _has_audio:

                    imagebutton:
                        idle "gui/dictionary/Icon_Small_Blank_Audio.png"
                        hover "gui/dictionary/Icon_Small_Blank_Audio.png"
                        at btn_interactive, dictionary_audio_small
                        action Play("voice", _audio_path)
                        xalign 1.0
                        yalign 0.5
                        focus_mask True

                else:

                    add "gui/dictionary/Icon_Small_Blank_AudioOff.png" at dictionary_audio_small:
                        xalign 1.0
                        yalign 0.5


            # ---------- JP / POS ----------
            fixed:
                xfill True
                ysize 64

                if entry.get("ja"):
                    text entry.get("ja", "") style "jp_title":
                        xpos 0
                        yalign 0.5

                if entry.get("pos"):

                    $ _pos_key = entry.get("pos", "").lower()
                    $ _pos_label = POS_JA.get(_pos_key, _pos_key)
                    $ _pos_color = POS_COLORS.get(_pos_key, "#FFFFFF")

                    text "[_pos_label]":
                        style "dictionary_pos_text"
                        color _pos_color
                        xalign 1.0
                        yalign 0.5


            text "例文 / Examples:" style "dictionary_section":
                xalign 0.5


            frame:
                background Frame("gui/dictionary/button_square_flat_blue.png", 32, 32)
                padding (24, 18)
                xfill True
                yfill True

                side "c r":

                    viewport id "examples_vp":
                        mousewheel True
                        draggable True
                        xfill True
                        yfill True

                        vbox:
                            spacing 10

                            for ex in entry.get("examples", []):

                                frame:
                                    background Null()
                                    padding (10, 8)

                                    vbox:
                                        spacing 4

                                        if ex.get("ja"):
                                            text ex["ja"] style "jp_text"

                                        if ex.get("en"):
                                            text "{i}%s{/i}" % ex["en"] style "dictionary_text_en"

                    vbar:
                        value YScrollValue("examples_vp")
                        style "dictionary_vscrollbar"


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