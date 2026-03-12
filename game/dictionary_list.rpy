# ============================================
# dictionary_list.rpy — Ren'Py 8.4/8.5 compatible
# Dictionary list screen:
# - Larger popup size
# - Centered on screen
# - Search label and search bar on the same row
# - Search field filters results live as the user types
# - Grid of buttons: 4 rows x 5 columns
# - 20 words per page
# - Fixed-size buttons
# - Button text constrained inside button area
# - Subtle centered hover/click animation
# - Page selector at the bottom
# - Search field uses a custom screen-based text input
# - Same input background whether selected or not
# ============================================

default dictionary_list_search = ""
default dictionary_list_page = 0
default dictionary_list_search_active = True

# Replace these with the exact same files used by your main menu.
default dictionary_ui_hover_sfx = "audio/ui/menu_hover.ogg"
default dictionary_ui_click_sfx = "audio/ui/menu_click.ogg"


init -5 python:
    import math
    import renpy.store as store

    DICTIONARY_LIST_PAGE_SIZE = 20
    DICTIONARY_LIST_COLUMNS = 5
    DICTIONARY_LIST_ROWS = 4
    DICTIONARY_LIST_MAX_SEARCH = 40

    def get_filtered_dictionary_ids(search_text=""):
        """
        Returns dictionary keys filtered by English term.
        Matches against the entry's 'en' value first, then falls back to key.
        """
        search_text = (search_text or "").strip().lower()
        results = []

        for key in DICTIONARY_IDS:
            entry = DICTIONARY_DATA.get(key, {})
            en_value = entry.get("en", key)

            if not search_text:
                results.append(key)
            else:
                if search_text in en_value.lower():
                    results.append(key)

        return results

    def get_dictionary_page_count(search_text=""):
        filtered = get_filtered_dictionary_ids(search_text)
        if not filtered:
            return 1
        return int(math.ceil(len(filtered) / float(DICTIONARY_LIST_PAGE_SIZE)))

    def get_dictionary_page_ids(search_text="", page=0):
        filtered = get_filtered_dictionary_ids(search_text)
        start = page * DICTIONARY_LIST_PAGE_SIZE
        end = start + DICTIONARY_LIST_PAGE_SIZE
        return filtered[start:end]

    def open_dictionary_entry_from_list(key):
        """
        Opens the dictionary entry popup from the list screen.
        """
        entry = DICTIONARY_DATA.get(key)
        if entry:
            renpy.show_screen("dictionary_popup", entry=entry, entry_key=key)

    def dictionary_search_add_char(ch):
        """
        Adds a character to the custom search field and resets to page 0.
        """
        current = store.dictionary_list_search or ""

        if len(current) >= DICTIONARY_LIST_MAX_SEARCH:
            return

        store.dictionary_list_search = current + ch
        store.dictionary_list_page = 0
        store.dictionary_list_search_active = True

    def dictionary_search_backspace():
        """
        Deletes one character from the custom search field and resets to page 0.
        """
        current = store.dictionary_list_search or ""
        store.dictionary_list_search = current[:-1]
        store.dictionary_list_page = 0
        store.dictionary_list_search_active = True

    def dictionary_search_clear():
        """
        Clears the search field and resets to page 0.
        """
        store.dictionary_list_search = ""
        store.dictionary_list_page = 0
        store.dictionary_list_search_active = True


init python:

    # ---------- Colors ----------
    LIST_COL_TEXT = "#ffffff"

    # ---------- Base/List Styles ----------
    EN_FONT = "fonts/Poppins/Poppins-Medium.ttf"

    style.dictionary_list_frame = Style(style.default)
    style.dictionary_list_frame.background = Frame("gui/dictionary/Box_Square.png", 32, 32)
    style.dictionary_list_frame.xpadding = 36
    style.dictionary_list_frame.ypadding = 32

    style.dictionary_list_title = Style(style.default)
    style.dictionary_list_title.font = JP_FONT
    style.dictionary_list_title.size = 42
    style.dictionary_list_title.color = "#ffe6b4"
    style.dictionary_list_title.outlines = [(3, "#1F1F1F", 0, 0)]

    style.dictionary_list_search_text = Style(style.default)
    style.dictionary_list_search_text.font = EN_FONT
    style.dictionary_list_search_text.size = 24
    style.dictionary_list_search_text.color = "#000000"
    style.dictionary_list_search_text.outlines = []
    style.dictionary_list_search_text.yoffset = -1

    style.dictionary_list_search_placeholder = Style(style.default)
    style.dictionary_list_search_placeholder.font = EN_FONT
    style.dictionary_list_search_placeholder.size = 24
    style.dictionary_list_search_placeholder.color = "#777777ff"
    style.dictionary_list_search_placeholder.outlines = [(0, "#1F1F1F", 0, 0)]
    style.dictionary_list_search_placeholder.yoffset = -1

    style.dictionary_list_search_label = Style(style.default)
    style.dictionary_list_search_label.font = JP_FONT
    style.dictionary_list_search_label.size = 24
    style.dictionary_list_search_label.color = "#ffffff"
    style.dictionary_list_search_label.outlines = [(2, "#1F1F1F", 0, 0)]

    style.dictionary_list_button_text = Style(style.default)
    style.dictionary_list_button_text.font = EN_FONT
    style.dictionary_list_button_text.size = 28
    style.dictionary_list_button_text.color = LIST_COL_TEXT
    style.dictionary_list_button_text.outlines = [(1, "#1F1F1F", 0, 0)]
    style.dictionary_list_button_text.text_align = 0.5
    style.dictionary_list_button_text.layout = "subtitle"

    style.dictionary_list_empty_text = Style(style.default)
    style.dictionary_list_empty_text.font = JP_FONT
    style.dictionary_list_empty_text.size = 28
    style.dictionary_list_empty_text.color = "#CFD7DE"
    style.dictionary_list_empty_text.outlines = [(1, "#1F1F1F", 0, 0)]

    style.dictionary_list_page_text = Style(style.default)
    style.dictionary_list_page_text.font = EN_FONT
    style.dictionary_list_page_text.size = 24
    style.dictionary_list_page_text.color = "#ffffff"
    style.dictionary_list_page_text.outlines = [(1, "#1F1F1F", 0, 0)]

    style.dictionary_list_page_current = Style(style.dictionary_list_page_text)
    style.dictionary_list_page_current.color = "#ffe6b4"

    # ---------- Search field container ----------
    style.dictionary_list_search_frame = Style(style.default)
    style.dictionary_list_search_frame.background = Frame("gui/dictionary/button_square_line_white.png", 24, 24)
    style.dictionary_list_search_frame.xpadding = 14
    style.dictionary_list_search_frame.ypadding = 8

    # ---------- List button ----------
    style.dictionary_list_item_button = Style(style.button)
    style.dictionary_list_item_button.background = Frame("gui/dictionary/list_button.png", 24, 24)
    style.dictionary_list_item_button.hover_background = Frame("gui/dictionary/list_button.png", 24, 24)
    style.dictionary_list_item_button.xpadding = 8
    style.dictionary_list_item_button.ypadding = 10

    style.dictionary_list_page_button = Style(style.button)
    style.dictionary_list_page_button.background = Frame("gui/dictionary/button_square_line_white.png", 24, 24)
    style.dictionary_list_page_button.hover_background = Frame("gui/dictionary/button_square_line_white.png", 24, 24)
    style.dictionary_list_page_button.xpadding = 0
    style.dictionary_list_page_button.ypadding = 0

    style.dictionary_list_page_current_frame = Style(style.default)
    style.dictionary_list_page_current_frame.background = Frame("gui/dictionary/button_square_border_blue.png", 24, 24)
    style.dictionary_list_page_current_frame.xpadding = 0
    style.dictionary_list_page_current_frame.ypadding = 0


# ---------- Subtle centered hover/click animation ----------
transform list_btn_interactive:
    zoom 1.0
    xanchor 0.5
    yanchor 0.5
    on hover:
        ease 0.10 zoom 1.03
    on idle:
        ease 0.10 zoom 1.0
    on activate:
        ease 0.03 zoom 0.98
        ease 0.06 zoom 1.03


# ---------- Cursor blink for custom search field ----------
transform dictionary_search_caret_blink:
    alpha 1.0
    linear 0.45 alpha 1.0
    linear 0.45 alpha 0.0
    repeat


screen dictionary_list_screen():

    # Disable mouse wheel advancing dialogue while this menu is open
    key "mousedown_4" action NullAction()
    key "mousedown_5" action NullAction()

    tag dictionary_list
    modal True
    zorder 190

    $ _filtered_ids = get_filtered_dictionary_ids(dictionary_list_search)
    $ _page_count = get_dictionary_page_count(dictionary_list_search)
    $ _safe_page = min(dictionary_list_page, _page_count - 1)
    $ _page_ids = get_dictionary_page_ids(dictionary_list_search, _safe_page)
    $ _slots = list(_page_ids) + [None] * (DICTIONARY_LIST_PAGE_SIZE - len(_page_ids))

    if dictionary_list_page != _safe_page:
        timer 0.0 action SetVariable("dictionary_list_page", _safe_page)

    add Solid("#0008")

    # ---------- Custom keyboard input ----------
    if dictionary_list_search_active:
        key "K_a" action Function(dictionary_search_add_char, "a")
        key "K_b" action Function(dictionary_search_add_char, "b")
        key "K_c" action Function(dictionary_search_add_char, "c")
        key "K_d" action Function(dictionary_search_add_char, "d")
        key "K_e" action Function(dictionary_search_add_char, "e")
        key "K_f" action Function(dictionary_search_add_char, "f")
        key "K_g" action Function(dictionary_search_add_char, "g")
        key "K_h" action Function(dictionary_search_add_char, "h")
        key "K_i" action Function(dictionary_search_add_char, "i")
        key "K_j" action Function(dictionary_search_add_char, "j")
        key "K_k" action Function(dictionary_search_add_char, "k")
        key "K_l" action Function(dictionary_search_add_char, "l")
        key "K_m" action Function(dictionary_search_add_char, "m")
        key "K_n" action Function(dictionary_search_add_char, "n")
        key "K_o" action Function(dictionary_search_add_char, "o")
        key "K_p" action Function(dictionary_search_add_char, "p")
        key "K_q" action Function(dictionary_search_add_char, "q")
        key "K_r" action Function(dictionary_search_add_char, "r")
        key "K_s" action Function(dictionary_search_add_char, "s")
        key "K_t" action Function(dictionary_search_add_char, "t")
        key "K_u" action Function(dictionary_search_add_char, "u")
        key "K_v" action Function(dictionary_search_add_char, "v")
        key "K_w" action Function(dictionary_search_add_char, "w")
        key "K_x" action Function(dictionary_search_add_char, "x")
        key "K_y" action Function(dictionary_search_add_char, "y")
        key "K_z" action Function(dictionary_search_add_char, "z")

        key "K_SPACE" action Function(dictionary_search_add_char, " ")
        key "K_MINUS" action Function(dictionary_search_add_char, "-")
        key "K_QUOTE" action Function(dictionary_search_add_char, "'")

        key "K_BACKSPACE" action Function(dictionary_search_backspace)
        key "K_DELETE" action Function(dictionary_search_clear)

    frame:
        style "dictionary_list_frame"
        at dictionary_popup_swipe_in
        xalign 0.5
        yalign 0.5
        yoffset -90
        xsize 1120
        ysize 820

        vbox:
            style "dbg_vbox"
            spacing 16
            xfill True
            yfill True

            # ---------- TOP ROW ----------
            fixed:
                xfill True
                ysize 56

                text "辞書 / Dictionary":
                    style "dictionary_list_title"
                    xalign 0.5
                    yalign 0.5

            # ---------- SEARCH AREA ----------
            hbox:
                spacing 14
                xalign 0.5
                yminimum 64
                ymaximum 64

                text "英語で検索":
                    style "dictionary_list_search_label"
                    yalign 0.5

                button:
                    background Null()
                    xsize 420
                    ysize 60
                    yalign 0.5
                    action SetVariable("dictionary_list_search_active", True)
                    focus_mask None

                    fixed:
                        xfill True
                        yfill True

                        frame:
                            style "dictionary_list_search_frame"
                            xfill True
                            yfill True

                        frame:
                            background Null()
                            xfill True
                            yfill True
                            xpadding 16
                            ypadding 12

                            $ _search_display_x = 0

                            if dictionary_list_search:
                                text "[dictionary_list_search]":
                                    style "dictionary_list_search_text"
                                    xpos _search_display_x
                                    yalign 0.5

                                if dictionary_list_search_active:
                                    text "|":
                                        style "dictionary_list_search_text"
                                        at dictionary_search_caret_blink
                                        xpos min(360, _search_display_x + 12 + len(dictionary_list_search) * 13)
                                        yalign 0.5
                            else:
                                text "Type to search...":
                                    style "dictionary_list_search_placeholder"
                                    xpos _search_display_x
                                    yalign 0.5

                                if dictionary_list_search_active:
                                    text "|":
                                        style "dictionary_list_search_text"
                                        at dictionary_search_caret_blink
                                        xpos _search_display_x
                                        yalign 0.5

            # ---------- GRID AREA ----------
            frame:
                background Frame("gui/dictionary/button_square_flat_blue.png", 32, 32)
                padding (22, 20)
                xfill True
                yfill True

                if _page_ids:

                    grid DICTIONARY_LIST_COLUMNS DICTIONARY_LIST_ROWS:
                        spacing 14
                        xfill True
                        yfill True

                        for key in _slots:

                            if key:
                                $ _entry = DICTIONARY_DATA.get(key, {})
                                $ _entry_en = _entry.get("en", key)

                                fixed:
                                    xsize 188
                                    ysize 108
                                    xalign 0.5
                                    yalign 0.5

                                    button:
                                        style "dictionary_list_item_button"
                                        at list_btn_interactive
                                        xalign 0.5
                                        yalign 0.5
                                        xsize 188
                                        ysize 108
                                        hover_sound dictionary_ui_hover_sfx
                                        activate_sound dictionary_ui_click_sfx
                                        action [
                                            SetVariable("dictionary_list_search_active", False),
                                            Function(open_dictionary_entry_from_list, key)
                                        ]

                                        fixed:
                                            xfill True
                                            yfill True

                                            text _entry_en:
                                                style "dictionary_list_button_text"
                                                xalign 0.5
                                                yalign 0.5
                                                xmaximum 148
                                                ymaximum 72

                            else:
                                fixed:
                                    xsize 188
                                    ysize 108

                else:

                    text "No matching words found.":
                        style "dictionary_list_empty_text"
                        xalign 0.5
                        yalign 0.5

            # ---------- PAGE SELECT ----------
            hbox:
                spacing 10
                xalign 0.5

                if _page_count > 1:

                    for i in range(_page_count):

                        fixed:
                            xsize 46
                            ysize 40

                            if i == _safe_page:
                                frame:
                                    style "dictionary_list_page_current_frame"
                                    xsize 46
                                    ysize 40
                                    xalign 0.5
                                    yalign 0.5

                                    text str(i + 1):
                                        style "dictionary_list_page_current"
                                        xalign 0.5
                                        yalign 0.5

                            else:
                                button:
                                    style "dictionary_list_page_button"
                                    at list_btn_interactive
                                    xsize 46
                                    ysize 40
                                    xalign 0.5
                                    yalign 0.5
                                    hover_sound dictionary_ui_hover_sfx
                                    activate_sound dictionary_ui_click_sfx
                                    action [
                                        SetVariable("dictionary_list_search_active", False),
                                        SetVariable("dictionary_list_page", i)
                                    ]

                                    text str(i + 1):
                                        style "dictionary_list_page_text"
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
                hover_sound dictionary_ui_hover_sfx
                activate_sound dictionary_ui_click_sfx
                action Hide("dictionary_list_screen")
                xalign 1.0
                yalign 0.0
                xoffset 52
                yoffset -60
                focus_mask True

    key "game_menu" action Hide("dictionary_list_screen")