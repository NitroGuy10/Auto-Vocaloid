
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
#   Complicated syllables shoud have longer notes
#   A word's syllables should be back-to-back
#   There should be a short pause between words
# I can read the screen and use PyAutoGUI's Locate functions
#   to determine where to click and stuff
#   https://pyautogui.readthedocs.io/en/latest/screenshot.html#the-locate-functions
# Each note can have its "pitch" and "expression" parameters set to the max
# Have the program CTRL+N before inputting every phrase
# Have "breaths" enabled
# Be sure to pick a comfortable tempo
#    Maybe I can pick a tempo based on the "energy/emotion" of the phrase
#    I can use NLTK's sentiment analysis to determine the emotion
#    https://www.nltk.org/api/nltk.sentiment.html
# Have it play the whole thing when it's done
#    One could use VoiceMeeter to feed the audio into a livestream
#


while True:
    phrase = input("> ")
    print(phrase)
