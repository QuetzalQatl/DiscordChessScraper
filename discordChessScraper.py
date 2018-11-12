import os
import requests
import time
import win32clipboard
#pip install imageio
import imageio

import shutil

#pip install Pillow
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

timeout=2500 # set time in milleseconds between updates
defaultBoardImg='0000000000000.png'
unknownImageFolder='unknownImage'

#used inside, dont change
gifSettingsFile='gif.txt'
gifSettings="""beginFrame=_begin.png          # filename to the beginframe png
beginFrameDuration=3.0         # seconds to show the beginframe, showing who is black and who white
preEndFrameDuration=5.0        # seconds to show the board after the last move has been played
endFrameDuration=5.0           # seconds to show the resultframe
minimumDurationFrame= 0.2      # seconds that a turn should be visible at minimum
maximumDurationFrame= 5.0      # seconds that a turn should be visible at maximum
timeCompression=0.1            # normal playback: use 1. Half speed: use 2. Double speed: use 0.5, etc.
frameTimestampLength=13        # frames start with this amount of numbers. discord timestamp has 13
frameExtension=png             # frames are expected to have this extension type, only 'png' is tested
frameTimestampResolution=10000 # this indicates where the comma should be, to make the timestamp ín seconds. discord is in 10000/th second"""
activeplayers={}
olddata=''

logging=False

def makeNameSafe(name):
	keepcharacters = ('_',' ', '.')
	result="".join(c for c in name if c.isalnum() or c in keepcharacters).rstrip()
	return result

def logLine(line):
	if logging:
		with open('log.txt', 'a') as f:
			f.write(str(line)+'\n')
	else:
		print(str(line))

#clear old log file
if os.path.isfile('log.txt'):
	with open('log.txt', 'w') as f:
		f.write('\n')
		
def MakeTextPng(upper, up, down, downer, dirname, filename, size=32):
	size1=size2=size3=size4=size
	fit=False
	while not fit:
		font1 = ImageFont.truetype("arial.ttf", size1, encoding="unic")
		text_width1, text_height1 = font1.getsize(upper)
		if text_width1>400:
			size1=size1-1
		else:
			fit=True
	fit=False
	while not fit:
		font2 = ImageFont.truetype("arial.ttf", size2, encoding="unic")
		text_width2, text_height2 = font2.getsize(up)
		if text_width2>400:
			size2=size2-1
		else:
			fit=True
	fit=False
	while not fit:
		font3 = ImageFont.truetype("arial.ttf", size3, encoding="unic")
		text_width3, text_height3 = font3.getsize(down)
		if text_width3>400:
			size3=size3-1
		else:
			fit=True
	fit=False
	while not fit:
		font4 = ImageFont.truetype("arial.ttf", size4, encoding="unic")
		text_width4, text_height4 = font4.getsize(downer)
		if text_width4>400:
			size4=size4-1
		else:
			fit=True
			
	canvas = Image.new('RGB', (400,400), "black")
	draw = ImageDraw.Draw(canvas)
	draw.text((200-(text_width1/2), 70-(text_height1/2)), upper, 'white', font1)
	draw.text((200-(text_width2/2), 130-(text_height2/2)), up, 'white', font2)
	draw.text((200-(text_width3/2), 270-(text_height3/2)), down, 'white', font3)
	draw.text((200-(text_width4/2), 330-(text_height4/2)), downer, 'white', font4)
	if not os.path.isdir(dirname):
		os.mkdir(dirname) 
	canvas.save(dirname+'\\'+filename+".png", "PNG")

def getBoardPicture(url, filePath):
	try:
		if not os.path.isfile(filePath):
			page = requests.get(url)
			with open(filePath, 'wb') as f:
				f.write(page.content)
			print ('saved board: '+filePath)		
		return filePath
	except:
		return ""


def getTheClipboardTypes():
    formats = []
    win32clipboard.OpenClipboard()
    lastFormat = 0
    while True:
        nextFormat = win32clipboard.EnumClipboardFormats(lastFormat)
        if 0 == nextFormat:
            break
        else:
            formats.append(nextFormat)
            lastFormat = nextFormat
    win32clipboard.CloseClipboard()
    return formats
	
def get_clipboard(clipboardtype):
	win32clipboard.OpenClipboard()
	data = win32clipboard.GetClipboardData(clipboardtype)
	win32clipboard.CloseClipboard()
	return data

def getSecondName(data):
	if data.find('class="mention wrapper')>0:
		try:
			data=data.replace('<','>')
			data=data.split('>')
			data=data[6]
			data=data[1:]
			return makeNameSafe(data)
		except:
			pass
	return ''

	
def isHumanName(data):
	if data.find('class="username')>0:
		data=data.replace('<','>')
		data=data.split('>')
		if data[2]!='Chess':
			return True
	return False
	
def isBotName(data):
	if data.find('class="username')>0:
		data=data.replace('<','>')
		data=data.split('>')
		if data[2]=='Chess':
			return True
	return False

def hasBotTag(data):
	if data.find('class="botTagRegular')>0:
		data=data.replace('<','>')
		data=data.split('>')
		if data[2]=='BOT':
			return True
	return False

def getTimeStamp(data):
	if data.find('class="timestampCozy')>0:
		data=data.replace('<','>')
		data=data.split('>')
		data=data[1]
		data=data.split(' ')
		data=data[2]
		data=data.split('="')
		data=data[1]
		data=data[:-1]
		return int(data)
	return 0
	
def getImage(data):
	if data.find('class="imageWrapper')>0:
		try:	
			data=data.split(' ')
			data=data[4]
			data=data.split('="')
			data=data[1]
			data=data[:-1]
			#https://cdn.discordapp.com/attachments/506653350125895690/508740136633106436/boardimages_60.png 
			if data[:6]=='https:' and data[-4:]=='.png' and data.find('boardimages')>0:
				return data
		except:
			pass
	return ''

def getCheckMate(data):
	if data.find('class="mention wrapper')>0:
		try:	
			data=data.replace('<','>')
			data=data.split('>')
			if data[8]=='! Checkmate!':
				return True			
		except:
			pass
	return False
	
def getResigned(data):
	if data.find('class="markup')>0:
		try:
			data=data.replace('<','>')
			data=data.split('>')
			if data[2]=="You have resigned! ":
				return True
		except:
			pass
	return False

def getDrawOffer(data):
	if data.find('class="mention wrapper')>0:
		try:
			data=data.replace('<','>')
			data=data.split('>')
			#print (data)
			#print (data[4])
			if data[4]==', you are being offered a draw from ':
				return True
		except:
			pass
	return False

def getGameOffered(data):
	if data.find('class="mention wrapper')>0:
		try:
			data=data.replace('<','>')
			data=data.split('>')
			#print (data)
			#print (data[4])
			if data[4]==', you are being challenged to a chess game by ':
				return True
		except:
			pass
	return False
	
def getDrawExpired(data):

#d=<div class="markup-2BOw-j" style="border: 0px; font-family: inherit; font-size: 0.9375rem; font-style: inherit; font-weight: inherit; margin: 0px; padding: 0px; vertical-align: baseline; outline: 0px; line-height: 1.3; user-select: text; white-space: pre-wrap; word-wrap: break-word; color: rgb(220, 221, 222);">The request has timed out!</div>
	if data.find('class="markup')>0:
		try:
			data=data.replace('<','>')
			data=data.split('>')
			#print (data)
			#print (data[2])
			if data[2]=='The request has timed out!':
				return True
		except:
			pass
	return False
	

def getName1(data):
	
	if data.find('class="mention wrapper')>0:
		data=data.replace('<','>')
		data=data.split('>')
		#print (data)
		#print (makeNameSafe(data[2][1:]))
		return makeNameSafe(data[2][1:])
	return ''

def getName2(data):
	if data.find('class="mention wrapper')>0:
		data=data.replace('<','>')
		data=data.split('>')
		#print (data)
		#print (makeNameSafe(data[6][1:]))
		return makeNameSafe(data[6][1:])
	return ''
	

	
def getGameStarted(data):
	if data.find('class="markup')>0:
		try:
			data=data.replace('<','>')
			data=data.split('>')
			#print (data)
			#print (data[2])
			if data[2]=='The game has started! Type |board to see the board!':
				return True
		except:
			pass
	return False

	
def getDrawAccept(data):
	if data.find('class="markup')>0:
		try:
			data=data.replace('<','>')
			data=data.split('>')
			#print (data)
			#print (data[2])
			if data[2]=='Draw offer accepted! The game is a draw!':
				return True
		except:
			pass
	return False
	

def getResignWinner(data):
	if data.find('class="markup')>0:
		try:
			data=data.replace('<','>')
			data=data.split('>')
			data=data[4]
			data=data[1:]
			return data
		except:
			pass
	return ''
	
def getWinnerCheckMate(data):
	if data.find('class="mention wrapper')>0:
		try:	
			data=data.replace('<','>')
			data=data.split('>')
			data=data[2]
			data=data[1:]
			return makeNameSafe(data)
		except:
			pass
	return ''
	
def getFunlineCheckMate(data):
	if data.find('class="mention wrapper')>0:
		try:	
			data=data.replace('<','>')
			data=data.split('>')
			return data[4]
		except:
			pass
	return ''

def createGame(timestamp, whiteName, blackName):

	folder='game'+str(timestamp)
	if not os.path.isdir(folder):
		os.mkdir(folder) 
	filename='game'+str(timestamp)+'.txt'
	time2='{0:013}'.format(0)
	savePath=folder+'\\'+time2+whiteName+'.png'
	shutil.copyfile(defaultBoardImg, savePath)  
	with open(folder+'\\black.txt', 'w') as F:
		F.write(blackName+'\n')
	with open(folder+'\\white.txt', 'w') as F:
		F.write(whiteName+'\n')
	MakeTextPng("White:", whiteName, "Black:", blackName, folder,'_begin')
	with open(folder+'\\'+gifSettingsFile, 'w') as F:
		F.write(gifSettings)	
	
	if os.path.isdir(unknownImageFolder):
		dirnames=os.listdir(unknownImageFolder)

		#check if unknownimagesfolder has images
		for d in dirnames:
			starttime=d[:13]
			name=d[13:-4]
			if int(starttime)>=int(timestamp) and (whiteName.strip()==name.strip() or blackName.strip()==name.strip()):
				dif=int(starttime)-int(timestamp)
				difstr='{0:013}'.format(dif)
				print ('copy '+unknownImageFolder+'\\'+d, folder+'\\'+difstr+name+'.png')
				shutil.copyfile(unknownImageFolder+'\\'+d, folder+'\\'+difstr+name+'.png')  
				os.remove(unknownImageFolder+'\\'+d) 
	
	readBoards()
		
def addMove(timestamp, player, imagename):
	try:
		currentFolder=activeplayers[player]
		td=int(timestamp)-int(currentFolder[4:17])
		timeDif='{0:013}'.format(td)
		newImagename=timeDif+player+'.png'
		newImagePath=currentFolder+'\\'+newImagename
		if not os.path.isfile(newImagePath):
			getBoardPicture(imagename, newImagePath)
	except: #activeplayer not found, handle unknownimage
		if not os.path.isdir(unknownImageFolder):
			os.mkdir(unknownImageFolder) 
		currentFolder=unknownImageFolder
		newImagename=str(timestamp)+player+'.png'
		newImagePath=currentFolder+'\\'+newImagename
		#check if fits in closed games
		dirnames=os.listdir()
		gamefound=False
		for d2 in dirnames:
			if len(d2)==17 and d2[:4]=='game':
				dname=os.listdir(d2)
				black=''
				white='' 
				hasresult=False
				for d in dname:
					if d=='black.txt':
						black=d2
					elif d=='white.txt':
						white=d2
					elif d=='result.txt':
						hasresult=True
						
				if len(white)>0 and len(black)>0 and hasresult:
					with open(d2+'\\white.txt', 'r') as F:
						whiteName=F.read()
					with open(d2+'\\black.txt', 'r') as F:
						blackName=F.read()
					result=[]
					with open(d2+'\\result.txt', 'r') as F:
						result.append(F.readlines())
					if int(result[0][0].strip())>int(timestamp) and int(d2[4:])<int(timestamp):
						timediff=int(timestamp)-int(d2[4:])
						timediffstr='{0:013}'.format(timediff)
						timediffstr=timediffstr+'.png'
						newImagePath=currentFolder+player+'\\'+timediffstr
						if not os.path.isfile(newImagePath):
							getBoardPicture(imagename, newImagePath)		
						gamefound=True	
		if not gamefound:
			if not os.path.isfile(newImagePath):
				getBoardPicture(imagename, newImagePath)		

def moveOlderPicturesOut(folder,timestamp):
	folderTime=folder[4:]
	dirnames=os.listdir(folder)	
	for d in dirnames:
		if len(d)>17 and d[-4:]=='.png':
			thisTime=d[:13]
			actualTime=int(thisTime)+int(folderTime)
			actualTimeStr='{0:013}'.format(actualTime)
			playername=d[13:-4]
			if int(thisTime)>(int(timestamp)-int(folderTime)):
				print ('copy '+folder+'\\'+d+' '+unknownImageFolder+'\\'+actualTimeStr+playername+'.png')
				shutil.copyfile(folder+'\\'+d, unknownImageFolder+'\\'+actualTimeStr+playername+'.png') 
				os.remove(folder+'\\'+d) 

def addDraw(player, timestamp):
	try:
		filename=activeplayers[player]
	except:
		return
	for d in activeplayers:
		if activeplayers[d]==activeplayers[player]:
			if d!=player:
				other=d
	
	timediff=int(timestamp)-int(filename[4:])
	timediffstr='{0:013}'.format(timediff)
	MakeTextPng("Draw:", player, 'equals', other,filename,timediffstr)
	with open(filename+'\\result.txt', 'w') as F:
		F.write(str(timestamp)+'\n')
		F.write('draw:\n')		
		F.write(player+'\n')		

	moveOlderPicturesOut(filename,timestamp)
	readBoards()
	#makeGif(filename)
	
def addResign(player, timestamp):
	try:
		filename=activeplayers[player]
	except:
		return
	
	for d in activeplayers:
		if activeplayers[d]==activeplayers[player]:
			if d!=player:
				loser=d
	timediff=int(timestamp)-int(filename[4:])
	timediffstr='{0:013}'.format(timediff)
	MakeTextPng(loser, 'Resigned', 'Winner:', player,filename,timediffstr)
	with open(filename+'\\result.txt', 'w') as F:
		F.write(str(timestamp)+'\n')
		F.write('resigned:\n')		
		F.write(loser+'\n')		
	moveOlderPicturesOut(filename,timestamp)
	readBoards()
	
#	makeGif(filename)
	
def addMate(funline, player, timestamp):
	try:
		filename=activeplayers[player]
	except:
		return
	for d in activeplayers:
		if activeplayers[d]==activeplayers[player]:
			if d!=player:
				loser=d
	timediff=int(timestamp)-int(filename[4:])
	timediffstr='{0:013}'.format(timediff)
	MakeTextPng("Checkmate", player, funline, loser,filename,timediffstr)
	with open(filename+'\\result.txt', 'w') as F:
		F.write(str(timestamp)+'\n')
		F.write('checkmate:\n')		
		F.write(loser+'\n')	
		F.write(player+funline+loser+'\n')
	moveOlderPicturesOut(filename,timestamp)
	readBoards()
	#makeGif(filename)
	
def readBoards():
	activeplayers.clear()
	boardnames=[]
	dirnames=os.listdir()
	
	for d2 in dirnames:
		if len(d2)==17 and d2[:4]=='game':
			dname=os.listdir(d2)
			black=''
			white='' 
			hasresult=False
			for d in dname:
				if d=='black.txt':
					black=d2
				elif d=='white.txt':
					white=d2
				elif d=='result.txt':
					hasresult=True
			if len(white)>0 and len(black)>0 and not hasresult:
				with open(d2+'\\white.txt', 'r') as F:
					whiteName=F.read()
				with open(d2+'\\black.txt', 'r') as F:
					blackName=F.read()
				activeplayers[whiteName.strip()] = d2
				activeplayers[blackName.strip()] = d2
	print()
	print ('activeplayers:')
	print (activeplayers)
	print()
	
def checkdata(data):
	
	data=str(data)
	data=data.replace("><",">\\r\\n<")
	data=data.split("\\r\\n")
	IsBotName=False
	HasBotTag=False
	LastKnownTimeStamp=0
	Name1=''
	Name2=''
	image=''
	hasResigned=False
	CheckMate=False
	foundDrawOffer=False
	foundDrawAccept=False
	gameOffered=False
	gameStarted=False
	funline=''

	for d in data:
		#logLine ('----')
		#logLine ('d='+d)
		
		
		if isHumanName(d):
			logLine ('(-HasBotTag)')
			HasBotTag=False
			logLine ('(-IsBotName)')
			IsBotName=False
			
		if isBotName(d):
			logLine ('(+IsBotName)')
			IsBotName=True
		
		if hasBotTag(d):
			logLine ('(+HasBotTag)')
			HasBotTag=True

		if LastKnownTimeStamp>0 and IsBotName and HasBotTag:
			nm1=getName1(d)
			if len(nm1):
				Name1=nm1
				logLine ('(+Name1)'+Name1)			
		
		ts=getTimeStamp(d)
		if ts>0:
			time2='{0:013}'.format(ts)
			logLine ('(+hasTimeStamp)'+time2)
			LastKnownTimeStamp=ts
			
		im=getImage(d)
		if len(im):
			logLine ('(+len(im))'+im)	
			image=im
			
		if getGameOffered(d):
			logLine ('(+getGameOffered)')
			Name1=getName1(d)
			Name2=getName2(d)
			logLine ('(+Name1)'+Name1)
			logLine ('(+Name2)'+Name2)
			gameOffered=True

		if getGameStarted(d):
			logLine ('(+getGameStarted)')
			gameStarted=True
			
		if getResigned(d):
			logLine ('(+getResigned)')
			hasResigned=True
			Name1=getResignWinner(d)
			logLine ('(+Name1)'+Name1)
			
			
		if getCheckMate(d):
			logLine ('(+getCheckMate)')	
			CheckMate=True
			Name1=getWinnerCheckMate(d)
			funline=getFunlineCheckMate(d)
			logLine ('(+Name1)'+Name1)
			logLine ('(+funline)'+funline)

		if getDrawOffer(d):
			logLine ('(+foundDrawOffer)')
			Name1=getName1(d)
			Name2=getName2(d)
			logLine ('(+Name1)'+Name1)
			logLine ('(+Name2)'+Name2)
			foundDrawOffer=True
		
		if getDrawExpired(d):
			logLine ('(-foundDrawOffer)')
			foundDrawOffer=False

		if getDrawAccept(d):
			logLine ('(+foundDrawAccept)')
			foundDrawAccept=True
			
		# if len(d)>25:
			# logLine('')
			# logLine ('IsBotName='+str(IsBotName))
			# logLine ('HasBotTag='+str(HasBotTag))
			# logLine ('LastKnownTimeStamp='+str(LastKnownTimeStamp))
			# logLine ('Name1='+str(Name1))
			# logLine ('Name2='+str(Name2))
			# logLine ('image='+str(image))
			# logLine ('hasResigned='+str(hasResigned))
			# logLine ('CheckMate='+str(CheckMate))
			# logLine ('foundDrawOffer='+str(foundDrawOffer))
			# logLine ('foundDrawAccept='+str(foundDrawAccept))
			# logLine ('gameOffered='+str(gameOffered))
			# logLine ('gameStarted='+str(gameStarted))
			# logLine('')
		
		if LastKnownTimeStamp>0 and IsBotName and HasBotTag and len(Name1) and foundDrawOffer and foundDrawAccept:
			logLine ('\naddDraw("'+Name1+'", '+str(LastKnownTimeStamp)+')\n')
			addDraw(Name1, LastKnownTimeStamp)
			Name1=''
			Name2=''
			IsBotName=False
			HasBotTag=False
			hasResigned=False
			CheckMate=False
			foundDrawOffer=False
			foundDrawAccept=False
			gameOffered=False
			gameStarted=False
			image=''
			LastKnownTimeStamp=0	
		
		if LastKnownTimeStamp>0 and IsBotName and HasBotTag and len(Name1) and hasResigned:
			logLine ('\naddResign("'+Name1+'", '+str(LastKnownTimeStamp)+')\n')
			addResign( Name1,LastKnownTimeStamp )
			Name1=''
			Name2=''
			IsBotName=False
			HasBotTag=False
			hasResigned=False
			CheckMate=False
			foundDrawOffer=False
			foundDrawAccept=False
			gameOffered=False
			gameStarted=False
			image=''
			LastKnownTimeStamp=0		
		
		if CheckMate and len(Name1) and len(funline):
			logLine ('\naddMate("'+funline+'", "'+Name1+'", '+str(LastKnownTimeStamp)+')\n')
			addMate(funline, Name1, str(int(LastKnownTimeStamp)+2000))
			Name1=''
			Name2=''
			IsBotName=False
			HasBotTag=False
			hasResigned=False
			CheckMate=False
			foundDrawOffer=False
			foundDrawAccept=False
			gameOffered=False
			gameStarted=False
			image=''
			LastKnownTimeStamp=0
		
		if LastKnownTimeStamp>0 and IsBotName and HasBotTag and len(Name1) and len(image):
			logLine ('\naddMove('+str(LastKnownTimeStamp)+', "'+Name1+'", "'+image+'")\n')
			addMove(LastKnownTimeStamp, Name1, image)
			Name1=''
			Name2=''
			IsBotName=False
			HasBotTag=False
			hasResigned=False
			CheckMate=False
			foundDrawOffer=False
			foundDrawAccept=False
			gameOffered=False
			gameStarted=False
			image=''
			#LastKnownTimeStamp=0			
		
		if LastKnownTimeStamp>0 and HasBotTag and len(Name1) and len(Name2) and gameOffered and gameStarted:
			logLine ('\ncreateGame('+str(LastKnownTimeStamp)+', "'+Name2+'", "'+Name1+'")\n')
			createGame(LastKnownTimeStamp, Name2, Name1)
			Name1=''
			Name2=''
			IsBotName=False
			HasBotTag=False
			hasResigned=False
			CheckMate=False
			foundDrawOffer=False
			foundDrawAccept=False
			gameOffered=False
			gameStarted=False
			image=''
			LastKnownTimeStamp=0
			
readBoards()			
while True:
	for cbt in getTheClipboardTypes():
		if cbt==49364: #clipboard type: html snippet of the discord channel
			newdata=get_clipboard(cbt)
			if newdata!=olddata:
				olddata=newdata
				print('---parsing incoming data---')
				checkdata(olddata)
				print('---------------------------')
	time.sleep(timeout/1000.0)
	
