"""Basic calendar that the user will be able to interact with. View calendar, add event calendar, update existing event, delete existing event"""

from time import sleep, strftime
USER = "Gerry Anglada"
calendar = {}

def welcome():
  print "Welcome " + USER + "."
  print "Loading calendar..."
  sleep(1)
  print "Today is: " + strftime("%A, %b %d, %Y") 
  print "Current time: " + strftime("%H:%M:%S")
  sleep(1)
  print "What would you like to do?"

def start_calendar():
  welcome()
  start = True
  
  while start:
    user_choice = raw_input("Select:\n A to Add\n U to Update\n V to View\n D to Delete\n X to Exit\n\n  Option: ")
    user_choice = user_choice.upper()
    
    if user_choice == "V":
      if len(calendar.keys()) < 1:
        print "Calendar is empty!"
      else:
        print calendar
    elif user_choice == "U":
      date = raw_input("What date? ")
      update = raw_input("Enter the update: ")
      calendar[date] = update
      print "Update successfull"
      print calendar
    elif user_choice == "A":
      event = raw_input("Enter event: ")
      date = raw_input("Enter date [MM/DD/YYYY]:  ")
      if len(date) > 10 or int(date[6:]) < int(strftime("%Y")):
        try_again = raw_input("Invalid date. Try Again? [Y/N]: ")
        try_again = try_again.upper()
        if try_again == "Y":
          continue
        elif try_again == "N":
          start = False
      else:
        calendar[date] = event
        print "Event added!"
        print calendar
    elif user_choice == "D":
      if len(calendar.keys()) < 1:
        print "Calendar is already empty!"
      else:
        event = raw_input("What event? ")
        for keys_dates in calendar.keys():
          if event == calendar[keys_dates]:
            del calendar[keys_dates]
            print "Event deleted."
            print calendar
          else:
            "That date isn't registered"
    elif user_choice == "X":
      start = False
    else:
      "Option does not exist, exiting..."
      sleep(1)
      start = False
      
start_calendar()