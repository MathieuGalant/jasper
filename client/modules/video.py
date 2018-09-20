# -*- coding: utf-8-*-
import re
import logging
import difflib
import mpd
from client.mic import Mic
import os


from xml.dom import minidom

import xml.etree.ElementTree as ET
from threading import Thread, Lock


# Standard module stuff
WORDS = ["VIDEO", "PLAY", "SHOW", "START" ]

commandFile="/home/debian/beamy/XML/command.xml"

commandVideoFile="/home/debian/beamy/XML/commandVideo.xml"

videoFile="/home/debian/beamy/media/video/"



def handle(text, mic, profile):
    """
    Responds to user-input, typically speech text, by telling a joke.

    Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone
                   number)
    """
    

 

    mic.say("Starting video mode")
    handleForever(mic)
    mic.say("Exiting video mode")

    return


def isValid(text):
    """
        Returns True if the input is related to jokes/humor.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return any(word in text.upper() for word in WORDS)
               
               
def loadMusicNames(videoFile):
        
        videoNames=[]
        videoExtention=[]
        for video in os.listdir(videoFile):
            sep = '.'
            rest = video.split(sep, 1)[0]
            extention=video.split(sep, 1)[1]
            videoNames.append(rest)
            videoExtention.append(extention)
        return videoNames, videoExtention
    
    
def delegateInput(mic,input):

        command = input.upper()


        if "CONTINUE" in command:
            mic.say("Continue video")
            readCommandVideoXML("continue")
            return
        elif "PAUSE" in command:
            mic.say("Pausing video")
            readCommandVideoXML("pause")
            return
        elif any(ext in command for ext in ["LOUDER", "HIGHER"]):
            mic.say("Louder")
            readCommandVideoXML("volume up")
            return
        elif any(ext in command for ext in ["SOFTER", "LOWER"]):
            mic.say("Softer")
            readCommandVideoXML("volume down")
            return
        else:
            mic.say("Can you repeat")
            return
        

 

def handleForever(mic):
    
        videoNames,videoExtention=loadMusicNames(videoFile)
        mic.say("What video do you want to play")

        while True:    
            videoName = mic.activeListen()
            print(videoName)
            
            if any(s in videoName for s in videoNames):
                for i in [i for i,x in enumerate(videoNames) if (x == videoName)]:
                    completeName=videoName+"."+videoExtention[i]
                    print(completeName)
                    readCommandXML(completeName)
                    mic.say("Starting %s video" % videoName)
                
                while True :
                    command = mic.activeListen()
                    if any(ext in command for ext in ["quit", "stop"]):
                        mic.say("Closing video")
                        readCommandVideoXML("quit")
                        return
                    else:
                        delegateInput(mic,command)


            elif any(ext in videoName for ext in ["quit", "stop"]):
                mic.say("Closing video")
                readCommandVideoXML("quit")
                return
            else:
                mic.say("Can you repeat")
 



 


      



def readCommandVideoXML(commandVideo):
    
        tree = ET.parse(commandVideoFile)  
        root = tree.getroot()

        # changing a field text
        for elem in root.iter('etat'):  
            elem.text = commandVideo
            
 

        tree.write(commandVideoFile)
        
        

def readCommandXML(videoName):
    
        tree = ET.parse(commandFile)  
        root = tree.getroot()

        # changing a field text
        for elem in root.iter('etat'):  
            elem.text = "play video"
        for elem in root.iter('name'):  
            elem.text = videoName 
 

        tree.write(commandFile)



