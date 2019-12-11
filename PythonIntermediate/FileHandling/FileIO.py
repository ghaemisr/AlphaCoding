# ######### Reading files
with open('myfile.txt', 'r') as file:
    content = file.read()

# ######### Read file challenge
# Solution 1
listed = content.split('.\n')
for i in listed:
    if i[-1] == '.':
        print(i.replace('\n', ' '))
    else:
        print(i.replace('\n', ' ') + '.')

# Solution 2
listed = content.split('.')
for i in listed:
    if len(i) > 0:
        print(i.strip().replace("\n", " ") + '.')

# Solution 3
listed = content.split('.')
for i in listed:
    if len(i) > 0:
        if i[0] == '\n':
            i = i[1:]
        print(i.replace("\n", " ") + ".")


# ######### Writing files
with open('new_file.txt', 'w') as file:
    file.write('Hello!')

# ######### Appending to file
with open('new_file.txt', 'a') as file:
    file.write('Hello!')

# ######### Grocery list
