import json                            # import the JSON file
from datetime import datetime          # import datetime module for update date to today's date if entered invalid date type 
import tkinter as tk                   # import and assigning the tkinter module as 'tk' 
from tkinter import ttk, messagebox    # import ttk and messagebox from tkinter module library

# create the FinanceTrackerGUI class
class FinanceTrackerGUI:
    def __init__(self, root, transactions):
        self.root = root
        self.root.title("Personal Finance Tracker GUI (Using Tkinter)")
        self.transactions = transactions
        self.filtered_transactions = None      # To store filtered transactions
        self.create_widgets()
        self.display_transactions()            # call display transaction module to display all transactions in GUI Treeview

    # create a module for create widgets
    def create_widgets(self):
        # Frame for table and scrollbar
        table_frame = ttk.Frame(self.root)
        table_frame.pack(pady=10, padx=5)

        # create tree heading to display transaction details with relevent colomns in Treeview
        self.tree = ttk.Treeview(table_frame, columns=("Description", "Amount", "Date"), show="headings")
        self.tree.heading("Description", text="Description", command=lambda: self.sort_by_column("Description"))           # Description colomn heading
        self.tree.heading("Amount", text="Amount", command=lambda: self.sort_by_column("Amount"))                          # Amount colomn heading
        self.tree.heading("Date", text="Date", command=lambda: self.sort_by_column("Date"))                                # Date colomn heading
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)                                 # set the geometries of the main table in GUI

        # create a vertical scrollbar for the Treeview
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)                            # the scrollbar set to the right side side of the Treeview
        self.tree.config(yscrollcommand=scrollbar.set)

        # Create a frame frame for the "Search"
        search_frame = ttk.Frame(self.root)
        search_frame.pack(pady=10, padx=30)

        # create a StringVar to store the search item inputs (this is a special variable type in tkinter)
        self.search_var = tk.StringVar()

        # create a search input cell for the user inputs 
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        self.search_entry.pack(side=tk.LEFT, padx=8)

        # create a button for search
        search_button = ttk.Button(search_frame, text="Search", command=self.search_transactions)
        search_button.pack(side=tk.LEFT)                        # the search button is displayed to the left of the search entry cell

    # create a module for display transactions
    def display_transactions(self):
        # Clear existing entries in the treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Determine which transactions to display (filtered or all)
        # if searched transaction category already exist, then "filtered_transaction" will triggered
        # id searched transaction doesn't exist, then all transactions will displayed  
        transactions_to_display = self.filtered_transactions if self.filtered_transactions else self.transactions

        # Populate treeview with transactions
        for category, transactions_list in transactions_to_display.items():
            for index, transaction in enumerate(transactions_list):
                amount = transaction['amount']
                date = transaction['date']
                self.tree.insert("", "end", values=(category, f"{amount:.2f}", date))       # amount of transaction is display with two floating points

    # create a module for search transaction
    def search_transactions(self):
        search_term = self.search_var.get().strip().lower()

        if not search_term:
            messagebox.showinfo("Search", "Please enter a search term.")
            return

        self.filtered_transactions = {}                   # create a dictionary to store searched transactions
        for category, transactions_list in self.transactions.items():
            filtered_transactions_list = [transaction for transaction in transactions_list
                                          if search_term in category.lower() or search_term in transaction['date'].lower()]
            if filtered_transactions_list:
                self.filtered_transactions[category] = filtered_transactions_list               # confermation for searched transaction is exist in the JSON file

        self.display_transactions()     # call "display transaction" module if searched transaction doesn't exist

    def sort_by_column(self, column):
        # Determine which transactions to sort (filtered or all)
        transactions_to_sort = self.filtered_transactions if self.filtered_transactions else self.transactions

        # Sort transactions list based on the selected column (considering the letter case and acsending order)
        for category, transactions_list in transactions_to_sort.items():
            transactions_list.sort(key=lambda x: x[column.lower()])              

        self.display_transactions()           # display the transactions, after sorting by given order

# create the "FinanceTrackerCLI" class
class FinanceTrackerCLI:
    def __init__(self):
        self.transactions = {}             # create transaction dictionary to store transactions
        self.load_transactions("transactions.json")             # load the JSON file
        self.main_menu()                   # calling main menu to display all selections for the user

    # create a module for load transactions
    def load_transactions(self, filename):
        try:                                              # validating the "transactions.json" file is exist or not
            with open(filename, "r") as file:             # open the "transaction.json" file in read mode
                self.transactions = json.load(file)       # loading the JSON file
            print("Transactions loaded successfully.")
        except FileNotFoundError:
            print("No transactions file found.")

    # create a module for save transaction
    def save_transactions(self):                          
        with open("transactions.json", "w") as file:      # open the JSON file in write mode
            json.dump(self.transactions, file)
        print("Transactions saved.")

    # create a module for add transaction
    def add_transaction(self):
        try:                                                                  # if user enter a invalid entry for the amount the program will give a error message
            category = input("Please enter the Description (category): ").lower()
            amount = float(input("Please enter the amount: "))
            date = input("Please enter the date of transaction (YYYY-MM-DD): ")

            # makeing sure that date is not to be a empty cell.
            if date == "":
                # Get the current date and time.
                current_datetime = datetime.now()
                # Take out the date part only.
                current_date = current_datetime.date()
                # Converet the date as a string in a special format.
                formatted_date = current_date.strftime("%Y-%m-%d")
                # set the transaction date as formatted date.
                date = formatted_date

            try:
                # checking the inputed date is valid date or not.
                datetime.strptime(date, '%Y-%m-%d')

            except ValueError:
                print("Invalid date format!!!. Therefore the date updated to current date...")

                # Get the current date and time.
                current_datetime = datetime.now()
                # Take out the date part only.
                current_date = current_datetime.date()
                # Converet the date as a string in a special format.
                formatted_date = current_date.strftime("%Y-%m-%d")
                # set the transaction date as formatted date.
                date = formatted_date

            if category not in self.transactions:                # check user entered category is already exist. if it doesn't exist then a new category will create in the JSON file
                self.transactions[category] = []               # create a new list for new categories

            self.transactions[category].append({"amount": amount, "date": date})    # if entered category is already exist then the transaction may added to that category as a children
            print("Transaction added successfully.")
            self.save_transactions()            # call save transaction module for save the new transactions
        except ValueError:
            print("Please enter valid values for amount.")             # the error message for invalid amount entries

    # create a module for delete a specific transaction that given by user
    def delete_transaction(self):
        self.view_transactions()                # before delete a transaction user could be watch wll the transactions. call view transaction module for that task
        category = input("Enter the category to delete transaction from: ").lower()

        if category in self.transactions:                # validation for the given category in the transactions or not
            number = int(input("Enter the number of the transaction to delete: "))
            if 1 <= number <= len(self.transactions[category]):               # validating the given number is valid or not
                del self.transactions[category][number - 1]
                print("Transaction deleted successfully.")
                if len(self.transactions[category]) == 0 :            # if a specific transaction hasn't any child then that ategory will removed
                    del self.transactions[category]
                self.save_transactions()
            else:
                print("Invalid number.")                # if user gave a invalid number then the error will displayed
        else:
            print("Category not found.")              # if the user gave a invalid category then the error will displayed

    # create a module for view transactions
    def view_transactions(self):
        for category, transactions_list in self.transactions.items():
            print(f"{category}:")
            counter = 1
            for transaction in transactions_list:
                amount = transaction['amount']
                date = transaction['date']
                print(f"{counter}. Amount: {amount:.2f}, Date: {date}")
                counter += 1

    # create a module for update transaction
    def update_transaction(self):
        self.view_transactions()           # before update a transaction user could be watch wll the transactions. call view transaction module for that task
        category = input("Enter the Description (category) of the transaction to update: ")

        if category in self.transactions:          # validation for the given category in the transactions or not
            
            try:
                number = int(input("Enter the number of the transaction to update: "))
                if 1 <= number <= len(self.transactions[category]):           #validating the index number is valid or not
                    amount = float(input("Enter new amount: "))     #get new details related to the updatable transaction
                    date = input("Enter new date (YYYY-MM-DD): ")

                    # makeing sure that date is not to be a empty cell.
                    if date == "":
                        # Get the current date and time.
                        current_datetime = datetime.now()
                        # Take out the date part only.
                        current_date = current_datetime.date()
                        # Converet the date as a string in a special format.
                        formatted_date = current_date.strftime("%Y-%m-%d")
                        # set the transaction date as formatted date.
                        date = formatted_date

                    try:
                        # checking the inputed date is valid date or not.
                        datetime.strptime(date, '%Y-%m-%d')

                    except ValueError:
                        print("Invalid date format!!!. Therefore the date updated to current date...")

                        # Get the current date and time.
                        current_datetime = datetime.now()
                        # Take out the date part only.
                        current_date = current_datetime.date()
                        # Converet the date as a string in a special format.
                        formatted_date = current_date.strftime("%Y-%m-%d")
                        # set the transaction date as formatted date.
                        date = formatted_date

                    
                    self.transactions[category][number - 1] = {"amount": amount, "date": date}
                    print("Transaction updated successfully.")
                else:
                    print("\n!!! Enter a valid index value.!!!")      #if user entered a invalid index number
            except ValueError:
                print("\nPlease enter a valid value.\nRecorded previous transaction was discarded!")                # if user gave a invalid value then the update will discard

        else:
            print("Category not found.")                     

    # create a module for display a summary of all transactions had been done so far
    def display_summary(self):
        for category, transactions_list in self.transactions.items():
            total_amount = sum(transaction['amount'] for transaction in transactions_list)
            print(f"Total {category} Amount: {total_amount:.2f}")

    # create a module for main menu
    def main_menu(self):
        while True:
            print("\n--- Personal Finance Tracker Main Menu ---")              # heading prompt
            print("1. Add Transaction")                                        # prompts for user input
            print("2. View Transactions")
            print("3. Delete Transaction")
            print("4. Update Transaction")
            print("5. Transaction Menu")
            print("6. Display Summary")
            print("7. Save and Quit")

            choice = input("Enter your choice (1-7): ")            # get user input as choice

            if choice == '1':
                self.add_transaction()
            elif choice == '2':
                self.view_transactions()
            elif choice == '3':
                self.delete_transaction()
            elif choice == '4':
                self.update_transaction()
            elif choice == '5':
                self.open_gui()
            elif choice == '6':
                self.display_summary()
            elif choice == '7':
                self.save_transactions()
                break
            else:
                print("Invalid choice. Please try again.")              # for invalid user inputs

    def open_gui(self):                      # open the GUI to display transactions from GUI Treeview
        root = tk.Tk()
        app = FinanceTrackerGUI(root, self.transactions)
        root.mainloop()

# create the main program FinanceTracker  
def main():                                
    finance_tracker = FinanceTrackerCLI()

if __name__ == "__main__":
    main()
