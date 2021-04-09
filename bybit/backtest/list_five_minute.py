import bybit
import time
import csv

# 실 서버
#client = bybit.bybit(test=False, api_key="p3KDyF3Iw4FpFNk8WH", api_secret="5fmrUMCPXvrD5XEpfj88fINvYdE5aAz7ENoy")
#TEST 서버
client = bybit.bybit(test=True, api_key="XhDNloMOlbRWSarTu1", api_secret="q3VFEFNUTGLbCXfPm50mIZUVBi86CfI47Iy8")
# Get server time
#print("서버시간")
time_now = int(round(float(client.Common.Common_getTime().result()[0]['time_now'])))

# init
list_goal = [['시간', '거래량', '시가', '고가', '저가', '종가']]
while True:
    time_now = time_now-60000
    list = client.Kline.Kline_get(symbol="BTCUSD", interval="5", **{'from':time_now}).result()

    for i in reversed(range(len(list[0]['result']))):
        open_time = list[0]['result'][i]['open_time']
        opens = list[0]['result'][i]['open']
        highs = list[0]['result'][i]['high']
        lows = list[0]['result'][i]['low']
        closes = list[0]['result'][i]['close']
        volumes = list[0]['result'][i]['volume']

        # timestamp 0일 때 1970년 1월 1일 9:00 AM
        timestamp = 197001010900
        # timesamp 시간 정의
        year = open_time//31536000
        month = (open_time-(31536000*year))//2628000
        # 뭔가 이상하게 안맞아서 보정(UTC 시간으로 - 한국시간이랑 다름)
        day = (open_time-(31536000*year)-(2628000*month))//86400 - 12
        hour = (open_time-(31536000*year)-(2628000*month)-(86400*(day+12)))//3600 - 3
        minute = (open_time-(31536000*year)-(2628000*month)-(86400*(day+12))-(3600*(hour+3)))//60
        #print(year, month, day, hour, minute)
        real_time = timestamp + (year*100000000) + (month*1000000) + (day*10000) + (hour*100) + minute
        #print(real_time)
        # csv 기록하기
        f = open('list_five_minute.csv', 'a', newline='')
        wr = csv.writer(f)
        # csv 기록하기
        wr.writerow([real_time, volumes, opens, highs, lows, closes])
        #print(open_time)

    # 2018년 11월 14일 - bybit 비트코인 시작일
    if open_time < 1542186000:
        break
