# ============================================
# fonts_setup.rpy
# - Global font setup using NotoSansJP
# ============================================

init 10 python:
    # Correct paths (relative to game/)
    JP_FONT_REGULAR = "fonts/NotoSansJP/NotoSansJP-Regular.ttf"
    JP_FONT_BOLD    = "fonts/NotoSansJP/NotoSansJP-Bold.ttf"
    JP_FONT_LIGHT   = "fonts/NotoSansJP/NotoSansJP-Light.ttf"

    # ---- Default / base style ----
    style.default.font = JP_FONT_REGULAR
    style.default.size = 34
    style.default.color = "#000000"
    style.default.outlines = []

    # ---- GUI fonts (menus, choices, etc.) ----
    gui.text_font = JP_FONT_REGULAR
    gui.name_text_font = JP_FONT_REGULAR
    gui.interface_text_font = JP_FONT_REGULAR

    # GUI colors (this is what say_dialogue uses)
    gui.text_color = "#000000"
    gui.interface_text_color = "#000000"
    gui.name_text_color = "#000000"

    gui.text_outlines = [ ]
    gui.name_text_outlines = []
    gui.interface_text_outlines = []

    # Make sure key styles are black too
    style.say_dialogue.color = gui.text_color
    style.say_thought.color = gui.text_color
    style.nvl_dialogue.color = gui.text_color
    style.menu_choice_button_text.color = gui.text_color

    # ---- Bold / italic mapping ----
    # {b} → Bold
    config.font_replacement_map[
        (JP_FONT_REGULAR, True, False)
    ] = (JP_FONT_BOLD, False, False)

    # {i} → Light (used as “italic”)
    config.font_replacement_map[
        (JP_FONT_REGULAR, False, True)
    ] = (JP_FONT_LIGHT, False, False)

    # {b}{i} → Bold (or change if you want)
    config.font_replacement_map[
        (JP_FONT_REGULAR, True, True)
    ] = (JP_FONT_BOLD, False, False)

    # ---- Ruby (furigana) style ----
    style.ruby_style.font = JP_FONT_REGULAR
    style.ruby_style.size = 16
    style.ruby_style.yoffset = -40
    style.ruby_style.color = None  # inherit color

    style.say_dialogue.ruby_line_leading = 20
    style.say_dialogue.ruby_style = style.ruby_style

    style.history_text.ruby_line_leading = 20
    style.history_text.ruby_style = style.ruby_style
