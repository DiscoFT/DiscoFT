import sys, json, os
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from nltk.tree import Tree
from ui_main import Ui_Dialog
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pandas as pd 
from datetime import datetime
from matplotlib import pyplot as plt
import collections
import re
from wordcloud import WordCloud
import ntpath
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

class MyDialog(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowTitle("DiscoFT - Conversation Analyser")

        self.setFixedSize(610, 270)

        self.lbl_progress.setText("Please open chat")

        self.btn_openChat.clicked.connect(self.slot_openChat)
        self.btn_openMultiple.clicked.connect(self.slot_openMultiple)
        self.btn_createReport.clicked.connect(self.slot_createReport)

        self.checboxLists = []
        self.checboxLists.append(self.chb_topicModels)
        self.checboxLists.append(self.chb_proNames)
        self.checboxLists.append(self.chb_timeframe)
        self.checboxLists.append(self.chb_timestampGraph)
        self.checboxLists.append(self.chb_top20Words)
        self.checboxLists.append(self.chb_wordMap)


        self.resultPath = "./Result"
        if not os.path.exists(self.resultPath):
            os.mkdir(self.resultPath)

        self.initial()
        
    def initial(self):
        self.files = []
        self.words = []
        self.wrapper_profileNames = ''
        self.wrapper_timeframe = ''
        self.wrapper_timestampGraph = ''
        self.wrapper_topicModels = ''
        self.wrapper_wordMap = ''
        self.wrapper_top20Words = ''
        self.btn_createReport.setEnabled(False)
        self.btn_createReport.show()

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileNames, _ = QFileDialog.getOpenFileName(self,"Open Chat File", "","CSV Files (*.csv)", options=options)
        if fileNames:
            self.files = [fileNames]
    
    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileNames, _ = QFileDialog.getOpenFileNames(self,"Open Chat Files", "","CSV Files (*.csv)", options=options)
        if fileNames:
            self.files = fileNames

    def slot_openChat(self):
        self.openFileNameDialog()
        if len(self.files) == 0:
            return
        self.lbl_progress.setText(str(len(self.files)) + " Chat loaded")
        self.btn_createReport.setEnabled(True)

    def slot_openMultiple(self):
        self.openFileNamesDialog()
        if len(self.files) == 0:
            return
        self.lbl_progress.setText(str(len(self.files)) + " Chat loaded")
        self.btn_createReport.setEnabled(True)

    def slot_createReport(self):
        flag = False
        for iter in self.checboxLists:
            if iter.isChecked() == True:
                flag = True
                break

        if flag == False:
            self.lbl_progress.setText("Please check options")
            return

        self.btn_createReport.hide()

        for file in self.files:
            self.outputPath = self.resultPath + "/" + ntpath.basename(file)[0:-4]
            if not os.path.exists(self.outputPath):
                os.mkdir(self.outputPath)
            if not os.path.exists(self.outputPath + '/img'):
                os.mkdir(self.outputPath + '/img')
            self.pos = 0

            filename = self.outputPath + '/index.html'
            f = open(filename,'w')
            wrapper = """<html>
            <head>
            <title>Chat Log Analysis</title>
            <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
            </head>
            <body>
            <div>%s</div>
            <div>%s</div>
            <div>%s</div>
            <div>%s</div>
            <div>%s</div>
            <div>%s</div>
            </body>
            </html>"""

            self.preProcess(file)
            if self.chb_proNames.isChecked() == True:
                self.slot_profileNames()

            if self.chb_timeframe.isChecked() == True:
                self.slot_conversationTimeframe()

            if self.chb_timestampGraph.isChecked() == True:
                self.slot_timestampGraph()

            if self.chb_top20Words.isChecked() == True:
                self.slot_top20Words()
            if self.chb_wordMap.isChecked() == True:
                self.slot_wordMap()
            if self.chb_topicModels.isChecked() == True:
                self.slot_topicModels()

            whole = wrapper % (self.wrapper_profileNames, self.wrapper_timeframe, self.wrapper_timestampGraph, self.wrapper_top20Words, self.wrapper_wordMap, self.wrapper_topicModels)
            f.write(whole)
            f.close()
            
        self.lbl_progress.setText("Finished...")
        self.initial()

    def preProcess(self, file):
        self.data = pd.read_csv(file) 
        self.stop_words = set(stopwords.words("english"))
        for iter in self.data.Content:
            words_in_quote = re.findall(r'\w+', str(iter))
            filtered_list = [word for word in words_in_quote if word.casefold() not in self.stop_words and not word.isdigit()] 
            self.words += filtered_list

    def slot_profileNames(self):
        profileNames = []

        self.pos += 1
        self.wrapper_profileNames = f"""
            <h3>{self.pos}) Profile Names in Conversation Data</h3>"""
        for profileName in profileNames:
            self.wrapper_profileNames += f"""
                <p class="pl-5">{profileName}</p>"""

    def slot_conversationTimeframe(self):
        timeframe = self.data.Date.iloc[0] + " ~ " + self.data.Date.iloc[-1]

        self.pos += 1
        self.wrapper_timeframe = f"""
            <h3>{self.pos}) Conversation Timeframe</h3>
            <p class="pl-5"><b>{timeframe}</p>"""

    def slot_timestampGraph(self):
        self.pos += 1
        self.wrapper_timestampGraph = f"""
            <h3>{self.pos}) Activity Graph of Timestamps in Conversation</h3>
            <p class="pl-5">Loading</p>"""
    
    def slot_top20Words(self):
        Counter = collections.Counter(self.words)
        most_occur = Counter.most_common(20)

        self.pos += 1
        self.wrapper_top20Words = f"""
            <h3>{self.pos}) Top 20 Used Words</h3>
            <div class="pl-5 pr-5">
                <table class="table table-success table-hover">
                    <thead>
                    <tr>
                        <th scope="col">Rank</th>
                        <th scope="col">Word</th>
                    </tr>
                    </thead>
                    <tbody>"""
        for i in range(20):
            self.wrapper_top20Words += f"""
                    <tr>
                        <th scope="row">{i + 1}</th>
                        <td>{most_occur[i][0]}</td>
                    </tr>"""
        self.wrapper_top20Words += """
                    </tbody>
                </table>
            </div>"""

    def slot_wordMap(self):
        comment_words = ''
        for i in range(len(self.words)):
            self.words[i] = self.words[i].lower()
        
        comment_words += " ".join(self.words)+" "
        
        wordcloud = WordCloud(width = 800, height = 800,
                        background_color ='white',
                        stopwords = self.stop_words,
                        min_font_size = 10).generate(comment_words)
        
        plt.figure(figsize = (8, 8), facecolor = None)
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.tight_layout(pad = 0)
        plt.savefig(self.outputPath + '/img/wordMap.png')
        
        self.pos += 1
        self.wrapper_wordMap = f"""
            <h3>{self.pos}) WordMap</h3>
            <p class="pl-5"><img src='./img/wordMap.png'></p>"""

    def slot_topicModels(self):
        count_vect = CountVectorizer(max_df=0.8, min_df=2, stop_words='english')
        doc_term_matrix = count_vect.fit_transform(self.data.Content.values.astype('U'))
        LDA = LatentDirichletAllocation(n_components=6, random_state=42)
        LDA.fit(doc_term_matrix)
        topics = []
        for topic in LDA.components_:
            top_topic_words  = [count_vect.get_feature_names()[i] for i in topic.argsort()[-3:]]
            topics.append(", ".join(top_topic_words[::-1]))
    
        self.pos += 1
        self.wrapper_topicModels = f"""
            <h3>{self.pos}) Identified Topic Models and Themes</h3>
            <div class="pl-5 pr-5">
                <table class="table table-success table-hover">
                    <thead>
                    <tr>
                        <th scope="col">No</th>
                        <th scope="col">Topic Words</th>
                    </tr>
                    </thead>
                    <tbody>"""
        for i in range(6):
            self.wrapper_topicModels += f"""
                    <tr>
                        <th scope="row">{i + 1}</th>
                        <td>{topics[i]}</td>
                    </tr>"""
        self.wrapper_topicModels += """
                    </tbody>
                </table>
            </div>"""

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyDialog()
    window.show()
    sys.exit(app.exec_())