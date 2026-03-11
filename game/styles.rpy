# styles.rpy
# Character-specific dialogue styling


init 20:

    ########################################
    # Narrator
    ########################################

    style narrator_name is say_label:
        color "#ffffff"
        outlines [(0, "#ffffff", 0, 0)]


    ########################################
    # Haruto (Main Character)
    ########################################

    style haruto_name is say_label:
        color "#0084ff"
        outlines [(0, "#0084ff", 0, 0)]


    ########################################
    # Aiomi (Goddess)
    ########################################

    style aiomi_name is say_label:
        color "#444444"
        outlines [(0, "#ffffff", 0, 0)]