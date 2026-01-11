# ============================================
# script.rpy — Test Script
# ============================================

define config.window = "hide"

# Character Name Shortcuts
define h = Character( # Haruto speaking
    "はると", 
    image="haruto",
    window_style="haruto_window",
    namebox_style="haruto_namebox",
    who_style="haruto_name",
    )
define ht = Character(  # Haruto Internal Thoughts
    image="haruto",
    window_style="haruto_window",
)
define a = Character(
    "あいおみ",
    image="aiomi",
    window_style="aiomi_window",
    namebox_style="aiomi_namebox",
    )
define k = Character(
    "カイ"
    )
define m = Character(
    "みお"
    )
define r = Character(
    "りな"
    )
define n = Character(
    window_style="narrator_window",
)


label start:

    camera:
        perspective True

    # Make sure the window is hidden before anything draws
    window hide

    # Start on pure black with no transition (avoids the "blank texture" flash)
    scene black with None

    # --- FIRST SCENE: street_day + Haruto intro ---

    # Fade in the background
    scene street_day with fade

    play music "music/IntroTrack_01.mp3" volume 0.2 fadein 1 fadeout 1

    # Now bring Haruto in with movement + a small fade
    show haruto neutral at walkinleft
    pause 1.5

    # Only show the textbox after everything is in place
    window show

    ht "僕は高校の２年生、はると鈴木です。 "

    ht "I always try and do my best.{p}I get good grades, I help out at school. {p}I always do what I'm supposed to do."

    # --- SCENE CHANGE: School Classroom ---
    scene classroom with fade
    show haruto neutral at walkinleft


    ht "I'm a member of the student council, and often get extra duties to help out."

    ht "But that's okay. I'm glad to help."

    ht "Sometimes it's hard to find the time to study, but I manage."

    ht "Mid term exams are coming up soon, and the school is getting ready for the culture festival, so things are getting pretty busy."

    ht "I'm worried I might not be able to do all the things everyone needs me to do."

    # --- SCENE CHANGE: Evening Street ---
    scene street_night with fade
    show haruto neutral at walkinleft

    ht "I had to stay late again today."

    ht "It can be tough sometimes, but this is what it is to be a high school student."

    # --- SCENE CHANGE: Evening Shrine ---
    scene shrine_night with fade
    show haruto neutral at bottomleft
    play music "music/Forgotten Memories.mp3" fadein 1 fadeout 1 volume 0.4

    ht "Oh, I didn't mean to come to a shrine."

    ht "Well, when you're at a shrine you're supposed to pray right?"

    # SFX: clap, clap
    h "*Clap*"
    # Close up of Haruto praying

    # Bell Chime - Ominous
    play sound "sfx/shrine_chime.mp3"

    h "Please, let me always make the right choice."

    

    "???" "Tch..."

    "???" "Are you sure?"

    h "Yes! I'm worried I might make too many mistakes and if I just knew what I needed to do things would be a lot better!"

    # Quick fade to Goddesses sad face, lower half, and back

    "???" "Ugh! Are you an idiot?!"

    h "What?!" with vpunch

    # Proper intro shot of Goddess
    show aiomi neutral at bottomright

    "???" "What kind of stupid wish is that?!"

    h "I... I just..."

    "???" "Don't you want to choose for yourself?"

    h "But what if I choose the wrong thing? How am I supposed to pass my exams and finish school and get a good job and-"

    "???" "Is that what you want to do?"

    h "Huh? What are you evening saying?"

    h "I just want to do what everyone does. Have a regular life and-" # Force to next line

    "???" "No."

    h "... {p}What?"

    "???" "No. I don't think that's what you want."

    "???" "You want to stay here forever and be a priest."

    h "..."

    "???" "Now what? Will you stay with me and be a priest?"

    "???" "You really should! It would be the best thing for you. And for me."

    h "Well... I don't..."

    # Angry Goddess

    "???" "So are you just doing whatever everyone else tells you or not? Make up you mind!"

    h "I don't..."

    "???" "CHOOSE!"

    menu:
        "Stay at the shrine and be a priest?"
        
        "Yes":
            "???" "Seriously? You'll really just listen to what anyone tells you to do?"
        "No":
            "???" "No? But you always wanted to make the right choice, so try again."

            menu:
                "Stay at the shrine and be a priest?"

                "Yes":
                    pass
                "Yes":
                    pass

    h "If this is what I'm meant to do, than it's fine right. I'll stay."

    "???" "HAH?!"

    "???" "Unbelievable... humans are so frustrating... 
            Why do I even show up? I should just stay at home and let them mess 
            up their lives all on their own. The gift of free will was wasted on humanity..."
    
    h "Uhh... anyway. Who are you?"

    "???" "Oh right!"

    # Anime pose Goddess

    a "I'm the Goddess of this shrine, Aiomi!"

    ht "A dangerous pervert... I should go home."

    h "Right, of course. I should probably be going anyway. Nice to meet you."

    a "You don't believe me?! Come on~"

    ht "Why am I even here. {p}I should go home quickly."

    # Serious Aiomi
    a "Haruto-kun, wait."

    h "How do you... know my name?"

    a "Do you still want your wish?"

    h "Yeah, I guess so. It would be nice to always know what to do..."

    a "I'm sorry, Haruto."

    # Big animation, Aiomi dashes in a gets face to face with Haruto
    # She whispers "Babel" in some glitch text or something
    # And then kisses Haruto

    ht "I knew it! She is a dangerous pervert..."

    # Fade to black
    scene black with fade
    # END OF PROLOGUE

    # Transition to opening theme/intro sequence
    jump tutorial

    return


# Tutorial sequence to explain the dictionary
label tutorial:

    n "This is the tutorial."

    n "Let's introduce the dictionary!"

    n "Here, in the top left is the dictionary symbol.{p} 
        Clicking that will open up the menu, try it out!"

    n "Great. Now there is lots of English in this game.{p}
        you will often see words like this: English.{p}
        Try clicking on it!"
    
    n "The dictionary will let you click on different words in the story to see their meaning."

    n "That's about it! Enjoy, and good luck!"

    return


# Script for day one
label dayOne:


    return