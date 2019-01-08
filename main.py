import requests
import sys
import random
from fuzzywuzzy import fuzz

def check_valid_continent(continent, continents):
    while continent.capitalize() not in continents:
        continent = input("Sorry that is not a valid response. Please choose one of the follwoing continents: \n{}\n\n".format('\n'.join(continents)))
    return continent

def ask_question(data):
    correct_answers = 0
    total_questions = len(data)
    random.shuffle(data)
       
    for item in data:
        if len(item['capital'])>1:
            answer = input('What is the capital city of {}\n'.format(item['name']))
            if fuzz.ratio(answer.lower(), item['capital'].lower()) != 100 and fuzz.ratio(answer.lower(), item['capital'].lower())> 90:
                print(f"Hmmm I'll give you this one, but the correct spelling is {item['capital']}.\n")
                correct_answers += 1
            elif fuzz.ratio(answer.lower(), item['capital'].lower())> 90:
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
    play_again = input("Do you want to play again? Please enter 'Y' or 'N'\n")
    
    while play_again.lower() not in ['y', 'n']:
        play_again = input("Please type 'Y' to continue or 'N' to quit\n")

    if play_again.lower() == 'y':
        return True

def leave_game(wants_to_play):
    print("'\nThat's too bad. Come back when you want to play again.\nBye!")
    sys.exit()
    
def main():
    print("Hey!\nWelcome to Capital City Challenge!\n")
    while True:
        #ask user to choose a contient
        continents = ['Africa', 'Asia', 'Europe', 'Americas', 'Oceania']
        continent = input("Choose a continent:\n{}\n".format('\n'.join(continents)))
        # checks if user chose a valid continent
        continent = check_valid_continent(continent, continents)
        print("Cool. You've Chosen {}. Let's see if you know your stuff.".format(continent.capitalize()))
        #gets data from Countries Api and converts it to JSON format
        res = requests.get('https://restcountries.eu/rest/v2/region/{}?fields=name;capital'.format(continent))
        data = res.json()
        #asks the user questions and keeps track of score
        correct_answers, total_questions = ask_question(data)
        #prints the score
        score_the_game(correct_answers, total_questions)
        #asks user if they want to play again
        if not play_again():
            leave_game()
            break
        
main()
