"""
BSD 3-Clause License

Copyright (c) 2021, DiscoFV
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import sys, os # Running OS functions
from PyQt5.QtWidgets import * # GUI
from PyQt5.QtGui import * # GUI
from PyQt5.QtCore import * # GUI
from ui_main import Ui_Dialog # GUI styling. File Required!
import numpy as np #Arrays
from nltk.corpus import stopwords # Stopword filtering using Natural Language Toolkit
import pandas as pd # Base Data Analysis
from datetime import datetime # Date.. Time..
from matplotlib import pyplot as plt # Graphing
import collections # Tabulation
import re # Regular Expressions
from wordcloud import WordCloud # Required for WordMap
import ntpath # Pathing (Windows)
import en_core_web_sm # Required from Spacy but not featured as a standalone module.
import gensim # Topic Modelling
import gensim.corpora as corpora # Topic Modelling
import pyLDAvis # LDA Visualisation
import pyLDAvis.gensim_models # LDA Visualisation

class WorkerThread(QThread):
    progress = pyqtSignal(str) # The message to be displayed in label

    def __init__(self, files, resultPath, checkboxLists):
        QThread.__init__(self)
        self.files = files
        self.resultPath = resultPath
        self.chb_proNames = checkboxLists[0]
        self.chb_timeframe = checkboxLists[1]
        self.chb_timestampGraph = checkboxLists[2]
        self.chb_top20Words = checkboxLists[3]
        self.chb_wordMap = checkboxLists[4]
        self.chb_topicModels = checkboxLists[5]

        self.wrapper_profileNames = ''
        self.wrapper_timeframe = ''
        self.wrapper_timestampGraph = ''
        self.wrapper_topicModels = ''
        self.wrapper_wordMap = ''
        self.wrapper_top20Words = ''

    def run(self):
        for iter, file in enumerate(self.files):
            self.words = []
            self.words_sentence = []
            self.outputPath = self.resultPath + "/" + ntpath.basename(file)[0:-4]
            if not os.path.exists(self.outputPath):
                os.mkdir(self.outputPath)
            if not os.path.exists(self.outputPath + '/img'): # For Activity graph, Topic Modelling, & WordMap
                os.mkdir(self.outputPath + '/img')
            self.pos = 0

            filename = self.outputPath + '/chatreport.html' # Can be renamed to whatever is more appropriate
            f = open(filename,'wb') # Write Permission
            # Full comments beyond here break wrapper! Below is basic layout for the report
            wrapper = """<html>
            <head>
            <title>Chat Report</title>
            <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
            <style>
                body{padding: 61px 40px 0px 40px;}
                h2 {color: #2596be;
                    margin: 35px 60px 25px 0px;
                    font-weight: 800;}
                p  {font-weight: 600;
                    font-size: 24px}
                table {font-size: large;
                    font-weight: 600;
                    max-width: 500px;}
                img {max-width:500px;}
            </style>
            </head>
            <body>
            <div class="ml-5 mr-5">%s</div>
            <div class="ml-5 mr-5">%s</div>
            <div class="ml-5 mr-5">%s</div>
            <div class="ml-5 mr-5">%s</div>
            <div class="ml-5 mr-5">%s</div>
            <div class="ml-5 mr-5">%s</div>
            </body>
            </html>"""

            self.preProcess(file)
            if self.chb_proNames.isChecked() == True: # Checking Usernames
                self.slot_profileNames()

            if self.chb_timeframe.isChecked() == True: # Checking Timeframe
                self.slot_conversationTimeframe()

            if self.chb_timestampGraph.isChecked() == True: # Checking Activity Graph
                self.slot_timestampGraph()

            if self.chb_top20Words.isChecked() == True: # Checking Top 20 Words
                self.slot_top20Words()

            if self.chb_wordMap.isChecked() == True: # Checking WordMap
                self.slot_wordMap()

            if self.chb_topicModels.isChecked() == True: # Checking Topic Modelling
                self.slot_topicModels()

            whole = wrapper % (self.wrapper_profileNames, self.wrapper_timeframe, self.wrapper_timestampGraph, self.wrapper_top20Words, self.wrapper_wordMap, self.wrapper_topicModels)
            #f.write(whole) # Compile report. Breaks if certain special characters are used
            f.write(whole.encode("utf-8")) # Compile report with utf-8 encoding fixes this
            f.close() # Ends
            self.progress.emit(f"{iter + 1} Finished...") # When done
    
    def preProcess(self, file):
        self.data = pd.read_csv(file) 
        self.stop_words = set(stopwords.words("english")) # Adjustable for different languages. Only tested English!
        for iter in self.data.Content: # Contents column of CSV
            words_in_quote = re.findall(r'\w+', str(iter))
            filtered_list = [word for word in words_in_quote if word.casefold() not in self.stop_words and not word.isdigit()] # Stop! Stopword time
            self.words += filtered_list
            self.words_sentence.append(filtered_list)

    def slot_profileNames(self): # Report - Usernames
        profileNames = np.unique(self.data.Author.to_numpy()) # Author column in CSV

        self.pos += 1
        self.wrapper_profileNames = f"""
            <h2>{self.pos}) Usernames in Conversation</h2>"""
        for profileName in profileNames:
            self.wrapper_profileNames += f"""
                <p class="pl-5">- {profileName}</p>"""

    def slot_conversationTimeframe(self): # Report - Conversation Timeframe
        timeframe = self.data.Date.iloc[0] + " ~ " + self.data.Date.iloc[-1] # Date column in CSV

        self.pos += 1
        self.wrapper_timeframe = f"""
            <h2>{self.pos}) Conversation Timeframe</h2>
            <p class="pl-5">{timeframe}</p>"""

    def slot_timestampGraph(self): # Report - Activity Graph
        fig, ax = plt.subplots(figsize=(10, 10), facecolor=(.38, .51, .51)) # Decent colours for now
        plt.locator_params(axis="x", nbins=15)
        timeline = pd.DataFrame(pd.to_datetime(self.data.Date), columns=['Date'])
        timeline['timestamp'] = [datetime.timestamp(x) for x in timeline.Date]
        ax = timeline['timestamp'].plot(kind='kde')
        x_ticks = ax.get_xticks()
        xlabels = [datetime.fromtimestamp(int(x)) for x in x_ticks]
        ax.set_xticklabels(xlabels)
        fig.autofmt_xdate()
        ax.set_facecolor('#eafff5') # Decent colours for now
        plt.tight_layout(pad=3)
        plt.savefig(self.outputPath + '/img/activityGraph.png')
        
        self.pos += 1
        self.wrapper_timestampGraph = f"""
            <h2>{self.pos}) Conversation Activity Graph</h2>
            <p class="pl-5"><img style="width:100%;" src='./img/activityGraph.png'></p>"""
    
    def slot_top20Words(self): # Report - Top 20 Words
        Counter = collections.Counter(self.words)
        most_occur = Counter.most_common(20)

        self.pos += 1
        self.wrapper_top20Words = f"""
            <h2>{self.pos}) Top 20 Used Words</h2>
            <div class="pl-5 pr-5">
                <table class="table table-hover table-striped table-sm">
                    <thead class="thead-dark">
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

    def slot_wordMap(self): # Report - WordMap
        comment_words = ''
        for i in range(len(self.words)):
            self.words[i] = self.words[i].lower()
        
        comment_words += " ".join(self.words)+" "
        
        wordcloud = WordCloud(width = 800, height = 800,
                        background_color ='white',
                        stopwords = self.stop_words,
                        min_font_size = 10).generate(comment_words)
        
        plt.figure(figsize = (10, 10), facecolor = None)
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.tight_layout(pad = 0)
        plt.savefig(self.outputPath + '/img/wordMap.png')
        
        self.pos += 1
        self.wrapper_wordMap = f"""
            <h2>{self.pos}) WordMap</h2>
            <p class="pl-5"><img style="width:100%;" src='./img/wordMap.png'></p>"""

    def slot_topicModels(self): # Report Topic Modelling
        bigram = gensim.models.Phrases(self.words_sentence, min_count=5, threshold=100)
        bigram_mod = gensim.models.phrases.Phraser(bigram)
        
        data_words_bigrams = [bigram_mod[doc] for doc in self.words_sentence]
        nlp = en_core_web_sm.load()
        # nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
        allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']
        data_lemmatized = [] # Lemmatising
        for sent in data_words_bigrams:
            doc = nlp(" ".join(sent)) 
            data_lemmatized.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
        
        id2word = corpora.Dictionary(data_lemmatized)
        texts = data_lemmatized # Sorted
        corpus = [id2word.doc2bow(text) for text in texts] # The whole body of text

        lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                           id2word=id2word,
                                           num_topics=10, # Topic numbers considered. Set small because of small data size
                                           random_state=100, # Seed for the process, should it want to be repeated
                                           update_every=1, # Updates model after every 1 chunk
                                           chunksize=100, # Number of documents considered at once
                                           passes=15, # Does 15 passes of the whole corpus
                                           alpha='auto', # Used to set specific array, left to auto here
                                           per_word_topics=True) # Picks most likely topics
                        
        topic_pairs = lda_model.show_topics(num_topics=10, num_words=3, log=False, formatted=False)
        vis = pyLDAvis.gensim_models.prepare(lda_model, corpus, id2word) # This breaks in Pycharm with Process error. Doesn't like gensim. Switched to Visual Studio
        pyLDAvis.save_html(vis, self.outputPath + '/img/topicModeling.html')
        topics = [ [y[0] for y in x[1]] for x in topic_pairs]
        str_topics = [", ".join(x) for x in topics]
        contents =''
        with open(self.outputPath + '/img/topicModeling.html') as f: # Topic modelling created
            contents = f.read()

        self.pos += 1
        self.wrapper_topicModels = f"""
            <h2>{self.pos}) Identified Topic Models</h2>
            <div class="pl-5 pr-5">
                <h3>Keywords in the 10 topics</h3>
                <table class="table table-hover table-striped table-sm">
                    <thead class="thead-dark">
                    <tr>
                        <th scope="col">No</th>
                        <th scope="col">Topic Words</th>
                    </tr>
                    </thead>
                    <tbody>"""
        for i in range(10):
            self.wrapper_topicModels += f"""
                    <tr>
                        <th scope="row">{i + 1}</th>
                        <td>{str_topics[i]}</td>
                    </tr>"""
        self.wrapper_topicModels += """
                    </tbody>
                </table>
                <br>
                <h3>Visualize the topics</h3>"""
        self.wrapper_topicModels += contents
        self.wrapper_topicModels += """
            </div>"""
        


class MyDialog(QDialog, Ui_Dialog): # GUI Dialog
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowTitle("DiscoFV") # That's me!

        self.setFixedSize(610, 270) # Changeable if too small

        self.lbl_progress.setText("Please open chat") # Select a chat file with the library program please

        self.btn_openChat.clicked.connect(self.slot_openChat) # Openchat confirmed
        self.btn_openMultiple.clicked.connect(self.slot_openMultiple) # Openmultiple confirmed
        self.btn_createReport.clicked.connect(self.slot_createReport) # Createreport confirmed

        self.checkboxLists = [] # The tickboxes themselves
        self.checkboxLists.append(self.chb_proNames)
        self.checkboxLists.append(self.chb_timeframe)
        self.checkboxLists.append(self.chb_timestampGraph)
        self.checkboxLists.append(self.chb_top20Words)
        self.checkboxLists.append(self.chb_wordMap)
        self.checkboxLists.append(self.chb_topicModels)

        self.resultPath = "./Result" # Make Result folder
        if not os.path.exists(self.resultPath): # Make if not existing
            os.mkdir(self.resultPath)

        self.initial()
        
    def initial(self):
        self.files = []
        self.words = []
        self.btn_createReport.setEnabled(False)
        self.btn_createReport.show()

    def openFileNameDialog(self): # Open chat
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileNames, _ = QFileDialog.getOpenFileName(self,"Open Chat File", "","CSV Files (*.csv)", options=options) # Limited to CSV, could add All files option if necessary.
        if fileNames:
            self.files = [fileNames]
    
    def openFileNamesDialog(self): # Open multiple
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileNames, _ = QFileDialog.getOpenFileNames(self,"Open Chat Files", "","CSV Files (*.csv)", options=options) # Limited to CSV, could add All files option if necessary.
        if fileNames:
            self.files = fileNames

    def slot_openChat(self):
        self.openFileNameDialog()
        if len(self.files) == 0:
            return
        self.lbl_progress.setText(str(len(self.files)) + " Chat loaded") # When single chat opened
        self.btn_createReport.setEnabled(True)

    def slot_openMultiple(self):
        self.openFileNamesDialog()
        if len(self.files) == 0:
            return
        self.lbl_progress.setText(str(len(self.files)) + " Chats loaded") # When multiple chat files opened
        self.btn_createReport.setEnabled(True)

    def slot_createReport(self): # Create report check checkboxes
        flag = False
        for iter in self.checkboxLists:
            if iter.isChecked() == True:
                flag = True
                break

        if flag == False:
            self.lbl_progress.setText("Select options!") # If you somehow don't select any options...
            return

        self.btn_createReport.hide() # Visibility

        self.workerThread = WorkerThread(self.files, self.resultPath, self.checkboxLists)
        self.workerThread.progress.connect(self.setProgress)
        self.workerThread.finished.connect(self.threadDeleteLater)
        self.workerThread.start()
        self.lbl_progress.setText("Working...") # Begins processing

    @pyqtSlot(str)
    def setProgress(self, value):
        self.lbl_progress.setText(value)

    @pyqtSlot()
    def threadDeleteLater(self):
        self.lbl_progress.setText("Completed!") # All done
        self.workerThread.deleteLater()
        self.initial()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyDialog()
    window.show()
    sys.exit(app.exec_())