import requests
import sys
import random
from fuzzywuzzy import fuzz

def check_if_user_wants_to_play():
    wants_to_play = input()
    while wants_to_play.lower() not in ['yes', 'no']:
        wants_to_play = input("Sorry that is not a valid option. Please choose 'yes' or 'no'\n")
    return wants_to_play

def leave_game(wants_to_play):
    print("'\nThat's too bad. Come back when you are ready to play.'")
    print('\nBye!')
    sys.exit()

def check_valid_continent(continent, continents):
    while continent.capitalize() not in continents:
        continent = input("Sorry that is not a valid response. Please choose one of the follwoing continents: \n{}\n\n".format('\n'.join(continents)))
    return continent

def ask_question(data):
    correct_answers = 0
    total_questions = len(data)
    random.shuffle(data)
       
    for item in data:
        answer = input('What is the capital city of {}\n'.format(item['name']))
        if answer.lower() == 'quit':
            wants_to_play = 'no'
            leave_game(wants_to_play)
        elif fuzz.ratio(answer.lower(), item['capital'].lower()) > 90:
            print("Well done! That is correct.\n")
            correct_answers += 1
        else:
            print("Sorry, the correct answer is {}\n".format(item['capital']))
    
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
    wants_to_play = input("Do you want to play again? Please enter 'Yes' or 'No'\n")
    
    while wants_to_play.lower() not in ['yes', 'no']:
        wants_to_play = input("Please type 'yes' or 'no'\n")
    
    return wants_to_play
    
def main():
    print("Hey!\nWelcome to Capital City Challenge!\nAre you ready to play? Yes or No")
    wants_to_play = check_if_user_wants_to_play()
    if wants_to_play.lower() == 'no':
        leave_game(wants_to_play)
        
    while wants_to_play.lower() == 'yes':
        print("\nCool let's play!")
        #ask user to choose a contient
        continents = ['Africa', 'Asia', 'Europe', 'Americas', 'Oceania']
        continent = input("Choose a continent:\n{}\n".format('\n'.join(continents)))
        # checks if user chose a valid continent
        continent = check_valid_continent(continent, continents)
        print("Cool. You've Chosen {}. Let's see if you know your stuff.".format(continent.capitalize()))
        print("Psss type 'quit' if you get bored and wat to exit game.\n")
        #gets data from Countries Api and converts it to JSON format
        res = requests.get('https://restcountries.eu/rest/v2/region/{}?fields=name;capital'.format(continent))
        data = res.json()
        #asks the user questions and keeps track of score
        correct_answers, total_questions = ask_question(data)
        #prints the score
        score_the_game(correct_answers, total_questions)
        #asks user if they want to play again
        wants_to_play = play_again()
    else:
        leave_game(wants_to_play)
        
main()
