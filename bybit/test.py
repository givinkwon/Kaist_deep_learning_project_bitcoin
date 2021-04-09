import bybit
import time

# 실 서버
#client = bybit.bybit(test=False, api_key="p3KDyF3Iw4FpFNk8WH", api_secret="5fmrUMCPXvrD5XEpfj88fINvYdE5aAz7ENoy")
#TEST 서버
client = bybit.bybit(test=True, api_key="XhDNloMOlbRWSarTu1", api_secret="q3VFEFNUTGLbCXfPm50mIZUVBi86CfI47Iy8")
time_now = 60
while True:
    # SymbolInfo - Symbol에 따른 정보 가져오기
    info = client.Market.Market_symbolInfo().result()

    # btc 가격 가지고 오기
    keys = info[0]['result']
    btc = keys[0]['last_price']

    # 지갑에 비트코인 가지고오기
    wallet = client.Wallet.Wallet_getBalance(coin="BTC").result()
    btc_balance = wallet[0]['result']['BTC']['available_balance']

    # 전체 잔고 계산하기
    total_price = float(btc_balance) * float(btc)
    #print(total_price)

    # Get server time
    #print("서버시간")
    time_now = int(round(float(client.Common.Common_getTime().result()[0]['time_now'])))
    #print(time_now)
    #print(time_now-12000)
    # 레버리지 설정
    client.Positions.Positions_saveLeverage(symbol="BTCUSD", leverage="10").result()

    # 분봉마다 데이터 불러오기
    if round(time_now) % 60 == 0:
        # 확실하게 가지고오기 위함
        time.sleep(2)
        # 비트코인 현재 시고저종과 거래량 가져오기, 200개 밖에 안됌 - 최근 시간부터 200봉
        list = client.Kline.Kline_get(symbol="BTCUSD", interval="1", **{'from':time_now-12000}).result()
        #print(list)
        data_list = list[0]['result']
        #print(data_list)
        #init
        open_list = []
        high_list = []
        low_list = []
        close_list = []
        volume_list = []

        for i in data_list:
            open_list.append(i['open'])
            high_list.append(i['high'])
            low_list.append(i['low'])
            close_list.append(i['close'])
            volume_list.append(i['volume'])


        # M / K로 표시되는 분기점에서 더 큰 변수로 인식하기 위해서는 tuple of list >> int of list화가 필요함
        open_list = [int(round(float(i))) for i in open_list]
        high_list = [int(round(float(i))) for i in high_list]
        low_list = [int(round(float(i))) for i in low_list]
        close_list = [int(round(float(i))) for i in close_list]
        volume_list = [int(round(float(i))) for i in volume_list]


        #print(volume_list)
        # 가장 최근 분봉의 거래량 제거
        #print(volume_list[:-1])
        # 가장 최근 분봉의 거래량
        #print(volume_list[-1])

        # 뒤에서 세번째, 두번재, 첫번째(최근) 종가
        #print(close_list[-3], close_list[-2], close_list[-1])



        # 가장 최근 분봉의 거래량이 120분봉 최고 거래량 깬 경우
        print(volume_list[:-1], max(volume_list[-10:-1]), volume_list[-1], close_list[-9], close_list[-1])
        if max(volume_list[:-1]) < volume_list[-1]:
            print(0)
            #가장 최근 10봉 전 대비 가격이 1% 이상 하락
            if float(close_list[-10]) * 0.99 > float(close_list[-1]):
                print(1)
                print(client.Order.Order_new(side="Buy", symbol="BTCUSD", order_type="Limit", qty=total_price, price=int(float(btc)*1.01), take_profit=int(float(btc)*1.01), stop_loss=int(float(btc)*0.99), time_in_force="GoodTillCancel").result())

            # 가장 최근 10봉 전 대비 가격이 1% 이상 상승
            elif float(close_list[-10]) * 1.01 < float(close_list[-1]):
                print(2)
                print(client.Order.Order_new(side="Sell", symbol="BTCUSD", order_type="Limit", qty=total_price, price=int(float(btc)*1.01), take_profit=int(float(btc)*1.01), stop_loss=int(float(btc)*0.99), time_in_force="GoodTillCancel").result())

        #print(volume_list[-20], volume_list[-19], volume_list[-18], volume_list[-17], volume_list[-16])
        # 가장 최근 분봉의 거래량이 10분봉 최고 거래량 깬 경우
        #print(volume_list[-10:-1],max(volume_list[-10:-1]), volume_list[-1], close_list[-9], close_list[-1])
        #if max(volume_list[-10:-1]) < volume_list[-1]:
        #    print(0)
        #    #가장 최근 10봉 전 대비 가격이 0.2% 이상 하락
        #    if float(close_list[-9]) * 0.998 > float(close_list[-1]):
        #        print(1)
        #        print(client.Order.Order_new(side="Buy", symbol="BTCUSD", order_type="Market", qty=total_price, take_profit=float(btc) * 1.01, stop_loss=float(btc)*0.99, time_in_force="GoodTillCancel").result())

        #    # 가장 최근 10봉 전 대비 가격이 0.2% 이상 상승
        #    elif float(close_list[-9]) * 1.002 < float(close_list[-1]):
        #        print(2)

# 각 Symbol별로 데이터 추출하기 - ret_code | ret_msg 등의 Json 신호를 받아오는 내용과 Result가 있음
#keys = info[0]['result']
#for i in keys:
#    print(i)

# 비트코인만 추출하기
#keys = info[0]['result']
#btc = keys[0]
#for i in btc:
#    print(i)


# 비트코인 현재 가격 받아오기
#keys = info[0]['result']
#btc = keys[0]['last_price']
#print(btc)
