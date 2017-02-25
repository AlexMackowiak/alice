import os, sys
import urllib
import commands as COMMANDS

class CommandActuator:

    GOOGLE_QUERY_URL = "https://www.google.com/search?hl=en&q=%s&btnG=Google+Search&tbs=com&safe=true"

    def __init__(self, talk=True, volume_controller=None):
        self.command_mapping = {
            "EXIT_ALICE.model" : self.exit,
            "KILL_ACTIVE_WINDOW.model" : self.kill_active_window,
            "SHUTDOWN_COMPUTER.model" : self.shutdown,
            "VOLUME_CONTROL.model" : self.volume,
            "LOCK_COMPUTER.model" : self.lock,
            "OPEN_WEB_BROWSER.model" : self.open_web_browser,
            "GOOGLE_SEARCH.model" : self.google_search
        }
        self.talk = talk
        self.volume_controller = volume_controller

    def exit(self, s):
        sys.exit()

    def kill_active_window(self, s):
        if self.talk:
            os.system(COMMANDS.SAY % ("Killing active window",))
        os.system(COMMANDS.KILL_ACTIVE_WINDOW)

    def shutdown(self, s):
        if self.talk:
            os.system(COMMANDS.SAY % ("Shutting down",))
        os.system(COMMANDS.SHUTDOWN)
        sys.exit()

    def open_file_browser(self, s):
        if self.talk:
            os.system(COMMANDS.SAY % ("Opening file browser",))
        os.system(COMMANDS.OPEN_FILE_BROWSER)

    def volume(self, s):
        if self.volume_controller == None:
            intersect = lambda l1, l2 : [ i for i in l1 if i in l2 ]
            t = (0, "")
            if "mute" in s:
                t = (0, "")
            elif len(intersect(["higher","louder","increase","up"], s.split(" "))) > 0:
                t = (5, "+")
            elif len(intersect(["lower","softer","quieter","decrease","down"],s.split(" "))) > 0:
                t = (5, "-")
            os.system(COMMANDS.VOLUME_CONTROL % t)
        else:
            volume_controller.adjust(s)

    def lock(self, s):
        os.system(COMMANDS.LOCK)

    def open_web_browser(self, s):
        command = s.split(" dot ")
        site = command[0].split(" ")[-1]
        top_level_domain = command[-1]
        if top_level_domain is not None or not top_level_domain:
            top_level_domain = "com"
        second_level_domain = site + "." + top_level_domain
        os.system(COMMANDS.OPEN_WEB_BROWSER % (second_level_domain,))

    def google_search(self, s):
        if (s.count("google") >= 1):
            s = s.replace("google", "", 1)
        if (s.count("search") >= 1):
            s = s.replace("search", "", 1)
        if (s.count("please") >= 1):
            s = s.replace("please", "", 1)
        if (s.count("for") >= 1):
            s = s.replace("for", "", 1)
        s = s.lstrip(' ').replace("'", "\\'").replace("\"", "\\\"")
        site = CommandActuator.GOOGLE_QUERY_URL % (s.replace(" ", "+"),)
        os.system(COMMANDS.OPEN_WEB_BROWSER % (site,))

class DummyActuator:
    def __init__(self, talk=True):
        self.command_mapping = {
            "EXIT_ALICE.model" : sys.exit,
            "KILL_ACTIVE_WINDOW.model" : self.no_op,
            "SHUTDOWN_COMPUTER.model" : self.no_op,
            "VOLUME_CONTROL.model" : self.no_op,
            "LOCK_COMPUTER.model" : self.no_op
        }

    def no_op(self, s):
        pass

class VolumeController:

    def __init__(self, volume_ordinal_scale_model):
        self.volume_ordinal_scale_model = volume_ordinal_scale_model

    def adjust(self, s):
        rating = volume_ordinal_scale_model.rate(s)
        if rating == 0:
            t = (0, "")
        elif rating == 1:
            t = (5, "-")
        elif rating == 2:
            t = (5, "+")
        os.system(COMMANDS.VOLUME_CONTROL % t)

class SpotifyController:

    def __init__(self, spotify_ordinal_scale_model):
        self.model = spotify_ordinal_scale_model
    
    def perform_action(self, sentence):
        myid = self.model.rate(sentence)

        if (myid == 0):
            os.system(COMMANDS.SPOTIFY_PLAY_PAUSE)
        # elif (myid == 1):

        # elif (myid == 2):

        # elif (myid == 3):
            

