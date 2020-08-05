from janome.tokenizer import Tokenizer
import pandas as pd
import jaconv as jc
import os, re, random
import make_csv


def make_dic(words):
    tmp = ["@"]
    dic = {}

    for i in words:
        w = i.surface
        if w == "" or w == "/r/n" or w == "\n":
            continue
        tmp.append(w)
        
        if  len(tmp) < 3:
            continue
        if len(tmp) > 3:
            tmp = tmp[1:]
        set_word3(dic, tmp)
        
        if w == "。":
            tmp = ["@"]
            continue

    return dic

def set_word3(dic, s3):
    w1, w2, w3 = s3
    if not w1 in dic:
        dic[w1] = {}
    if not w2 in dic[w1]:
        dic[w1][w2] = {}
    if not w3 in dic[w1][w2]:
        dic[w1][w2][w3] = 0
    dic[w1][w2][w3] += 1


def make_scentence(dic):
    ret = []
    if not "@" in dic:
        return "no dic"
    top = dic["@"]
    w1 = word_choice(top)
    w2 = word_choice(top[w1])
    ret.append(w1)
    ret.append(w2)

    while True:
        w3 = word_choice(dic[w1][w2])
        ret.append(w3)
        if w3 == "。":
            break
        w1, w2 = w2, w3

    return "".join(ret)


def word_choice(sel):
    keys = sel.keys()
    return random.choice(list(keys))

b = 0

while b == 0:
    talk_room = input("Who do you want to talk with? (exact LINE name) \n\n > ")
    fixed_tr = talk_room
    try:
        make_csv.mk_csv(talk_room)
    except:
        print("\n[Error] no txt data\n")
    if os.path.exists(talk_room + ".csv"):
        b = 1

print("""\n\n ---   type [LINE name] [grade or "al"]    or    [exit]   -----\n
中1の佐藤      =  佐藤j1
高2のsakura　　=  sakurah2
sakura         =  sakuraal
""")

a = 0
rframe = pd.read_csv("./" + talk_room + ".csv")
list_talk = []

for talk in rframe["talk"]:
    if bool(re.search(r"☎", talk)):
        talk = "☎"
    new_talk = talk.replace("[", "a")
    if talk != new_talk:
        talk = "NONE"
    list_talk.append(talk)
data = {"time" : rframe["time"], "grade" : rframe["grade"], "name" : rframe["name"], "talk" : list_talk}
frame = pd.DataFrame(data)
names = frame["name"].unique()
cancels = []
couple = []

for name in names:
    m = re.search(r"メッセージの送信を取り消しました$", name)
    if not m is None:
        cancels.append(name)
    else:
        couple.append(name)

for name in couple:
    if name != talk_room:
        my_name = name

not_talk = ["NONE", "☎"]
sentinels = {"name" : cancels, "talk" : not_talk}
os.remove("./" + talk_room + ".csv")
frame.to_csv("./" + talk_room + "2.csv")
frame = pd.read_csv("./" + talk_room + "2.csv", na_values = sentinels)
s = 0
n = 0

while True:
    while a == 0:
        info = input("> " + "")
        name = info[:-2]
        grade = info[-2:]
        if info == "exit":
            exit()
        elif len(info) <= 2:
            continue
        for nam in couple:
            if bool(re.search(nam, info)):
                n += 1
        if n == 0:
            print("name is incorrect")
            continue
        elif grade == "al":
            break
        elif grade[0] != "j" and grade[0] != "h" and grade[0] != "u":
            print("type correctly\n")
        elif bool(re.match(r"[0-9]", grade[1])) is False:
            print("last letter must be a number")
        else:
            n = 0
            break

    if grade == "al":
        df = frame[frame["name"] == name]
        t = Tokenizer()
        list_talk = []
        for talk in df["talk"].dropna():
           list_talk.append(talk)
        str_talk = "。".join(list_talk)
        str_talk.replace("None。", "")
        talk = t.tokenize(str_talk)
        dic = make_dic(talk)
        a = 0
    else:
        i = int(grade[1])
        if grade[0] == "h": i += 3
        if grade[0] == "u": i += 6
        end_day = i * 100 + 201404
        sta_day = end_day - 100
        df = frame[sta_day < frame["grade"]]
        df = df[df["grade"] < end_day]
        ndf = df[df["name"] == name]
        if len(ndf) == 0:
            print("out of range")
            continue
        t = Tokenizer()
        list_talk = []
        for talk in ndf["talk"].dropna():
           list_talk.append(talk)
        str_talk = "。".join(list_talk)
        str_talk.replace("None。", "")
        talk = t.tokenize(str_talk)
        dic = make_dic(talk)
        a = 0

    for i in range(1):
        try:
            rrtext = make_scentence(dic)
            rtext = jc.h2z(rrtext, digit = True, ascii = True)
        except:
            if s != 0:
                print("\t\t\t\t\t\t\t|\t\t\t\t\t\t\t      |")
            continue
        if len(rtext) >= 45:
            if s != 0:
                print("\t\t\t\t\t\t\t|\t\t\t\t\t\t\t      |")
            continue
        if s == 0:
            header = "\t\t\t\t\t\t\t\t\t--------   " + talk_room + "   --------\n\n\n"
            s = 1
        else: header = ""
        if name == talk_room:
            arrow = ">"
            tab = ""
            if 30 > len(rtext) > 15:
                space = []
                for i in range(len(talk_room)):
                    space.append("　")
                line_one, line_two = rtext[:15], rtext[15:]
                exspace = []
                exs = 25 - len(line_two)
                for i in range(exs):
                    exspace.append("  ")
                exspaces = "".join(exspace)
                text = line_one + "\t\t      |\n" + "\t\t\t\t\t\t\t|" + "".join(space) + "     " + line_two + exspaces + "|"
            elif len(rtext) >= 30:
                space = []
                for i in range(len(talk_room)):
                    space.append("　")
                line_one, line_two, line_three = rtext[:15], rtext[15:30], rtext[30:]
                exspace = []
                exs = 25 - len(line_three)
                for i in range(exs):
                    exspace.append("  ")
                exspaces = "".join(exspace)
                text = line_one + "\t\t      |\n" + "\t\t\t\t\t\t\t|" + "".join(space) + "     " + line_two+ "\t\t      |\n" + "\t\t\t\t\t\t\t|" + "".join(space) + "     " + line_three + exspaces + "|"
            else:
                exspace = []
                exs = 25 - len(rtext)
                for i in range(exs):
                    exspace.append("  ")
                exspaces = "".join(exspace)
                text = rtext + exspaces + "|"

        else:
            talk_room = ""
            tab = "\t\t    "
            arrow = ""
            if 30 >len(rtext) > 15:
                line_one, line_two = rtext[:15], rtext[15:]
                exspace = ["  "]
                exs = 15 - len(line_two)
                for i in range(exs):
                    exspace.append("  ")
                exspaces = "".join(exspace)
                text = "          " + line_one + " |\n\t\t\t\t\t\t\t|\t\t               " + line_two + exspaces + " |"
            elif len(rtext) >= 30:
                line_one, line_two, line_three = rtext[:15], rtext[15:30], rtext[30:]
                exspace = ["  "]
                exs = 15 - len(line_three)
                for i in range(exs):
                    exspace.append("  ")
                exspaces = "".join(exspace)
                text = "          " + line_one + " |\n\t\t\t\t\t\t\t|\t\t\t       " + line_two + " |\n\t\t\t\t\t\t\t|\t\t\t       " + line_three + exspaces + " |"
            else:
                ext = 15 - len(rtext)
                extab = ["            "]
                for i in range(ext):
                    extab.append("  ")
                tab += "".join(extab)
                text = rtext + " |"

        print(header, "\t\t\t\t\t\t\t|", talk_room, arrow, tab, text.replace("。", "") + "\n\t\t\t\t\t\t\t|" + "\t\t\t\t\t\t\t      |")
        talk_room = fixed_tr