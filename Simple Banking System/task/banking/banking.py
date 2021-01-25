# Write your code here
import random


def print_menu():
    print("""1. Create an account
2. Log into account
0. Exit""")


def create_account():
    #todo chequear que no existe ya
    iin = str(400000)
    acc_number = str(random.randint(0, 999999999)).zfill(9)
    checksum = str(random.randint(0, 9))
    full_number = iin + acc_number + checksum
    return full_number

def create_pin():
    return str(random.randint(0, 9999)).zfill(4)

def check_card(lista_tarjetas, numero, pin):
    print("lista", lista_tarjetas)
    print("numero", str(numero))
    print("pin",str(pin))
    if numero in lista_tarjetas.keys() and lista_tarjetas[numero] == pin:
        print("You have successfully logged in!")
        print()
        return True
    else:
        print("Wrong card number or PIN!")
        print()
        return False


cards = {}
account_number = 0
logged = False
continuar = True

while continuar == True:

    if logged == False:
        print_menu()
        response = input()
        print()
        card_number = ""
        pin_number = ""

        if response == "1":
            card_number = create_account()
            print("Your card has been created")
            print("Your card number:")
            print(card_number)

            pin_number = create_pin()
            print("Your card PIN:")
            print(pin_number)
            cards[card_number] = pin_number
        elif response == "2":
            print("Enter your card number:")
            card_number_readed = input()
            print("Enter your PIN:")
            pin_number_readed = input()
            logged = check_card(cards, card_number_readed, pin_number_readed)
        elif response == "0":
            print("Bye!")
            continuar = False
        print()
    elif logged == True:
        print()
        print("1. Balance")
        print("2. Log out")
        print("0. Exit")

        choice = input()
        print()
        if choice == "1":
            print("Balance: 0")
        elif choice == "2":
            print("You have successfully logged out!")
            logged = False
        elif choice == "0":
            print("Bye!")
            continuar = False
        print()