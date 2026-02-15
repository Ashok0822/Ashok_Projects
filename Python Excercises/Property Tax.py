# Input property value
property_value = float(input("Enter the property actual value: "))
# Calculate assessed value (60% of property value)
assesment_value = 0.6*property_value
# Calculate property tax (0.72% of assessed value)
property_tax = (assesment_value/100)*0.72
# Print assessed value and property tax, #{:.2f}formatted to two decimal values
print("Final assesment_value:{:.2f}".format(assesment_value))
print("Total property_tax:{:.2f}".format(property_tax))
