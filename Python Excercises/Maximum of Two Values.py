# Enter the input value of A
A = int(input("Enter the value A: "))
# Enter the input value of B
B = int(input("Enter the value B: "))
#Function to return the greatest of two input values provided
def evaluate_max(A, B):
    if A >= B:
        return A
    else:
        return B
#print the greatest value
print("The greater value is:", evaluate_max(A, B))

