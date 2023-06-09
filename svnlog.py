import re
import sys,getopt
from datetime import datetime

def analyze(filePath:str,printLog:bool,zh:bool,valid:str):

    splitStr='\n版本: '
    rexAuth=r'作者: (.+?)\n'
    rexDate=r'日期: (.+?)\n'
    rexMessage=r'信息:\n(.*?)\n----'
    dateFomat="%Y年%m月%d日 %H:%M:%S"
    dateFormat2="%Y年%m月%d日"

    if zh is False:
        splitStr='\nRevision: '
        rexAuth=r'Author: (.+?)\n'
        rexDate=r'Date: (.+?)\n'
        rexMessage=r'Message:\n(.*?)\n----'
        dateFomat="%Y年%m月%d日 %H:%M:%S"
        dateFormat2="%Y年%m月%d日"

    file_path = filePath 

    with open(file_path, "r",encoding="utf8") as file:
        diary_entries = file.read()

    entries = diary_entries.split(splitStr)

    dayToUsers=dict[str,set[str]]()
    usernameToListData=dict[str,set[str]]()
    usernameToListLogs=dict[str,list[str]]()

    for entry in entries:
        if not re.search(valid,entry):
            continue

        username = re.search(rexAuth, entry, re.MULTILINE).group(1)
        date = re.search(rexDate, entry, re.MULTILINE).group(1)
        log = re.search(rexMessage, entry, re.S).group(1)
        day = datetime.strptime(date,dateFomat).isoweekday()
        dayStr = date.split(" ")[0] #2222年2月2日
        
        if(day in {6,7}):
            if dayToUsers.get(dayStr) is None:
                dayToUsers[dayStr] = set()
            dayToUsers[dayStr].add(username)
        
        if usernameToListData.get(username) is None:
            usernameToListData[username] = set[str]()
        usernameToListData[username].add(dayStr)

        if usernameToListLogs.get(username) is None:
            usernameToListLogs[username] = list()
        usernameToListLogs[username].append(log)

    keys = dayToUsers.keys()
    keys = sorted(keys,key=lambda x:datetime.strptime(x,dateFormat2), reverse=True)
    print("---------------------------------------")
    print("周末上班数据")
    for k in keys:
        print(k)
        for i in dayToUsers[k]:
            print("   ",i)
    print("---------------------------------------")
    print("人员数据")
    names = usernameToListData.keys()
    datas=dict()
    for name in names:
        days = sorted(usernameToListData[name],key=lambda x:datetime.strptime(x,dateFormat2))
        spanDays = (datetime.strptime(days[-1],dateFormat2)-datetime.strptime(days[0],dateFormat2)).days
        txt=name+" "+days[0]+" "+days[-1]+" "+str(spanDays)+"天"
        datas[name]=(txt,spanDays,name)
    
    datasKey=sorted(datas.keys(),key=lambda x:datas[x][1])
    for dataKey in datasKey:
        print()
        print("->",datas[dataKey][0])
        if printLog:
            for log in usernameToListLogs[datas[dataKey][2]]:
                if len(log.strip())>0:
                    print("   ",log)



if __name__ == "__main__":
    opts, args = getopt.getopt(sys.argv[1:],"i:v:h",["file=","valid=","help"])
    file=""
    valid=".*"
    # print(opts)
    for opt, arg in opts:
        if opt == '-h':
            print ('-i <inputfile>')
            print ('-v regex valid string')
            print ('enablelog: log')
            print ('lang: zh')
            print ('example: python svnlog.py -i log.txt -v "Modules/.*.cs" log zh')
            sys.exit()
        elif opt in ("-i","--file"):
            file = arg
        elif opt in ("-v","--valid"):
            valid = arg

    if len(file)==0:
        print("-i <inputfile>")
        sys.exit()

    printLog=False
    printLog= "log" in args
    zh = "zh" in args
    # print(valid)
    analyze(file,printLog,zh,valid)
