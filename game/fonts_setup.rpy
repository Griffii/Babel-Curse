# ============================================
# fonts_setup.rpy
# - Global font setup using NotoSansJP
# - Centralized font/color/outline control
# ============================================

init 10 python:
    # --------------------------------------------
    # Font paths (relative to game/)
    # --------------------------------------------
    JP_FONT_REGULAR = "fonts/NotoSansJP/NotoSansJP-Regular.ttf"
    JP_FONT_BOLD    = "fonts/NotoSansJP/NotoSansJP-Bold.ttf"
    JP_FONT_LIGHT   = "fonts/NotoSansJP/NotoSansJP-Light.ttf"

    # --------------------------------------------
    # Base/default font
    # --------------------------------------------
    style.default.font = JP_FONT_REGULAR
    style.default.size = 34

    # --------------------------------------------
    # GUI fonts
    # Keep all font assignments centralized here
    # --------------------------------------------
    gui.text_font = JP_FONT_REGULAR
    gui.name_text_font = JP_FONT_REGULAR
    gui.interface_text_font = JP_FONT_REGULAR

    # --------------------------------------------
    # Core text colors
    # --------------------------------------------
    gui.text_color = "#ffffff"
    gui.interface_text_color = "#ffffff"
    gui.name_text_color = "#ffffff"

    # --------------------------------------------
    # Outlines
    # Dialogue: thicker black outline
    # Names: thin black outline
    # Interface: no outline by default
    # --------------------------------------------
    gui.text_outlines = [(1, "#1F1F1F", 0, 0)]
    gui.name_text_outlines = [(1, "#1F1F1F", 0, 0)]
    gui.interface_text_outlines = []

    # --------------------------------------------
    # Dialogue / thought / NVL
    # --------------------------------------------
    style.say_dialogue.color = gui.text_color
    style.say_dialogue.outlines = gui.text_outlines

    style.say_thought.color = gui.text_color
    style.say_thought.outlines = gui.text_outlines

    style.nvl_dialogue.color = gui.text_color
    style.nvl_dialogue.outlines = gui.text_outlines

    style.history_text.color = gui.text_color
    style.history_text.outlines = gui.text_outlines

    # --------------------------------------------
    # Character name styling
    # Character-specific styles like:
    #   style haruto_name is say_label:
    #       color "#001e39"
    # will inherit this outline automatically.
    # --------------------------------------------
    style.say_label.color = gui.name_text_color
    style.say_label.outlines = gui.name_text_outlines

    # Optional: keep menu choice text readable too.
    style.menu_choice_button_text.outlines = gui.text_outlines

    # --------------------------------------------
    # Bold / italic mapping
    # {b} -> Bold
    # {i} -> Light (used as “italic”)
    # --------------------------------------------
    config.font_replacement_map[
        (JP_FONT_REGULAR, True, False)
    ] = (JP_FONT_BOLD, False, False)

    config.font_replacement_map[
        (JP_FONT_REGULAR, False, True)
    ] = (JP_FONT_LIGHT, False, False)

    config.font_replacement_map[
        (JP_FONT_REGULAR, True, True)
    ] = (JP_FONT_BOLD, False, False)

    # --------------------------------------------
    # Ruby (furigana) style
    # Leave color inherited from parent text
    # --------------------------------------------
    style.ruby_style.font = JP_FONT_REGULAR
    style.ruby_style.size = 16
    style.ruby_style.yoffset = -40
    style.ruby_style.color = None

    style.say_dialogue.ruby_line_leading = 20
    style.say_dialogue.ruby_style = style.ruby_style

    style.history_text.ruby_line_leading = 20
    style.history_text.ruby_style = style.ruby_style