
#作成したログファイルからデータを取得
f =  open('monitoringlog.txt', 'r')
datalist = f.readlines()
f.close()


#サーバー数と初期設定
M=len(datalist)-1
date = [0]*M
server = [0]*M
pingtime = [0]*M


#データを確認日時、サーバーアドレス、応答結果に分割
for i in range(M):
    splitdata = datalist[i].split(',')
    date[i] = splitdata[0]
    server[i] = splitdata[1]
    pingtime[i] = splitdata[2].rstrip('\n')

    
#サーバー毎にデータをまとめる
serverlist = list(dict.fromkeys(server))
dates = [[] for i in range(len(serverlist))]
pingtimes = [[] for i in range(len(serverlist))]

#サーバー数
server_count = len(serverlist)

for i in range (len(serverlist)):
    for j in range(M):
        if server[j] == serverlist[i]:
            dates[i].append(date[j])
            pingtimes[i].append(pingtime[j])

#サーバー毎へのping回数
ping_count = len(pingtimes[0])


#サーバー毎に情報表示
for i in range(server_count):
    print(str(server[i]) + ":" + str(pingtimes[i]))
    print("-------------------------------------------------")


#タイムアウト連続回数
N=3

#故障判定
for i in range(server_count):
    for j in range(ping_count):
        if pingtimes[i][j] == '-' and pingtimes[i][j-1] != '-' or pingtimes[i][j] == '-' and j == 0:
            if j == len(pingtimes[i])-1:
                print("サーバーアドレス:" + serverlist[i])
                print("故障期間:" + dates[i][j] + "--  :" + '故障の可能性有り' )
                print("-------------------------------------------------")
            else:
                s=1
                while True:
                    if pingtimes[i][j+s] == '-' and j+s == len(pingtimes[i])-1:
                        print("サーバーアドレス:" + serverlist[i])
                        print("故障期間:" + dates[i][j] + "--  :" + "故障の可能性有り")
                        print("-------------------------------------------------")
                        break
                    elif pingtimes[i][j+s] != '-' and s < N:
                        break
                    elif pingtimes[i][j+s] != '-' and s >= N:
                        print("サーバーアドレス:" + serverlist[i])
                        print("故障期間:" + dates[i][j] + "--" + dates[i][j+s])
                        print("-------------------------------------------------")
                        break
                    else:
                        s += 1


#直近回数と過負荷判定時間                        
m=4
t=100

#タイムアウト情報の削除
organize_dates = [[] for i in range(len(serverlist))]
organize_pingtimes = [[] for i in range(len(serverlist))]

for i in range (server_count):
    for j in range(M):
        if server[j] == serverlist[i] and pingtime[j] != '-':
            organize_dates[i].append(date[j])
            organize_pingtimes[i].append(int(pingtime[j]))


#過負荷判定
for i in range(server_count):
    if len(organize_dates[i]) <= m:
        average_time = sum(organize_pingtimes[i]) / len(organize_pingtimes)
        if average_time > t:
            print("過負荷サーバ:" +serverlist[i])
            print("過負荷期間:" + organize_dates[i][0] + "-" + organize_dates[i][-1])
            print("-------------------------------------------------")
    else:
        for j in range(len(organize_pingtimes[i])-m+1):
            average_time = sum(organize_pingtimes[i][j:j+m])/m
            if average_time > t:
                print("過負荷サーバ:" +serverlist[i])
                print("過負荷期間:" + organize_dates[i][j] + "-" + organize_dates[i][j+m-1])
                print("-------------------------------------------------")


