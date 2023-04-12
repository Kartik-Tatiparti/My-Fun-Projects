import json
from random import randint

# word_to_guess -> The word to be guessed by player
# guessed_word -> Elements of the word already guessed
# letters_already_guessed -> List of letters already read
# remaining_word -> Part of word that is remaining(to check for new letters)


class Hangman:
    def __init__(self):
        self._word_to_guess = []
        self._guessed_word = []
        self._letters_already_guessed = []
        self._remaining_word = []
        self._hangman = list('HANGMAN')
        self._hangman_game_status = []

    def set_word_to_guess(self, file_name) -> None:
        word_list = json.load(open('words.json', 'r'))['data']
        self._word_to_guess = list(word_list[randint(0, len(word_list))])
        self._remaining_word = self._word_to_guess.copy()
        self._guessed_word = ['_'] * (len(self._word_to_guess))

    def check_already_guessed(self, guessed_letter):
        return guessed_letter in self._letters_already_guessed

    def add_to_letters_already_guessed(self, guessed_letter):
        self._letters_already_guessed.append(guessed_letter)

    def check_input(self, guessed_letter, remaining_word):
        if guessed_letter in list(remaining_word):
            return True
        else:
            return False

    def get_letter_indices(self, guessed_letter, word_to_guess):
        return [
            i for i in range(len(word_to_guess))
            if word_to_guess[i] == guessed_letter
        ]

    def edit_remaining_word(self, index_list, remaining_word):
        for index in index_list:
            self._remaining_word.remove(self._word_to_guess[index])

    def get_guessed_word(self, index_list, guessed_letter):
        for index in index_list:
            self._guessed_word[index] = guessed_letter

    def add_to_hangman(self):
        self._hangman_game_status.append(self._hangman.pop(0))

    # gameplay functions

    def start_play(self):
        name = input("Hey there!!!! Please tell me your name: ")
        print(f"Hi {name}!!! Welcome to the amazing game of hangman!!")

    def ask_input(self):
        return input("Guess a letter: ")


def main():
    hangman = Hangman()
    hangman.start_play()
    hangman.set_word_to_guess('words.json')
    consecutive_miss = 0

    while(
        ''.join(hangman._guessed_word) != ''.join(hangman._word_to_guess) and
        ''.join(hangman._hangman_game_status) != 'HANGMAN'
    ):
        guessed_letter = hangman.ask_input().lower()

        if(guessed_letter.isalpha() is False):
            print("Please enter alphabets only.")

        elif(len(guessed_letter) > 1):
            print("Please only enter one letter.")

        elif(hangman.check_already_guessed(guessed_letter)):
            print(f"You've already guessed this letter!! Try another one! \
{' '.join(hangman._guessed_word)}")

        elif(hangman.check_input(guessed_letter, hangman._remaining_word)):
            index_list = hangman.get_letter_indices(
                guessed_letter,
                hangman._word_to_guess
            )
            hangman.get_guessed_word(index_list, guessed_letter)
            hangman.edit_remaining_word(index_list, hangman._remaining_word)
            hangman.add_to_letters_already_guessed(guessed_letter)
            print(
                f"Yay you got that right!! {' '.join(hangman._guessed_word)}"
            )
            consecutive_miss = 0

        else:
            hangman.add_to_hangman()
            print(
                f"Oh no!!You got that wrong!! \
{' '.join(hangman._guessed_word)}"
            )
            print('-'.join(hangman._hangman_game_status))
            hangman.add_to_letters_already_guessed(guessed_letter)
            consecutive_miss += 1
            if consecutive_miss > 3:
                print("C'mon! Try Harder!")
                # Add another function to give random hints
                print(f"The word stars with \
{''.join(hangman._word_to_guess)[0]}")

    if(''.join(hangman._guessed_word) == ''.join(hangman._word_to_guess)):
        print(
            f"Hurray!! You've guessed the word!! \
It was {''.join(hangman._guessed_word)}")
    else:
        print(f"Oh no!! {'-'.join(hangman._hangman_game_status)}")
        print(f"The word was {''.join(hangman._word_to_guess)}")


if __name__ == '__main__':
    main()
