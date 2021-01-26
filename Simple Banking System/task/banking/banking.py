# Write your code here
import random
import sqlite3

def print_menu():
    print("""1. Create an account
2. Log into account
0. Exit""")

def luhn(card):
    # it receives a string
    # print(card)
    card_numbers = list(card)
    card_numbers_int = [int(item) for item in card_numbers if item ]
    index = 0
    for item in card_numbers_int:
        if index % 2 == 0:
            card_numbers_int[index] = item * 2
        index += 1
    # print(card_numbers_int)
    index = 0
    for item in card_numbers_int:
        if item > 9 :
            card_numbers_int[index] = item - 9
        index += 1
    # print(card_numbers_int)
    suma = 0
    for item in card_numbers_int:
        suma += item
    # print("suma:", suma)
    resto = suma % 10
    checksum = 0
    if resto > 0:
        checksum = 10 - resto
    # print("check:", checksum)
    return str(checksum)

def create_account():
    #todo chequear que no existe ya
    iin = str(400000)
    acc_number = str(random.randint(0, 999999999)).zfill(9)
    #checksum = str(random.randint(0, 9))
    full_number = iin + acc_number
    checksum = luhn(full_number)
    full_number = full_number + checksum
    return full_number

def create_pin():
    return str(random.randint(0, 9999)).zfill(4)

def check_card(numero, pin):
    print("numero", str(numero))
    print("pin",str(pin))

    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()

    # creamos la tabla
    cur.execute("SELECT pin FROM card WHERE number = '{}';".format(numero))
    row = cur.fetchone()
    conn.close()
    if row:
        db_PIN = row[0]
        print("extracted PIN:", str(db_PIN))

        if db_PIN == pin:
            print("You have successfully logged in!")
            print()
            return True
        else:
            print("Wrong card number or PIN!")
            print()
            return False
    else:
        print("Wrong card number or PIN!")
        print()
        return False



def crear_base_datos():
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()

    # borramos la tabla card si ya existia
    # cur.execute("""DROP TABLE card""")
    # conn.commit()

    # creamos la tabla sólo si no existe
    cur.execute("""CREATE TABLE IF NOT EXISTS card (
                id INTEGER,
                number TEXT,
                pin TEXT,
                balance INTEGER DEFAULT 0);""")
    conn.commit()
    conn.close()

def guardar_cuenta(cuenta, PIN):
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    sql_string = "INSERT INTO card (number, pin) VALUES ('{}', '{}');".format(cuenta, PIN)
    cur.execute(sql_string)
    conn.commit()
    conn.close()



cards = {}
account_number = 0
logged = False
continuar = True

crear_base_datos()

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
            guardar_cuenta(card_number, pin_number)
        elif response == "2":
            print("Enter your card number:")
            card_number_readed = input()
            print("Enter your PIN:")
            pin_number_readed = input()
            # logged = check_card(cards, card_number_readed, pin_number_readed)
            logged = check_card(card_number_readed, pin_number_readed)
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