import sys
import os 

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
	
	print('\nreversing board...\n')
	os.system('python reverseBoards.py '+sys.argv[1])
	print('\n[x] done')
	print('\nmaking animated gif...\n')
	os.system('python makeGif.py '+sys.argv[1])
	print('\n[x] done')
	print('\nmaking animated gif for reversed board...\n')
	os.system('python makeGif.py '+sys.argv[1]+'reversed')
	print('\n[x] done')
