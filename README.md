DiscoFT is still a work in progress!

DiscoFT's GUI is designed in PyQT

To successfully run DiscoFT you will need to install the modules it is asking for.


DiscoFT is capable of opening CSV files extracted from DiscordChatExporter (or similarly formatted chat files).
From the opened CSV it performs a number of selected functions on the data, then ouptuts the results to a HTML report.

Functions:
1) Outputting the Profile/UserNames involved in the conversation
2) Displaying the Start - End point of the conversation in the form of a Timeframe
3) Generating an Activity graph based on the timestamps in the conversation to help hightlight peak times
4) Displaying the top 20 used words in a table
5) Displaying the top used words in the form of a Word Map (created using WordCloud)
6) Identifying Topic Models based on learning from the conversation data and then outputting into a table
