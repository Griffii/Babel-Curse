# Put this in game/dictionary_list.rpy (replace previous versions).

screen dictionary_list():

    tag menu

    # --- Load dictionary.json safely right here (not at init time) ---
    $ _rows = []
    $ _err = None
    python:
        import json
        try:
            if not renpy.loadable("dictionary.json"):
                _err = "dictionary.json not found (expected at game/dictionary.json)."
            else:
                f = renpy.file("dictionary.json")
                try:
                    data = json.load(f)   # no object_pairs_hook needed; Python 3.7+ preserves dict order
                except Exception as e:
                    _err = "JSON parse error: %r" % (e,)
                else:
                    if isinstance(data, dict):
                        # object form: { "forest": {...}, ... }
                        for k, v in data.items():
                            en = ""
                            if isinstance(v, dict):
                                try:
                                    en = v.get("en") or ""
                                except Exception:
                                    en = ""
                            _rows.append((str(k), str(en)))
                        if not _rows:
                            _err = "Loaded object, but it contains zero usable entries."
                    elif isinstance(data, list):
                        # array form: [ {"key":"forest","en":"Forest",...}, ... ]
                        for item in data:
                            if isinstance(item, dict) and isinstance(item.get("key"), str) and item["key"]:
                                _rows.append((str(item["key"]), str(item.get("en") or "")))
                        if not _rows:
                            _err = "Loaded array, but found no entries with a non-empty 'key'."
                    else:
                        _err = "Root must be an object or an array."
        except Exception as e:
            _err = "Unexpected error: %r" % (e,)

    frame:
        background Solid("#00000080")
        padding (24, 24)
        xfill True
        yfill True

        vbox:
            spacing 16

            hbox:
                xfill True
                text "Dictionary (read-only)"
                null width 20
                textbutton "Close" action Return()

            if _err:
                vbox:
                    spacing 8
                    text "No dictionary entries to display." color "#FF8080"
                    text _err size 18 color "#FFB0B0"

            elif not _rows:
                vbox:
                    spacing 8
                    text "No dictionary entries to display." color "#FF8080"
                    text "Checked path: game/dictionary.json" size 18 color "#CCCCCC"

            else:
                viewport:
                    draggable True
                    mousewheel True
                    scrollbars "vertical"
                    yfill True

                    vbox:
                        spacing 8
                        # Print: key — en  (avoid braces; en shouldn't have them)
                        for _k, _en in _rows:
                            if _en:
                                # Use substitute False to avoid any chance of tag parsing
                                text (_k + " — " + _en) substitute False
                            else:
                                text _k substitute False
