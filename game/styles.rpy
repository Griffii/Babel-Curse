# Character-specific styles
# This can live in characters.rpy or its own file.

init 20:
    # Haruto name color
    style haruto_name is say_label:
        color "#001e39"

    # Haruto window
    style haruto_window is window:
        background Image("gui/textboxes/haruto_textbox.png", xalign=0.5, yalign=1.0)

    style haruto_namebox is namebox:
        background Frame(
            "gui/textboxes/haruto_namebox.png",
            gui.namebox_borders,
            tile=gui.namebox_tile,
            xalign=gui.name_xalign,
        )


    # Aiomi
    style aiomi_name is say_label:
        color "#b8005c"

    style aiomi_window is window:
        background Image("gui/textboxes/aiomi_textbox.png", xalign=0.5, yalign=1.0)

    style aiomi_namebox is namebox:
        background Frame(
            "gui/textboxes/aiomi_namebox.png",
            gui.namebox_borders,
            tile=gui.namebox_tile,
            xalign=gui.name_xalign,
        )


    # Narrator
    style narrator_window is window:
        background Image("gui/textboxes/textbox_light_yellow.png", xalign=0.5, yalign=1.0)


    # Kai
    style kai_window is window:
        background Image("gui/textboxes/kai_textbox.png", xalign=0.5, yalign=1.0)

    style kai_namebox is namebox:
        background Frame(
            "gui/textboxes/kai_namebox.png",
            gui.namebox_borders,
            tile=gui.namebox_tile,
            xalign=gui.name_xalign,
        )
