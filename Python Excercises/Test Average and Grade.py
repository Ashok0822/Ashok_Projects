# Input five test scores
Test1 = int(input("Enter the Score of Test1: "))
Test2 = int(input("Enter the Score of Test2: "))
Test3 = int(input("Enter the Score of Test3: "))
Test4 = int(input("Enter the Score of Test4: "))
Test5 = int(input("Enter the Score of Test5: "))
#Function to calculate the average score
def calc_average(Test1 ,Test2 ,Test3 ,Test4 ,Test5):
    return(Test1+Test2+Test3+Test4+Test5)/5
average= calc_average(Test1 ,Test2 ,Test3 ,Test4 ,Test5)
#Print the average score
print("The average score is:", average)
#Function to find the letter grade based on the average
def determine_grade(average):
    if average >=90 and average <=100:
        return 'A'
    elif average >=80 and average <=89:
        return 'B'
    elif average >=70 and average <=79:
        return 'C'
    elif average >=60 and average <=69:
        return 'D'
    elif average <60:
        return 'F'
    else:
        return 'Enter the valid Score'
#Print the letter grade for the average score
grade = determine_grade(average)
print("The letter grade is:" , grade)




