from datetime import datetime, timedelta

plazo = 90



test1 = "25/Nov/2021, 19:52:04"
test2 = "28/Aug/2021, 19:52:04"
test3 = "1/Jan/2022, 09:02:14"
test4 = "1/Jan/2021, 09:02:14"


test1_str = datetime.strptime(test1, "%d/%b/%Y, %H:%M:%S")
test2_str = datetime.strptime(test2, "%d/%b/%Y, %H:%M:%S")
test3_str = datetime.strptime(test3, "%d/%b/%Y, %H:%M:%S")
test4_str = datetime.strptime(test4, "%d/%b/%Y, %H:%M:%S")



print((test1_str - test3_str).days)
input("Pausa")




hoy = datetime.now()

fin_plazo = (hoy + timedelta(days = plazo)).strftime("%d/%b/%Y")
print(fin_plazo)
print()
print()





print(test1_str-hoy)
print(test2_str-test3_str)
print(test3_str-test4_str)
print((hoy-test1_str).days)

if (test1_str - test2_str).days > 3:
    print("worked1")

if (test2_str-test3_str).days > 3:
    print("worked2")

if (test3_str-test4_str).days > 3:
    print("worked3")

if (test4_str-test1_str).days > 3:
    print("worked4 abs((d2 - d1).days)")
