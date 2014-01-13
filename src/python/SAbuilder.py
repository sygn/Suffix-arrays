import os.path
import globals
import datetime
from array import *
from globals import *



class SAbuilder(object):
    """
    SA  generator class
    Methods: sort,start, find_next_BH, write_to_file
    """
    def sort(self):
        if(DEBUG):
            print("Sort started")
            print(self.N)

        POS = [None]*(self.N)   #Suffix Array (Output)
        PRM = [None]*(self.N)   #Inverse Suffix Array (PRM[POS[i]] = i)
        Count = [None]*(self.N) #Points to the leftmost suffix of a H-bucket
        BH = [None]*(self.N)    #Marks moved suffixes; After checking, points to the leftmost suffix in 2H-bucket
        B2H = [None]*(self.N)   #internal array
        Next = [None]*(self.N)  #internal array
        alphabet = {}

        '''
        This section sets all arrays according to the first stage
        Sets all the suffixes according to their first letter (Sets POS, PRM and BH arrays)
        '''
        t = 0
        if(DEBUG):
            print("Dict initialized")
        for c in self.word:
            if c in alphabet.keys():
                alphabet[c] += 1
            else:
                alphabet[c] = 1
            POS[t] = -1
            BH[t] = FALSE
            B2H[t] = FALSE
            Count[t] = 0
            t += 1

        Letters = list(alphabet.keys())
        Letters.sort()

        letterPosition = 0
        for x in self.word:
            letterFirstPosition = 0
            for y in Letters:
                if(x != y):
                    letterFirstPosition += alphabet[y]
                else:
                    break
            letterOffset = letterFirstPosition
            BH[letterFirstPosition] = TRUE
            while (POS[letterOffset] != -1):
                letterOffset += 1
            POS[letterOffset] = letterPosition
            PRM[letterPosition] = letterOffset
            letterOffset = 0
            letterPosition += 1

        if(DEBUG):                     #Debugging information of all local variables
            print("initialized")
            print("Status after initialization")
            print("alphabet: " + str(alphabet))
            print("Letters: " + str(Letters))
            print("POS: " + str(POS))
            print("PRM: " + str(PRM))
            print("BH: " + str(BH))
            print("B2H: " + str(B2H))
            print("Count: " + str(Count))

        for h in range(1,self.N):
            buckets = 0
            i = 0
            while(i<self.N):
                j = i + 1
                while (j < self.N and not BH[j]):
                    j += 1
                Next[i] = j
                buckets += 1
                i = j

            if(buckets == self.N):   #Algorithm is done after every suffix is in its own bucket
                break

            k = 0
            while(k<self.N): #Sets PRM array
                Count[k] = 0
                j = k
                while(j<Next[k]):
                    PRM[POS[j]] = i
                    k += 1
                k = Next[k]

            Count[PRM[(self.N - h)]] += 1
            B2H[PRM[self.N - h]] = TRUE

            l = 0
            while (l<self.N): #Scan all buckets and update PRM, Count and B2H arrays
                j = l
                while(TRUE):  #Update arrays
                    if(j>=Next[l]):
                        break
                    s = POS[j] - h
                    if(s >= 0):
                        head = PRM[s]
                        PRM[s] = head + Count[head]
                        Count[head] += 1
                        B2H[PRM[s]] = TRUE
                    j += 1
                l = Next[l]

                j=l
                while(j<Next[l]):           #Reset B2H array such that only the leftmost of them in each
                    s = POS[j] - h          #2H-bucket is set to 1, and rest are reset to 0
                    if(s>= 0 and B2H[PRM[s]]):
                        k = PRM[s]+1
                        while(k<self.find_next_BH(k,BH,self.N)):
                                B2H[k] = FALSE
                                k += 1
                    j += 1
                
                    i = 0
                while(i<self.N):
                    POS[PRM[i]] = i
                    BH[i] = BH[i] | B2H[i]
                    i += 1
            i = 0
            while(i <self.N):
                PRM[POS[i]] = i
                i += 1
            h = h*2
        

        if(DEBUG):                      #Debugging information on finish
                print("Status after finish")
                print("alphabet: " + str(alphabet))
                print("Letters: " + str(Letters))
                print("POS: " + str(POS))
                print("PRM: " + str(PRM))
                print("BH: " + str(BH))
                print("B2H: " + str(B2H))
                print("Count: " + str(Count))

        self.write_to_file(POS, PRM)    #writing to file
        return

    def find_next_BH(self, x, BH, end):
        i = x
        while(i<end):
            if(BH[i] == TRUE):
                return i
            i += 1
        return end

    def write_to_file(self,a,b): #method for writing to output file
        f = open(".\SAOutput.txt","w")
        f.write("   \n")
        f.write("------------------------------------------------------------------------\n")
        f.write(str(datetime.datetime.now()))
        f.write("\nSA")
        f.write(str(a))
        f.write("\nPRM (Inverse SA)")
        f.write(str(b))
        f.close()            

    def start(self, word):        #
        if(DEBUG):
            print("Word: "+ word)
        self.word = word
        self.N = len(word)

        self.sort()
        return

        
    