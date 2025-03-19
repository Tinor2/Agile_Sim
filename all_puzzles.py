import random
import time 

def riddle_game():
    riddles = {
        "I stand with two arms, open or closed... What am I?": "Gate",
        "I slumber deep where treasures gleam... What am I?": "Dragon",
        "I hold a secret, locked away tight... What am I?": "Key",
        "I fall to ash, yet rise once more... What am I?": "Phoenix",
        "I'm a stick, but not for trees... What am I?": "Wand"
    }
    riddle, answer = random.choice(list(riddles.items()))
    attempts = 3
    while attempts > 0:
        print(riddle)
        user_answer = input(f"Your answer ({attempts} attempts left): ").strip().lower()
        if user_answer == answer.lower():
            print("Correct!")
            return True
        else:
            print("Wrong!")
            attempts -= 1
    print(f"Out of attempts! The answer was {answer}.")
    return False
 
def unscramble_word():
    words = {
        "TADNECNHE": "enchanted",
        "TYMHICAL": "mythical",
        "TOLARP": "portal",
        "GKNIDOM": "kingdom",
        "TGKNHI": "knight",
        "CSUER": "curse",
        "YRCOSER": "sorcery",
    }
    scrambled, correct_word = random.choice(list(words.items()))
    attempts = 3
    while attempts > 0:
        print(f"Unscramble this word: {scrambled}")
        user_guess = input(f"Your answer ({attempts} attempts left): ").strip().lower()
        if user_guess == correct_word.lower():
            print("Correct!")
            return True
        else:
            print("Wrong!")
            attempts -= 1
    print(f"Out of attempts! The correct word was {correct_word}.")
    return False
 
def guess_the_number():
    number = random.randint(1, 100)
    attempts = 6
    print("Guess the number between 1 and 100!")
    while attempts > 0:
        try:
            guess = int(input(f"Enter your guess ({attempts} attempts left): "))
            if guess < number:
                print("Too low!")
            elif guess < number:
                print("Too high!")
            else:
                print(f"Correct! You guessed it.")
                return True
            attempts -= 1
        except ValueError:
            print("Please enter a valid number.")
    print(f"Out of attempts! The correct number was {number}.")
    return False
 
def memory_challenge():
    words = ["Dragon", "Magic", "Castle", "Wizard", "Phoenix", "Knight", "Enchanted", "Portal", "Wand"]
    chosen_words = random.sample(words, 5)
    correct_guesses = 0
    wrong_guesses = 0
    used_words = []

    print("\n=== Memory Challenge ===")
    print("\nMemorize these words:")
    print("\n" + ", ".join(chosen_words))
    time.sleep(2.5)  # Show words for 2.5 seconds
    
    # Clear screen
    print("\033[H\033[J", end="")
    
    print("\n=== Memory Challenge ===")
    print("\nRecall the words one at a time!")
    print(f"Get 4 correct to win. 3 wrong guesses and you lose.")
    
    while correct_guesses < 4 and wrong_guesses < 3:
        word = input(f"\nEnter a word ({4-correct_guesses} needed to win, {3-wrong_guesses} attempts left): ").strip().lower()
        
        if word in used_words:
            print("\n🔄 You already used that word!")
            continue
            
        if word in [w.lower() for w in chosen_words]:
            print("\n✨ Correct!")
            correct_guesses += 1
            used_words.append(word)
        else:
            print("\n❌ Wrong!")
            wrong_guesses += 1
    
    if correct_guesses >= 4:
        print("\n🎉 Victory! You remembered enough words!")
        return True
    else:
        print("\n💔 Too many wrong guesses...")
        print(f"\n📝 The words were: {', '.join(chosen_words)}")
        return False
 
def quick_math():
    operations = ['+','-','*','/']
    Total_Problems = 6  # Changed from 10 to 6
    def generateProblem(minN, maxN):
        operation = random.choice(operations)
        num1 = random.randint(minN, maxN)
        while True:    
            num2 = random.randint(minN, maxN)
            if operation == '/' and num2 == 0:
                continue
            if operation == '/' and num1 % num2 != 0:
                continue
            break
        problem = f"{num1} {operation} {num2}"
        awnser = int(eval(problem))
        return problem, awnser

    incorrectGuesses = 0
    input("Enter to start the game: ")
    print("_"*100)
    start = time.time()

    for problemNum in range(Total_Problems):
        if incorrectGuesses > 4:  # Check for failure condition
            print("Too many incorrect answers! You failed.")
            return False

        problem, correctResponse = generateProblem(1, 10)
        while True:    
            print("Problem #"+ str(problemNum+1), end=": ")    
            guess = input(f"{problem} = ")
            if guess == str(correctResponse):
                print("Correct!")
                break
            elif guess == "q":
                return False
            else:
                incorrectGuesses += 1
                if incorrectGuesses > 4:  # Check again inside the retry loop
                    print("Too many incorrect answers! You failed.")
                    return False
                print("Incorrect. Re-attempt.")
        if guess == "q":
            return False

    print("_"*100)
    end = time.time()
    print("FINISHED. You had an accuracy rate of: ",end="")
    print(100-(incorrectGuesses/Total_Problems)*100, "%")
    print(f"Time taken: {end-start:0.2f} seconds")
    return True

def boss_puzzle():
    # Define the magical symbols and their valid text inputs
    symbols = {
        "🔥": ["f", "fire"],
        "💧": ["w", "water"],
        "🌍": ["e", "earth"],
        "✨": ["m", "magic"]
    }

    # Difficulty settings
    sequence_length = 3  # Starting sequence length
    max_rounds = 3       # Number of rounds to win
    time_limit = 8       # Time limit per round in seconds

    print("\n=== Spell Sequence Challenge ===")
    print("The boss casts a sequence of magical symbols. Memorize and replicate it!")
    print("Symbols: 🔥 (Fire), 💧 (Water), 🌍 (Earth), ✨ (Magic)")
    print(f"You have {time_limit} seconds to input each symbol.\n")
    time.sleep(2)

    for round in range(1, max_rounds + 1):
        # Generate a random sequence of symbols
        sequence = random.choices(list(symbols.keys()), k=sequence_length)
        print(f"\nRound {round}: Memorize this sequence!")
        print(" ".join(sequence))
        time.sleep(2)  # Show the sequence for 2 seconds

        # Erase the line with the sequence
        print("\033[F\033[2K", end="")  # Move cursor up and clear the line

        # Get player input
        print(f"Round {round}: Enter the sequence one symbol at a time.")
        player_input = []
        start_time = time.time()

        for i in range(sequence_length):
            # Prompt for each symbol in the sequence
            symbol_input = input(f"Symbol {i + 1}: ").strip().lower()
            elapsed_time = time.time() - start_time

            # Check if the player ran out of time
            if elapsed_time > time_limit:
                print("\n⏰ Time's up! The boss's magic overwhelms you.")
                return False

            # Validate the input
            valid_inputs = symbols[sequence[i]]
            if symbol_input not in valid_inputs:
                print(f"\n❌ Incorrect! The boss's magic strikes you.")
                print(f"The correct sequence was: {' '.join(sequence)}")
                return False

            player_input.append(symbol_input)

        # If the player completes the sequence successfully
        print("\n✨ Correct! You matched the sequence.")
        sequence_length += 1  # Increase sequence length for the next round

    # If the player completes all rounds successfully
    print("\n🎉 You defeated the boss's spell sequence challenge!")
    return True

# Store functions in a list without calling them
normal_puzzles = [
    riddle_game,
    unscramble_word,
    guess_the_number,
    memory_challenge,
    quick_math
]

# Boss puzzle stored separately
key_puzzles = [
    boss_puzzle  # Add your boss puzzle function here
]
