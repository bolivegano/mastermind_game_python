import random
import sys
import pdb
from termcolor import colored


COLORS = ["R", "G", "B", "Y", "C", "M"]
TRIES = 8
CODE_LENGTH = 4
#CURSOR_UP = "\033[1A"
#CLEAR = "\x1b[2K"

#Generate a code sequence based on the length of the global variable. 
def generate_code():
    code = []
    for _ in range(CODE_LENGTH):
        color = random.choice(COLORS)
        code.append(color)

    return code

#user will guess the code, they must enter 4 colors with a space between each.
#if they enter more or less than 4 colors, the "continue" takes us back to prompt.
#if they do enter 4 colors, we loop through and see if those colors are in our global list.
#if the color is not in global list we break out of the for loop and this restarts the while loop.
#if we reach the final else statement it means we have satisfied the previous conditions
#we can then break out of the while loop?
def guess_code():
    while True:    
        guess_input = input("\nGuess a color sequence: ").upper()

        guess = []

        for character in guess_input:
            guess.append(character)

        if len(guess) != CODE_LENGTH:
            print(f"You must guess {CODE_LENGTH} colors.")
            continue

        for color in guess:
            if color not in COLORS:
                print(f"{color} is and invalid choice. Guess again.")
                break
        else:
            break

    return guess

def check_code(guess, real_code):
    #create an empty dictionary (keys, values), + counters for correct and incorrect positions
    color_counts = {}
    correct_pos = 0
    incorrect_pos = 0

    #loop through the generated code to add the colors and the number of times to the dictionary
    for color in real_code:
        if color not in color_counts:
            color_counts[color] = 0
        color_counts[color] += 1

    #use the zip function to join two interables together (our guess and actual code strings)
    #loop through the resulting tuple to see if the pairs of items at the same index match
    #if the colors match, increment the correct_pos variable.
    #if the colors match, decrement the dictionary count by 1 (NOT SURE WHY YET but I think
    # it is because if the position is correct, we want to assume that the color no longer
    # exists to check for new instances of that color becuase it is already matched in its location)
    for guess_color, real_color in zip(guess, real_code):
        if guess_color == real_color:
            correct_pos += 1
            color_counts[guess_color] -= 1

    #again use the zip function to join two iterables together (our guess and actual code strings)
    #loop through the resulting tuple
    #if the guessed color is in the color_counts dictionary 
    #and there is at least 1 number of it, we can say that this color is in the incorrect position.
    #if it were in the correct position, we would have decremented the dictionary count accordingly.
    #so we increment incorrect_pos variable.
    #now we decrement the color_counts for the guessed color, heres' why:
    #i think it's because of the scope of that for loop 
    # so if we guess Green and there is a Green one to match with 
    # (but in a different spot than our guess) we want to decrement that dictionary count 
    # so on the next time through this particular loop cycle, 
    # if we guessed another occurance of Green in our code guess it wouldn't 
    # still tell us there is a Green spot available if there was just 1 remaining on 
    # the previous time through the loop, for example.

    for i in guess:
        if i in color_counts and color_counts[i] > 0:
            incorrect_pos += 1

    return correct_pos, incorrect_pos

def game():
    print(f"\nWelcome to MASTERMIND. You have {TRIES} attempts to guess the color code sequence.")
    print("\nThe valid colors are:", *COLORS)
    
    code = generate_code()
    #print("\nfor testing purposes, this is the answer:", *code)
    for attempts in range(1, TRIES + 1):
        #pdb.set_trace()
        guess = guess_code()
        correct_pos, incorrect_pos = check_code(guess, code)

        #move cursor up one line
        sys.stdout.write("\x1b[1A")
        
        #clear line
        sys.stdout.write("\x1b[2K")
        
        print(f"____ [Colors in position: {correct_pos}] [Colors out of position: {incorrect_pos}]")
    
        sys.stdout.write("\x1b[1A")

        for i in range(len(guess)):
            if guess[i] == code[i]:
                if guess[i] == "R":
                    print(colored(guess[i], "red"), end="")
                if guess[i] == "G":
                    print(colored(guess[i], "green"), end="")
                if guess[i] == "B":
                    print(colored(guess[i], "blue"), end="")
                if guess[i] == "Y":
                    print(colored(guess[i], "yellow"), end="")
                if guess[i] == "C":
                    print(colored(guess[i], "cyan"), end="")
                if guess[i] == "M":
                    print(colored(guess[i], "magenta"), end="")
            else:
                print(colored(guess[i], "dark_grey"), end="")
        
        if correct_pos == CODE_LENGTH:
            print(colored(f"\nBOOM! You guessed the code in {attempts} tries.\n", "light_green"))
            break
    else:
        print("\nYou ran out of attempts. \nThe code was:", *code)


if __name__ == "__main__":
    game()