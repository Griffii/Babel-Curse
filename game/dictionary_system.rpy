# ============================================
# dictionary_system.rpy (Ren'Py 8.x)
#
# Features
# --------------------------------------------
# - Auto-tags words from dictionary.json
# - POS-specific colors
# - Yellow outline styling
# - Click word → dictionary popup
# - Hover word → tooltip screen (if tooltip_on is true)
# - Supports toggling tooltip_on from the popup UI
#
# Tooltip UI is implemented in:
# dictionary_tooltip.rpy
# ============================================


default dict_tooltip_term = None
default dict_tooltip_x = 0
default dict_tooltip_y = 0


init -1 python:

    import json
    import re
    import os


    # --------------------------
    # POS color map
    # --------------------------
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

    DEFAULT_POS_COLOR = "#FFFFFF"


    # --------------------------
    # Globals
    # --------------------------
    _DICTIONARY = {}
    _ID_TO_POS = {}
    _DICTIONARY_RE = None


    # --------------------------
    # Base hyperlink style
    # --------------------------
    def _ensure_base_dictionary_styles():

        style.dictionary_word = Style(style.say_dialogue)

        style.dictionary_word.outlines = [
            (3, "#000000", 0, 0),
            (2, "#FFD700", 0, 0),
        ]

        style.dictionary_word.color = "#ffffff"
        style.dictionary_word.hover_color = "#ffff88"
        style.dictionary_word.underline = False


    _ensure_base_dictionary_styles()


    # --------------------------
    # Dictionary path helpers
    # --------------------------
    def get_dictionary_json_write_path(filename="dictionary.json"):
        """
        Real writable filesystem path.
        Works in development / unpacked projects.

        If dictionary.json is packed into an archive in a built game,
        writing back to it may not work.
        """
        return os.path.join(config.gamedir, filename)


    # --------------------------
    # Load dictionary JSON
    # --------------------------
    def load_dictionary_json(path="dictionary.json"):

        global _DICTIONARY
        global _ID_TO_POS
        global _DICTIONARY_RE

        try:
            with renpy.file(path) as f:
                data = json.load(f) or {}
        except Exception:
            data = {}

        _DICTIONARY = data
        _ID_TO_POS.clear()

        def normalize_pos(pos):

            if not pos:
                return None

            pos = pos.strip().lower()

            if pos in POS_COLORS:
                return pos

            return None

        ids = []

        for word_id, entry in data.items():

            if not isinstance(word_id, str):
                continue

            low = word_id.lower()
            ids.append(low)
            _ID_TO_POS[low] = normalize_pos(entry.get("pos"))

        ids.sort(key=len, reverse=True)

        if ids:
            pattern = r"\b(" + "|".join(re.escape(k) for k in ids) + r")\b"
            _DICTIONARY_RE = re.compile(pattern, re.IGNORECASE)
        else:
            _DICTIONARY_RE = None


    load_dictionary_json("dictionary.json")


    # --------------------------
    # Save dictionary JSON
    # --------------------------
    def save_dictionary_json(path="dictionary.json"):
        """
        Save the current in-memory _DICTIONARY back to disk.
        """
        write_path = get_dictionary_json_write_path(path)

        with open(write_path, "w", encoding="utf-8") as f:
            json.dump(_DICTIONARY, f, ensure_ascii=False, indent=2)


    # --------------------------
    # Tooltip flag helpers
    # --------------------------
    def entry_tooltip_is_on(entry):
        """
        Default behavior:
        - missing tooltip_on => True
        - explicit false => False
        """
        if not isinstance(entry, dict):
            return True

        return bool(entry.get("tooltip_on", True))


    def should_show_dictionary_tooltip(term):
        entry = _DICTIONARY.get(term)
        if not entry:
            return False

        return entry_tooltip_is_on(entry)


    def toggle_dictionary_tooltip_for_entry(term):
        """
        Flip tooltip_on for a specific dictionary entry,
        save dictionary.json, reload in-memory dictionary,
        and refresh currently open popup.
        """
        if not term:
            return

        entry = _DICTIONARY.get(term)
        if not entry:
            return

        current = bool(entry.get("tooltip_on", True))
        entry["tooltip_on"] = not current

        try:
            save_dictionary_json("dictionary.json")
        except Exception as e:
            renpy.notify("Failed to save dictionary.json")
            return

        load_dictionary_json("dictionary.json")

        updated_entry = _DICTIONARY.get(term, entry)

        store.dict_tooltip_term = None
        renpy.hide_screen("dictionary_hover_tooltip")
        renpy.show_screen("dictionary_popup", entry=updated_entry, entry_key=term)
        renpy.restart_interaction()


    # --------------------------
    # Inject dictionary tags
    # --------------------------
    def _inject_dictionary_tags(text):

        if not _DICTIONARY_RE or not text:
            return text

        parts = re.split(r"(\{[^}]*\})", text)

        for i, chunk in enumerate(parts):

            if not chunk or chunk.startswith("{"):
                continue

            def repl(match):

                shown = match.group(1)
                key = shown.lower()

                pos = _ID_TO_POS.get(key)
                color = POS_COLORS.get(pos, DEFAULT_POS_COLOR)

                return (
                    "{=dictionary_word}"
                    "{a=dictionary:%s}"
                    "{color=%s}%s{/color}"
                    "{/a}"
                    "{/=}"
                ) % (key, color, shown)

            parts[i] = _DICTIONARY_RE.sub(repl, chunk)

        return "".join(parts)


    config.say_menu_text_filter = _inject_dictionary_tags


# ============================================
# Hyperlink handlers
# ============================================

init -10 python:


    # --------------------------
    # Click handler
    # --------------------------
    def _dictionary_hyperlink(term):

        entry = _DICTIONARY.get(term)

        if not entry:
            entry = {
                "en": term,
                "ja": "—",
                "ja_expl": "該当する項目が見つかりません。",
                "tooltip_on": True,
            }

        store.dict_tooltip_term = None
        renpy.hide_screen("dictionary_hover_tooltip")

        renpy.show_screen("dictionary_popup", entry=entry, entry_key=term)
        renpy.restart_interaction()


    config.hyperlink_handlers["dictionary"] = _dictionary_hyperlink


    # --------------------------
    # Tooltip helpers
    # --------------------------
    def _show_dictionary_tooltip(term):

        if not term:
            _hide_dictionary_tooltip()
            return

        if not should_show_dictionary_tooltip(term):
            _hide_dictionary_tooltip()
            return

        x, y = renpy.get_mouse_pos()

        store.dict_tooltip_term = term
        store.dict_tooltip_x = x
        store.dict_tooltip_y = y

        renpy.show_screen("dictionary_hover_tooltip")
        renpy.restart_interaction()


    def _hide_dictionary_tooltip():

        store.dict_tooltip_term = None
        renpy.hide_screen("dictionary_hover_tooltip")
        renpy.restart_interaction()


    def _update_dict_tooltip_mouse():

        if store.dict_tooltip_term:
            x, y = renpy.get_mouse_pos()
            store.dict_tooltip_x = x
            store.dict_tooltip_y = y


    # --------------------------
    # Hyperlink style
    # --------------------------
    def dictionary_hyperlink_styler(target):

        if target and target.startswith("dictionary:"):
            return style.dictionary_word

        return style.hyperlink_text


    # --------------------------
    # Hyperlink click behavior
    # --------------------------
    def dictionary_hyperlink_clicked(target):

        if not target:
            return

        if target.startswith("dictionary:"):
            term = target[len("dictionary:"):]
            _dictionary_hyperlink(term)

        return


    # --------------------------
    # Hover focus handler
    # --------------------------
    def dictionary_hyperlink_focus(target):

        if target and target.startswith("dictionary:"):
            term = target[len("dictionary:"):]
            _show_dictionary_tooltip(term)
        else:
            _hide_dictionary_tooltip()

        return


    # --------------------------
    # Apply hyperlink behavior
    # --------------------------
    style.say_dialogue.hyperlink_functions = (
        dictionary_hyperlink_styler,
        dictionary_hyperlink_clicked,
        dictionary_hyperlink_focus,
    )