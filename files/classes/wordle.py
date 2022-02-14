import random
from os import environ

def format_guesses(guesses):
    return " -> ".join(guesses)

def format_all(guesses, status, answer):
    formatted_guesses = format_guesses(guesses)
    return f'{formatted_guesses}_{status}_{answer}'

class Wordle:
    def __init__(self, g):
        self.word_list = environ.get('WORDLE').split(' ')
        self.command_word = "!wordle"
        self.db = g.db

    def check_for_wordle_commands(self, in_text, from_user, from_comment):
        word_list = self.word_list
        command_word = self.command_word
        if command_word in in_text:
            answer = random.choice(word_list) # choose a random word from word list
            guesses = []
            status = 'active'
            from_comment.wordle_result = format_all(guesses, status, answer)

    def check_guess(self,from_comment, guess):
        guesses, status, answer = from_comment.wordle_result.split("_")
        guesses = guesses.split(" -> ")
        if (guesses[0] == ""):
            guesses = []
        count = len(guesses)

        if (guess != None and len(guess) == 5 and status == "active"):
            result = ["🟥"]*5
            pos = 0 # letter position
            guess = guess.lower()
            for i in guess:
                result[pos] = i.upper()
                if i == answer[pos]: 
                    result[pos] = result[pos] + "🟩" # green
                elif i in answer: 
                    result[pos] = result[pos] + "🟨" # yellow
                else: 
                    result[pos] = result[pos] + "🟥" # red
                pos += 1 # add 1 to the letter position
            guesses.append("/".join(result))
            

        if (guess.lower() == answer): status = "won"
        elif (count == 5): status = "lost"

        from_comment.wordle_result = format_all(guesses, status, answer)