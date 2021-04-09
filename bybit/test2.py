import bybit
import time

#TEST 서버
client = bybit.bybit(test=True, api_key="XhDNloMOlbRWSarTu1", api_secret="q3VFEFNUTGLbCXfPm50mIZUVBi86CfI47Iy8")

info = client.Market.Market_symbolInfo().result()

keys = info[0]['result']
btc = keys[0]['last_price']

wallet = client.Wallet.Wallet_getBalance(coin="BTC").result()
btc_balance = wallet[0]['result']['BTC']['available_balance']
total_price = float(btc_balance)*float(btc)
print(total_price)
# 구매하기 시장가
#print(client.Order.Order_new(side="Buy", symbol="BTCUSD", order_type="Market", qty=total_price, take_profit=float(btc)*1.01,stop_loss=float(btc)*0.99, time_in_force="GoodTillCancel").result())

# 구매하기 지정가
print(client.Order.Order_new(side="Buy", symbol="BTCUSD", order_type="Limit", qty=total_price, price=int(float(btc)*1.01), take_profit=int(float(btc)*1.01), stop_loss=int(float(btc)*0.99), time_in_force="GoodTillCancel").result())