from globals import *
from SAbuilder import *
import timeit
import sys
if(MEMORY):
    import resource


def main():
    word = ""    
    path = sys.argv[1]
    try: 
        with open(os.path.normpath(path),"r") as f:
            for l in f.read():
                word += l.rstrip()
            word = str(word)
            

    except:
        print("Something went wrong while opening file")
        return

    if(DEBUG):
        print("Path: " + path)
        print("Word: " + word) 
        print('Application started')
    if(TIME):
        start = timeit.default_timer()
 
    builder = SAbuilder()  #builder intialization
 
    try:
        builder.start(word) #algorithm start
    except:
        pass

    if(TIME):   
        stop = timeit.default_timer()
        print("SA created in: " + str(stop-start) + " seconds\n and saved to SAOutput.txt file")

    print("\n!!!----------------NOTE----------------!!!")
    print("If your input txt file has any other characters but letters, this SA is invalid and you should check your input file!")

    if(MEMORY): #Works only on linux machines
        print("Memory usage statistics")
        print(resource.getrusage(resource.RUSAGE_SELF))

if  __name__ =='__main__':
    main()


