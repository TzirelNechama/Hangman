
from stages import stages
from requests import session
from datetime import datetime

session = session()

basic_url = "http://127.0.0.1:5000"

def start_game(id_num, name):
    message = {'id': id_num, "name": name}
    response = session.post(f"{basic_url}/start_game", json=message)
    if response.status_code == 200:
        print(response.text)
        continue_game()
    else:
        print(f"Error: {response.status_code} cookie error")

def get_word(num):
    response = session.get(f"{basic_url}/get_word", json={"num": num})
    if response.status_code == 200:
        return response.text
    if response.status_code == 403:
        a = input("Your time is up do you want to register again? (y/n)")
        while a != 'y' and a != 'n':
            a = input("Your time is up do you want to register again? (y/n)")
        if a == 'n':
            print('Thank You for playing hangman!')
        elif a == 'y':
            a = relogin()
            if a == "relog ended":
                return print("Invalid id please try again later")
        continue_game()
    else:
        print("get word error")

def continue_game():
    print(open('./logo.txt').read())
    while True:
        try:
            num = int(input("In order to pick a word enter a number:"))
            break
        except ValueError as a:
            print("That was not a number")
    word = get_word(num)
    # if word == None:
    #     return "i dont know what is going on"
    lines = ""
    for x in word:
        lines += '_'
    print(lines)
    good = 0
    bad = 0
    while True:
        if good >= word.__len__():
            print("YOU WON!!!!😊😜😃☺️")
            end_game(1, word)
            break
        if bad == 7:
            print("You Lost 😔😥😢😞🥺")
            print(f"The hidden word is: {word}")
            end_game(0, word)
            break
        l = input("Input a letter:")
        while l=="" or l.__len__()!=1:
            l = input("Invalid input! Try again.\nInput a letter:")
        i = 0
        print("letter inputted")
        if l in word:
            while l != '' and l in word[i::]:
                index = word.index(l, i)
                if lines[index] == '_':
                    good += 1
                    lines = lines[:index] + l + lines[index + 1::]
                    i += index + 1
                else:
                    print("Double letter!")
                    break
            print(lines)
        else:
            print(stages[bad])
            bad += 1
            print(lines)

def register(name, idn, pas):
    message = {"name": name, "id": idn, "pas": pas}
    response = session.post(f'{basic_url}/add_user', json=message)
    if response.status_code == 200:
        start_game(idn, name)
    else:
        print(f"Error: {response.status_code} cant register")


def login():
    tt = datetime.now().hour
    if tt < 12:
        a = "Good morning"
    elif tt < 17:
        a = "Good afternoon"
    else:
        a = "Good evening"
    name = input(f"{a}! Please enter your name: ")
    idn = input(f"Please enter your identity number: ")
    password = input(f"Please enter your password: ")
    response = session.get(f"{basic_url}/login", json={"name": name, "id": idn, "password": password})
    if response.status_code == 200:
        if response.text == "found":
            start_game(idn, name)
        elif response.text == 'no':
            reg = input("You are not registered! do you want to register? (y/n)")
            while reg != "y" and reg != "n":
                reg = input("You are not registered! do you want to register? (y/n)")
            if reg == "y":
                register(name, idn, password)
            else:
                print("Goodbye!")
        elif response.text == "error":
            return print("Your name is incorrect please try again later!")
        else:
            print(response.text)
            correct_password = response.text
            print("Invalid password! Please try again!")
            password = input(f"Please enter your password: ")
            while correct_password != password:
                print("Invalid password! Please try again!")
                password = input(f"Please enter your password: ")
            start_game(idn, name)
    else:
        print("login error")


def history():
    response = session.get(f'{basic_url}/get_history')
    if response.status_code == 200:
        print(f"You played {response.json()['play_times']} times\n"
              f"You won the game {response.json()['num_win']} times!\n"
              f"The words you played: {response.json()['word_list']}")
        a = input("Do you want to start the game? (y/n)")
        while a != 'y' and a != 'n':
            a = input("Do you want to start the game? (y/n)")
        if a == 'n':
            return print('Thank You for playing hangman!')
        elif a == 'y':
            continue_game()
    elif response.status_code == 403:
        print(response.status_code)
        a = input("Your time is up do you want to register again? (y/n)")
        while a != 'y' and a != 'n':
            a = input("Your time is up do you want to register again? (y/n)")
        if a == 'n':
            print('Thank You for playing hangman!')
        elif a == 'y':
            return relogin()
    else:
        print('Sorry an error occurred')

def begin():
    l = input("Press s to start the game or h to see your history?")
    while l != 's' and l != 'h':
        l = input("Press s to start the game or h to see your history?")
    if l == 's':
        continue_game()
    elif l == 'h':
        history()


def end_game(win, word):
    response = session.post(f"{basic_url}/end_game", json={'win': win, 'word': word})
    if response.status_code == 200:
        begin()
    elif response.status_code == 403:
        a = input("Your time is up do you want to register again? (y/n)")
        while a != 'y' and a != 'n':
            a = input("Your time is up do you want to register again? (y/n)")
        if a == 'n':
            print('Thank You for playing hangman!')
        elif a == 'y':
            a =  relogin()
            if a == "relog ended":
                return print("Invalid id please try again later")
            end_game(win, word)
    else:
        print("end game error")

def relogin():
    idn = input("Please input your identity number:")
    response = session.get(f"{basic_url}/relogin", json={'id':idn})
    if response.status_code == 200:
        return response.text
    else :
        return "relog ended"

if __name__ == "__main__":
    login()
