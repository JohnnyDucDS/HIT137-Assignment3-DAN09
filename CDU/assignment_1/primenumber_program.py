#find prime number
import math

def find_prime(limit):

    #Limit number to 100
    if limit > 10000:
        print("please enter number less than 1000")
        return

    #Case when there is no prime number
    if limit < 2:
        print("No prime numbers found")
        return
    primes = []

    #Check all numbers from 2 to 100
    for num in range(2, limit):
        is_prime = True
        #Find prime through formula
        for i in range(2, int(math.sqrt(num)+1)):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)

    # Display the results 
    print(f"Prime numbers found: {' '.join(map(str, primes))}")
    print(f"Total primes found: {len(primes)}")
    print(f"Largest prime: {primes[-1]}")
    print(f"Smallest prime: {primes[0]}")
    print(f"Sum of all primes: {sum(primes)}")


# User input
try:
    limit = int(input("Input: "))
    find_prime(limit)
except ValueError:
    print("Please enter a valid integer.")