import json
import sys
import random
from fuzzywuzzy import fuzz

with open('data.json', 'r') as f:
  data = json.load(f)

def check_valid_continent(chosen_continent, data):
    while chosen_continent.capitalize() not in data.keys():
        chosen_continent = input("\nSorry that is not a valid response. Please choose one of the follwoing continents: \n{}\n\n".format('\n'.join(data.keys())))
    return chosen_continent.capitalize()

def ask_question(data, chosen_continent):
    correct_answers = 0
    total_questions = len(data[chosen_continent])
    random.shuffle(data[chosen_continent])
       
    for i in data[chosen_continent]:
        answer = input('What is the capital city of {}\n'.format(i['Country']))
        if answer.lower() == i['Capital'].lower():
            print("Well done! That is correct.\n")
            correct_answers += 1
        elif fuzz.ratio(answer.lower(), i['Capital'].lower()) != 100 and fuzz.ratio(answer.lower(), i['Capital'].lower())> 90:
            print(f"Hmmm I'll give you this one, but the correct spelling is {i['Capital']}.\n")
            correct_answers += 1
        else:
            print(f"Sorry, the correct answer is {i['Capital']}\n")
    
    return correct_answers, total_questions
        
def display_score(correct_answers, total_questions):
    print(f"You got {correct_answers} out of cities {total_questions} correct.")

def score_the_game(correct_answers, total_questions):
    print('\nResult:')
    if correct_answers / total_questions == 1:
        display_score(correct_answers, total_questions)
        print('Wow, you really know your stuff. Very Impressed!')
    elif correct_answers / total_questions > 0.7:
        display_score(correct_answers, total_questions)
        print('Quite the geographer we have here. I am impressed')
    elif correct_answers / total_questions > 0.5:
        display_score(correct_answers, total_questions)
        print('Not bad, not bad at all.')
    elif correct_answers / total_questions > 0.4:
        display_score(correct_answers, total_questions)
        print('Admirable attemp young Grasshopper. Though there is yet room for improvement.')
    else:
        display_score(correct_answers, total_questions)
        print('Looks like you need a little more practice.') 

def play_again():
    play_again = input("Do you want to play again? Please enter 'Y' or 'N'\n")
    
    while play_again.lower() not in ['y', 'n']:
        play_again = input("Please type 'Y' to continue or 'N' to quit\n")

    if play_again.lower() == 'y':
        return True

def leave_game():
    print("\nThat's too bad. Come back when you want to play again. Bye!\n")
    sys.exit()
    
def main():
    print("""\n~~~~~~~~~~~~~~~~~~~~~~~ Capital City Challenge ~~~~~~~~~~~~~~~~~~~~~~~\n""")
    while True:
        #ask user to choose a contient
        chosen_continent = input("Choose a chosen_continent:\n{}\n\n".format('\n'.join(data.keys()))).capitalize()
        # checks if user chose a valid chosen_continent
        chosen_continent = check_valid_continent(chosen_continent, data)
        print(f"Cool. You've Chosen {chosen_continent.capitalize()}. Let's see if you know your stuff.\n")
        # asks the user questions and keeps track of score
        correct_answers, total_questions = ask_question(data, chosen_continent)
        #prints the score
        score_the_game(correct_answers, total_questions)
        #asks user if they want to play again
        if not play_again():
            leave_game()
            break
        
main()
