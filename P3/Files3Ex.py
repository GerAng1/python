import csv
import json

compromised_users = []

with open('passwords.csv', newline = '') as pws_file:
  pws_csv = csv.DictReader(pws_file)

  for row in pws_csv:
    compromised_users.append(row['Username'])

with open('compromised_users.txt', 'w') as comp_usrs_txt:
  for line in compromised_users:
    comp_usrs_txt.write(line)
    comp_usrs_txt.write('\n')

with open('boss_message.json', 'w') as boss_message_json:
  boss_message_dict = {'recipient': 'The Boss', 'message': 'Mission Success'}
  json.dump(boss_message_dict, boss_message_json)

with open('new_passwords.csv', 'w') as new_pws_file:
  slash_null_sig = """
 _  _     ___   __  ____
/ )( \   / __) /  \(_  _)
) \/ (  ( (_ \(  O ) )(
\____/   \___/ \__/ (__)
 _  _   __    ___  __ _  ____  ____
/ )( \ / _\  / __)(  / )(  __)(    \
) __ (/    \( (__  )  (  ) _)  ) D (
\_)(_/\_/\_/ \___)(__\_)(____)(____/
        ____  __     __   ____  _  _
 ___   / ___)(  )   / _\ / ___)/ )( \
(___)  \___ \/ (_/\/    \\___ \) __ (
       (____/\____/\_/\_/(____/\_)(_/
 __ _  _  _  __    __
(  ( \/ )( \(  )  (  )
/    /) \/ (/ (_/\/ (_/\
\_)__)\____/\____/\____/"""

  new_pws_file.write(slash_null_sig)

  
