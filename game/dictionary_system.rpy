# ============================================
# dictionary_system.rpy (Ren'Py 8.x)
# - Auto-tags words from dictionary.json
# - POS-specific colors (inline {color=} so hyperlink can't override)
# - Yellow outline; no underline
# - Opens dictionary popup as an OVERLAY screen (does not pause/hide script)
# ============================================

init -1 python:
    import json, re

    # --------------------------
    # POS color map (dialogue)
    # --------------------------
    POS_COLORS = {
        "noun":        "#4CAF50",  # Green
        "verb":        "#2196F3",  # Blue
        "adjective":   "#E91E63",  # Pink
        "adverb":      "#9C27B0",  # Purple
        "pronoun":     "#FF9800",  # Orange
        "preposition": "#009688",  # Teal
        "conjunction": "#3F51B5",  # Indigo
        "interjection":"#F44336",  # Red
        "determiner":  "#795548",  # Brown
        "phrase":      "#607D8B",  # Gray
    }
    DEFAULT_POS_COLOR = "#FFFFFF"

    # --------------------------
    # Globals
    # --------------------------
    _DICTIONARY = {}       # id -> entry (for tagging/lookup)
    _ID_TO_POS = {}        # id -> normalized pos
    _DICTIONARY_RE = None  # compiled regex

    # --------------------------
    # Base style (outline, hover, underline off)
    # --------------------------
    def _ensure_base_dictionary_styles():
        style.dictionary_word = Style(style.say_dialogue)
        style.dictionary_word.outlines = [
            (3, "#000000", 0, 0),  # halo
            (2, "#FFD700", 0, 0),  # yellow edge
        ]
        style.dictionary_word.color = "#ffffff"       # default if no POS
        style.dictionary_word.hover_color = "#ffff88"
        style.dictionary_word.underline = False

        # Uncomment below if you don't want hyperlinks to have underlines
        # style.hyperlink_text.underline = False
        
    _ensure_base_dictionary_styles()

    # --------------------------
    # Load dictionary JSON (ids + pos for injector)
    # --------------------------
    def load_dictionary_json(path="dictionary.json"):
        global _DICTIONARY, _ID_TO_POS, _DICTIONARY_RE

        with renpy.file(path) as f:
            data = json.load(f) or {}

        _DICTIONARY = data
        _ID_TO_POS.clear()

        # Normalize POS keys to our map
        def norm_pos(p):
            if not p: return None
            p = p.strip().lower()
            return p if p in POS_COLORS else None

        ids = []
        for _id, entry in data.items():
            if not isinstance(_id, str):
                continue
            low = _id.lower()
            ids.append(low)
            _ID_TO_POS[low] = norm_pos(entry.get("pos"))

        if ids:
            pat = r"\b(" + "|".join(re.escape(k) for k in ids) + r")\b"
            _DICTIONARY_RE = re.compile(pat, re.IGNORECASE)
        else:
            _DICTIONARY_RE = None

    load_dictionary_json("dictionary.json")

    # --------------------------
    # Text filter: inject style + hyperlink + POS color
    # Style wraps hyperlink to preserve outline; inline {color} inside to force POS color.
    # --------------------------
    def _inject_dictionary_tags(s: str):
        if not _DICTIONARY_RE or not s:
            return s

        parts = re.split(r"(\{[^}]*\})", s)  # preserve existing tags

        for i, chunk in enumerate(parts):
            if not chunk or chunk.startswith("{"):
                continue

            def repl(m):
                shown = m.group(1)     # original casing
                key   = shown.lower()
                pos   = _ID_TO_POS.get(key)
                col   = POS_COLORS.get(pos, DEFAULT_POS_COLOR)
                # Style outside -> keeps outline.
                # Inline {color} inside -> beats hyperlink_text.color.
                return "{=dictionary_word}{a=dictionary:%s}{color=%s}%s{/color}{/a}{/=}" % (
                    key, col, shown
                )

            parts[i] = _DICTIONARY_RE.sub(repl, chunk)

        return "".join(parts)

    # Apply to say/menu text automatically
    config.say_menu_text_filter = _inject_dictionary_tags

# --------------------------
# Hyperlink handler → opens popup above dialogue (overlay)
# (UI implemented in dictionary_menu.rpy)
# --------------------------
init -10 python:  
    def _dictionary_hyperlink(term: str):
        # Overlay popup without pausing or hiding the current screen.
        entry = _DICTIONARY.get(term)
        if not entry:
            entry = {
                "en": term,
                "ja_kanji": "—",
                "ja_expl": "該当する項目が見つかりません。"
            }

        # Show or update the same popup (tag = dictionary_popup)
        renpy.show_screen("dictionary_popup", entry=entry)
        renpy.restart_interaction()  # make it appear immediately

    # Register this handler key BEFORE any dialogue runs
    config.hyperlink_handlers["dictionary"] = _dictionary_hyperlink
