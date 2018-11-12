import sys
import os
import shutil

#pip install Pillow
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

sideWidthBoard=20 #pixels
widthBoard=400 #pixels

def logLine(line,file='log.txt'):
	with open(file, 'a') as F:
		F.write(line+'\n')

if __name__ == "__main__":
	nrOfArguments=len(sys.argv)
	if nrOfArguments!=2:
		print ('  please include folder containing the white board moves')
		print ('  like this:')
		print ('python '+sys.argv[0]+' someFolderName')
		exit(1) # error: incorrect nr of arguments
	if not os.path.isdir(sys.argv[1]):
		print ('  folder "' + sys.argv[1] + '" not found.')
		print ('  please include folder containing the white board moves')
		print ('  like this:')
		print ('python '+sys.argv[0]+' someFolderName')
		exit(2) # error: folder not found
	
	blackFolder=sys.argv[1]+'reversed'
	if os.path.isdir(blackFolder):
		print ('previous folder '+blackFolder+' found & deleted')
		shutil.rmtree(blackFolder)
	print ('shutil.copytree '+ sys.argv[1]+' '+blackFolder+'\n')
	shutil.copytree(sys.argv[1], blackFolder)
	
	if os.path.isfile(blackFolder+'\\'+sys.argv[1]+'movie.gif'):
		os.remove(blackFolder+'\\'+sys.argv[1]+'movie.gif')
	lines=os.listdir(blackFolder)
	
	rangenrs=[]
	rangenrs.append(0)
	rangenrs.append(sideWidthBoard)
	partwidth=(widthBoard-(sideWidthBoard+sideWidthBoard))/8
	for i in range (8):
		sideWidthBoard=int(sideWidthBoard+partwidth)
		rangenrs.append(sideWidthBoard)
	rangenrs.append(widthBoard)
	
	for l in lines:
		if len(l)>17 and l[-4:]=='.png':
			print ('reversing: '+ l)
			image=Image.open(blackFolder+'\\'+l)
			image2=Image.open(blackFolder+'\\'+l)
			pix = image.load()
			pix2 = image2.load()
			for x in range(10):
				xfrom=rangenrs[x]
				xto=rangenrs[x+1]-1
				x2from=widthBoard-rangenrs[x+1]
				dif=x2from-xfrom
				for yy in range(0,widthBoard):
					for xx in range(xfrom,xto+1):
						pix2[xx+dif,yy]=pix[xx,yy]
			image2.save(blackFolder+'\\'+l)	
			
			image=Image.open(blackFolder+'\\'+l)	
			image2=Image.open(blackFolder+'\\'+l)
			pix = image.load()
			pix2 = image2.load()
			for x in range(10):
				xfrom=rangenrs[x]
				xto=rangenrs[x+1]-1
				x2from=widthBoard-rangenrs[x+1]
				dif=x2from-xfrom
				for xx in range(0,widthBoard):
					for yy in range(xfrom,xto+1):
						pix2[xx,yy+dif]=pix[xx,yy]
			image2.save(blackFolder+'\\'+l)	
