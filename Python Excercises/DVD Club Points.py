#Request the user to provide the number of videos purchased each month.
customer_purchases = int(input("Enter the number of videos purchased for each month: "))
#Check if the customer made 0 purchases
if customer_purchases == 0:
# If no videos were purchased, the customer earns 0 points
    print("Earned Points = 0")
# Check if the customer made exactly 1 purchase
elif customer_purchases == 1:
# If 1 video was purchased, the customer earns 2 points
    print("Earned points = 2")
# Check if the customer made exactly 2 purchases
elif customer_purchases == 2:
#If 2 videos were purchased, the customer earns 5 points
    print("Earned points = 5")
# Check if the customer made exactly 3 purchases
elif customer_purchases == 3:
# If 3 videos were purchased, the customer earns 10 points
    print("Earned points = 10")
# Check if the customer made 4 or more purchases
elif customer_purchases >= 4:
# If 4 or more videos were purchased, the customer earns 25 points
    print("Earned points = 25")
#Fallback else clause (should not be reached due to above conditions)
else:
#In Default case, printing 0 points if none of the above conditions are applied
    print("Earned points = 0")
