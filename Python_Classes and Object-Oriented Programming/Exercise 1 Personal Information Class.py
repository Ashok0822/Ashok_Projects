#Class to hold the personal data like name, address, age, phone number.
class PersonalData:
    def __init__(self, name, address, age, phone_number):
        self._name = name
        self._address = address
        self._age = age
        self._phone_number = phone_number

    # Mutators (Setter)-Used to "set" the value of a private field.
    def set_name(self, name):
        self._name = name
    def set_address(self, address):
        self._address = address
    def set_age(self, age):
        self._age = age
    def set_phone_number(self, phone_number):
        self._phone_number = phone_number
        
    # Accessors(Getter)- Used to "get" the value of a private field.
    def get_name(self):
        return self._name
    def get_address(self):
        return self._address
    def get_age(self):
        return self._age
    def get_phone_number(self):
        return self._phone_number 

    # String representation, which converts the object data into a readable string format.
    def __str__(self):
        return f"Name: {self._name}, Address: {self._address}, Age: {self._age}, Phone_number: {self._phone_number} \n"    

# Create an object with the data.
Personal_Information = PersonalData("Ashok Enukonda", "Dalarna, Sweden", 25, "+46 742561324 \n")

# Access details via getter method
print("Personal Information")
print("Name:", Personal_Information.get_name())
print("Address:", Personal_Information.get_address())
print("Age:", Personal_Information.get_age())
print("Phone_number:", Personal_Information.get_phone_number())


# Modify details using setter method
Personal_Information.set_name("Vishal Gunni")
Personal_Information.set_address("Ladugårdsgatan 20, Sundbyberg, Stockholm 17466")
Personal_Information.set_age(30)
Personal_Information.set_phone_number("+46 767676767")


# Prints the updated object details
print("Friend Information")
print(Personal_Information) 

Personal_Information.set_name("John Smith")
Personal_Information.set_address("Fleminggatan 18, Kungsholmen, Stockholm 11226")
Personal_Information.set_age(34)
Personal_Information.set_phone_number("+46 734732723")


# Prints the updated object details
print("Family Information")
print(Personal_Information)
