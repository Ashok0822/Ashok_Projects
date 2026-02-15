# Import the math module for mathematical functions
import math
# Get the user's weight in kilograms
weight = float(input("Enter your weight in kgs: "))
# Get the user's height in meters
height = float(input("Enter your height in Meters: "))
# Calculate the Body Mass Index (BMI) # Divide weight by the square of height
BMI = weight/math.pow(height,2)
# Print the BMI, formatted to 2 decimal places
print("Your BMI is: {:.2f}".format(BMI))
# print the weight category based on BMI value
if BMI < 18.5:
    print("You are Under weight")
elif BMI <= 22.99:
    print("You are Normal Weight")
elif BMI <= 29.99:
    print("You are Over Weight")
else:
    print("You have Obesity")
