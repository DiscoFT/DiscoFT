# DiscoFT

**DiscoFT** is  a free-to-use visualization aide for conversation files. The tool is capable of opening CSV files extracted from [DiscordChatExporter](https://github.com/Tyrrrz/DiscordChatExporter) or similarly formatted chat files.
Once a CSV has been selected, it performs a number of selected functions on the 'Author', 'Date', and 'Content' CSV columns, then ouptuts the results to a HTML report.

# Requirements

**Copy all files included to a project folder of your choice.**

Using your terminal window, navigate using the cd command to your project folder where the **DiscoFT** has been located.

This tool was made using **Python 3.9.5**. Use "python -V" to check your version. 

## Modules

These are: [PyQT5](https://www.riverbankcomputing.com/static/Docs/PyQt5/introduction.html), [Numpy](https://numpy.org/doc/stable/), [NLTK](https://www.nltk.org/), [Pandas](https://pandas.pydata.org/), [Gensim](https://radimrehurek.com/gensim/index.html), [PyLDAvis](https://github.com/bmabey/pyLDAvis), [MatPlotLib](https://matplotlib.org/), [Wordcloud](https://github.com/amueller/word_cloud), and [Spacy](https://spacy.io/).

To download them use:

```py -m pip install -r requirements.txt```

or

```pip3 install -r requirements.txt```

Additionally you may need to run the following command if en_core_web_sm doesn't correctly install:

```python -m spacy download en``` 




# Usage

 ```$ python .\main_thread.py``` to run inside your project folder.

# Functions

<img src=DiscoFT_GUI.PNG>

**The Functions:**
1.  Outputting the Usernames involved in the conversation
2.  Displaying the Start - End point of the conversation in the form of a Timeframe
3.  Generating an Activity graph based on the timestamps in the conversation to help hightlight peak times
4.  Displaying the top 20 used words in a table
5.  Displaying the top used words in the form of a Word Map
6.  Identifying Topic Models based on learning from the conversation data and then outputting into a table & graph

Files over 1MB in size might take a while to Topic Model. Tested a 4MB file with 50,000 lines - Took about 5 mins.

An example file titled 'test.csv' is included with the program, as well as 'ExampleReportOutput.zip'.

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
