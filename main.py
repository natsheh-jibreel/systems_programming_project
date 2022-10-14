import math
import sys 
def WordCheck(Line,i , j):                          # to read the String in specific location
    st =""
    str1=""
    while i < j:
        if Program[Line][i] != " ":
            st += Program[Line][i]
            i += 1
        else:
            str1 = st    
            return str1
def getIndex(str):                                  #
    index = 0
    while index < len(AppindexA):
        if(AppindexA[index][0] == word):
            return index
        else:
            index += 1
    return -1    
def LabelCheck(word):                               # To check if the Label is already exist or not
    index = 0
    while index < len(LABEL):
        if LABEL[index][0] == word:
            return False
        index += 1
    return True        
def OPCheck(word):                                  # To check if the OPCODE is valid or not
    index = 0
    while index < len(AppindexA):
        if AppindexA[index][0] == word:
            return True
        index += 1
    return False        
def byteCheck(word,index,ctr):                      # To calculate the length of Char or X
    num =0
    if word[index] == 'C':
        while word[ctr] != '\'':
            num += 1
            ctr += 1
    elif word[index] == 'X':
        while word[ctr] != '\'':
            num += 0.5  
            ctr += 1
        num = math.ceil(num)
    else:
        print("Error Flag activated \nByte is not  'C' or 'B'")
    return num    
def HexCheck(word):                                 # To return the Hex number in a good form
    str2 = word+""
    str4 = ""
    index = 0
    if str2[1] =='x':
        index =2
    while index < len(word):
        if str2[index].isalpha():
            str4 += str2[index].upper()
        else:
            str4+=str2[index]
        index +=1    
    return str4

intmdte = open("intmdte_file.txt","w")              #
PronameFile = open("Proname.txt","w")               #
ProLengthFile = open("ProLength.txt","w")           #  These files are the output of Pass 1
StartAddFile = open("StartAdd.txt","w")             #      And we will use them is Pass 2
LOCCTRFile = open("LOCCTR.txt","w")                 #
SYMTABFile = open("SYMTABFile.txt","w")             #

AppindexA = []
s =""
ctr =0
with open("OPTAB.txt", "r") as fin:         # AppemdixA read from file
    for line in fin:
        s = line.split(' ')
        AppindexA.append([s[0],s[1]])

Program = []
LOCCTRarr = []
FileCtr = 0
with open("sample1.asm", "r") as fin2:        # Read the test file
    for line in fin2:
            Program.append(line)

checkCTR = 0
while Program[checkCTR][0] == '.':
    checkCTR += 1

ProName = "ProName"
WhatToDo = WordCheck(checkCTR,11,20)
if WhatToDo == "START":
    ProName = WordCheck(checkCTR,0,10)
    LOCCTRtest = WordCheck(checkCTR,21,29)
    LOCCTR = str(int(LOCCTRtest,16))
else:
    LOCCTR = "0"    
    LOCCTRarr.append(LOCCTR)

LOCATION = []
LOCATION.append('#')
LABEL = []
index = checkCTR
index2 = 0
word = ""
wordT = ""
LOCCTRnext = 0
StarCTR = 0
EndFlag = 0
while index < len(Program):
    if Program[index][0] != '.':
        word = WordCheck(index,11,20)
        if word != "START":
            LOCCTR = LOCCTRnext
            if word == "END":
                EndFlag = 1
                if(index < len(Program)-1):
                    word = "LTORG"
                else:
                    print("{: >4}".format(''),"{: >35}".format(Program[index]))
                    intmdte.write("{: >4}".format(''))
                    intmdte.write("{: >35}".format(Program[index]))
                    break
            elif word =="WORD":
                LOCCTRnext = str((int(LOCCTR)+3))
            elif word == "RESW":
                word = WordCheck(index,21,35)
                if word.isnumeric():
                    LOCCTRnext = str((int(LOCCTR)) + (int(word) * 3)) 
                else:
                    print("Error Flag activated \nError in the representaion of reserved location")
                    sys.exit()
            elif word == "RESB":
                word = WordCheck(index,21,35)
                if word.isnumeric():
                    LOCCTRnext = str((int(LOCCTR)) + (int(word))) 
                else:
                    print("Error Flag activated \nError in the representaion of reserved location")
                    sys.exit()
            elif word == "BYTE":
                word = WordCheck(index,21,35)
                wordn = byteCheck(word,0,2)
                LOCCTRnext = str((int(LOCCTR)) + (int(wordn))) 
            elif word == "LTORG":
                word == "LTORG"
            elif word =="RSUB":
                LOCCTRnext = str((int(LOCCTR)+3))
            elif OPCheck(word):
                LOCCTRnext = str((int(LOCCTR)+3))
                wordT = WordCheck(index,21,35)
                if wordT[0] =="=":
                    StarCTR += 1
                    LABEL.append([wordT , 0])
            else:
                print("Error Flag activated \nOPCODE '"+ word +"' is wrong \"Line "+ str(index+checkCTR) +"\" , please check your SIC code")           # Error Flag (OPCODE is wrong)
                sys.exit()
            if word != "LTORG":
                LOCATION.append(LOCCTR)    
                word = WordCheck(index , 0 , 10)
                yeee = LabelCheck(word)
                if yeee:
                    if word != "":
                        LABEL.append([word,LOCCTR])
                else:
                    print("Error Flag activated \nDuplicated Label '"+ word +"' at line "+ str(index+checkCTR) +" please check your SIC code")       # Error Flag (Duplicated Label)
                    sys.exit()
                print("{:0>4}".format(HexCheck(hex(int(LOCCTR)))),"{: >38}".format(Program[index])) 
                intmdte.write("{:0>4}".format(HexCheck(hex(int(LOCCTR))))+"  ")
                intmdte.write("{: >38}".format(Program[index]))
                LOCCTRarr.append(LOCCTR)
                index +=1
            else:
                print("{: >8}".format(''),"{: >35}".format(Program[index]))
                intmdte.write("{: >56}".format(Program[index]))
                index +=1
                word = WordCheck(index , 0 , 10)
                while word =='*':
                    wordT = WordCheck(index ,11 ,20 )
                    Accept = -1
                    AccIndex =0
                    while AccIndex < len(LABEL):
                        if LABEL[AccIndex][0] == wordT:
                            Accept = AccIndex
                            break
                        AccIndex +=1
                    if Accept == -1:
                        print("Literal missing ,Please check your code")        # Error Flag (Missing location for Literal)
                        sys.exit()
                    StarCTR -=1
                    print("{:0>4}".format(HexCheck(hex(int(LOCCTR)))),"{: >35}".format(Program[index])) 
                    intmdte.write("{:0>4}".format(HexCheck(hex(int(LOCCTR))))+"  ")
                    intmdte.write("{: >35}".format(Program[index]))
                    LOCCTRarr.append(LOCCTR)
                    word = WordCheck(index,11,20)
                    LABEL[Accept][1] = LOCCTR
                    wordn = byteCheck(word,1,3)
                    LOCCTRnext = str((int(LOCCTR)) + (int(wordn)))
                    LOCCTR = LOCCTRnext
                    index +=1 
                    if index < len(Program):
                        word = WordCheck(index , 0 , 10)
                if StarCTR != 0:
                    print("Literal missing ,Please check your code")                # Error Flag (Wrong Literal)
                    sys.exit()
        else:
            LOCCTRnext = LOCCTR
            print("{:0>4}".format(HexCheck(hex(int(LOCCTR)))),"{: >35}".format(Program[index]))
            intmdte.write("{:0>4}".format(HexCheck(hex(int(LOCCTR))))+"  ")
            intmdte.write("{: >35}".format(Program[index]))
            LOCCTRarr.append(LOCCTR)
            index += 1
    else:
        intmdte.write(Program[index])
        print(Program[index])
        index +=1

index = 0    
if ProName != "ProName":
    PronameFile.write(ProName)
else:
    PronameFile.write("No name found")

ProLength = HexCheck(hex(int(LOCCTRarr[len(LOCCTRarr)-1]) - int(LOCCTRarr[0])))

ProLengthFile.write(ProLength)

StartAddFile.write(HexCheck(hex(int(LOCCTRarr[0]))))

while index < len(LOCCTRarr):
    LOCCTRFile.write(HexCheck(hex(int(LOCCTRarr[index]))) + "\n")
    index += 1

if EndFlag == 0 :
    print("Error Flag activated \nno 'End' in your file")
    sys.exit()
index = 0
print("\n\n\n\n\n\n")
while index < len(LABEL):
    print("{:0>4}".format(HexCheck(hex(int(LABEL[index][1]))))+ "  "+ LABEL[index][0])
    SYMTABFile.write("{:0>4}".format(HexCheck(hex(int(LABEL[index][1]))))+ "  "+ LABEL[index][0] + "\n")
    index += 1
