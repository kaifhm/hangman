#!/usr/bin/env python3

import random
from sys import exit


alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def get_hidden(word, entered):
    hidden = ''
    for x in word:
        if x in entered:
            hidden += x
        elif x == ' ':
            hidden += x
        else:
            hidden += '-'
    return hidden

print('Welcome to hangman')

while True:
    try:
        category = input('''
What do you want the theme to be?
Press:
1 for Animals and Birds
2 for Vocabulary
3 for Countries
4 for Cars
''')
        if category == '1':
            category = 'Animals and birds'
        elif category == '2':
            category = 'Vocabulary'
        elif category == '3':
            category = 'Countries'
        elif category == '4':
            category = 'Cars'
        else:
            print('Enter a valid number')
            continue
        break
    except:
        pass

chance_left = 6
hidden = ''
entered = ''
won = False

with open(category + '.csv') as file:
    word_list = file.readlines()
word = random.choice(word_list)[:-1].upper()

print(f'\nYou have {chance_left} chances')

print(get_hidden(word, entered))

while chance_left > 0:
    while True:
        letter = input('\nGuess a letter ').upper()
        if letter in entered:
            print('You guessed this letter already. Try another one ')
        elif len(letter) > 1:
            print('Please enter a letter ')
        elif not letter.isalpha():
            print('Please enter a single letter ')
        else:
            entered += letter
            break

    if letter in word:
        print('You guessed right')
        print(get_hidden(word, entered))
        if hidden == word:
            print('\nCongratulations! You won!!!')
            won = True
            break
    else:
        print(get_hidden(word, entered))
        chance_left -= 1
        print(f'You guessed wrong. You only have {chance_left} chances left')
    hidden = ''
    print(f"Letters already entered: {' '.join(entered.upper().split())}")

if not won:
    print('You lost.')
    print(f'The word was {word}\nBetter luck next time')
input()
