Installation
--
Using your terminal window, navigate using the cd command to your project folder where the DiscoFT has been located.

Use "python -V" to check your version. This tool was made using Python 3.9.5.

Before running the program you will need to run some commands to give access to certain modules if you don't already have them.

>pip install pyqt5
>pip install numpy
>pip install nltk
>pip install pandas
>pip install gensim
>pip install pyLDAvis
>pip install matplotlib
>pip install wordcloud
>pip install spacy
>python -m spacy download en


Finally, use >python .\main_thread.py to run inside your project folder

Usability
--

DiscoFT is capable of opening CSV files extracted from DiscordChatExporter (or similarly formatted chat files).
Once a CSV has been selected, it performs a number of selected functions on the data, then ouptuts the results to a HTML report.

Functions
--
1) Outputting the Usernames involved in the conversation
2) Displaying the Start - End point of the conversation in the form of a Timeframe
3) Generating an Activity graph based on the timestamps in the conversation to help hightlight peak times
4) Displaying the top 20 used words in a table
5) Displaying the top used words in the form of a Word Map
6) Identifying Topic Models based on learning from the conversation data and then outputting into a table & graph

How to use
--

