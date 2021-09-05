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

### List of machines in a given state
class MachineList():
    def __init__(self, vendors): #initiation takes in a list of vending machine classes
        self.IDLoc = { "ID":{vendor.ID: vendor for vendor in vendors}, "Location": {vendor.location: vendor for vendor in vendors}}
        return 
        
    def addVendor(self, vendor): #Alternatively, add vending machines using add_vendor method
        self.IDLoc["ID"][vendor.ID] = vendor
        self.IDLoc["Location"][vendor.location] = vendor
        return
    
    def printList(self):
        for choice, vendor_dict in self.IDLoc.items(): 
            print(choice + ': ')
            for ID in vendor_dict.keys():
                print(ID)
        return 

class ShopItem():
    def __init__(self, cost, stock, sales):
        self.cost = cost
        self.stock = stock
        self.sales = sales
### Coins are also a shop item; the "sales" attribute refers to the number of # coins used.

class VendingMachine():
    def __init__(self, money, location):
        ### Generate a random 6 digit number for itself.
        self.ID = ''.join(["{}".format(np.random.randint(0, 9)) for num in range(0, 10)]) 
        self.location = location

        self.money = money #money put into the vending machine

        self._max_items = 10 #Maximum stock of items and coins
        self._max_coins = 20
        self._PIN = 0000 #Secret maintenance PIN
        self._balance = money #Current remaining balance

        item_names = ["Water", "Coke", "Diet Coke", "Iced Tea", "Swiss Chocolate", "Candy", "Chips",
        "Bubble Gum", "Turkish Delight"] #List of item names
        costs = [0.75, 1.20, 1.20, 1.00, 1.50, 0.95, 1.10, 0.50, 1.20]
        coins = [1, 0.50, 0.20, 0.10, 0.05] #Coin denominations
        self.num_items = len(item_names)
        dict_items = dict(zip(item_names, costs))

        self.items = {name: ShopItem(cost, self._max_items, 0) for name, cost in dict_items.items()}
        self.coins = {denom: ShopItem(denom, self._max_coins, 0) for denom in coins}
        self._sales = dict(zip(item_names,np.zeros(self.num_items)))

        self._income = 0

    def DisplayErrorMessage(self):
        print("Error! The selected item is out of stock.") #Generic error message.
        return 

    def RestockVend(self):
        for item in self.items.values(): 
            item.stock = self._max_items
        for coin in self.coins.values(): 
            coin.stock = self._max_coins
        print("Restocking performed.")
        return 

    def ComputeCost(self, choice): #Given a list of selections, return the total cost.
        cost = 0
        for select in choice: 
            item_key = list(self.items.keys())[select-1]
            cost += self.items[item_key].cost
        return cost

    def ShowMenu(self):
        for name, item in self.items.items():
            print(f"{name}: ${item.cost}")
        pass

    def MakeSelection(self):
        choice = []
        choice_names = []
        while True: 
            selection = int(input("Choose an option from 1 to 9, or 10 to quit. "))
            ### Check if secret code was given first
            if selection == 99: 
                #Enter maintenance routine
                PIN = int(input("Enter PIN: "))

                if PIN == 0000: ###Odd thing is happening with \, \n and spacing - fix?
                    print(f"Balance: ${self._balance}\n\
                    Income: ${self._income:.2f}\n\
                    Stock (Items): { {str(item_name): item.stock for item_name, item in self.items.items() } }\n\
                    Stock (Coins): { {denom: coin.stock for denom, coin in self.coins.items()} }")
                    self.RestockVend()
                    return [], 0

            if selection == 10:
                print("Your selections have been made.")
                return choice, self.ComputeCost(choice)

            item_key = list(self.items.keys())[selection-1]
            choice_names.append(item_key)

            if self.items[item_key].stock == 0: 
                self.DisplayErrorMessage() 

            else:  
                choice.append(selection)

                print(f"You have chosen {selection}: {item_key}, costing ${self.items[item_key].cost:.2f}")
                cont = input("Continue? (y/n) ")

                if cont == "n":  #Use switch() statements here instead?
                    cost = self.ComputeCost(choice)
                    if cost > self.money: 
                        print("You don't have enough money! Returning...")
                        return [], 0
                    print(f"Your total cost is ${cost:.2f}.")
                    return choice, cost

                elif cont == "y":
                    print(f"The running total is ${self.ComputeCost(choice):.2f}, with selections:")
                    print(choice_names)
                else: 
                    print("Invalid input.")
                    return choice, self.ComputeCost(choice)          
        return 
        
    def ReturnChange(self, choice, cost): #Takes in selected choices as a list
        if (choice == []) and (cost == 0):
            return
        change_dict = dict()
        temp_money = cost 
        for denom, coin in self.coins.items():
            temp_money = np.round_(temp_money, 2)
            (mod, remain) = divmod(temp_money, denom) ### Roundoff errors sometimes??
            pocket = min(mod, coin.stock) ### The pocket change taken out of the machine
            temp_money = temp_money - pocket * coin.cost
            change_dict[denom] = pocket
            ### Decrease num_coins by pocket
            coin.stock -= pocket
            coin.sales += pocket

        if temp_money != 0: #After spitting out all change, there is still money left.
            print(temp_money)
            print("We don't have enough change for you. Returning your money...")
            return self.money
        else:
            self._balance -= cost #Purchase complete: update balance and cost.
            self._income += cost
            print(f"Thank you for your purchase! Your change is:")
            for denom, pocket in change_dict.items():
                print(f"{pocket:.0f} x {denom:.2f} coin(s)")

        
        pass

def main():
    # if __name__ == "__main__":
    #     VM = VendingMachine(10, "Sydney")
    #     while True: 
    #         VM.ShowMenu()
    #         choice, cost = VM.MakeSelection()
    #         VM.ReturnChange(choice, cost)
    # return 0 
    VM1 = VendingMachine(10, "Sydney")
    VM2 = VendingMachine(10, "Auckland")
    VM3 = VendingMachine(10, "Venice")
    
    V = [VM1, VM2, VM3]

    ML = MachineList(V)
    ML.printList()

main()