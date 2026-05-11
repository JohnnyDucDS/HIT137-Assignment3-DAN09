#question 2

number = int(input('n = '))
prime_list = []
sum_prime = 0
for x in range(2, number):          # 10: 2 3 4 5 6 7 8 9
    for y in range(2, x):
        if x % y == 0:
            break
    else:
        prime_list.append(x)
        sum_prime += x

print(f'all prime numbers lower than {number}: {prime_list}')
print(f'min = {prime_list[0]}')      # OR prime_list[0]
print(f'max = {prime_list[-1]}')      # OR prime_list[-1]
print(f'sum = {sum_prime}')            # print(sum(prime_list))
