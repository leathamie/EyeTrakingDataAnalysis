# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 13:40:36 2019

@author: Lea
"""
import re
import os


def getFilesNames():
    files = []
    folderPath = "DATA/"
    for filename in os.listdir(folderPath):
        """
            Browe all the cha files, for each files in the folder check 
            if it's a csv file 
        """
        match = re.match(".*\.csv",filename)
        if match:
            files.append(folderPath + filename)
            
    return files

def extractFileContent(filename):
    """
        take a cha file path and return a str with cha content
    """
    print("dans le extract content")
    fileContent = ""
    file = open(filename, "r")
    for line in file : 
        fileContent = fileContent + line
    return fileContent

def contentToArray(fileContent):
    print("dans le content to array")
    tab = []
    cols = fileContent.split('\n')
    for col in cols: 
        line = col.split(',')
        tab.append(line)
    return (tab)

    
#def getImgZones(filecontent): 
    
    
files = getFilesNames()
print (files)
print ("Avant le for")
tab = []
for file in files:
    print (file)
    content = extractFileContent(file)
    print ("ap content")
    tabFile = contentToArray(content)
    print ("ap array")
    tab.append(tabFile)

print ()

    
