# create list of 100 random numbers from 0 to 1000
# import random module
import random

# declare empty list, which will be filled with random numbers
a = []

# for loop goes from 1 to 100 and adds a random number for each index of the range
for i in range(100):
    a.append(random.randint(0, 1000))

# sort list from min to max (without using sort())
# Bubble sorting method
for i in range(len(a)-1):
    for b in range(len(a)-1-i):
        if a[b] > a[b+1]:
            a[b], a[b+1] = a[b+1], a[b]

#print(a)
# calculate average for even and odd numbers

# declare empty lists, which will be filled with even and odd numbers
even_list = []
odd_list = []

# for loop goes through every number in the list and calculates modula, if it is equal to 0, then the number is even, if it is not, the number is odd
# when even and odd lists are created, their average result is calculated: all the numbers in the list are summed and then divided by the number of elements in the list
for num in a:
    if num % 2 == 0:
        even_list.append(num)
        avg_even = sum(even_list) / len(even_list)
    else:
        odd_list.append(num)
        avg_odd = sum(odd_list) / len(odd_list)

# print both average result in console
print(avg_even)
print(avg_odd)

