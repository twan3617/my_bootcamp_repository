
class Person: 
    def __init__(self, id, fname, lname, email): 
        self.personid = id
        self.fname = fname
        self.lname = lname
        self.age = 0 
        self.weight = 0

        self.height = 1
        self.email = email
        self.past_weights = []
        self.weight_date = []
        self.BMI = 0
    
    def __iter__(self):
        for attr, value in self.__dict__.iteritems():
            yield attr, value
        