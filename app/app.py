import os, sys, subprocess
import pickle
import glob

import argparse

import speech_recognition as sr
import core_funcs

# Version Control Constants
APPLICATION_NAME = "Alice"
APPLICATION_RELEASE = 0
APPLICATION_REVISION = 0

should_listen = False
recognizer = None
VERBOSITY = 0

prompts = [ "hey alice", "alice", "okay alice", "hey alex", "alex", "okay alex" ]
alice = None

def log(s, tolerance=1):
    global VERBOSITY

    if VERBOSITY >= tolerance:
        print(s)

def capture_voice(speech_recognizer):
    with sr.Microphone() as source:
        audio = speech_recognizer.listen(source)
    try:
        res = speech_recognizer.recognize_google(audio).lower()
        log("You said: " + res)
        return res
    except sr.UnknownValueError:
        log("Google Speech Recognition could not understand audio")
        return ""
    except sr.RequestError as e:
        log("Could not request results from Google Speech Recognition service; {0}".format(e))
        return ""

def parse_query(res):
    global should_listen, prompts

    if use_voice:
        for prompt in prompts:
            if res.startswith(prompt) and len(res) > len(prompt):
                res = res[ len(prompt): ]
                should_listen = True

    if use_voice == False or should_listen:
        cross_check_models(res)

    should_listen = res in prompts


models = []
ordinal_scalers = []
def load_models():
    global models
    model_list = glob.glob("../training/MODELS/*.model")
    log("Found %d models" % (len(model_list),))
    for model_name in model_list:
        with open(model_name, 'r') as MODEL_FILE:
            models.append(pickle.load(MODEL_FILE))
        log("Loaded model: %s" % (models[-1].name,))

def cross_check_models(sentence):
    log("Checking << %s >> with existing models..." % (sentence,))
    for model in models:
        if model.match(sentence):
            log("Matched with %s" % (model.name,))
            alice.command_mapping[ model.name ](sentence)
            return
        else:
            log("Did not match with %s" % (model.name,), tolerance=2)

def main():
    global use_voice, recognizer

    load_models()
    if use_voice:
        recognize = sr.Recognizer()

    query = ""
    while True:
        query = capture_voice(r) if use_voice else str(raw_input("alice > "))
        parse_query(query)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Alice - Linux Virtual Assistant")
    parser.add_argument("--use-voice", "-V", action="store_true")
    parser.add_argument("--talk", "-t", action="store_true")
    parser.add_argument("--test", "-T", action="store_true")
    parser.add_argument('--verbose', '-v', action='count')
    parser.add_argument('--version', action='version', version="%s %d.%d" %
            (APPLICATION_NAME, APPLICATION_RELEASE, APPLICATION_REVISION))

    args = parser.parse_args()

    use_voice = args.use_voice
    VERBOSITY = args.verbose
    if args.test:
        alice = core_funcs.DummyActuator()
    else:
        alice = core_funcs.CommandActuator(talk=args.talk)

    main()

