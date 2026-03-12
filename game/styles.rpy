# styles.rpy
# Character-specific dialogue styling


init 20:

    ########################################
    # Narrator
    ########################################

    style narrator_name is say_label:
        color "#E8F2FF"
        outlines [(2, "#242424", 0, 0)]


    ########################################
    # Haruto (Main Character)
    ########################################

    style haruto_name is say_label:
        color "#6FB6FF"
        outlines [(2, "#242424", 0, 0)]


    ########################################
    # Aiomi (Goddess)
    ########################################

    style aiomi_name is say_label:
        color "#FF8FD6"
        outlines [(2, "#242424", 0, 0)]