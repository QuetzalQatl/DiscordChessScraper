import sys
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

S={} # dict with settings that can be tinkered with via checkSettingsFile.txt, if any
S['beginFrameDuration']=3.0 #seconds
S['preEndFrameDuration']=5.0 
S['endFrameDuration']=5.0 #seconds
S['minimumDurationFrame'] = 0.2
S['maximumDurationFrame'] = 5.0
S['timeCompression']=0.1
S['beginFrame']='_begin.png' 
S['frameTimestampLength']=13
S['frameExtension']='png' 
S['frameTimestampResolution']=10000

gifColletingFolder='gifs' # leave empty for none

checkSettingsFile='gif.txt'
videoTimerList=[]

def writeMovie(moviedir, moviename, filenames):
	if not os.path.isdir(moviedir):
		os.mkdir(moviedir) 
	print ('writing '+moviedir+'\\'+moviename)
	with imageio.get_writer(moviedir+'\\'+moviename, mode='I', duration=videoTimerList) as writer:
		for filename in filenames:
			image = imageio.imread(filename)
			writer.append_data(image)
	if len(gifColletingFolder)>0:
		if not os.path.isdir(gifColletingFolder):
			os.mkdir(gifColletingFolder)
		shutil.copy(moviedir+'\\'+moviename, gifColletingFolder+'\\'+moviename)
		

def makeGif(board):
	print()
	print ('assembling gif from data in folder:\n'+board+'\n')
	print ('settings used:')
	for item in S:
		print (item+'='+str(S[item]))
	print ()
	
	filenames=[]
	lines=os.listdir(board)
	totalTime=0.0
	
	#add begin frame
	picName=board+'\\'+S['beginFrame']
	t="{:.5f}".format(S['beginFrameDuration'])
	print ('('+str(t)+') '+S['beginFrame'])
	totalTime=totalTime+S['beginFrameDuration']

	filenames.append(picName)
	videoTimerList.append(S['beginFrameDuration'])

	oldtimestamp=''
	currentImage=''
	oldImage=''
	pointExtension='.'+S['frameExtension']
	for l in lines:
		if len(l)>S['frameTimestampLength']+4 and l[-4:]==pointExtension:
			newtimestamp=l[:S['frameTimestampLength']]
			currentImage=l
			if len(oldImage)>0: # skip first frame
				startTime=int(oldtimestamp)
				stopTime=int(newtimestamp)
				picName=board+'\\'+oldImage
				lenFrame=stopTime-startTime
				lenFrame=lenFrame*S['timeCompression']
				lenFrame=lenFrame/S['frameTimestampResolution']
				if lenFrame<S['minimumDurationFrame']:
					lenFrame=S['minimumDurationFrame']
				elif lenFrame>S['maximumDurationFrame']:
					lenFrame=S['maximumDurationFrame']
				t="{:.5f}".format(lenFrame)
				print ('('+str(t)+') '+oldImage)
				totalTime=totalTime+lenFrame
				filenames.append(picName)
				videoTimerList.append(lenFrame)
				rLenFrame=lenFrame
				
			oldImage=currentImage
			oldtimestamp=newtimestamp
		elif len(l)==S['frameTimestampLength']+4 and l[-4:]==pointExtension: # last frame has no name behind it
			#repeat last frame preEndDuration time (minus the part we already did)
			picName=board+'\\'+oldImage
			t="{:.5f}".format(S['preEndFrameDuration'])
			print ('('+str(t)+') '+oldImage)
				
			totalTime=totalTime+S['preEndFrameDuration']
			filenames.append(picName)
			videoTimerList.append(S['preEndFrameDuration'])

			#show end frame for enduration time
			picName=board+'\\'+l
			t="{:.5f}".format(S['endFrameDuration'])
			print ('('+str(t)+') '+l)
				
			totalTime=totalTime+S['endFrameDuration']
			filenames.append(picName)
			videoTimerList.append(S['endFrameDuration'])
	print('total time: '+str(totalTime))
	writeMovie(sys.argv[1], board+'movie.gif', filenames)
	

if __name__ == "__main__":
	nrOfArguments=len(sys.argv)
	if nrOfArguments!=2:
		print ('  please include folder containing the board moves')
		print ('  like this:')
		print ('python '+sys.argv[0]+' someFolderName')
		exit(1) # error: incorrect nr of arguments
	if not os.path.isdir(sys.argv[1]):
		print ('  folder "' + sys.argv[1] + '" not found.')
		print ('  please include folder containing the board moves')
		print ('  like this:')
		print ('python '+sys.argv[0]+' someFolderName')
		exit(2) # error: folder not found
	if os.path.isfile(sys.argv[1]+'\\'+checkSettingsFile):
		with open(sys.argv[1]+'\\'+checkSettingsFile, 'r') as F:
			lines=F.readlines()
		for line in lines:
			if line.find('=')>0:
				line=line.split('=')
				parameter=str(line[0].strip())
				if line[1].find('#')>0:
					line[1]=line[1].split('#')
					value=str(line[1][0]).strip()
				else:
					value=str(line[1]).strip()
				if parameter in S:
					if parameter=='beginFrame' or parameter=='frameExtension':
						S[parameter]=value
					elif parameter=='frameTimestampLength':
						S[parameter]=int(value)
					else:
						try:
							S[parameter]=float(value)
						except:
							pass		
	
	makeGif(sys.argv[1])
