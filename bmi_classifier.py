import datetime
from bisect import bisect


### The following code creates a basic BMI classifier.
### When run, you will be asked for your birthdate, age, weight and height. Then it will compute
### your BMI (making the necessary conversions), and return your classification on the BMI scale.

### FUTURE IMPROVEMENTS:
### Instead, we can instantiate a Person class which has attributes age, height and weight.

# class Person: 
#     def __init__(self, id, fname, lname, email): 
#         self.personid = id
#         self.fname = fname
#         self.lname = lname
#         self.age = 0 
#         self.weight = 0

#         self.height = 1
#         self.email = email
#         self.past_weights = []
#         self.weight_date = []
#         self.BMI = 0
    
#     def __iter__(self):
#         for attr, value in self.__dict__.iteritems():
#             yield attr, value
# Put in an __iter__ method, like above, or use vars(instance) to get a dictionary of attributes 

def get_bdate():
    print(f"Enter the following information using numeric values. \n")
    
    #Obtain year month day information
    year = int(input('Enter a year: ')) 
    month = int(input('Enter a month: '))
    day = int(input('Enter a day: '))


    #For aesthetic purposes
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"] 
    
    date1 = datetime.date(year, month, day)
    now = datetime.datetime.now()
    age = now.year - year #Compute turning age

    print(f"Your birthdate is {day} {months[month-1]}, {year}. You are turning {age}.")
    return age

#Get height and weight function
def get_hw():
    weight = int(input("Please input your weight in kg: "))

    height_unit = input("What unit do you want to input your height in? Choose out of meters (type m) or inches and feet (type f) . \n") 
    
    meter_option = ["meters", "metres", "meter", "m"]
    feet_option = ["ft", "feet", "f", "i", "inches", "in"]
    if height_unit in meter_option:
        height = float(input("Please input your height in meters (m). "))
    elif height_unit in feet_option:
        feet_inch = input("Please input your height in feet and inches in the form *ft **in.")
        feet_inch = int(''.join(c for c in feet_inch if c.isdigit())) # If feet_inch is given with chars, remove them and turn into 3 digit int.
        temp = divmod(feet_inch,100) #temp is of the form (ft, in); now perform conversion to meters
        height = 0.3048 * temp[0] + 0.0254 * temp[1]

    print(f"Your weight is {weight} kg. Your height is (after conversion, if required) {height:.3f} meters.")
    return weight, height

def get_bmi(weight, height): #bmi computation
    bmi = weight / (height**2)
    return bmi


def get_class(bmi, breakpoints, classify): #Use bisect function and breakpoints to fit given bmi into classes.
    i = bisect(breakpoints, bmi)
    return classify[i]


if __name__ == "__main__": 
    while True:
        #BMI = kg / m^2
        age = get_bdate()
        weight, height = get_hw()
        bmi = get_bmi(weight, height)

        # Adults range
        if age >= 18:
            breakpoints = [16, 17, 18.5, 25, 30, 35, 40]
            classify = ["Underweight (severe thinness)", "Underweight (moderate thinness)", "Underweight (mild thinness)", 
            "Normal range", "Overweight (pre-obese)", "Obese (I)", "Obese (II)", "Obese (III)"]
        else: #Children range
            breakpoints = [20, 29, 31, 32]
            classify = ["Underweight", "Healthy weight", "Overweight", "Obese"]

        classification = get_class(bmi, breakpoints, classify)

        print(f"Your results: You have a BMI of {bmi:.3f}. You are classified as: {classification}. \n")


        #Quitting loop. 
        quit = input("Do you want to quit? (y/n)\n")
        options = ["y", "n"]
        if quit not in options:
            print(f"Type either y or n.")

        elif quit == "y":
            print(f"Quitting...")
            break


    


