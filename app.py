
#
# Get a phrase from the user
# Use NLTK to tokenize the phrase into words, then syllables
#   https://www.nltk.org/api/nltk.tokenize.sonority_sequencing.html
# (Possibly, but probably not) Use CMUdict to get the phonemes for each word
#
# Use PyAutoGUI's mouse/keyboard automation to interact with VOCALOID
# For each word, add the syllables as notes to the VOCALOID editor
#   I guess I can use random numbers to determine the note for syllable
#   They should be within a certain range,
#       with a comfortably large jump between each one
#   I can make the fine pitch be random too so the words sound less sing-songy
#   Complicated syllables shoud have longer notes
#   A word's syllables should be back-to-back
#   There should be a short pause between words
#   There should be a longer pause between sentences, denoted by ./?/!
#   Maybe questions can end off with a higher note
#   You can type spaces into vocaloid to input multiple words at once
#   Maybe I don't have to click at precise locations to place notes
# I can read the screen and use PyAutoGUI's Locate functions
#   to determine where to click and stuff
#   https://pyautogui.readthedocs.io/en/latest/screenshot.html#the-locate-functions
# Each note can have its "pitch" parameters set to the max
#       These are set by clicking and dragging the dots
#       OR by using the inspector side panel
# Have the program CTRL+N before inputting every phrase
# Have "breaths" enabled
# Be sure to pick a comfortable tempo
#    Maybe I can pick a tempo based on the "energy/emotion" of the phrase
#    I can use NLTK's sentiment analysis to determine the emotion
#    https://www.nltk.org/api/nltk.sentiment.html
# Have it play the whole thing when it's done
#    One could use VoiceMeeter to feed the audio into a livestream
#


import random
from nltk.tokenize import SyllableTokenizer
from nltk import word_tokenize

import pyautogui as pag

pag.PAUSE = 0.1
pag.FAILSAFE = True
pag.useImageNotFoundException()

input("Press enter to continue (the program will take control of the mouse and keyboard)...")

# Find the VOCALOID window
if len(pag.getWindowsWithTitle("VOCALOID6 Editor")) == 0:
    print("Couldn't find VOCALOID window")
    exit()

# Focus and resize the VOCALOID window
# Window stuff is technically PyGetWindow btw
# https://pygetwindow.readthedocs.io/en/latest/
window = pag.getWindowsWithTitle("VOCALOID6 Editor")[0]
window.restore()
window.activate()
window.moveTo(0, 0)
window.resizeTo(1800, 1000)
pag.sleep(1)

# Open the editor if it's not already open
if not pag.pixelMatchesColor(1165, 58, (61, 126, 165)):
    pag.click(1165, 58)
    pag.sleep(0.2)


# Close the inspector if it's open
if pag.pixelMatchesColor(1284, 63, (61, 126, 165)):
    pag.click(1284, 63)
    pag.sleep(0.2)


# Resize the editor
editor_resize_location = pag.locateOnScreen("locate_images/style.png")
pag.moveTo(editor_resize_location[0], editor_resize_location[1] + 2)
pag.mouseDown()
pag.moveTo(900, 200)
pag.sleep(0.3)
pag.mouseUp()

# Disable grid snapping
pag.moveTo(548, 223)
pag.mouseDown()
pag.sleep(0.4)
pag.moveTo(548, 482)
pag.mouseUp()

# Set the editor to the minimum horizontal zoom
pag.moveTo(1719, 989)
pag.mouseDown()
pag.moveTo(1619, 989)
pag.sleep(0.2)
pag.mouseUp()

# Set the editor to the minimum vertical zoom
pag.moveTo(1789, 741)
pag.mouseDown()
pag.moveTo(1789, 641)
pag.sleep(0.2)
pag.mouseUp()

# Show pitch bend automation
pag.click(30, 825)
pag.sleep(0.2)
pag.click(30, 865)



SSP = SyllableTokenizer()

while True:
    # Create a new project
    pag.hotkey("ctrl", "n")
    pag.sleep(0.5)
    try:
        # Don't save changes if there are any
        pag.locateOnScreen("locate_images/save_changes.png")
        pag.press("right")
        pag.press("enter")
    except pag.ImageNotFoundException:
        pass
    pag.sleep(1)
    pag.press("enter")
    pag.sleep(0.3)

    # Scroll to a desirable location
    pag.moveTo(1787, 522)
    pag.mouseDown()
    pag.moveTo(1787, 463)
    pag.sleep(0.1)
    pag.mouseUp()

    # Set the tempo
    pag.doubleClick(1043, 68)
    pag.write("130")
    pag.press("enter")

    phrase = input("> ")
    window.activate()

    # Tokenize the phrase into words
    phrase = phrase.replace("/", " slash ").replace("_", " underscore ").replace("@", " at ").replace("%", " percent ").replace("&", " and ").replace("#", "hashtag").replace("$", " dollar ")
    words = word_tokenize(phrase)
    fixed_words = []
    # Smoosh contractions together
    for i in range(len(words)):
        word = words[i].lower()
        if "'" in word and i > 0 and fixed_words[-1] not in ".,?!":
            fixed_words[-1] += word
        else:
            fixed_words.append(word)
    print(fixed_words)

    # Tokenize the words into syllables
    # syllables = [SSP.tokenize(word) for word in fixed_words]
    # print(syllables)

    vocaloid_string = " ".join(fixed_words)
    print(vocaloid_string)

    # Generate notes
    NOTE_WIDTH = 18
    MIN_Y = 500
    MAX_Y = 550
    MIN_X = 68
    MAX_X = 400
    notes = []
    last_x = MIN_X
    while last_x < MAX_X:
        y = random.randint(MIN_Y, MAX_Y)
        notes.append((last_x, y))
        last_x += NOTE_WIDTH

    # Place notes in the editor
    pag.PAUSE = 0.01
    for note in notes:
        pag.moveTo(note[0], note[1])
        pag.mouseDown()
        # pag.sleep(0.1)
        pag.moveRel(NOTE_WIDTH, 0)
        # pag.sleep(0.1)
        pag.mouseUp()
    pag.sleep(3)

    # Input the phrase
    pag.press("left", presses=len(notes))
    pag.sleep(1)
    pag.press("enter")
    pag.sleep(1)
    pag.write(vocaloid_string)
    pag.sleep(1)
    pag.press("enter")
    pag.sleep(3)

    # Remove excess notes
    pag.click(247, 218)
    pag.sleep(0.1)
    first_unused_note_location = None
    try:
        first_unused_note_location = pag.locateOnScreen("locate_images/selected_note_outline.png", region=(MIN_X - 10, MIN_Y - 10, MAX_X - MIN_X + 10, MAX_Y - MIN_Y + 10))
    except pag.ImageNotFoundException:
        first_unused_note_location = pag.locateOnScreen("locate_images/selected_note_outline2.png", region=(MIN_X - 10, MIN_Y - 10, MAX_X - MIN_X + 10, MAX_Y - MIN_Y + 10))
    pag.moveTo(first_unused_note_location[0], first_unused_note_location[1] - 200)
    pag.mouseDown()
    pag.moveTo(MAX_X + 50, first_unused_note_location[1] + 200)
    pag.mouseUp()
    pag.sleep(0.5)
    pag.press("delete")

    # Open the inspector panel
    pag.press("f5")

    # Set note transitions and drift to the max
    pag.hotkey("ctrl", "a")
    pag.click(1737, 336)
    pag.click(1737, 399)
    pag.click(1737, 432)
    pag.click(1737, 463)
    pag.click(1737, 495)
    pag.sleep(0.2)

    # Play the phrase
    pag.press("space")

    break

input()

# Temporary singing demo
window.activate()
pag.sleep(1)
pag.press("alt")
pag.sleep(0.1)
pag.press("enter")
pag.press("down", presses=2)
pag.press("right")
pag.press("enter")
pag.sleep(1)
try:
    # Don't save changes if there are any
    pag.locateOnScreen("locate_images/save_changes.png")
    pag.press("right")
    pag.press("enter")
except pag.ImageNotFoundException:
    pass
pag.sleep(1)
pag.press("enter")
pag.sleep(1)

lyrics = input("> ")

window.activate()
pag.sleep(1)
pag.doubleClick(309, 200)
pag.sleep(0.1)
pag.press("right")
pag.press("enter")
pag.sleep(0.1)
pag.write(lyrics)
pag.sleep(0.5)
pag.press("enter")
pag.sleep(2)
pag.press("space")

