import time # importing various modules (time for animation)
import os #                             (Clearing the terminal)
import random #                         (probabillity)
import sys #                            (ending the program)
pathTracker = []
class exception(Exception): pass # Normal exception, used for when a invalid input is entered
class endException(Exception):pass # This condition will be used to restart the game when an ending is reached
os.system('cls' if os.name == 'nt' else 'clear') # clear the terminal when the
def answerProcess(initialA):
    initialA = initialA.lower() # lowercase the input
    if initialA in ["1","a","first","one"]: #Check whether the option chosen is valid between a variety of variations
        return 1
    elif initialA in ["2","b","second","one"]:
        return 2
    else:
        raise Exception() # if it is not within these options, call an exception, to allow for a retry
def colors(text:str = "", color = "plain"): # Allow for changing the colors of a text. Takes an input of a certain string, and then a color. The default color is plain
    color = color.lower()
    startingEscape = "\033[" # Uses tags that indicate different colors to change the color
    endingEscape = "\033[0m"
    options = {"plain":"37m", # Linking different colors with their corrosponding tags
               "red":"31m", 
               "green":"32m",
               "yellow":"33m",
               "blue":"34m",
               "magenta":"35m", 
               "cyan":"36m"}
    if color in options:    
        colorToken = options[color] # find the tag based on the input 
    else: 
        colorToken = options["plain"] # If there is any misspellings, it will just show it to be plain
    text = startingEscape + colorToken + text + endingEscape # add in the tags
    return text
def typing(text:str, delay:float = 0.005): # An animation of 
    finalChar =  text[-1] # get the 
    text = text[:-1] # remove the last charactar from the string
    for char in text:
        print(char, end='', flush=True) #Print the char, without creating a new line in the terminal
        time.sleep(delay) #Delay for a momment
    print(finalChar)
def endCondition(optionsChoosen): # Raise an exception to restart the main script, and start a new game afresh
    displayList = input("Would you like to see the options you choose?")
    if displayList in ["y","yes","t","1"]:
        typing(colors(str(optionsChoosen),"magenta"))
    retry = str(input("Would you like to play again, and achieve all of the endings? "))
    retry = retry.lower()
    if retry in ["y","yes","t","1"]: #If affirmitive action is provided, restart the program
        raise endException()
    else:
        sys.exit("ENDING PROGRAM...") # Otherwise quit the program
def step(prelim:str,question:str, result1:str ,result2:str="deFault", prelimTrue:bool = True,): # A template for every single step used later. Consisted with a preliminary statement (which can be toggled), the question, and the two different resutls. 
    if prelimTrue: # If a preliminary statement is required before the question itself, display this text in a plain color
        typing(colors(prelim, "plain"))
    while True:
        try: # using a try loop to deal with any possible errors.
            typing(colors(question,"cyan")) #display the question in cyan
            answer = input("") # record the awnser
            answer = answerProcess(answer) #process the awnser
            if answer == 1 or result2 == "deFault": # if there is no result 2 (no matter the awnser gien to the question, the same result is achieved)
                pathTracker.append(1) # Store this result in a list, as a method of having a memory of previous choices
            elif answer == 2: 
                typing(colors(result2,"magenta"))
                pathTracker.append(2) 
            else:
                raise exception() # Raise an exception if the answer is invalid.
        except:
            print("That's an invalid input, try again.") #Ask the question again, after notifiying the user
        else:
            break #break out of the forever loop if it is exeecuted perfectly
    input("...")
def attackingOrFearingLaboon(pathTracker:list): #1 in 5 chance of option 1 (surviving), 4 in 5 chance of option 2, unlcoking a new ending (perishing)
    if random.randint(1,5) == 1: # Choose a random number from 
            entry = "With an incredible strock of luck, the whale does not fully submerge, buying you valuable time! \n\
You decide to look around to utilze this precious luck. You notice a trapdoor ahead. You shake your head to remove your previous fright."
            typing(colors(entry,"green")) # Use green to siginfy the positive outocme
            firstChoice = pathTracker[0] # Creating a new tree, in order to revert to a previous choice (n,1,2,1)
            pathTracker = [firstChoice,1,2,1]
    else:
        typing(colors("You perish in the waves of the sea, drowning before your story can really begin\nPERISH ENDING","red")) # Ending
        endCondition(pathTracker) # Raise an endCodnition exception, triggers the ending of a loop, and gets the program to ask for a restart
def introStep(): # first step, where player chooses their charactar and the player creates their first decision
    cowardCounter = 0 
    typing("You are a Straw Hat pirate, recruited by the soon-to-be Pirate King, Monkey D. Luffy") # preliminary
    typing(colors("Which straw hat are you? \n(hint: choose between Zoro, Nami, Sanji, or Ussop)", "cyan")) # asks a question 
    strawHat = input("")
    strawHat = strawHat.lower()
    strawHatOptions = ["zoro","nami","sanji","usopp"] # all of the possible options for which straw hat can be choosen
    formattedStrawHats = ["Zoro","Nami","Sanji","Usopp"] # Formatted list
    if strawHat not in strawHatOptions:
        raise exception("") # if a wrong name is typed, restart the intro step
    else:
        strawHat = formattedStrawHats[strawHatOptions.index(strawHat)] # otherwise, set a variable name to the formatted version of the choice made
    if strawHat == formattedStrawHats[3]:
        cowardCounter += 1 # If the strawhat is usopp, add a cowardCoutner 
    entry = "\
Alright "+strawHat+ ", it's finally time to enter the Grand Line!\n\
Ahead of you is the daunting entrance point" # introduction 

    typing(entry)
    print("              ", end='', flush=True)
    entry = "●> REVERSE MOUNTAIN <●"
    typing(colors(entry,"yellow")) # INtroduction prelimintary
    entry = "The Going Merry has just emerged from the Calm belt, surrounding the Grand Line. \n\
After going through the reverse mountain, there won't be any going back! "
    entry1 = "Do you choose to travel up the mountain, or will your fear get the better of you?"
    result = "You yell in  encouragement as the Going Merry enters the ravegous stream, laughing with excitement as the Merry is launched up the mountain"
    result1 = "You try to yell at Luffy, that the Merry won't survive this journey. \nHe just turns and laughs in your face, a huge grin stretching across the captains face. \nYou cowardly scream as the ship gets launched up the mountain, wondering why you listened to a random pirate "
    step(entry, entry1, result, result1,True)
    if pathTracker[-1] == 2: # if the cowardly option is chosen, increase the coward Counter     
        cowardCounter += 1
    typing(colors("You all survive the journey","green"))
    input("...")
    return cowardCounter # allow for the rest of the code register

typing(colors("This is a ONE PIECE inspired choose your own adventure!","yellow")) # introduction briefing: Provide rules and notes
typing(colors("You will be presented with multiple decisions as you progress through the straw Hat's journey. ", "yellow"))
typing(colors("""Choose "1" for the first option presented, and "2" for the second option. 1 is also equivelent to YES and 2 is equivelent to NO""", "blue"))
typing(colors("""Try not to type anything while the game is generating text, as this will register as your actual input.""", "blue"))
typing(colors("Let your journey begin!","green"))
print("____________________________________________________________________________________________________")
print()
cowardCounter = 0 # reset the coward counter to 0
while True: # Loops as long a break argument is never called
    try:   
        while True:
            try:
                cowardCounter = introStep() # run the intro step
                
            except exception:
                print("That was incorrect input, please repeat") # if any problem occurs in the intro step, retry the intro step
            else:
                break # otherwise break out of the intro step loop
        
        entry = "Upon entering the base of the mountain, your passage is blocked by a massive whale, with scars on it's head. \n\
It lets out a massive groan and ram's it's head into the mountain, sending rocks and boulders tumbling down"
        entry1= "Do you choose to fight or hide"
        result1 = "You, along with the captain, prepare for a battle with this fearsome whale.\n\
You and the captain yell angrily, and send an impact hurling towards the behemoths eye"
        result2 = "You cowardly hide on the Going Merry. The monster opens it's mouth, \
and you and the crew get sucked inside the monster."
        step(entry,entry1,result1,result2) # Run the first choice
        if pathTracker[-1] == 1: # if the latest choice was choice number 1
            entry = "The whale becomes enraged, and opens it's mouth, swallowing everyone except for you and the captain."
            entry1 = "Do you investigate the whale you find yourself standing upon, or angrily fight the monster?"
            result2 = "The leviathin, growing tired of your feeble attempts, yells out a massive roar, and dives begins to dive \
underwater."
            result1 = "After quickly looking around, you notice a trapdoor on the whale's back"
            step(entry,entry1,result1,result2) # then ask the player whether to invesitgate or fight the whale 
            if pathTracker[-1] == 2: # if the fight option is called, the run the random option
                attackingOrFearingLaboon(pathTracker)
            elif pathTracker[-1] == 1:
                entry = ""
                entry1 = "Do you dive through this strange trapdoor, or are you too scared to enter?"
                result1 = "You dive into the trapdoor and seal the door before Laboon can once again submerge into the depths, saving you from drowning."
                result2 = "Paraylsed in fear, you stay still"
                step(entry,entry1,result1,result2, False)
                if pathTracker[-1] == 2: # If the player freezes up, run the random option anyways, as the same result is incited
                    cowardCounter += 1
                    attackingOrFearingLaboon(pathTracker)
                typing(colors(entry,"magenta")) 
            else:
                endCondition(pathTracker)
            if pathTracker[-1] ==2:
                typing("You dive into the trapdoor and seal the door before Laboon can once again submerge into the depths, saving you from drowing.")
            entry = "In the hallway, you notice a little ahead, there is another trapdoor heading below."
            entry1 ="Do you drop down below, or are you too scared to take a leap of faith? "
            result1 = "The captain, before you can even blink, laughs delirously, and pushes you down the trapdoor, tumbling out behind you. \nYou both crash on a beach island, dazed and stunned. You both recover and get up."
            step(entry, entry1, result1)
            if pathTracker[-1] == 2:
                cowardCounter += 1

        elif pathTracker[-1] == 2: # if the player decides to hide instead of fighting, they get swallowed by the whale
            cowardCounter += 1 # increase the coward counter
            typing("After sitting there, blankly looking around you see figures in the distance.")
        typing(colors("The rest of the crew is coming towards your position!","green")) # This is the point where both paths converge (assuming the PERISH ENDING was not achieved)
        input("...") # create a pause
        typing("After looking around for a momment, you notice a man sitting on a beach chair. You begin to approach him.") # introduction of crocus
        entry = "The man introduces himself as Crocus, a mysterious retired pirate! \nAfter a tense introduction, he agrees to assist the crew."
        entry1 = "Do you agree for Crocus's help?"
        result1 = "Crocus explains how the whale's name is Laboon, and how he keeps the whale alive as it's surgeon, while it waits for a mysterious group of friends to eventually return. \nCrocus had engineered a trapdoor to exit Laboon's body. He directs the entire crew to the exit."
        result2 = "I dont know why you didn't get his help, honestly."
        step(entry,entry1,result1,result2)
        if pathTracker[-1] == 2:
            typing(colors("You died what else did you expect?\nSTUPID ENDING","red")) # Creates the stupid ening
            print("⣿⣻⣿⣿⡟⠀⠀⠀⠀⠀⠀⢀⣴⣿⡿⢟⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢫⣊⣽⣵⠖⠀⠻⣿⣿⣿⣿⣿⣿⣯⢻⣿⣷⠀⠀⠈⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀⠀⠀⠙⠳⣄⠀⠀⠀⠀⠀⠀⠀⠀⣐⢣\n\
⣿⣷⣻⣿⠁⠀⠀⠀⠀⠀⣰⣿⠟⠉⢐⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠜⣫⣿⢯⡞⠀⠀⠹⣿⣿⣿⣿⣿⣿⠀⢿⣿⡄⣀⣴⣟⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣄⠀⠀⠀⠀⠈⠂⠀⠀⠀⠀⠀⠀⠀⢆⢧\n⣿⣿⣷⠉⠀⠀⠀⠀⢀⡾⠋⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢻⣿⣿⣇⣴⢏⣵⢏⠀⠀⠀⠀⠹⣿⣿⣿⣿⣿⠀⠈⢿⣧⠓⢉⣯⢧⢿⣿⣿⣿⣿⠌⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢈⡜⣎\n\
⣿⣿⣿⠀⠀⠀⠀⠀⠋⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⠇⣼⣷⠟⠁⠀⢀⡴⢃⠀⠹⣿⣿⣿⣿⡃⠀⠈⣿⡔⠋⣡⢣⣾⠿⣿⣿⣿⡃⢸⣿⣿⣿⣿⣿⣿⣿⣿⣷⡈⢻⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠜⣲\n⣿⣿⡯⠀⠀⠀⠀⠀⠀⠀⠀⢀⢮⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣗⣿⣿⣿⠾⠋⠁⠀⣠⢞⡿⡵⡻⣂⠀⢹⣿⣿⣿⡇⠀⣴⡻⣷⣔⣯⢾⠵⢫⢿⣿⣿⠅⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠙⢿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⡜⣸⡱\n⣞⣿⡃⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿⢟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢨⡗⣿⣿⠀⠀⠀⠈⠙⢫⢋⣼⣿⡛⠀⠀⢻⣿⣿⡆⠀⠙⣡⣼⣾⢜⣣⢔⣵⣫⣿⣿⡁⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀⠻⣿⠀⠀⠀⠀⠀⠀⠀⠀⠰⢨⣱⢹\n\
⣿⠼⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⡿⠟⠁⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠈⠀⢻⣿⢀⣀⣀⣀⠤⢤⣉⣁⠈⠛⠃⠀⠘⣿⣿⠇⠀⠀⠀⠀⣈⣧⣉⣛⣑⣛⡍⢿⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣄⠀⠚⣧⠀⠀⠀⠀⠀⠀⢀⢃⠳⣬⠳\n⣿⠃⠀⠀⠀⠀⠀⠀⢀⣾⠟⠋⠀⠀⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠐⠒⢻⣿⠁⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⡹⣿⡃⠀⠀⠉⠉⠁⠀⠀⠀⠀⠀⠈⠹⠉⠓⠂⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀⠀⠑⠀⠀⠀⠀⠀⠄⣎⢳⡜⡳\n⣿⠁⠀⠀⠀⠀⠀⠀⠋⠁⠀⠀⠀⢀⢼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡗⠀⠀⠈⣿⣀⡤⠠⠄⠤⣀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠅⢠⠄⠀⠀⣴⣒⠶⠭⠤⢄⣀⡀⠀⠀⠀⢸⡏⢿⣿⣿⣿⣿⣿⣿⣿⠈⠻⣿⣷⣄⠀⠀⠀⠀⠀⢀⡚⣬⢳⣚⠵\n⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡌⢢⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⢀⣨⣟⠶⠶⠉⠛⠓⠭⣍⣉⠒⠀⠀⠀⠀⠀⠸⠇⡞⠀⢒⡩⢕⡒⠐⠂⠒⠒⠒⠪⢅⡀⠀⢸⠀⢸⣿⣿⣿⣿⣿⣿⣿⡇⠀⠈⠙⢿⣮⣢⣄⠀⡐⢬⡺⡵⣏⢮⡓\n\
⡗⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⡄⣻⣿⣿⣿⡿⣻⣿⣿⣿⣿⣿⣿⢻⣿⣿⡇⣠⠟⣉⣀⣀⣀⡠⠄⣀⣀⠈⡙⠻⠄⠀⠀⠀⢀⣴⢿⠃⢰⣟⠫⠥⠤⠠⢠⣤⠠⠤⠤⣀⡉⠂⠀⠀⠘⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀⠈⠪⠝⠿⣽⣰⢣⣟⡽⣎⠷⡡\n⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡘⢰⣻⣿⣿⡟⠁⣿⣿⣿⣿⣿⣿⣿⠈⣿⣿⡟⠫⠥⠤⠤⠼⠿⠧⠤⠔⢒⡋⠁⠀⠀⠀⠀⠀⠉⣼⣻⠀⠘⠫⢔⣒⡒⠠⠼⢟⢣⢖⣒⠒⠋⠁⢀⠀⢨⣿⣿⣿⣿⡝⣿⣿⣿⠀⠀⢀⠠⡐⣋⠖⣼⣻⠿⣼⢯⡝⣧⠑\n\
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡱⠌⣿⣿⡟⠀⢸⣿⣿⣿⣿⣿⣿⣿⡀⢹⣿⡗⠈⠓⠒⠒⠒⠒⠒⠲⠟⠛⢉⣵⡦⣶⠀⠀⠀⠀⠉⣟⠀⠀⠙⠒⠒⠠⠍⠻⡤⠂⠒⠲⡖⠋⠉⠉⠀⢸⣿⣿⣿⣿⡇⠸⣿⣿⡃⠰⣌⠲⡱⡜⣾⣱⢯⡿⡽⣾⡹⢆⡍\n\
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⢑⡀⣿⡟⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⢿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠟⠁⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⠀⠀⠈⠁⠀⠀⠀⠉⠀⠀⠀⠀⣾⣿⣿⣿⣿⣷⢐⢻⣿⣇⠳⣌⡳⣽⣹⢾⣽⢯⡿⣽⢶⡛⢦⠐\n\
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⢢⠀⣿⠁⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠸⢿⠀⠀⣀⠀⣀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⠀⠀⠀⠀⠹⠰⢤⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⢻⣿⣿⣿⣿⣿⣎⡽⣿⣧⣛⡼⣳⢷⣯⡿⣯⡿⣽⡳⣯⢝⠢⡁\n\
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⡠⢈⠃⢠⣾⡿⠋⢁⣿⣿⣿⡿⣿⣿⣷⠀⠀⠈⣀⣼⣥⢞⣅⠀⠀⠀⠀⠀⠀⡰⠋⢉⣉⡀⠀⠀⠀⠀⢀⣠⣀⠀⠹⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡿⠿⠳⣿⣿⣷⣽⣻⡷⣾⢽⣯⣿⢾⣟⣷⣻⡗⣿⡱⣎⠱⡀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⢁⠂⣾⡿⠋⠀⠀⢸⣿⣽⢱⢲⡌⠻⣿⣇⢰⡾⣟⣷⡟⣫⠞⠀⠀⠀⠀⠀⠀⢧⡀⢾⣿⣿⠀⠀⠀⠠⣻⣿⡿⢂⡴⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⡴⣾⢣⢹⣿⢿⡿⣟⡿⣽⣻⢾⣽⣻⢞⡷⣯⢟⡾⣱⢎⠱⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠃⠄⠁⠀⠀⠀⢀⠀⢻⢿⠀⢸⣽⣆⢹⡹⠀⢀⣼⣷⠿⣫⠀⡀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣯⣶⣿⠀⣾⣿⣻⣽⢿⣽⣳⣯⣟⡾⣽⢯⡿⣭⣟⣞⡳⢎⠢⠁\n\
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⣈⠂⠄⠀⠀⠀⠈⠀⠀⢪⢧⠘⣧⣻⣀⡇⠀⠚⡡⢋⣴⡷⣻⡧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣼⡧⠏⣰⣿⣳⣟⡾⣯⣟⣷⣻⢾⡽⣯⢷⣻⣳⡽⢮⡝⢎⡰⠁\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠐⣄⠊⠄⠀⠀⠀⠀⠀⠀⠀⠩⡳⣀⠉⠙⠻⡄⠀⣵⣿⡯⣺⣿⡥⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢤⠋⢀⣠⢞⡏⢷⣛⡾⣽⣳⣟⡾⣽⢯⡿⣽⢯⣷⣻⡼⣻⡜⣡⠂⡁\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠌⡰⢈⠄⠀⠀⠀⠀⠀⠀⠀⠀⠉⡈⠳⢦⣄⣹⡄⠑⠋⠈⠙⠋⠓⠀⢀⣀⡤⠴⢖⡒⣒⢒⡒⣒⢒⡒⢖⠲⡒⢦⠤⣤⣄⣀⣀⠀⠀⠀⠀⠀⠀⣠⠞⢒⠫⡐⢊⠜⣢⢛⡼⢳⣛⡾⣽⢯⡿⣽⢯⣟⣾⣳⡽⣣⠟⡤⠁⠄\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⡑⢌⠐⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡑⢢⠐⡀⠙⢦⡀⠀⠀⠀⠀⠐⠛⠓⠚⠓⠒⠓⠚⠒⠓⠞⠦⠙⠮⠱⠭⠖⠳⠴⠒⠦⠭⠟⠂⠀⠀⢀⡴⠃⠁⠀⠁⡘⠄⢊⢄⠣⢜⠣⣏⡽⣏⡿⣽⢯⣟⡾⣷⢯⣷⢫⣝⡰⢁⠀\n\
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⡑⢌⠂⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠢⠑⠄⠂⠀⠙⢦⡀⠀⠀⠀⠀⠀⠉⠒⠒⠦⠤⠤⠤⢀⣀⣀⠀⡀⣀⢀⡠⠤⠤⠀⠀⠀⠀⣠⠴⠋⠀⠀⠀⠀⠀⠀⠈⠀⠌⠒⡈⠱⢌⡚⣭⢻⣽⣻⢾⡽⣯⣟⡾⣝⢦⡑⢂⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡜⢠⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠡⢈⠐⠀⠈⠐⣙⢳⡤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⠴⠚⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⢁⠂⡱⢌⡻⣜⣯⠿⣽⣳⢯⡽⣞⢧⡙⠄⠂\n\
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠜⣄⠊⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠂⠄⠀⠁⢆⠣⣜⠢⡉⠙⣶⢦⣤⣄⣀⣀⣀⡀⣀⣀⣀⣀⣤⡤⠴⠒⠋⠍⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⢀⠢⠱⣙⢮⢿⡽⢯⣻⡽⣝⡮⡕⢊⠄\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢭⠰⡈⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠈⢄⠫⡔⢣⠐⠀⢸⣎⡜⡹⢻⢿⣿⣿⣿⣿⣿⠟⣻⠁⠀⠀⠀⠒⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠑⡌⢾⡹⣞⣯⢷⣻⡝⣾⣉⠆⡀\n\
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢊⠵⣁⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠈⡕⣪⢅⠊⠀⠸⡝⢶⣡⢃⡎⡜⣩⢫⡑⢦⣹⢾⠀⠀⠀⠀⡁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⡰⣙⠾⣽⣞⣳⣻⠵⣍⠖⡀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢜⡢⢅⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢈⠒⡥⣊⠔⠀⠀⡇⠀⠙⢶⣸⡰⢡⢆⣹⠖⠃⢸⠀⠀⠀⠀⡐⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠡⠐⣩⢛⡼⣞⣳⣭⠿⣜⢣⠐\n\
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢪⡜⡥⠊⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡉⢖⡡⢊⠀⠀⡇⠀⠀⠀⠀⠉⠉⠉⠀⠀⠀⢸⠄⠀⠀⠀⠐⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠠⢋⡼⢭⣳⣭⢟⡼⢢⠁\n\
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⢡⢚⡴⡁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣢⢑⠢⠀⢀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⢸⡆⠀⠀⠀⠐⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠂⡜⢣⢗⣮⢻⣜⠣⠌\n\
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⣈⠞⡴⣁⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⢎⡁⠂⢸⠃⠀⠀⠀⠀⠀⠀⠀⠀⣴⠇⠸⡇⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠡⠘⠤⣋⢼⡳⢮⣙⠂\n\
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠡⣀⠻⡴⣁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⣌⣧⣘⡀⡟⠀⠀⠀⠀⠀⠀⠀⠀⣴⣿⠇⠀⢿⡂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢁⠂⡱⢪⣝⡳⣌⠣\n\
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠁⠤⣛⠴⣁⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣾⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⣠⠞⣱⠗⣳⡄⠘⣧⣶⣶⣷⣶⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠂⡁⠳⣌⠷⣭⠒\n\
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠤⢁⠲⣍⠷⣀⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣶⣿⣿⣿⣿⣿⠿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠸⣾⠕⣹⣟⣴⠆⠘⢏⠙⢿⣿⡿⣿⣶⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢈⠱⡌⣟⢶⡩\n\
⠀⠀⠀⠀⠀⠀⠀⠀⠠⡘⢀⠲⣭⡳⡅⠀⠀⠀⠀⣠⣤⣤⣤⣤⣴⣶⣶⣿⣿⣿⣿⣿⣿⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⣰⠟⡵⢃⣤⠏⡀⠓⠌⣻⣿⣟⣿⣿⣿⣿⣶⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠒⡸⢬⣳⢣\n⠀⠀⠀⠀⠀⠀⠀⠀⠤⡑⠂⡜⣶⡻⡔⣁⡤⠤⠚⣿⣿⣿⣿⢿⣻⣿⣻⣿⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠞⢡⡮⠔⢡⢫⡿⠃⠀⠀⠀⢿⣿⣻⣿⣿⢿⣿⡿⣿⣿⣿⣶⣶⣾⣶⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠣⢏⡾⣱\n\
⠀⠀⠀⠀⠀⠀⠀⢀⠢⢡⠁⣼⣳⠟⠋⠁⠀⠀⠀⣿⣿⣿⣿⣻⣿⣳⣿⣿⣻⣯⣿⡏⠒⠲⠤⠤⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠰⢃⣉⡤⠤⠤⠴⠒⠚⣿⣿⣽⣿⣿⣿⣿⣟⣾⡿⣽⣿⢿⣿⣿⣷⠢⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣍⢺⡱⢧\n⠀⠀⠀⠀⠀⠀⠀⢀⠎⣐⡶⠋⠀⠀⣀⠀⠀⠀⠀⢼⣿⣿⡿⣽⣷⣿⣿⣻⣽⣷⡿⠁⠀⠀⠀⠀⠀⠀⠙⢦⠀⠀⠀⠀⠀⠀⠀⠀⣠⠞⠉⠀⠀⠀⠀⠀⠀⠀⢸⣿⣯⣿⣿⣿⣿⣿⣯⣿⣟⣯⣿⣿⣷⣿⡆⠀⠉⠲⢄⡀⠀⠀⠀⠀⠀⠀⣂⠧⡝⣧\n\
⠀⠀⠀⠀⠀⠀⠀⢢⡼⠋⠀⢀⡠⠞⠁⠀⠀⠀⠀⣾⣿⣿⡿⣿⣽⣾⣟⣿⣽⣾⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⠒⠀⠀⠀⠀⠀⠾⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⣽⣿⣿⣯⣿⣿⢷⣿⣻⣽⣿⣯⣿⡇⠀⠀⠀⠀⠉⠢⣄⠀⠀⠀⠀⢄⠫⡼⣱\n⠀⠀⠀⠀⠀⠀⣰⠏⢀⣠⢔⡋⠀⣀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣻⣽⣾⢿⣽⣾⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡎⢸⣿⣯⣿⣿⣿⣿⣾⢿⣻⣿⣽⣿⣿⣽⣿⠀⠀⠀⠀⠀⣠⢼⠗⣤⠀⠀⢀⢣⢳⡱\n\
⠀⠀⠀⠀⠀⡴⠃⡨⠏⣡⣫⠔⠋⠁⠀⠀⠀⠀⢰⣿⣿⣿⣷⣿⣻⣽⡿⣯⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⢞⠝⣜⣨⣿⣿⣽⣿⣿⣿⣾⡿⣟⣷⡿⣽⣿⡿⣿⠀⠀⠀⡴⠊⠱⢃⣞⠴⡷⣄⠀⢎⠲⣍\n⠀⠀⠀⠀⡼⠑⣊⠤⢚⡥⣊⡀⠀⠀⠀⡀⠀⠀⢸⣿⣿⣿⡾⣟⣿⣽⣿⣻⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⠃⣎⠜⣫⡠⣿⣿⣽⣿⣷⣿⣿⢿⣟⣯⣿⡿⣿⣿⢿⡇⠀⠀⠀⢠⠴⠊⠁⠼⣵⡏⡳⣌⠳⣌\n\
⠀⠀⠀⡼⠁⠀⢠⠔⢉⢴⠟⠀⣀⡴⠚⠁⠀⠀⣿⣿⣿⣷⡿⣿⣯⣿⢾⣟⣿⠀⠀⠀⠀⠀⠀⢀⡴⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢠⠞⢁⢞⡕⢡⣿⣿⣽⣾⣿⣯⣿⣿⣿⣻⣷⣿⣿⡿⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⠀⠈⢷⡌\n\
⠀⠀⣰⠃⠀⠀⠀⠀⠑⢃⡤⡞⠁⠀⠀⠀⠀⢸⣿⣿⣿⢷⣿⣟⣷⡿⣿⣻⣿⡀⠀⠀⠀⠀⢶⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⣿⡇⢸⣿⡿⣾⣟⣿⣻⣽⣿⣷⣿⣻⣾⢿⣿⣟⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻\n\
⠀⢀⠃⠀⠀⠀⢀⡠⠖⣡⢞⠤⠀⠀⠀⠀⢀⣿⣿⣿⣿⣻⣽⣾⣟⣿⣟⣯⣿⣧⠀⠀⠀⠀⠈⢛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠴⠃⠀⠀⠀⠀⠀⠀⠀⠈⠀⣾⣿⣟⣿⣽⣟⣿⣻⣿⣿⢾⡿⣽⣿⣿⡿⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
            #ascii art
            endCondition(pathTracker) # call an ending exception
        if cowardCounter >= 3: # if you have choosen to many cowardly options, you unlcok the DOCTORS ASSISTANT ENDING, (Crocus is a doctor himself)
            typing("""As the crew emerges out of the exit, Crocus holds you behind. He looks at your fearful eyes, and shakes his head.\nHe says, "a coward like you is not ready for the Grand Line. I needed an assistant anyways!".""")
            typing(colors("You are left behind as the rest of the leave the clutches of Laboon.\nDOCTORS ASSISTANT ENDING","red"))
        else: 
            # otherwise a positive ending is achieved, similiar to the canon of the actual show
            typing(colors("The entire crew emerges out of the whale, having faced their first threat of the Grand Line. The journey to Laugh tale begins now!\nTHE JOURNEY BEGINS ENDING", "green"))
        endCondition(pathTracker)
    except endException:
        # whenever an endException is called, this means that the player has chosen wheter or not to see their option they have choosen, and they have choosen to replay
        cowardCounter = 0 # reset the cowardCounter to create fresh start
        pathTracker = [] # reset the path tracker
