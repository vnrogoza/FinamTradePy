title = "Привет"
def start():
    print("Starting...")

def GetToken():
  file = open("token.txt", "r")
  token = file.readline()
  return token

if __name__ == "__main__":    
    start()
    #print(GetToken())