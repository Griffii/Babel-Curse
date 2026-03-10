screen dictionary_hover_tooltip():

    zorder 300

    if dict_tooltip_term and dict_tooltip_term in _DICTIONARY:

        timer 0.02 repeat True action Function(_update_dict_tooltip_mouse)

        $ entry = _DICTIONARY[dict_tooltip_term]
        $ ja_text = entry.get("ja", "")

        if ja_text:

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
                    outlines [(2, "#000000cc", 0, 0)]