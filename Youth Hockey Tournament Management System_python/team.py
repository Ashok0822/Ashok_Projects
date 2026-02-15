from datetime import datetime

class Team:
    """Represents a youth hockey team participating in a tournament."""

    _id_counter = 1  # Auto-incrementing ID

    def __init__(self, name, team_type, fee_paid, coach, age_group, team_size):
        """Initializes a team with all necessary details."""
        self._id = Team._id_counter  # Unique ID
        Team._id_counter += 1  # Increment counter for next team

        self._date = datetime.now().strftime("%Y-%m-%d")  # Auto-set creation date
        self.cancellation_date = None  #  New attribute to store cancellation date

        # Validate and set attributes
        self.name = self._validate_name(name)
        self.type = self._validate_type(team_type)
        self.fee_paid = fee_paid  # Boolean: True = Paid, False = Not Paid
        self.fee = 500  # Fixed participation fee

        self.coach = self._validate_name(coach)  # Validate coach name
        self.age_group = self._validate_age_group(age_group)# Validate age group
        self.team_size = self._validate_team_size(team_size)# Validate team size

    # Read-only properties for ID and Date
    @property
    def id(self):
        return self._id

    @property
    def date(self):
        return self._date

    @staticmethod
    def _validate_name(name):
        """Ensures name is not empty and formats it correctly."""
        if not name.strip():
            raise ValueError("Name cannot be empty.")
        return name.strip().title()

    @staticmethod
    def _validate_type(team_type):
        """Ensures type is either 'boys' or 'girls'."""
        team_type = team_type.strip().lower()
        if team_type not in ["boys", "girls"]:
            raise ValueError("Invalid type. Must be 'boys' or 'girls'.")
        return team_type

    @staticmethod
    def _validate_age_group(age_group):
        """Ensures age group is valid (between 5-18 years)."""
        if not (5 <= age_group <= 18):
            raise ValueError("Age group must be between 5 and 18 years.")
        return age_group

    @staticmethod
    def _validate_team_size(team_size):
        """Ensures team size is reasonable (5-20 players)."""
        if not (5 <= team_size <= 20):
            raise ValueError("Team size must be between 5 and 20 players.")
        return team_size

    # Getter and Setter for Name
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = self._validate_name(value)

    # Getter and Setter for Type
    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = self._validate_type(value)

    # Getter and Setter for Fee Paid
    @property
    def fee_paid(self):
        return self._fee_paid

    @fee_paid.setter
    def fee_paid(self, value):
        if not isinstance(value, bool):
            raise ValueError("Fee paid must be True or False.")
        self._fee_paid = value
        
    def cancel_participation(self, cancel_date):
        """Stores the cancellation date when a team cancels."""
        self.cancellation_date = cancel_date
        print(f"Participation for team '{self.name}' has been cancelled on {cancel_date}.")

    def get_details(self):
        """Returns a dictionary of all team details."""
        return {
            "ID": self._id,
            "Created Date": self._date,
            "Team Name": self.name,
            "Type": self.type.capitalize(),
            "Fee Paid": "Yes" if self.fee_paid else "No",
            "Fee Amount": self.fee,
            "Coach": self.coach,
            "Age Group": self.age_group,
            "Team Size": self.team_size,
        }

    def __str__(self):
        """Returns a string representation of the team."""
        fee_status = "Paid" if self.fee_paid else "Not Paid"
        return (f"ID: {self._id} , Date: {self._date} | Name: {self.name} | "
                f"Type: {self.type.capitalize()} | Coach: {self.coach} | "
                f"Age Group: {self.age_group} | "
                f"Team Size: {self.team_size} | Fee: {self.fee} ({fee_status}) | "
                f"Cancellation Date: {self.cancellation_date}")

    # Create Team from Dictionary    
    @staticmethod
    def from_dict(data):
        """Creates a Team instance from a dictionary."""
        team = Team(data["name"], data["type"], data["fee_paid"], data["coach"], 
                    data["age_group"], data["team_size"])
        team._id = data["id"]
        team._date = data["date"]
        Team._id_counter = max(Team._id_counter, team._id + 1)
        return team

    # Convert Team to Dictionary
    def to_dict(self):
        """Converts the Team object to a dictionary."""
        return {
            "id": self._id,
            "date": self._date,
            "name": self.name,
            "type": self.type,
            "fee_paid": self.fee_paid,
            "fee": self.fee,
            "coach": self.coach,
            "age_group": self.age_group,
            "team_size": self.team_size,
            "cancellation_date": self.cancellation_date
        }