nums = input("Enter comma separated nums: ")

nums_list = nums.split(",")
even = 0
odd = 0

for num in nums_list:
    num = int(num.strip())

    if num % 2 == 0:
        even += 1
    else:
        odd += 1

print("Count of even nums:", even)
print("Count of odd nums:", odd)
