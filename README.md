# DiscordChessScraper
Python tool to scrape the clipboard for information from the Chess Bot. 
Can also reverse the boards to show the black side of the game, 
and can make an animated gif off the game. 

dependencies:
pip install imageio
pip install Pillow

Usage: 
python dicordChessScraper.py
select and ctrl-c chessbot channel information
after each ctrl-c, wait for the parser to finish, before you do another one.

Boards found will be saved into the folder holding their game, or, if no game is (yet) known, in a folder called 'unknownImage'.
When a game starts, a title frame will be generated showing who is black and who is white.
When a game ends, an end frame will be generated showing the result.

If you think you scraped an entire game (you can check this by browsing the folder images to see if all the moves show up)
Games will show up in someGameFolder, wich looks like game0150532345134, 'game', followed by a discord timestamp at which the game started.

you can 
python reverseBoards.py someGameFolder
this will create a folder called someGameFolderReversed, with all the boards in it, but shown from black side.

and you can
python makeGif.py someGameFolder
this will create an animated gif using the settings in the 'gif.txt' file.
You are free to tinker with these settings:
beginFrameDuration=3.0         # seconds to show the beginframe, showing who is black and who white
preEndFrameDuration=5.0        # seconds to show the board after the last move has been played
endFrameDuration=5.0           # seconds to show the resultframe
minimumDurationFrame= 0.2      # seconds that a turn should be visible at minimum
maximumDurationFrame= 5.0      # seconds that a turn should be visible at maximum
timeCompression=0.1            # normal playback: use 1. Half speed: use 2. Double speed: use 0.5, etc.
Note that the timeCompression is only applied to the turns played.

and you can 
python makeGifs.py someGameFolder
will reverse the board, and make both animated gifs in the original and the reverse folder. 

