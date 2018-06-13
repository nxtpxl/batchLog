

import os
import sys
import PyQt4
from PyQt4 import QtGui, QtCore, uic


# Your UI filename
_UI = 'C:/Users/nitin.singh/Dropbox/MAYA_2018_python_code/Dragon_001.ui'


class batcher_batch_log(QWidget):
    def __init__(self):

        QWidget.__init__(self)

        self.path = []
        self.notesFileToRead = []
        self.project_Dir = []
        # windows path

        if platform.system()=='Windows':
            path = "C:/Users/nitin.singh/Dropbox/MAYA_2018_python_code/batcher_job_log.ui"
            self.notesFileToRead.append('L:/NXTPXLENT/pipe___RND/library/library_JSON_tags/batcher__job_log.txt')
            self.path.append(path)


        if platform.system()=='Darwin':
            path = "/Users/nitin/Dropbox/MAYA_2018_python_code/batcher_job_log.ui"
            self.path.append(path)
        p = (self.path)[0]
        self.ui = QUiLoader().load(p)
        self.notesFileToRead = self.notesFileToRead[0]

        self.ui.totalNum_lineEdit.setStyleSheet("* { background-color: rgba(0, 0, 0, 0); }");
        self.ui.totalNum_lineEdit.setEnabled(False);
        self.ui.assets_selected_radioButton.setChecked(True)
        self.ui.groupBox_2.setStyleSheet("""QGroupBox { border: 1.2px solid grey;}""")
        self.ui.assetsList_tableWidget.resizeColumnsToContents()
        self.ui.assetsList_tableWidget.resizeRowsToContents()
        self.ui.assetsList_tableWidget.horizontalHeader().setStretchLastSection(True)
        self.ui.assetsList_tableWidget.setSelectionBehavior(QTableView.SelectRows)
        self.ui.assetsList_tableWidget.verticalHeader().resizeSections(QHeaderView.ResizeToContents);
        self.ui.reload_log_pushButton.clicked.connect(self.Updating_batcher_LOG_JsonFile)
        self.ui.assetsList_tableWidget.setCornerButtonEnabled (True)
        self.ui.assetsList_tableWidget.resizeColumnsToContents()
        self.ui.assetsList_job_tableWidget.setCornerButtonEnabled (True)
        self.ui.assetsList_job_tableWidget.resizeColumnsToContents()
        self.ui.assetsList_job_tableWidget.setSelectionBehavior(QTableView.SelectRows)
        self.ui.assetsList_job_tableWidget.resizeRowsToContents()
        self.ui.assetsList_job_tableWidget.horizontalHeader().setStretchLastSection(True)

        self.Updating_batcher_LOG_JsonFile()

        self.ui.batch_start_pushButton.clicked.connect(self.startBatchProcess)
        self.ui.Tags_comboBox.currentIndexChanged.connect(self.updateSelectedTagList)
        self.ui.assetsList_tableWidget.clicked.connect(self.getselectedJobDetails)

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
        print (notesFile)
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
                    #print a

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
                    jobpath = logEntry[9].split('______')
                    #print jobpath[0], jobpath[1]

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
                TagsForList = list(set(TagsForList))
                self.getAllTagsForComboBox(TagsForList)
        else:
                print ('')

    ##########################################################################################
    # writing JSON file in the JOB folder

    def updateSelectedTagList(self):
        tagName = str(self.ui.Tags_comboBox.currentText())
        print tagName
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
                    #print (job)
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
                    jobpath = logEntry[9].split('______')
                    #print jobpath[0], jobpath[1]
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

        else:
                print ('')

    def readingJOB_log_file(self, jobFilePath):
        notesFile = jobFilePath
        notesFileChk = os.path.exists(notesFile)
        TagsForList = []
        if notesFileChk == True:
            with open(notesFile, 'r') as file:
                jsondata = json.load(file)
                #print (jsondata)

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
            self.readingJOB_log_file(jobPath)


    def getAllTagsForComboBox(self, allTagsToLoad):
        self.ui.Tags_comboBox.clear()
        listToAdd = ['All']
        self.ui.Tags_comboBox.addItems(listToAdd)
        self.ui.Tags_comboBox.addItems(allTagsToLoad)


    def getStartEndTime(self):
        startTime =(self.ui.start_time_timeEdit.time().toString())
        endTime = (self.ui.end_time_timeEdit.time().toString())
        return startTime, endTime

    def selectedJobs(self):
        rows=[]
        for idx in self.ui.assetsList_tableWidget.selectionModel().selectedRows():
            rows.append(idx.row())

        rows = list(set(rows))
        for job in rows:
            print ('____________________________________________________')
            jobClass =  self.ui.assetsList_tableWidget.item(job,0).text()
            jobName =   self.ui.assetsList_tableWidget.item(job,1).text()
            # joing jobName and jobClass to select job details
            jobID = (jobClass + '_'+jobName)
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
                                print 'TT'
                            if jobClass == 'Asset_LODs':
                                print 'LODS'
                        else:
                            pass

    def startBatchProcess(self):
        self.getStartEndTime()
        self.selectedJobs()

def run():
    global batcher_batch_log_UI
    batcher_batch_log_UI = batcher_batch_log()
    batcher_batch_log_UI.ui.show()
run()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
