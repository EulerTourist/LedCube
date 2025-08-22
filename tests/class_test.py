class Test:
    var1 = 12 # default value provided by the class
    var2 = 22 # default value that will be overrided by the instance

    def __init__(self, v2, v3):
        self.var2 = v2 # class variable - cls
        self.var3 = v3 # instance variable - self

    def __str__(self):
        return f"{self.var1} {self.var2} {self.var3}"
    

class Dog:
    species = "Canis familiaris"
    def __init__(self, name, age):
       self.name = name
       self.age = age


s = Dog("Henry", 9)
Dog.species = "Dawg"
t = Dog("Max", 3)
t.species = "Gawd Knows"
t.name = "Naughty Max"


print(s.name, s.species, t.name, t.species)