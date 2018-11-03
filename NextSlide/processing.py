import transcription
import itertools
import re
import sys
import pyautogui
import Powerpoint2Text
import string

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import cosine_similarity


class Processor:
    commands = {"exit": "", "next slide": "right", "previous slide": "left"}

    def __init__(self, powerpoint):
        self.textOfPPT = Powerpoint2Text.parsePPTX(powerpoint)
        print(self.textOfPPT)
        self.numberSlides = len(self.textOfPPT)
        self.currentSlide = 0

        self.endOfSlideCues = []
        self.startOfSlideCues = []

        # self.endOfSlideCues=self.getEndCues(textOfPPT)
        # self.startOfSlideCues=self.getStartCues(self.textOfPPT)

        self.setStartAndEndCues()
        print(self.startOfSlideCues)
        print(self.endOfSlideCues)
        # self.endOfSlideCues = ["end of first", "second end second", "end of third third", "fourth end fourth"]
        # self.startOfSlideCues = ["the beginning", "start of second", "start of third", "start of fourth"]
        self.unmatchedFinals = ""
        self.BREAK = False

    def weighter(currentPowerPointContent, stringOfWordsSaid):
        if type(stringOfWordsSaid) is str: stringOfWordsSaid = [stringOfWordsSaid]
        documents = [currentPowerPointContent]
        for strs in stringOfWordsSaid:
            documents.append(strs)

        # vectorizer fits our powerpoint / document
        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix = tfidf_vectorizer.fit_transform(documents)

        # gives matrix of simlarity
        similarityResult = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix)[0]
        return (sum(similarityResult) - 1) / (len(similarityResult) - 1)

    def callCommand(self, command):
        if (command == "next slide" and self.currentSlide == self.numberSlides - 1) or (command == "previous slide" and self.currentSlide == 0):
            return
        pyautogui.press(self.commands[command])
        if self.commands[command] == "right": self.currentSlide += 1
        if self.commands[command] == "left": self.currentSlide -= 1
        print("Slide: %i" % self.currentSlide)

    def parseForCue(self, transcript):
        for cue in self.commands:
            if re.search(r'\b(%s)\b' % cue, self.unmatchedFinals + transcript, re.I):
                if cue == "exit":
                    self.BREAK = True
                    return True
                self.callCommand(cue)
                return True  # only want to run one command

        space = " "
        lastFour = space.join((self.unmatchedFinals + transcript).split(" ")[:4])

        if self.similar(self.endOfSlideCues[self.currentSlide], lastFour):
            # if re.search(r'\b(%s)\b' % (self.endOfSlideCues[self.currentSlide]), self.unmatchedFinals+transcript, re.I):
            self.callCommand("next slide")  # should be in commands
            return True

        for i in range(len(self.startOfSlideCues)):  # todo edge cases
            if self.similar(self.startOfSlideCues[i], lastFour):
                # if self.startOfSlideCues[i]!=" " and re.search(r'\b(%s)\b' % self.startOfSlideCues[i], self.unmatchedFinals+transcript, re.I):
                self.goToSlide(i)
                return True

        return False

    def goToSlide(self, slide):
        difference = self.currentSlide - slide
        if difference == 0:
            return
        command = "previous slide" if difference > 0 else "next slide"
        for i in range(abs(difference)):
            self.callCommand(command)

    def listen_print_loop(self, responses):
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

        keeplooking = True
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

            if result.is_final:
                if keeplooking:  # haven't found a command yet
                    keeplooking = not self.parseForCue(transcript)
                    if not keeplooking:  # found a command
                        self.unmatchedFinals = ""
                if keeplooking: self.unmatchedFinals += transcript  # if we still haven't found a command, add to unmatched
                keeplooking = True

            elif keeplooking:
                keeplooking = not self.parseForCue(transcript)  # if something not found, keeplooking
                if not keeplooking:
                    self.unmatchedFinals = ""
            if self.BREAK: break

            # num_chars_printed = 0

    def setStartAndEndCues(self):
        for element in self.textOfPPT:
            space = " "
            self.startOfSlideCues.append(space.join(element.split(" ")[:4]))
            self.endOfSlideCues.append(space.join(element.split(" ")[-4:]))

    def similar(self, endCues, transcript):
        listOfEndCues = [w for w in re.split('\W', endCues) if w]
        listTranscript = transcript.split(" ")
        count = 0
        for i, j in zip(listOfEndCues, listTranscript):
            if i == j: count += 1
        return (count >= len(endCues) * 0.7)

    def unPunctuatedAndLower(self, str):
        exclude = set(string.punctuation)
        s = "".join(ch.lower() for ch in str if ch not in exclude)
        return s
