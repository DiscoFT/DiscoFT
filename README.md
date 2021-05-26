# Setup & Prerequisites

**Copy all files included to a project folder of your choice.**

Using your terminal window, navigate using the cd command to your project folder where the **DiscoFT** has been located.

This tool was made using **Python 3.9.5**. Use "python -V" to check your version. 

Before running the program you will need to run some commands to give access to certain modules if you don't already have them.

>pip install [pyqt5](https://www.riverbankcomputing.com/static/Docs/PyQt5/introduction.html)

>pip install [numpy](https://numpy.org/doc/stable/)

>pip install [nltk](https://www.nltk.org/)

>pip install [pandas](https://pandas.pydata.org/)

>pip install [gensim](https://radimrehurek.com/gensim/index.html)

>pip install [pyLDAvis](https://github.com/bmabey/pyLDAvis)

>pip install [matplotlib](https://matplotlib.org/)

>pip install [wordcloud](https://github.com/amueller/word_cloud)

>pip install [spacy](https://spacy.io/)

>python -m [spacy](https://spacy.io/) download en


Finally, use >python .\main_thread.py to run inside your project folder.

# Usability

<img src=DiscoFT_GUI.PNG>


**DiscoFT** is capable of opening CSV files extracted from [DiscordChatExporter](https://github.com/Tyrrrz/DiscordChatExporter) or similarly formatted chat files.
Once a CSV has been selected, it performs a number of selected functions on the data, then ouptuts the results to a HTML report.

Files over 1MB in size might take a while to Topic Model. Tested a 4MB file with 50,000 lines - Took about 5 mins.

# Functions

1.  Outputting the Usernames involved in the conversation
2.  Displaying the Start - End point of the conversation in the form of a Timeframe
3.  Generating an Activity graph based on the timestamps in the conversation to help hightlight peak times
4.  Displaying the top 20 used words in a table
5.  Displaying the top used words in the form of a Word Map
6.  Identifying Topic Models based on learning from the conversation data and then outputting into a table & graph

# How to use


## Opening A Chat
Once the interface is up and the program has initialised, click 'Open Chat' for one CSV, or 'Open Multiple' to load multiple CSV's.

*If you choose multiple, they will be iterated through one after another, rather than all at once. DiscoFT will state the progress as it goes.*

## Creating Your Report
After opening your chat files, tick the options you'd like in a report and click 'Create Report'.

DiscoFT will procedurally initiate each option and generate a folder called "Result" if none exists in the working directory.

Inside this folder will be the chatreport in HTML format and any images necessary to display the report options selected.

**Open your chat report to see the results!**

# Licensing
**DiscoFT** is provided free under the BSD 3-Clause License

Copyright (c) 2021, DiscoFT
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
