
# ---------- Backgrounds ----------
image street_day = "bg/Backstreet_Spring_Day.png"
image street_night = "bg/Backstreet_Spring_Night.png"
image city_day = "bg/City_Morning.png"

image shrine_day = "bg/Street_Summer_Day.png"
image shrine_night = "bg/Shrine_Summer_Night.png"

image school_hall = "bg/School_Hallway_Day.png"
image classroom = "bg/Classroom_Day.png"

# ---------- Haruto  ----------
image haruto neutral = "sprites/Haruto_Placeholder.png"
image aiomi neutral = "sprites/Aiomi_Placeholder.png"
image kai neutral = "sprites/Kai_Placeholder.png"
image mio neutral = "sprites/Mio_Placeholder.png"
image rina neutral = "sprites/Rina_Placeholder.png"

# ---------- Props (foreground) ----------



# ---------- Animations ----------
transform walkinleft:
    subpixel True
    xpos 0.0
    ypos 0.0
    alpha 1.0

    on show:
        xpos -0.39
        alpha 0.0
        
        parallel:
            linear 1.32 xpos 0.0
        parallel:
            linear 0.30 alpha 1.0
            linear 0.21 ypos -0.03
            linear 0.23 ypos 0.0
            linear 0.20 ypos -0.03
            linear 0.21 ypos 0.0
            linear 0.23 ypos -0.03
            linear 0.24 ypos 0.0

transform walkinright:
    subpixel True
    xpos 0.0
    ypos 0.0
    alpha 1.0

    on show:
        xpos 1.39       
        alpha 0.0

        parallel:
            linear 1.32 xpos 0.0

        parallel:
            linear 0.30 alpha 1.0
            linear 0.21 ypos -0.03
            linear 0.23 ypos 0.0
            linear 0.20 ypos -0.03
            linear 0.21 ypos 0.0
            linear 0.23 ypos -0.03
            linear 0.24 ypos 0.0




