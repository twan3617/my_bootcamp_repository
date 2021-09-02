import numpy as np

class VendingMachine():
    def __init__(self, money):
        self.items = ["Water", "Coke", "Diet Coke", "Iced Tea", "Swiss Chocolate", "Candy", "Chips",
        "Bubble Gum", "Turkish Delight"]
        self.costs = [0.75, 1.20, 1.20, 1.00, 1.50, 0.95, 1.10, 0.50, 1.20] ### A dictionary here would help!

        self.num_items = len(self.items)

        self.money = money #money put into the vending machine
        self.coins = [1, 0.50, 0.20, 0.10, 0.05] #Coin denominations

        self._PIN = 0000 #Secret maintenance PIN
        self._balance = 0 #Day's balance
        self._max_items = 10
        self._max_coins = 20

        self._stock = self._max_items * np.ones(self.num_items)
        self._num_coins = self._max_coins * np.ones(len(self.costs))
        self._sales = np.zeros(self.num_items)
        self._income = 0

    def DisplayErrorMessage(self):
        print("Error! The selected item is out of stock.")
        return 

    def RestockVend(self):
        self._stock = self._max_items * np.ones(self.num_items) #restock
        self._num_coins = self._max_coins * np.ones(len(self.costs))
        print("Restocking performed.")
        return 

    def ShowMenu(self):
        print(f"Menu: \n")
        for i in range(0,len(self.items)):
            print(f"{i+1}: {self.items[i]}          ${self.costs[i]}")
        return 

    def MakeSelection(self):
        choice = []
        while True: 
            selection = int(input("Choose a number from 1 to 9. "))

            if self._stock[selection-1] == 0: 
                self.DisplayErrorMessage() #Check whether out of stock or not
            else:  
                choice.append(selection)

                if selection == 99: 
                    #Enter maintenance routine
                    PIN = int(input("Enter PIN: "))
                    if PIN == 0000:
                        print(f"Balance: {self._balance} \n Stock: {self._stock} \n Coins: {self._num_coins} \n Sales: {self._sales} \n Income: {self._income}")
                        self.RestockVend()
                        return 

                print(f"You have chosen {selection}: {self.items[selection - 1]}, costing ${self.costs[selection - 1]:.2f}")
                cont = input("Continue? (y/n) ")

                if cont == "n": 
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
        change = []
        temp_money = cost 

        for index, coins in enumerate(self.coins):

            temp_money = np.round_(temp_money, 2)

            (mod, remain) = divmod(temp_money, coins) ### Roundoff errors sometimes??
            ### Evil fix 
            pocket = min(mod, self._num_coins[index])
            temp_money = temp_money - pocket * self.coins[index]
            change.append(pocket)
        


        if temp_money != 0:
            print(temp_money)
            print("We don't have enough change for you. Returning your money...")
            return self.money
        else: 
            print(f"Thank you for your purchase! Your change is:")
            for iters, changes in enumerate(change):
                print(f"{abs(changes):.0f} x {self.coins[iters]:.2f} coin(s)")
        pass 
        

def main():
    if __name__ == "__main__":
        VM = VendingMachine(10)
        VM.ShowMenu()
        (choices, cost) = VM.MakeSelection()
        VM.ReturnChange(choices, cost)

main()