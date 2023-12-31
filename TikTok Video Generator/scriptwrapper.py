import subprocess
import os
import math
import datetime
import pickle
import random
current_path = os.path.dirname(os.path.realpath(__file__))



def createTwitchVideoFromJSON(videojson):
    #print(videojson)
    final_clips = []

    clips = videojson["clips"]
    name = videojson["name"]


    for clip in clips:
        id = clip["id"]
        audio = clip["audio"]
        used = clip["keep"]

        isUpload = clip["isUpload"]
        isIntro = clip["isIntro"]
        isInterval = clip["isInterval"]
        uploadMp4 = clip["mp4"]
        uploadDuration = clip["duration"]
        author_name = clip["author_name"]



        wrapper = ClipWrapper(id, author_name)
        wrapper.mp4 = uploadMp4
        wrapper.vid_duration = uploadDuration
        wrapper.isUpload = isUpload
        wrapper.isInterval = isInterval
        wrapper.isIntro = isIntro
        wrapper.audio = audio
        wrapper.isUsed = used

        final_clips.append(wrapper)

    video = TikTokVideo(final_clips, name)
    #print(final_clips)
    return video


def saveTwitchVideo(folderName, video):
    print(f'Saved to Temp/%s/vid.data' % folderName)
    with open(f'Temp/%s/vid.data' % folderName, 'wb') as pickle_file:
        pickle.dump(video, pickle_file)



class TikTokVideo():
    def __init__(self, clips, name):
        self.clips = clips
        self.name = name



class ClipWrapper():
    def __init__(self, id, author_name):
        self.id = id
        self.author_name = author_name
        self.audio = 1
        self.isUsed = False
        self.isInterval = False
        self.isUpload = False
        self.mp4 = "AndreasGreenLive-702952046"
        self.isIntro = False
        # result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
        #              "format=duration", "-of",
        #              "default=noprint_wrappers=1:nokey=1", f"{current_path}\VideoFiles\AndreasGreenLive-702952046.mp4"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self.vid_duration = None

        #Getting duration of video clips to trim a percentage of the beginning off




class ScriptWrapper():
    def __init__(self, script):
        self.rawScript = script
        self.scriptMap = []
        self.setupScriptMap()


    def addClipAtStart(self, clip):
        self.rawScript = [clip] + self.rawScript
        self.scriptMap = [True] + self.scriptMap


    def addScriptWrapper(self, scriptwrapper):
        self.rawScript = self.rawScript + scriptwrapper.rawScript
        self.scriptMap = self.scriptMap + scriptwrapper.scriptMap


    def moveDown(self, i):
        if i > 0:
            copy1 = self.scriptMap[i-1]
            copy2 = self.rawScript[i-1]

            self.scriptMap[i-1] = self.scriptMap[i]
            self.rawScript[i-1] = self.rawScript[i]

            self.scriptMap[i] = copy1
            self.rawScript[i] = copy2
        else:
            print("already at bottom!")

    def moveUp(self, i):
        if i < len(self.scriptMap) - 1:
            copy1 = self.scriptMap[i+1]
            copy2 = self.rawScript[i+1]

            self.scriptMap[i+1] = self.scriptMap[i]
            self.rawScript[i+1] = self.rawScript[i]

            self.scriptMap[i] = copy1
            self.rawScript[i] = copy2
        else:
            print("already at top!")

    def setupScriptMap(self):
        for mainComment in self.rawScript:
            line = False
            self.scriptMap.append(line)


    def keep(self, mainCommentIndex):
        self.scriptMap[mainCommentIndex] = True

    def skip(self, mainCommentIndex):
        self.scriptMap[mainCommentIndex] = False

    def setCommentStart(self, x, start):
        self.rawScript[x].start_cut = start

    def setCommentEnd(self, x, end):
        self.rawScript[x].end_cut = end

    def getCommentData(self, x, y):
        return self.rawScript[x][y]

    def getCommentAmount(self):
        return len(self.scriptMap)

    def getEditedCommentThreadsAmount(self):
        return len([commentThread for commentThread in self.scriptMap if commentThread[0] is True])

    def getEditedCommentAmount(self):
        commentThreads = ([commentThread for commentThread in self.scriptMap])
        count = 0
        for commentThread in commentThreads:
            for comment in commentThread:
                if comment is True:
                    count += 1
        return count

    def getEditedWordCount(self):
        commentThreads = ([commentThread for commentThread in self.scriptMap])
        word_count = 0
        for x, commentThread in enumerate(commentThreads):
            for y, comment in enumerate(commentThread):
                if comment is True:
                    word_count += len(self.rawScript[x][y].text.split(" "))
        return word_count

    def getEditedCharacterCount(self):
        commentThreads = ([commentThread for commentThread in self.scriptMap])
        word_count = 0
        for x, commentThread in enumerate(commentThreads):
            for y, comment in enumerate(commentThread):
                if comment is True:
                    word_count += len(self.rawScript[x][y].text)
        return word_count


    def getCommentInformation(self, x):
        return self.rawScript[x]


    def getKeptClips(self):
        final_script = []
        for i, clip in enumerate(self.scriptMap):
            if clip:
                final_script.append(self.rawScript[i])
        return final_script

    def getEstimatedVideoTime(self):
        time = 0
        for i, comment in enumerate(self.scriptMap):
            if comment is True:
                time += round(self.rawScript[i].vid_duration - (self.rawScript[i].start_cut / 1000) - (self.rawScript[i].end_cut / 1000), 1)
        obj = datetime.timedelta(seconds=math.ceil(time))
        return  obj

