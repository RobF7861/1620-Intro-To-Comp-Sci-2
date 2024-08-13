from PyQt6.QtWidgets import *
from gui import *
import csv


#TODO: Create a .csv file for accounts
#Look over teacher project video for better instruction
#TODO: Implement an account number input unique to all accounts
#TODO: Remove 'Set Balance' feature
#TODO: Make sure account balances keep last activity (ex.: Withdrawing 10 from Tom's 30 persists even after app is closed)
class Logic(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.button_name.clicked.connect(lambda: self.submit_name())
        self.button_enter.clicked.connect(lambda: self.amount_enter())
        self.button_clear.clicked.connect(lambda: self.clear_button())
        self.button_enter.setEnabled(False)
        self.button_clear.setEnabled(False)

    def submit_name(self):
        try:
            name: str = (self.entry_name.text()).capitalize()
            account_num: int = int(self.entry_accountNum.text())
            with open('accounts.csv', 'r') as accounts:
                reader = csv.reader(accounts, delimiter=',')
                for row in reader:
                    if name == row[0] and account_num == int(row[1]):
                        self.label_name_output.setText(f'Hello {name}! Your balance is: ${float(row[2]):.2f}')
                        self.radio_withdraw.setEnabled(True)
                        self.radio_deposit.setEnabled(True)
                        self.entry_amount.setReadOnly(False)
                        self.button_enter.setEnabled(True)
                        self.button_clear.setEnabled(True)
                        break
                    elif name == '' or account_num == '':
                        self.label_name_output.setText(f'Please enter a name and account number')
                        self.radio_withdraw.setEnabled(False)
                        self.radio_deposit.setEnabled(False)
                        self.entry_amount.setReadOnly(True)
                        self.button_enter.setEnabled(False)
                        self.button_clear.setEnabled(False)
                    elif name != row[0] or account_num != int(row[1]):
                        self.label_name_output.setText(f'Invalid account, please try again')
                        self.radio_withdraw.setEnabled(False)
                        self.radio_deposit.setEnabled(False)
                        self.entry_amount.setReadOnly(True)
                        self.button_enter.setEnabled(False)
                        self.button_clear.setEnabled(False)
        except ValueError:
            self.label_name_output.setText(f'Please enter a name and account number')
            self.radio_withdraw.setEnabled(False)
            self.radio_deposit.setEnabled(False)
            self.entry_amount.setReadOnly(True)
            self.button_enter.setEnabled(False)
            self.button_clear.setEnabled(False)

    def amount_enter(self):
        try:
            name: str = (self.entry_name.text()).capitalize()
            account_num: int = int(self.entry_accountNum.text())
            amount: float = float(self.entry_amount.text())
            with open('accounts.csv') as readaccounts:
                reader = csv.reader(readaccounts.readlines())
                with open('accounts.csv', 'w', newline='') as writeaccounts:
                    writer = csv.writer(writeaccounts)
                    if self.radio_withdraw.isChecked():
                        for row in reader:
                            if name == row[0] and account_num == int(row[1]):
                                if amount <= 0 or amount > float(row[2]):
                                    writer.writerow(row)
                                    self.label_amount_output.setText(f'Withdrawal could not be completed,\nPlease try again')
                                else:
                                    writer.writerow([row[0], row[1], str(float(row[2]) - amount)])
                                    self.label_amount_output.setText(f'Your balance is now: ${(float(row[2]) - amount):.2f}')
                                    self.label_name_output.setText(f'Hello {name}! Your balance is: ${(float(row[2]) - amount):.2f}')
                            else:
                                writer.writerow(row)
                    elif self.radio_deposit.isChecked():
                        for row in reader:
                            if name == row[0] and account_num == int(row[1]):
                                if amount <= 0:
                                    raise ValueError
                                else:
                                    writer.writerow([row[0], row[1], str(float(row[2]) + amount)])
                                    self.label_amount_output.setText(f'Your balance is now: ${(float(row[2]) + amount):.2f}')
                                    self.label_name_output.setText(f'Hello {name}! Your balance is: ${(float(row[2]) + amount):.2f}')
                            else:
                                writer.writerow(row)
        except ValueError:
            self.label_amount_output.setText(f'Please enter only positive integers')

    def clear_button(self):
        self.entry_name.clear()
        self.entry_accountNum.clear()
        self.entry_amount.clear()
        self.label_name_output.clear()
        self.label_amount_output.clear()
        self.radio_withdraw.setChecked(False)
        self.radio_deposit.setChecked(False)
        self.radio_withdraw.setEnabled(False)
        self.radio_deposit.setEnabled(False)
        self.entry_amount.setReadOnly(True)
        self.button_enter.setEnabled(False)
        self.button_clear.setEnabled(False)
