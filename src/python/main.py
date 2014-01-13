from globals import *
from SAbuilder import *
import timeit
import sys


def main():
    word = ""    
    path = sys.argv[1]

    f = open(os.path.normpath(path),"r")
       
    for l in f:
        word += l
    #f.close()

    if(DEBUG):
        print("Path: " + path)
        #print("Word: " + word) 
        print('Application started')

    if(TIME):
        start = timeit.default_timer()
 
    builder = SAbuilder() 
 
    try:
        builder.start(word)
    except:
        pass

    if(TIME):
        stop = timeit.default_timer()
        print("SA created in: " + str(stop-start) + " seconds\n and saved to SAOutput.txt file")
        print("\n!!!----------------NOTE----------------!!!")
        print("If your input txt file has any other characters but letters, this SA is invalid and you should check your input file!")
    if(MEMORY):
        print(resource.getrusage(resource.RUSAGE_SELF))

if  __name__ =='__main__':
    main()


