import pandas as pd
import os, re


def mk_csv(pathname):
    if os.path.exists(pathname + ".csv"):
        if __name__ == "__main__":
            print("\n[ " + pathname + ".csv ] has been existed")
        return
    fname = pathname + ".txt"
    rmemo = open(fname, "rb").read()
    memo = rmemo.decode("utf-8").split("\r\n")[3:]
    memo = "\r\n".join(memo)
    time = []; grade = []; name = []; talk = []

    for day_talk in memo.split("\r\n\r\n"):
        lines = day_talk.split("\r\n")
        day = lines[0]

        for line in lines[1:]:
            item = line.split("\t")
            tim = day + item[0]
            time.append(tim)
            try:
                name.append(item[1])
            except:
                name.append("NONE")
            try:
                check_box = item[2]
            except:
                check_box = "NONE"
            if bool(re.search(r"http", check_box)):
                check_box = "NONE"
            if bool(re.match(r"w", check_box)):
                check_box = "NONE"
            gr = day.replace("/", "")[:6]
            grade.append(gr)
            talk.append(check_box)

    data = {"time": time, "grade" : grade, "name" : name, "talk" : talk}

    frame = pd.DataFrame(data, columns = ["time", "grade", "name", "talk"])
    savename = pathname + ".csv"
    frame.to_csv("./" + savename)
    return(print("\n[" + savename + "]", "was made successfully\n"))


if __name__ == "__main__":
    a = 0
    while a == 0:
        name = input("type [LINE name]\n > ")
        try:
            mk_csv(name)
            a = 1
        except:
            print("\n[Error] no txt data\n")