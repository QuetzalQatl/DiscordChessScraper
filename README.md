# DiscordChessScraper
<i>todo: uses win32api, so windows only, needs mac/linux implementations to: grab clipboard contents for type html (simple text wont do!), and for uniform filepath handling

Warning: use python version 3.6.7, and dependencies loaded from pip, <br>
or 3.7, but then you will have to compile some dependencies yourself that are not in pip (yet?)<br>
Using anything lower then 3.6.7 would probably work (fingers crossed), but dont use version 2
</i>

Python tool to scrape the clipboard for information from the Chess Bot. 
Can also reverse the boards to show the black side of the game, 
and can make an animated gif off the game. 

 <b>-dependencies:<br/></b>
pip install imageio<br/>
pip install Pillow

 -Usage:<br/>
<b>python dicordChessScraper.py<br/></b>
select and ctrl-c chessbot channel information<br/>
after each ctrl-c, wait for the parser to finish, before you do another one.

Boards found will be saved into the folder holding their game, or, if no game is (yet) known, in a folder called 'unknownImage'.
When a game starts, a title frame will be generated showing who is black and who is white.
When a game ends, an end frame will be generated showing the result.

Games will show up in someGameFolder, wich looks like game0150532345134, 'game', followed by a discord timestamp at which the game started. You can check if you have a complete game by browsing throught the files in the folder.

 -you can <br/>
<b>python reverseBoards.py someGameFolder<br/></b>
this will create a folder called someGameFolderReversed, with all the boards in it, but shown from black side.

 -you can<br/>
<b>python makeGif.py someGameFolder<br/></b>
this will create an animated gif using the settings in the 'gif.txt' file.<br/>
You are free to tinker with these settings:<br/>
beginFrameDuration=3.0         # seconds to show the beginframe, showing who is black and who white<br/>
preEndFrameDuration=5.0        # seconds to show the board after the last move has been played<br/>
endFrameDuration=5.0           # seconds to show the resultframe<br/>
minimumDurationFrame= 0.2      # seconds that a turn should be visible at minimum<br/>
maximumDurationFrame= 5.0      # seconds that a turn should be visible at maximum<br/>
timeCompression=0.1            # normal playback: use 1. Half speed: use 2. Double speed: use 0.5, etc.<br/>
Note that the timeCompression is only applied to the turns played.

 -and you can <br/>
<b>python makeGifs.py someGameFolder<br/></b>
will reverse the board, and make both animated gifs in the original and the reverse folder. 

