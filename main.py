from database import CRUD as db
from datetime import datetime
import time
import random as rd


# requirement

# dedicated input handler with a while loop
# class beased menu view
t = '\t'
n = '\n'
e = '='
nt = '\n\n\t\t\t\t'

class menuView:
    global t, n, e, nt
    msg = f'{t*4}{e*10} WELCOME TO ATM MACHINE MADE BY #SHYAM_MAHANTA {e*10}{t*3}'

    # main menu view
    def FrontMenu(self):
        view = f"{nt}{menuView.just('1. Balance Check')}{t*3}{menuView.just('2. Deposit Cash')}{nt}{menuView.just('3. Withdraw Money')}{t*3}{menuView.just('4. Pin Change')}{nt}{menuView.just('5. Mobile No Change')}{t*3}{menuView.just('6. Exit')}"
        return view

    # to check account balance
    def balCheck(self):
        view = f"{nt}Your Clear Balance is ${db.lastValue('Balance')}"
        return view

    # deposit balance
    def Credit(self):
        amount = menuView.inputHandler('**Enter Amount to Deposit (press c for cancel)', 'Invalid Amount. Minmum Deposit Amount is $50', cashInput=True, exitKey=('c'))
        if amount:
            credit = db.creditEntry(amount, datetime.now())
            print(menuView.forMsg(f'Your Deposit was Successfully.{nt}{t}Transaction ID: {credit[1]}{nt}{t}Amount: ${credit[0]}'))
            print(view.balCheck())
            return
        print(menuView.forMsg('Transaction Declined'))
        return
    
    def Debit(self):
        amount = menuView.inputHandler('**Enter an Amount to Withdraw (press c for cancell)', 'Invalid Amount. Minmum withdrawl is $100', exitKey=('c'), cashInput=True, min=100)
        if not amount:
            print(menuView.forMsg('Transaction Declied'))
            return
        pin_check = user_update.UserInputHandler('Enter Your 4 Digit Pin', 'Invalid Pin.', pin=True, length=4, exitKey=('c'))
        if amount <= db.lastValue('Balance') and pin_check:
            debit = db.debitEntry(amount, datetime.now())
            print(menuView.forMsg(f'Your withdrawl was Sucessfully Done.{nt}{t}Transaction ID: {debit[1]}{nt}{t}Amount: ${debit[0]}'))
            print(view.balCheck())
            return
        elif not pin_check:
            print(menuView.forMsg('Transaction Declied'))
            return
        print(menuView.forMsg('Insffient Balance. Redirecting in 2 Sec. . .'))
        time.sleep(2)
        return        

    @staticmethod
    def just(string):
        return string.ljust(30)
    
    @staticmethod
    def forMsg(message): # this will format the any message we can show the user
        return f"{nt} => {message}"

    @staticmethod
    def inputHandler(ValidText, InvalidText, range=None, exitKey=tuple(), cashInput=False, min=50):    
        while True:
            msg = input(f'{n*2}{t*3}{ValidText}: ')
            try:
                if msg.lower() in exitKey:
                    return False
                elif cashInput and float(msg) >= min:
                    return float(msg)
                elif int(msg) in range or int(msg) in (int(db.lastValue('resetkey', 'userData', custom_db=True)),int(db.lastValue('accreset', db='userData', custom_db=True))):
                    return int(msg)
                print(f'{n*2}{t*4} => {InvalidText}')
            except:
                print(f'{n*2}{t*4} => {InvalidText}')

# Dedicated Pin section to generate pin & change pin and other required staff to handle

class UserUpdate:
    global nt

    def UserInputHandler(self, ValidText=None, InvalidText=None, length=None, pin=False, mobile=False, exitKey=tuple()):
        if pin:
            if int(db.lastValue('attempts', 'userData', custom_db=True)) == 0:
                print(menuView.forMsg("You have Blocked Your Pin. Please Enter the Reset Key!"))
                return False
            i = 3
            while True:
                if i == 0:
                    db.userUpdate('attempts', 0)
                    print(menuView.forMsg("You have Blocked Your Pin. Please Enter the Reset Key!"))
                    i = 3
                    return False
                msg = input(f"{n*2}{t*3}{ValidText} (press {exitKey[0]} to cancell): ")
                try:
                    if msg.lower() in exitKey:
                        return False
                    if int(msg) == int(db.lastValue('secretpin', db='userData', custom_db=True)):
                        i = 3
                        return int(msg)
                    if i == 1:
                        i -= 1
                        continue
                    print(menuView.forMsg(f"{InvalidText} {i-1} attempts left."))
                    i -= 1
                except:
                    if i == 1:
                        i -= 1
                        continue
                    print(menuView.forMsg(f"{InvalidText} {i-1} attempts left"))
                    i -= 1        
        key = rd.randrange(1000, 9999)
        db.userUpdate('secretpin', key)
        db.userUpdate('attempts', 3)
        time.sleep(1)
        print(menuView.forMsg(f"You Pin is Unblocked & Your New Pin is {key}"))

    @staticmethod
    def pinChange():
        if user_update.UserInputHandler('Enter Your Current Key', 'Invalid Key', length=4, pin=True, exitKey=('c')):
            while True:
                msg = input(f'{nt} => Enter Your New Pin (press c to cancell): ')
                try:
                    if msg.lower() in ('c'):
                        print(menuView.forMsg('New Pin Generation Processed didnot Completed.'))
                        return
                    if msg[0] == '0':
                        print(view.forMsg("Pin should be 4 Digit Number & Cannot Start With 0."))
                    elif int(msg) and len(str(msg)) == 4:
                        db.userUpdate('secretpin', msg)
                        print(menuView.forMsg('Secret Pin Changed Successfully'))
                        return
                    else:
                        print(menuView.forMsg("Something error occured."))
                        return
                except:
                    print(menuView.forMsg('What the f**k You are soo annoying. I have covered all the bugs. You Entered some f**king invalid Pin. get the f**k done again.'))
                    return

view = menuView()
user_update = UserUpdate()

def render():
    i = 1
    while True:
        if i:
            print(view.msg)
            i -= 1
        print(view.FrontMenu())
        run = view.inputHandler('Please Enter Your Preferred Choice (Press q or e to exit)', 'Invalid Input Detected Please Try Again', range(1,7), exitKey=('e', 'q'))

        if run == 1:
            print(view.balCheck())
        elif run == 2:
            view.Credit()
        elif run == 3:
            view.Debit()
        elif run == 4:
            user_update.pinChange()
        elif run == int(db.lastValue('resetkey', 'userData', custom_db=True)):
            user_update.UserInputHandler()
        elif run == int(db.lastValue('accreset', 'userData', custom_db=True)):
            time.sleep(1)
            print(view.forMsg("Your Account was Reset Successfully."))
            db.Delete()
        elif run == 5:
            print(menuView.forMsg("This Feature is Coming soon."))
        elif run == 6:
            return
        else:
            return
render()

