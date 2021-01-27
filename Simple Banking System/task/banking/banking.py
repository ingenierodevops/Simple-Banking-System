# Write your code here
import random
import sqlite3


def print_menu():
    print("""1. Create an account
2. Log into account
0. Exit""")


def luhn(card):
    # it receives a string
    #print(card)
    card_numbers = list(card)
    #print(card_numbers)
    card_numbers_int = [int(item) for item in card_numbers if item ]
    index = 0
    for item in card_numbers_int:
        if index % 2 == 0:
            card_numbers_int[index] = item * 2
        index += 1
    #print(card_numbers_int)
    index = 0
    for item in card_numbers_int:
        if item > 9 :
            card_numbers_int[index] = item - 9
        index += 1
    #print(card_numbers_int)
    suma = 0
    for item in card_numbers_int:
        suma += item
    #print("suma:", suma)
    resto = suma % 10
    checksum = 0
    if resto > 0:
        checksum = 10 - resto
    #print("check:", checksum)
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
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()

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
    cur.execute("DROP TABLE IF EXISTS card;")
    #cur.execute("""DROP TABLE card""")
    conn.commit()

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
    sql_string = "INSERT INTO card (number, pin, balance) VALUES ('{}', '{}', 0);".format(cuenta, PIN)
    cur.execute(sql_string)
    conn.commit()
    conn.close()


def get_balance(cuenta):
    #print("getting balance: ", cuenta)
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()

    cur.execute("SELECT balance FROM card WHERE number = '{}';".format(cuenta))
    row = cur.fetchone()
    #print(row)
    conn.close()
    if row:
        return row[0]
    else:
        return 0

def print_balance(cuenta):
    balance_to_print = get_balance(cuenta)
    print("Balance:", str(int(balance_to_print)))


def close_account(cuenta):
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()

    cur.execute("DELETE FROM card WHERE number = '{}';".format(cuenta))
    conn.commit()
    conn.close()
    print()
    print("The account has been closed!")


def add_income(cuenta, money):
    balance_anterior = get_balance(cuenta)
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    print(money)
    new_balance = int(balance_anterior) + int(money)
    print(new_balance)
    cur.execute("UPDATE card SET balance = {} WHERE number = '{}';".format(new_balance, cuenta))
    conn.commit()
    conn.close()
    print("Income was added!")


def do_transfer(cuenta, destino, money):
    balance_anterior_cuenta = get_balance(cuenta)
    balance_anterior_destino = get_balance(destino)

    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()

    new_balance_cuenta = int(balance_anterior_cuenta) - int(money)
    cur.execute("UPDATE card SET balance = {} WHERE number = '{}';".format(new_balance_cuenta, cuenta))
    conn.commit()

    new_balance_destino = int(balance_anterior_destino) + int(money)
    cur.execute("UPDATE card SET balance = {} WHERE number = '{}';".format(new_balance_destino, destino))
    conn.commit()

    conn.close()
    print("Success!!")

def check_card_checksum(numero_cuenta):
    check_sum = luhn(numero_cuenta[0:15])
    if check_sum == numero_cuenta[15]:
        return True
    else:
        return False

def check_card_exists(numero_cuenta):
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()

    cur.execute("SELECT number FROM card WHERE number = '{}';".format(numero_cuenta))
    row = cur.fetchone()
    conn.close()

    if row:
        if numero_cuenta == row[0]:
            return True
        else:
            return False
    else:
        return False

cards = {}
card_number = ""
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
            card_number = card_number_readed
        elif response == "0":
            print("Bye!")
            continuar = False
        print()
    elif logged == True:
        print()
        print("1. Balance")
        print("2. Add income")
        print("3. Do transfer")
        print("4. Close account")
        print("5. Log out")
        print("0. Exit")

        choice = input()
        print()
        if choice == "1":
            print_balance(card_number)
            ##pass
        elif choice == "2":
            # get info
            print("Enter income:")
            amount = input()
            add_income(card_number, amount)
        elif choice == "3":
            print("Transfer")
            print("Enter card number:")
            destination = input()
            if destination == card_number:
                print("You can't transfer money to the same account!")
            else:
                if check_card_checksum(destination):
                    # do things
                    # get info
                    # previous checks
                    if check_card_exists(destination):
                        print("Enter how much money you want to transfer:")
                        amount = input()
                        current_bal = get_balance(card_number)
                        if int(amount) > int(current_bal):
                            print("Not enough money!")
                        else:
                            ##pass
                            do_transfer(card_number, destination, amount)
                    else:
                        print("Such a card does not exist.")
                else:
                    print("Probably you made a mistake in the card number. Please try again!")
        elif choice == "4":
            close_account(card_number)
            logged = False
            ## pass
        elif choice == "5":
            print("You have successfully logged out!")
            logged = False
        elif choice == "0":
            print("Bye!")
            continuar = False
            logged = False
        print()
