fileName = "DB\GC_H1_27122023_28122023.txt"
fileNameOut = "DB\GC_H1_Out.txt"
fileIn = open(fileName, "r")
fileOut = open(fileNameOut, "w")
for line in fileIn:
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
                    items[i] = items[i][0:4]+'-'+items[i][4:6]+'-'+items[i][6:8]
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
