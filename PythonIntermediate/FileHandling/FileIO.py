# In this lesson students will learn how to work with files. 'r', 'w', 'r+'

# ######### 1) Reading files
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


# ######### 2) Writing files
with open('new_file.txt', 'w') as file:
    file.write('Hello!')

# ######### 3) Appending to file
with open('new_file.txt', 'a') as file:
    file.write('Hello!')

# ######### Grocery list

# Solution 1: with list append
# item = ''
# item_list = []
# print("Please enter anything you want to add to the list and type quit when you are finished.")
# while True:
#     item = input()
#     if item == 'quit':
#         break
#     if item not in item_list:
#         item_list.append(item)
#
# with open('grocery.txt', 'w') as file:
#     file.write('\n'.join(item_list))


# Solution 2: with r+ mode
item = ''
print("Please enter anything you want to add to the list and type quit when you are finished.")

with open('grocery.txt', 'r+') as file:
    while True:
        item = input()
        if item == 'quit':
            break
        file.seek(0)
        current = file.read()
        if item not in current:
            file.write(item + '\n')


