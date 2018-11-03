import transcription
import itertools
import re
import sys
import pyautogui

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import cosine_similarity

commands = {"exit": "", "next slide":"right", "previous slide":"left"}
endOfSlideCues = ["end of first", "second end second", "", ""]
startOfSlideCues = ["the beginning", "start of second", "start of third", "start of fourth"]

currentSlide=0
numberSlides=4

def weighter(input):
    documents = input

    #vectorizer fits our powerpoint / document
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(documents)

    #gives matrix of simlarity
    cosine_similarity(tfidf_matrix[0:1], tfidf_matrix)





def loadOfSlideCues(input):
    for slide in input:
        endOfSlideCues.append(slide[:-5])


def callCommand(command):
    global currentSlide
    if (command=="next slide" and currentSlide==numberSlides-1) or (command=="previous slide" and currentSlide==0):
        return
    pyautogui.press(commands[command])
    if commands[command] == "right": currentSlide+=1
    if commands[command] == "left": currentSlide-=1
    print("Slide: %i" % currentSlide)

def parseForCue(transcript):

    for cue in commands:
        if re.search(r'\b(%s)\b' % cue, transcript, re.I):
            if cue == "exit":
                return True
            callCommand(cue)
            return False #only want to run one command

    if re.search(r'\b(%s)\b' % (endOfSlideCues[currentSlide]), transcript, re.I):
        callCommand("next slide") # should be in commands
        return False

    for i in range(len(startOfSlideCues)):
        if re.search(r'\b(%s)\b' % startOfSlideCues[i], transcript, re.I):
            print("calling")
            goToSlide(i)
            return False

    return False

def  goToSlide(slide):
    print("go to slide %i" % slide)
    difference = currentSlide-slide
    if difference==0:
        return
    command = "previous slide" if difference>0 else "next slide"
    print(command)
    for i in range(abs(difference)):
        callCommand(command)


def listen_print_loop(responses):
    """Iterates through server responses and prints them.
    The responses passed is a generator that will block until a response
    is provided by the server.
    Each response may contain multiple results, and each result may contain
    multiple alternatives; for details, see https://goo.gl/tjCPAU.  Here we
    print only the transcription for the top alternative of the top result.
    In this case, responses are provided for interim results as well. If the
    response is an interim one, print a line feed at the end of it, to allow
    the next result to overwrite it, until the response is a final one. For the
    final one, print a newline to preserve the finalized transcription.
    """
    # num_chars_printed = 0
    BREAK = False
    for response in responses:
        if not response.results:
            continue

        # The `results` list is consecutive. For streaming, we only care about
        # the first result being considered, since once it's `is_final`, it
        # moves on to considering the next utterance.
        result = response.results[0]
        if not result.alternatives:
            continue

        # Display the transcription of the top alternative.
        transcript = result.alternatives[0].transcript

        # Display interim results, but with a carriage return at the end of the
        # line, so subsequent lines will overwrite them.
        #
        # If the previous result was longer than this one, we need to print
        # some extra spaces to overwrite the previous result
        # overwrite_chars = ' ' * (num_chars_printed - len(transcript))

        if not result.is_final:
            # sys.stdout.write(transcript + overwrite_chars + '\r')
            # sys.stdout.flush()
            #
            # num_chars_printed = len(transcript)
            pass

        else:
            # Exit recognition if any of the transcribed phrases could be
            # one of our keywords.
            BREAK = parseForCue(transcript)

        if BREAK: break

            # num_chars_printed = 0

