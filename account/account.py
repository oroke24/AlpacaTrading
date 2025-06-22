from auth.connectClient import paperTradingClient
from auth.connectClient import liveTradingClient

class Account:
    def __init__(self):
        self.paperClient = paperTradingClient
        self.liveClient = liveTradingClient

    def menu(self):
        print("--Main Menu--")
        loopAgain = True
        while(loopAgain == True):
            print(
                "Menu Options: \n",
                "l: Live"
                "p: Paper"
                "q: Quit\n"
                ""
                  )
            option = input("Enter option: ")
            #exit case
            if (option == 'q'): 
                print("good bye!")
                loopAgain = False

            elif(option == 'l'): self.paperOptions()                
            elif(option == 'p'): self.liveOptions()

            else:
                print("Try Again")
                loopAgain = True
                

            
    def paperOptions(self):
        print("--Paper Menu--")
        print(
            "Options: \n"
            "r: Research"
            "b: Buy"
            "s: Sell"
            "q: Quit"
            )

    def liveOptions(self):
        print("--Live Menu--")
        print(
            "Options: \n"
            "r: Research"
            "b: Buy"
            "s: Sell"
            "q: Quit"
            )