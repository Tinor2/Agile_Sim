print("INITIAL DESCRIPTION HERE")
class step():
    def __init__(self, tracker:list,prelim, question, option1, option2, result1, result2):
        self.description = prelim
        self.question = question
        self.option1 = option1
        self.option2 = option2
        self.tracker = tracker
        self.result1 = result1
        self.result2 = result2
    def renderSteps(self):
        opt1_Inputs = ["y","1"]
        opt2_Inputs = ["n","2"]
        print(self.description)
        print(self.question)
        print(self.option1)
        print("OR")
        print(self.option2+'\n')
        while True:    
            awnswer = input("What do you choose? ").lower()
            if awnswer in opt1_Inputs+opt2_Inputs:
                break
            else:
                print("Enter Valid input")
        if awnswer in opt1_Inputs:
            print(self.result1)
            self.tracker.append(1)
        elif awnswer in opt2_Inputs:
            print(self.result2)
            self.tracker.append(2)
        return self.tracker
        

firstStep = step([],"Welcome to our game!\nYou are in a kitchen and you have two foods in front of you.", "Which one to eat? ", "An Apple","a serated knife","The apple tasted good", "The knife cut your mouth, that was a great choice genius.")
tracker = firstStep.renderSteps()
print(tracker)