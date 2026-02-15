from datetime import datetime  # Import datetime module for handling date-related operations
from team import Team # Import the Team class from the team module

class UserInterface:
    """It Handles the user interface for managing youth hockey teams."""

    def __init__(self):
        """Initializes the menu with an empty list of teams."""
        self.teams = []  # List to store team instances
        self.cancellation_date = None # Initializes cancellation_date as None
        self._date = datetime.today().strftime('%Y-%m-%d')

    def display_menu(self):
        """Displays the main menu options to the user."""
        print("\nYouth Hockey Cup Team Details")
        print("1. Create a new team") #To create a new team
        print("2. View team details by ID") # View details of a specific team
        print("3. List all teams") #Display all teams
        print("4. List all boys teams") #Display boys team
        print("5. List all girls teams") #Display girls team
        print("6. Update an existing team") # Modify the details of existing team
        print("7. Delete a team") # Delete a team from the list
        print("8. Save teams to file") #Save the team details to a file
        print("9. retrieve the teams from file") # Load the teams from the file
        print("10. Cancel Team Participation") #remove a team from the participation
        print("11. Show total number of teams") #It shows the total number of teams
        print("12. Show percentage of teams that have paid their fee") # It dispays the fee payment percentage
        print("0. Exit the program") # Option to exit the program

    def create_team(self):
        """Prompts the user for team information and creates a new team."""
        print("\nEnter the details of the new team:")
        name = input("Team Name: ")
        
        # Validate team type (must be 'boys' or 'girls')
        while True:
            team_type = input("Team Type (boys/girls): ").strip().lower()
            if team_type in ['boys', 'girls']:
                break
            else:
                print("Invalid type. Please enter 'boys' or 'girls'.")
        
        fee_paid = input("Fee Paid (yes/no): ").lower() == 'yes' #convert input to Boolean
        coach = input("Coach Name: ")
        age_group = int(input("Age Group (5-18): ")) #It checks the age is within valid range
        team_size = int(input("Team Size (5-20): ")) #The Team size is within valid range

        new_team = Team(name, team_type, fee_paid, coach, age_group, team_size) #create a new team instance
        self.teams.append(new_team)  # Add the new team instance to the list
        print(f"Team '{new_team.name}' has been successfully created!")

    def view_team(self):
        """Prompts the user for a team ID and displays the team's details."""
        print("\nExisting team ID's:")
        for team in self.teams:
                print(team.id) #Display team details

        team_id = int(input("\nEnter the Team ID to view: "))
        team = self._find_team_by_id(team_id)
        if team:
            print("\nTeam Details:")
            print(team) #Print Details of teams
        else:
            print("No team found with that ID.") #Display error if no team found

    def list_teams(self):
        """Displays all teams that are currently registered."""
        if not self.teams:
            print("\nNo teams available.") #Display message if no teams exits
        else:
            print("\nList of all teams:")
            for team in self.teams:
                print(team) #Print details fo all teams

    def list_boys_teams(self):
        """Lists all boys' teams."""
        boys_teams = [team for team in self.teams if team.type == 'boys'] #It filters the Boys teams
        if not boys_teams:
            print("\nNo boys' teams available.") #Diplay a message if no boys team exit
        else:
            print("\nList of all boys' teams:")
            for team in boys_teams:
                print(team) #print details of boys 'teams'

    def list_girls_teams(self):
        """Lists all girls' teams."""
        girls_teams = [team for team in self.teams if team.type == 'girls']
        if not girls_teams:
            print("\nNo girls' teams available.") #Diplay a message if no girls team exit
        else:
            print("\nList of all girls' teams:")
            for team in girls_teams:
                print(team)#print details of girls 'teams'

    def update_team(self):
        """Allows the user to select and update a team."""
        print("\nExisting team ID's:")
        for team in self.teams:
                print(team.id)  # Display all existing team IDs before updating

        team_id = int(input("\nEnter the Team ID to update: ")) # Get user input for team ID
        team = self._find_team_by_id(team_id) # Find team by ID
        if team:
            print("\nCurrent Details:")
            print(team) # Display current team details

            # Allow user to update details, keeping current values if input is blank
            name = input("New Team Name (leave blank to keep current): ") 
            team.name = name if name else team.name
            while True:
                team_type = input("New Team Type (boys/girls, leave blank to keep current): ").strip().lower()
                if team_type in ['boys', 'girls'] or not team_type:  # Validate input
                    team.type = team_type if team_type else team.type
                    break
                else:
                    print("Invalid type. Please enter 'boys' or 'girls'.")
            coach = input("New Coach Name (leave blank to keep current): ")
            team.coach = coach if coach else team.coach # Update coach name
            while True:
                try:
                    age_group = input(f"New Age Group (Current: {team.age_group}, leave blank to keep current): ")
                    team.age_group = int(age_group) if age_group else team.age_group
                    if 5 <= team.age_group <= 18: # Validate age group
                        break
                    else:
                        print("Age group must be between 5 and 18.")
                except ValueError:
                    if age_group == "": # Allow blank input
                        break
                    else:
                        print("Invalid input. Please enter a number between 5 and 18.")
            
            # Update team size
            while True:
                try:
                    team_size = input(f"New Team Size (Current: {team.team_size}, leave blank to keep current): ")
                    team.team_size = int(team_size) if team_size else team.team_size # Update if input is given
                    if 5 <= team.team_size <= 20: # Ensure valid range
                        break
                    else:
                        print("Team size must be between 5 and 20.")
                except ValueError:
                    if team_size == "":
                        break
                    else:
                        print("Invalid input. Please enter a number between 5 and 20.")
            
            # Update fee paid status
            fee_paid = input(f"Fee Paid (Current: {'Yes' if team.fee_paid else 'No'}, yes/no, leave blank to keep current): ").lower()
            if fee_paid == "yes":
                team.fee_paid = True # Update if 'yes' is entered
            elif fee_paid == "no":
                team.fee_paid = False # Update if 'no' is entered
            print(f"Team '{team.name}' has been updated successfully!")
        else:
            print("No team found with that ID.") # Show message if no team found


    def delete_team(self):
        """Prompts the user to confirm and remove a team by its ID."""
        print("\nExisting team ID's:")
        for team in self.teams:
                print(team.id) # Display all teams
        team_id = int(input("\nEnter the Team ID to delete: "))
        team = self._find_team_by_id(team_id) # Find team by ID
        if team:
            print(f"Are you sure you want to delete this team? {team}")
            confirm = input("Type 'yes' to delete, 'no' to cancel: ").lower()
            if confirm == 'yes':
                self.teams.remove(team) # Remove team from list
                print(f"Team '{team.name}' has been deleted.")
            else:
                print("Deletion cancelled.")
        else:
            print("No team found with that ID.") # Show message if no team found


    def save_to_file(self):
        """Saves the list of teams to a plain text file."""
        with open("teams.txt", "w") as file:
            for team in self.teams:
                file.write(f"ID: {team.id} | Date: {self._date} | Name: {team.name} | Type: {team.type} | "
                           f"Fee Paid: {'Yes' if team.fee_paid else 'No'} | Coach: {team.coach} | "
                           f"Age Group: {team.age_group} | Team Size: {team.team_size} | "
                           f"Cancellation Date: {team.cancellation_date}\n")
        print("All teams have been saved to the file.") # Confirm save

    def load_from_file(self):
        """Loads the list of teams from a plain text file."""
        try:
            with open("teams.txt", "r") as file:
                lines = file.readlines() # Read file line by line
                for line in lines:
                    parts = line.strip().split("| ")
                    team_data = {}
                    for part in parts:
                        key, value = part.split(": ")
                        team_data[key] = value
                    # Extract data and create Team objects
                    name = team_data["Name"]
                    team_type = team_data["Type"]
                    fee_paid = team_data["Fee Paid"] == "Yes" # Convert to boolean
                    coach = team_data["Coach"]
                    age_group = int(team_data["Age Group"])
                    team_size = int(team_data["Team Size"])

                    new_team = Team(name, team_type, fee_paid, coach, age_group, team_size)
                    self.teams.append(new_team) # Add team to list
            print("Teams have been successfully loaded from the file.") # Confirm load
        except FileNotFoundError:
            print("No saved teams found.") # Handle missing file

    def cancel_team_participation(self):
        """Prompts the user for a team ID and cancels participation."""
        print("\nExisting team ID's:")
        for team in self.teams:
                print(team.id)
        team_id = int(input("\nEnter the Team ID to cancel participation: "))
        team = self._find_team_by_id(team_id)  # Find team by ID
        if team:
            cancel_date = input("Cancellation date YYYY-MM-DD: ")
            try:
                cancel_date = datetime.strptime(cancel_date, '%Y-%m-%d').date()  # Correct date format
                team.cancel_participation(cancel_date) # Call method to cancel participation
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.") # Handle invalid input
        else:
            print("No team found with that ID.") # Show message if no team found

    def show_total_teams(self):
        """Shows the total number of teams."""
        print(f"Total number of teams: {len(self.teams)}")  # Print count

    def show_fee_paid_percentage(self):
        """Shows the percentage of teams that have paid their fee."""
        if not self.teams:
            print("No teams available to calculate percentage.") # Handle no teams case
            return
        
        paid_teams = sum(1 for team in self.teams if team.fee_paid)# Count paid teams
        percentage = (paid_teams / len(self.teams)) * 100  # Calculate percentage
        print(f"{paid_teams} out of {len(self.teams)} teams have paid their fee. "
              f"Percentage: {percentage:.2f}%") # Display percentage

    def _find_team_by_id(self, team_id):
        """Searches for a team by its ID."""
        return next((team for team in self.teams if team.id == team_id), None) # Find and return team

    def run(self):
        """Runs the menu system and handles user input."""
        while True:
            self.display_menu() # Show menu options
            choice = input("\nEnter your choice: ")

            if choice == '1':
                self.create_team()# Create a team
            elif choice == '2':
                self.view_team()  # View team details
            elif choice == '3':
                self.list_teams() # List all teams
            elif choice == '4':
                self.list_boys_teams() # List boys' teams
            elif choice == '5':
                self.list_girls_teams() # List girls' teams
            elif choice == '6':
                self.update_team() # Update team details
            elif choice == '7':
                self.delete_team()# Delete a team
            elif choice == '8':
                self.save_to_file()# Save teams to file
            elif choice == '9':
                self.load_from_file()# Load teams from file
            elif choice == '10':
                self.cancel_team_participation()# Cancel a team's participation
            elif choice == '11':
                self.show_total_teams()# Show total teams
            elif choice == '12':
                self.show_fee_paid_percentage()# Show fee payment percentage
            elif choice == '0':
                print("Exiting the program. Thank you!") # Exit program
                break
            else:
                print("Invalid input, please try again.")# Handle invalid input