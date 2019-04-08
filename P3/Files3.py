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
