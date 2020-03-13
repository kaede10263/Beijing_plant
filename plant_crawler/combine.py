import pandas
import csv

old = pandas.read_csv("hello.csv",encoding = "utf-8")
new = pandas.read_csv("./taiwan_plant.csv",encoding = "utf-8")

old_list = []
att = []
chin = []
des = []
dist = []
sci = []

#for i in old.name:
for i in old.originalName:
    #print(i[1].name_code)
    old_list.append(i)


for i in new.name:
    #print(i)
    state = 0
    for j in old.iterrows():
        #print(j[1].originalName)
        #print("進行比對 %s , %s"%(i,j[1].originalName))
        if j[1].originalName == i:
            print("比對成功:",j[1].originalName)
            print("append : %s"%(j[1].originalName))
            print("--------------------------------")
            print("取得",j[1].attribute,j[1].chineseName,j[1].described,j[1].distribution,j[1].scientificName)
            print("--------------------------------")
            print(">>>>>> %s " %(i))
            print(j[1].attribute)
            att.append(j[1].attribute)
            print(j[1].chineseName)
            chin.append(j[1].chineseName)
            print(j[1].described)
            des.append(j[1].described)
            print(j[1].distribution)
            dist.append(j[1].distribution)
            print(j[1].scientificName)
            sci.append(j[1].scientificName)
            state = 1

    if state == 0:
        att.append("")
        chin.append("")
        des.append("")
        dist.append("")
        sci.append("")

new['attribute'] = att
new['chineseName'] = chin
new['described'] = des
new['distribution'] = dist
new['scientificName'] = sci

new.to_csv("result.csv", index = False, encoding = "utf_8_sig")