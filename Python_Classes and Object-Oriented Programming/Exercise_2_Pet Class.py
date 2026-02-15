#Class to represent a pet name, pet type and pet age.   
class Pet:
    def __init__(self, name, animal_type, age):
        self._name = name
        self._animal_type = animal_type
        self._age = age

    # Accessors(Getter)- Used to 'Get' the value of a private field.
    def get_name(self):
        return self._name
    
    def get_animal_type(self):
        return self._animal_type
    
    def get_age(self):
        return self._age

    # Mutators (Setter)-Used to 'Set' the value of a private field.
    def set_name(self, name):
        self._name = name
    
    def set_animal_type(self, animal_type):
        self._animal_type = animal_type
    
    def set_age(self, age):
        self._age = age

# Function to get the user input and create pet objects
def main():
    pets = []  # List to store pet objects
    #Get the number of pets from the user
    num_pets = int(input("How many pets do you like to add? "))
    
    #User needs to enter the pet details
    for i in range(num_pets):
        print(f"\nEnter details for pet {i+1}:")
        name = input("Enter the pet name: ")
        animal_type = input("Enter the type of pet (Bird, Dog, Cat, Rabbit, etc.,): ")
        age = int(input("Enter the age of pet: "))

        #Creates a pet object
        pet = Pet(name, animal_type, age)
        pets.append(pet)

    #Added the loop to go through the list and display the requested data according to the option chosen by user.
    while True:
        print("\nOptions:")
        print("1. Display all pets")
        print("2. Display pets of a specific type")
        print("3. Display pets of a specific age")
        print("4. Exit")
        choice = input("Enter your choice: ")

        
        #Option 1 - Display list of all the pets.
        if choice == '1':
            print("\nList of all pets:")
            for pet in pets:
                print(f"Name: {pet.get_name()}, Type: {pet.get_animal_type()}, Age: {pet.get_age()}")

                
        #Option 2 - Gives the type of the pet to display
        elif choice == '2':
            search_type = input("Enter the type of pet to display (e.g., Bird, Dog, Cat, Rabbit): ")
            print(f"\nPets of type {search_type}:")
            found = False

            #Checks for the matching pets type
            for pet in pets:
                if pet.get_animal_type().lower() == search_type.lower():
                    print(f"Name: {pet.get_name()}, Age: {pet.get_age()}")
                    found = True
            if not found:
                print("This type of pets not found")

        #Option 3 - Displays the pets of specific age
        elif choice == '3':
            try:
                search_age = int(input("Enter the age of pets to display: "))
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue
            
            print(f"\nThe pet age entered is {search_age}:")
            found = False
            for pet in pets:
                if pet.get_age() == search_age:
                    print(f"Name: {pet.get_name()}, Type: {pet.get_animal_type()}")
                    found = True
            if not found:
                print("No pets found of this age.")

        #Option 4 - Exits the program
        elif choice == '4':
            print("Exit program.")
            break

        #If no option selected, then it will display the Invalid option.
        else:
            print("Invalid option, please try again with valid option.")

# Run the program
if __name__ == "__main__":
    main()
