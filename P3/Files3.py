with open('document.txt', 'w') as doc:
  doc.write('Something')

with open('anotherdoc.txt', 'r') as doc2: # do not write the 'r' tho
    for line in doc2.readlines():
        print(line)
    # readline() for individual lines, starting from first
    # read() for whole text
    # these are strings, can be stored in variable

with open('anotherdoc.txt', 'a') as doc2cont:
  doc2cont.write("... and you can continue!")


# a csv

"""
import csv

# newline is to avoid that a line break is confused with new row...

with open('cool_csv.csv', newline='') as cool_csv_file:
  cool_csv_dict = csv.DictReader(cool_csv_file, delimeter = ';') # if comma, not necessary

# each row will be a dictionary

  for dicc in cool_csv_dict:
    for key in dicc:
      print(key)

      OR

  for dicc in cool_csv_dict:
    print(dicc['Cool Fact'])
"""

big_list = [{'name': 'Fredrick Stein', 'userid': 6712359021, 'is_admin': False}, {'name': 'Wiltmore Denis, 'userid': 2525942, 'is_admin': False}, {'name': 'Greely Plonk', 'userid': 15890235, 'is_admin': False}, {'name': 'Dendris Stulo', 'userid': 572189563, 'is_admin': True}]

import csv

with open('output.csv', 'w') as output_csv:
  fields = ['name', 'userid', 'is_admin']
  output_writer = csv.DictWriter(output_csv, fieldnames=fields)

  output_writer.writeheader()
  for item in big_list:
    output_writer.writerow(item)
