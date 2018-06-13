
import os
import sys
import re
import glob
import json
import copy
import time
import datetime
import subprocess
import math
from glob import glob, iglob
from functools import partial
import PyQt4
from PyQt4.QtGui import QTableWidgetItem
from PyQt4.QtGui import QTableView
from PyQt4 import QtGui,QtCore

import NXTPXL
import NXTLOG
from PROJECTLOG import *
from NXTPXL import batchLog_UI_path as BLUI 
from NXTPXL import projects_dir
from NXTPXL import notesLog
from NXTPXL import filePathFixed
from NXTPXL import userLogs


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        path = (BLUI +'/deadPool_001.ui')
        self.ui = uic.loadUi(path, self)
        self.projectDir = projects_dir
        self.notesFileToRead = notesLog
        self.projectLoad()

        # UI functionality and option setup
        self.ui.assets_selected_radioButton.setChecked(True)
        stylesheet = "::section{Background-color:rgb(50,50,50)}"
        self.ui.assetsList_tableWidget.horizontalHeader().setStyleSheet(stylesheet)
        self.ui.assetsList_tableWidget.verticalHeader().setStyleSheet(stylesheet)
        self.ui.assetsList_job_tableWidget.horizontalHeader().setStyleSheet(stylesheet)
        self.ui.assetsList_job_tableWidget.verticalHeader().setStyleSheet(stylesheet)
        self.ui.assetsList_tableWidget.resizeColumnsToContents()
        self.ui.assetsList_tableWidget.resizeRowsToContents()
        self.ui.assetsList_tableWidget.horizontalHeader().setStretchLastSection(True)
        self.ui.assetsList_job_tableWidget.horizontalHeader().setStretchLastSection(True)
        self.ui.assetsList_tableWidget.setCornerButtonEnabled (True)
        self.ui.assetsList_tableWidget.resizeColumnsToContents()
        self.ui.assetsList_tableWidget.setColumnWidth(0,150)
        self.ui.assetsList_tableWidget.setColumnWidth(1,250)
        self.ui.assetsList_tableWidget.setColumnWidth(2,100)
        self.ui.assetsList_tableWidget.setColumnWidth(3,200)
        self.ui.assetsList_tableWidget.setColumnWidth(4,100)
        self.ui.assetsList_tableWidget.setColumnWidth(5,80)
        self.ui.assetsList_tableWidget.setColumnWidth(6,180)
        self.ui.assetsList_tableWidget.setColumnWidth(7,150)
        self.ui.assetsList_tableWidget.setSelectionBehavior(QTableView.SelectRows)
        self.ui.assetsList_job_tableWidget.setColumnWidth(0,160)
        self.ui.assetsList_job_tableWidget.setColumnWidth(1,100)
        self.ui.assetsList_job_tableWidget.setColumnWidth(2,100)
        self.ui.assetsList_job_tableWidget.setColumnWidth(3,100)
        self.Updating_batcher_LOG_JsonFile()
        self.ui.batch_start_pushButton.clicked.connect(self.startBatchProcess)
        self.ui.Tags_comboBox.currentIndexChanged.connect(self.updateSelectedTagList)
        self.ui.assetsList_tableWidget.clicked.connect(self.getselectedJobDetails)

    def projectLoad(self):
        print ('loading the projects')
        existingProjects = sorted(os.listdir(self.projectDir))
    '''JSON entries'''
    def filePathFixed(self, path):
        if platform.system()=='Windows':
            filePath = path
            #print (filePath)
            separator = os.path.normpath("/")
            newPath = re.sub(re.escape(separator), "/", filePath)
            return newPath
            #print (path)
        else:
            return filePath


    def Updating_batcher_LOG_JsonFile(self):
        notesDictFromDisk = {'jobs':[]}
        notesFile = self.notesFileToRead
        notesFileChk = os.path.exists(notesFile)
        TagsForList = []
        if notesFileChk == True:

            # reading json file whixh is selcted by the user
            with open(notesFile, 'r') as file:
                jsondata = json.load(file)
                number = str(len(jsondata['jobs'])).decode("utf-8")
                self.ui.totalNum_lineEdit.clear()
                self.ui.totalNum_lineEdit.insert(number)
                #print (jsondata)
                self.ui.assetsList_tableWidget.clearContents()
                self.ui.assetsList_tableWidget.setRowCount(len(jsondata['jobs']))

                for i, a in enumerate(jsondata['jobs'], 0):
                    logEntry =  map(str, a)
                    #notesDictFromDisk['jobs'].append(map(str, a))
                    jobClass = logEntry[1]
                    TagsForList.append(jobClass)
                    jobName = logEntry[2]
                    Frame_Range = logEntry[3]
                    submitTime = logEntry[4]
                    size = logEntry[5]
                    status = logEntry[6]
                    outPut_Res = logEntry[7]
                    outPut_Format = logEntry[8]
                    jobpath = logEntry[9]
                    self.updateTableWidgetContent(self, jobClass, jobName, Frame_Range, submitTime, size, status, outPut_Res, outPut_Format, jobpath)
                TagsForList = list(set(TagsForList))
                self.getAllTagsForComboBox(TagsForList)
        else:
                print ('')

    ##########################################################################################
    # writing JSON file in the JOB folder

    def updateSelectedTagList(self):
        tagName = str(self.ui.Tags_comboBox.currentText())
        print (tagName)
        notesFile = self.notesFileToRead
        #print (notesFile)
        notesFileChk = os.path.exists(notesFile)
        TagsForList = []
        if notesFileChk == True:
            with open(notesFile, 'r') as file:
                jsondata = json.load(file)
                number = str(len(jsondata['jobs'])).decode("utf-8")
                self.ui.totalNum_lineEdit.clear()
                self.ui.totalNum_lineEdit.insert(number)
                #print (jsondata)
                self.ui.assetsList_job_tableWidget.clearContents()
                self.ui.assetsList_job_tableWidget.setRowCount(0)
                self.ui.assetsList_tableWidget.clearContents()
                self.ui.assetsList_tableWidget.setRowCount(len(jsondata['jobs']))
                selectedTagJobs = []
                for i, a in enumerate(jsondata['jobs'], 0):
                    print (a)
                    print ('v')
                    logEntry =  map(str, a)
                    if tagName == 'All':
                        selectedTagJobs.append (logEntry)
                    else:
                        jobClass = logEntry[1]
                        if jobClass == tagName:
                            selectedTagJobs.append (logEntry)
                        else:
                            pass
                number = str(len(selectedTagJobs))
                self.ui.totalNum_lineEdit.clear()
                self.ui.totalNum_lineEdit.insert(number)
                #print (jsondata)
                self.ui.assetsList_tableWidget.clearContents()
                self.ui.assetsList_tableWidget.setRowCount(len(selectedTagJobs))
                for i, job in enumerate(selectedTagJobs, 0):
                    logEntry =  map(str, job)
                    jobClass = logEntry[1]
                    TagsForList.append(jobClass)
                    jobName = logEntry[2]
                    Frame_Range = logEntry[3]
                    submitTime = logEntry[4]
                    size = logEntry[5]
                    status = logEntry[6]
                    outPut_Res = logEntry[7]
                    outPut_Format = logEntry[8]
                    jobpath = logEntry[9]
                    self.updateTableWidgetContent(self, jobClass, jobName, Frame_Range, submitTime, size, status, outPut_Res, outPut_Format, jobpath)
        else:
                print ('')
    def updateTableWidgetContent(self, jobClass, jobName, Frame_Range, submitTime, size, status, outPut_Res, outPut_Format, jobpath):
        jobspath = jobpath.split('______')
        self.ui.assetsList_tableWidget.setRowHeight (i, 40)
        self.ui.assetsList_tableWidget.setItem(i, 0, QTableWidgetItem(jobClass))
        self.ui.assetsList_tableWidget.setItem(i, 1, QTableWidgetItem(jobName))
        self.ui.assetsList_tableWidget.setItem(i, 2, QTableWidgetItem(Frame_Range))
        self.ui.assetsList_tableWidget.setItem(i, 3, QTableWidgetItem(submitTime))
        self.ui.assetsList_tableWidget.setItem(i, 4, QTableWidgetItem(size))
        self.ui.assetsList_tableWidget.setItem(i, 5, QTableWidgetItem(status))
        self.ui.assetsList_tableWidget.setItem(i, 6, QTableWidgetItem(outPut_Res))
        self.ui.assetsList_tableWidget.setItem(i, 7, QTableWidgetItem(outPut_Format))
        self.ui.assetsList_tableWidget.setItem(i, 8, QTableWidgetItem(jobpath[0]+"\n"+jobpath[1]))



    def readingJOB_log_file(self, jobFilePath):
        print ('updating job colums')
        notesFile = jobFilePath
        notesFileChk = os.path.exists(notesFile)
        TagsForList = []
        if notesFileChk == True:
            with open(notesFile, 'r') as file:
                jsondata = json.load(file)
                self.ui.assetsList_job_tableWidget.clearContents()
                self.ui.assetsList_job_tableWidget.setRowCount(len(jsondata['JOB_details']))
                for i, a in enumerate(jsondata['JOB_details'], 0):
                    logEntry =  map(str, a)
                    jobID =  logEntry[0]
                    jobStart = logEntry[1]
                    jobEnd = logEntry[2]
                    jobMem = logEntry[3]
                    jobDuration = logEntry[3]
                    self.ui.assetsList_tableWidget.setRowHeight (i, 40)
                    self.ui.assetsList_job_tableWidget.setItem(i, 0, QTableWidgetItem(jobID))
                    self.ui.assetsList_job_tableWidget.setItem(i, 1, QTableWidgetItem(jobStart))
                    self.ui.assetsList_job_tableWidget.setItem(i, 2, QTableWidgetItem(jobEnd))
                    self.ui.assetsList_job_tableWidget.setItem(i, 3, QTableWidgetItem(jobMem))
                    self.ui.assetsList_job_tableWidget.setItem(i, 4, QTableWidgetItem(jobDuration))
        else:
                print ('')

    def getselectedJobDetails(self):
        indexes = self.ui.assetsList_tableWidget.selectionModel().selectedRows()
        rows=[]
        for index in sorted(indexes):
            rows.append(index.row())
        for job in rows:
            jobPath =  self.ui.assetsList_tableWidget.item(job,8).text()
            jobPath = self.filePathFixed(os.path.join(os.path.dirname(jobPath.split('\n')[0]), 'jobLog.txt'))
            print (jobPath)
            self.readingJOB_log_file(jobPath)

    def getAllTagsForComboBox(self, allTagsToLoad):
        self.ui.Tags_comboBox.clear()
        listToAdd = ['All']
        self.ui.Tags_comboBox.addItems(listToAdd)
        self.ui.Tags_comboBox.addItems(allTagsToLoad)

    def getStartEndTime(self):
        #startTime =self.ui.start_time_timeEdit.currentTime()
        startTime =(self.ui.start_time_timeEdit.time().toString())
        endTime = (self.ui.end_time_timeEdit.time().toString())
        return (startTime, endTime)

    def selectedJobs(self):
        rows=[]
        for idx in self.ui.assetsList_tableWidget.selectionModel().selectedRows():
            rows.append(idx.row())

        rows = list(set(rows))
        for job in rows:
            jobClass =  self.ui.assetsList_tableWidget.item(job,0).text()
            jobName =   self.ui.assetsList_tableWidget.item(job,1).text()
            print (('jobClass :' + jobClass) +
                 ' \n' + ('jobName  : '+jobName))
            # joing jobName and jobClass to select job details
            jobID = (jobClass + '_'+jobName)
            print (jobID)
            # getting all the enteries of selected job from JSON file
            notesFile = self.notesFileToRead
            notesFileChk = os.path.exists(notesFile)
            if notesFileChk == True:
                with open(notesFile, 'r') as file:
                    jsondata = json.load(file)
                    for i, a in enumerate(jsondata['jobs'], 0):
                        logEntry =  map(str, a)
                        if jobID == logEntry[0]:
                            #print logEntry
                            if jobClass == 'Icon_Render':
                                self.render_icon(logEntry)
                            if jobClass == 'Asset_Turntable':
                                print ('TT')
                            if jobClass == 'Asset_LODs':
                                print ('LODS')
                        else:
                            pass

    def render_icon(self, selectedJob_log):
        # rendering ICON for selected Asset
        jobLog = selectedJob_log
        assetName = selectedJob_log[2]
        IconFormat = selectedJob_log[7]
        iconResolution = selectedJob_log[8].split(' x ')
        iconWidth = iconResolution[0]
        iconHeight = iconResolution[1]
        IconFIlePaths = selectedJob_log[9].split('______')
        mayaFIlePath = IconFIlePaths[0]
        iconSavePath = IconFIlePaths[1]
        print ('....................................................')
        print (assetName)
        print (IconFormat)
        print (iconWidth)
        print (iconHeight)
        print (mayaFIlePath)
        print (iconSavePath)
        print ('....................................................')
        # connect to Maya stndalone from here

    def startBatchProcess(self):
        self.getStartEndTime()
        self.selectedJobs()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

    
    
    
    
