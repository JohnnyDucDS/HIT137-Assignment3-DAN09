def celsius_to_fahrenheit(celsius_temp):
    
    # The math formula: (Celsius * 9/5) + 32
    fahrenheit_temp = (celsius_temp * 9/5) + 32
    
    # Send the final calculation back to the user
    return fahrenheit_temp

# --- How to use the function in your code ---

# 1. Pass a number (like 25) into the function and save the result
today_temp = celsius_to_fahrenheit(25)
print(f"Today's temperature is {today_temp} degrees Fahrenheit.") 
# Output: Today's temperature is 77.0 degrees Fahrenheit.

# 2. The beauty of functions is reusing them! Let's do it again.
freezing_point = celsius_to_fahrenheit(0)
print(f"Water freezes at {freezing_point} degrees Fahrenheit.")
# Output: Water freezes at 32.0 degrees Fahrenheit.