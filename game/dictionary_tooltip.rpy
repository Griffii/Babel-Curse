screen dictionary_hover_tooltip():

    zorder 300

    if dict_tooltip_term and dict_tooltip_term in _DICTIONARY:

        $ entry = _DICTIONARY[dict_tooltip_term]
        $ tooltip_enabled = bool(entry.get("tooltip_on", True))
        $ ja_text = entry.get("ja", "")

        if tooltip_enabled and ja_text:

            timer 0.02 repeat True action Function(_update_dict_tooltip_mouse)

            $ tooltip_w = 260
            $ tooltip_x = dict_tooltip_x + 20
            $ tooltip_y = dict_tooltip_y + 24

            if tooltip_x + tooltip_w > config.screen_width - 20:
                $ tooltip_x = dict_tooltip_x - tooltip_w - 20

            if tooltip_x < 20:
                $ tooltip_x = 20

            if tooltip_y < 20:
                $ tooltip_y = 20

            frame:
                xpos tooltip_x
                ypos tooltip_y
                xmaximum tooltip_w

                background Frame(
                    "gui/dictionary/button_square_border_green.png",
                    32, 32
                )

                padding (16, 12)

                text ja_text:
                    font "fonts/NotoSansJP/NotoSansJP-Bold.ttf"
                    size 30
                    color "#FFFFFF"
                    outlines [(1, "#1F1F1F", 0, 0)]