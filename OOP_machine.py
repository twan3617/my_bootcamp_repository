import numpy as np

### A basic rendition of the "vending machine" exercise. 
### Initiate the vending machine by instantiating the VendingMachine class with some initial amount of money.
### The vending machine comes with ShowMenu, MakeSelection and ReturnChange methods implemented. 
### It keeps track of the available items, costs, the number of items remaining in the machine, 
### the number of coins available to give out for change, the current balance, the days income and 
### the number of sales per item. If option 99 and PIN 0000 is given at the selection phase, 
### the machine prints the tracked information and restocks itself.

### FUTURE IMPROVEMENTS
### Use switch statements to remove the many if-else statements
### Use OOP to remove redundancies
### Also, use OOP to create a state-wide and nation-wide list of vending machines.

class VendingMachine():
    def __init__(self, money):
        self.items = ["Water", "Coke", "Diet Coke", "Iced Tea", "Swiss Chocolate", "Candy", "Chips",
        "Bubble Gum", "Turkish Delight"]
        self.costs = [0.75, 1.20, 1.20, 1.00, 1.50, 0.95, 1.10, 0.50, 1.20] ### A dictionary here would help!

        self.num_items = len(self.items)

        self.money = money #money put into the vending machine
        self.coins = [1, 0.50, 0.20, 0.10, 0.05] #Coin denominations

        self._PIN = 0000 #Secret maintenance PIN
        self._balance = money #Current remaining balance
        self._max_items = 10
        self._max_coins = 20

        self._stock = self._max_items * np.ones(self.num_items)
        self._num_coins = self._max_coins * np.ones(len(self.costs))
        self._sales = np.zeros(self.num_items)
        self._income = 0

    def DisplayErrorMessage(self):
        print("Error! The selected item is out of stock.") #Generic error message.
        return 

    def RestockVend(self):
        self._stock = self._max_items * np.ones(self.num_items) #restock coins and stock
        self._num_coins = self._max_coins * np.ones(len(self.costs))
        print("Restocking performed.")
        return 

    def ShowMenu(self):
        print(f"Menu:")
        for i in range(0,len(self.items)):
            print(f"{i+1}: {self.items[i]}          ${self.costs[i]}") #For future: align the print statements?
        return 

    def MakeSelection(self):
        choice = []
        while True: 
            selection = int(input("Choose an option from 1 to 9, or 10 to quit."))
            
            ### Check if secret code was given first
            if selection == 99: 
                #Enter maintenance routine
                PIN = int(input("Enter PIN: "))
                if PIN == 0000:
                    print(f"Items: {self.items} \n Balance: ${self._balance} \n Stock: {self._stock} \n Coins: {self._num_coins} \n Sales: {self._sales} \n Income: ${self._income:.2f}")
                    self.RestockVend()
                    return [], 0

            if selection == 10:
                print("Quitting...")
                return [10], 0

            ### Otherwise, check whether out of stock or not
            if self._stock[selection-1] == 0: 
                self.DisplayErrorMessage() 
            else:  
                choice.append(selection)

                print(f"You have chosen {selection}: {self.items[selection - 1]}, costing ${self.costs[selection - 1]:.2f}")
                cont = input("Continue? (y/n) ")

                if cont == "n":  #Use switch() statements here instead?
                    cost = self.ComputeCost(choice)
                    if cost > self.money: 
                        print("You don't have enough money! Returning...")
                        return 
                    print(f"Your total cost is ${cost:.2f}.")
                    return (choice, cost)

                elif cont == "y":
                    print(f"Your current choices are:")
                    for choices in choice:
                        print(f"{self.items[choices-1]}")
                    pass 
                else: 
                    print("Invalid input.")
                    return 

    def ComputeCost(self, choice): #given a selection of items, return total cost
        cost = 0
        for selection in choice:
            cost += self.costs[selection-1] 
        return cost

    def ReturnChange(self, choice, cost): #takes in the selected choices as a list.
        ### For maintenance routine: if inputs are default values, return.
        if (choice == []) and (cost == 0):
            return
        change = []
        temp_money = cost 

        for index, coins in enumerate(self.coins):

            temp_money = np.round_(temp_money, 2)

            (mod, remain) = divmod(temp_money, coins) ### Roundoff errors sometimes??
            ### Evil fix 
            pocket = min(mod, self._num_coins[index])
            temp_money = temp_money - pocket * self.coins[index]
            change.append(pocket)
            ### Decrease num_coins by pocket
            self._num_coins[index] = self._num_coins[index] - pocket

        if temp_money != 0: #After spitting out all change, there is still money left.
            print(temp_money)
            print("We don't have enough change for you. Returning your money...")
            return self.money
        else: 
            print(f"Thank you for your purchase! Your change is:")
            for iters, changes in enumerate(change):
                print(f"{abs(changes):.0f} x {self.coins[iters]:.2f} coin(s)")

            # Decrease stock and increase sales, increase income. Change baalnce
        for selections in choice:
            self._stock[selections-1] -= 1 #note that the stock > 0 check is made at selection.
            self._sales[selections-1] += 1
            self._income += self.costs[selections-1]
            self._balance -= self.costs[selections-1]
        return 0   
        

def main():
    if __name__ == "__main__":
        VM = VendingMachine(10)
        VM.ShowMenu()
        while True: 
            (choices, cost) = VM.MakeSelection()
            if 10 in choices: 
                break
            VM.ReturnChange(choices, cost)

main()