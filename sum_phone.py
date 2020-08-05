import pandas as pd
import os, re
import make_csv


name = input("LINE name > ")
fname = name + ".csv"
if not os.path.exists(fname):
    try:
        make_csv.mk_csv(name)
    except:
        print("[Error] no txt data")
        exit()

frame = pd.read_csv(fname)
phone_list = []
sum_hours = 0
sum_mins = 0
sum_secs = 0

for talk in frame["talk"]:
    if bool(re.search(r"☎", talk)):
        time = re.findall(r"[0-9]", talk)
        item = len(time)
        if item == 5:
            hour = time[0]
            min = time[1:3]
            sec = time[3:]
            hour = int("".join(hour))
            min = int("".join(min))
            sec = int("".join(sec))
        elif item == 4:
            hour = 0
            min = time[1:3]
            sec = time[3:]
            min = int("".join(min))
            sec = int("".join(sec))
        elif item == 3:
            hour = 0
            min = time[0]
            sec = time[1:]
            min = int("".join(min))
            sec = int("".join(sec))
        elif item <= 2 and item == 1:
            hour = 0
            min = 0
            sec = int("".join(time))
        else:
            continue

        hours = hour + min / 60 + sec / 3600
        mins = hour * 60 + min + sec / 60
        secs = hour * 3600 + min * 60 + sec
        sum_hours += hours
        sum_mins += mins
        sum_secs += secs

print("\nYou have wasted..\n")
print("\t" + str(sum_hours) + "  hours")
print("\t" + str(sum_mins) + "  minites")
print("\t" + str(sum_secs) + "  seconds")
print("\n\t\t\t\ton phone!!")
input()