fileName = "DB\GOLD_D1_240114_240115.txt"
fileNameOut = "DB\GC_D1_Out.txt"

def OnError(ErrorMessage):
        fileIn.close()
        fileOut.close()
        print(ErrorMessage)
        quit()

fileIn = open(fileName, "r")
fileOut = open(fileNameOut, "w")
i = 0
for line in fileIn:
    i += 1
    if i == 1:
        if line[0:8]!='<TICKER>':
            OnError("Проверьте заголовок файла")
    line = line.rstrip()    
    if line[0:8]=='<TICKER>':        
        sep = line[8:9]
        header = line.split(sep)
    else:        
        items = line.split(sep)
        for i in range(len(header)):
            #<TICKER>,<PER>,<DATE>,<TIME>,<OPEN>,<HIGH>,<LOW>,<CLOSE>,<VOL>
            #if header[i]=='<TICKER>':
            if header[i]=='<PER>':
                if items[i] == 'D':
                    items[i] = 'D1'
                if items[i] == '60':
                    items[i] = 'H1'
                TF = items[i]
            if header[i]=='<DATE>':                
                if items[i].find('-') == -1:
                    #230112
                    if len(items[i])==6:
                        items[i] = '20'+items[i][0:2]+'-'+items[i][2:4]+'-'+items[i][4:6]
                    elif len(items[i])==8:
                        items[i] = items[i][0:4]+'-'+items[i][4:6]+'-'+items[i][6:8]
                    else:
                        OnError("Проверьте формат даты")  
            if header[i]=='<TIME>':
                #if not (items[i] in ['00:00','00:00:00']):
                if TF in ['M5','M15','H1']:
                    items[i-1] = items[i-1]+' '+items[i]
            if header[i] in ['<OPEN>','<HIGH>','<LOW>','<CLOSE>']:
                items[i] = items[i].rstrip('0')
                items[i] = items[i].rstrip('.')
        #print(items)        
        fileOut.write(items[0]+';'+items[1]+';'+items[2]+';'+items[4]+';'+items[5]+';'+items[6]+';'+items[7]+';'+items[8]+'\n')    

fileIn.close()
fileOut.close()
print("Готово")
