import requests, json
import pandas as pd
import pytz
from datetime import *
import time
import calendar


class Strategy():

    def __init__(self,Secret_Key,API_KEY,stocks_array):
        self.url='https://data.alpaca.markets'
        self.paper_url='https://paper-api.alpaca.markets'
        self.HEADERS={'APCA-API-KEY-ID': API_KEY,'APCA-API-SECRET-KEY': Secret_Key}
        self.stocks=stocks_array
        self.trading_hours=None

    def RVOL_Strategy(self,symbol):
        unixday=24*60*60
        d = datetime.utcnow()
        unixtime = calendar.timegm(d.utctimetuple())
        list=[]
        for i in range(0,7):   #change value of n as described in tutorial by changing 7. Be carefull,  Alpaca only allows 200 API calls per minute. 
            tz = pytz.timezone('America/New_York')
            time2=datetime.fromtimestamp(unixtime-60*10, tz).isoformat()
            time3=datetime.fromtimestamp(unixtime+60*10, tz).isoformat()
            minute_bars_url= "https://data.alpaca.markets/v1/bars" + '/1Min?symbols={}&limit=1'.format(symbol)+'&start={}'.format(time2)+'&end={}'.format(time3)
            data= requests.get(minute_bars_url,headers=self.HEADERS)
            dictionairy=json.loads(data.content)
            try:
                list.append(int(dictionairy[symbol][0]['v']))
            except IndexError:
                pass
            unixtime=unixtime-unixday
        try:
            today=list[0]
        except IndexError:
            return "Error in gathering Data for RVOL strategy. Check time constraints."
        list=sorted(list)
        if list[int(len(list)*.75)]<=today:
            return "Buy"
        elif list[int(len(list)*.25)]>=today:
            return "Sell"
        else:
            return "Hold"


    def get_trading_hours(self):
        d = datetime.now()
        if d.isoweekday() in range(1,6):
            if d.hour in range(9, 16):
                self.trading_hours= True

        else:
            self.trading_hours= False

    def run(self):

        self.get_trading_hours()
        if self.trading_hours==False:
            return print("Error: Cannot Trade. Reason: Outside 9-4pm est trading window")
        while self.trading_hours:
            for i in self.stocks:
                decision=self.RVOL_Strategy(i)
                if decision=="Buy":
                    self.buy_fifth(i)
                elif decision=="Sell":
                    self.sell_half(i)
                else:
                    print("Hold "+i)
            self.get_trading_hours()
            time.sleep(30)   # Alpaca only allows 200 request per minute so we must wait a little before we make more API calls. 

    def create_order(self, symbol, qty, side, type='market', time_in_force='gtc'):
        data={
            "symbol":symbol,
            "qty":qty,
            "side":side,
            "type":type,
            "time_in_force":time_in_force
        }
        ORDERS_URL="{}/v2/orders".format(self.paper_url)
        r=requests.post(ORDERS_URL, json=data,headers=self.HEADERS)
        return json.loads(r.content)

    def buy_fifth(self,symbol):
        def get_data(symbol):
            d = datetime.utcnow()
            unixtime = calendar.timegm(d.utctimetuple())
            tz = pytz.timezone('America/New_York')
            time2=datetime.fromtimestamp(unixtime-60*10, tz).isoformat()
            time3=datetime.fromtimestamp(unixtime+60*10, tz).isoformat()
            minute_bars_url= "https://data.alpaca.markets/v1/bars" + '/1Min?symbols={}&limit=1'.format(symbol)+'&start={}'.format(time2)+'&end={}'.format(time3)
            data= requests.get(minute_bars_url,headers=self.HEADERS)
            dictionairy=json.loads(data.content)
            try:
                return dictionairy[symbol][0]['o']
            except KeyError:
                return None
            except IndexError:
                return None
        def get_remaining_balance():
            remaining_balance=requests.get(self.paper_url+'/v2/account',headers=self.HEADERS)
            balance_dict=json.loads(remaining_balance.content)
            buying_power= float(balance_dict["daytrading_buying_power"])
            return buying_power

        buying_power=get_remaining_balance()
        fifth_cash=buying_power//5
        price=get_data(symbol)
        shares, market_value, current_price = self.get_position(symbol)
        if shares==None:
            message=self.get_position(symbol,existence=False)
            if message is not None:
                shares=0
            else:
                return print("Error in get_position")
        shares=int(shares)
        if shares==0:
            if price is not None:
                current_price=int(price)
                executed_shares=int(fifth_cash//current_price)
                self.create_order(symbol, executed_shares, "buy")
                print("Bought " + str(executed_shares) + " shares of " + str(symbol) + " stock.")
            elif price is None:
                print("Error in get_data")
        elif shares>0:
            current_price=int(float(current_price))
            executed_shares=int(fifth_cash//current_price)
            self.create_order(symbol, executed_shares, "buy")
            print("Bought " + str(executed_shares) + " shares of " + str(symbol) + " stock")
        else:
            print("not enough cash on hand to execute trade")



    def sell_half(self,symbol):
        shares, market_value, current_price = self.get_position(symbol)
        if shares==None:
            message=self.get_position(symbol,existence=False)
            if message != None:
                return print("No shares of " + symbol + " to sell")
            else:
                return print("Error in get_positions")
        shares=int(shares)
        amount_sold=int(shares//2)
        self.create_order(symbol,amount_sold,"sell")
        print("Sold "+ str(amount_sold) + " shares of " + symbol)


    def get_position(self,symbol,existence=True):
        positions_url=self.paper_url+"/v2/positions/{}".format(symbol)
        request=requests.get(positions_url,headers=self.HEADERS)
        info=json.loads(request.content)
        if existence==False:
            try:
                return info["message"]
            except KeyError:
                return None
        try:
            shares=info['qty']
            market_value=info['market_value']
            current_price=info["current_price"]
        except KeyError:
            shares=None
            market_value=None
            current_price=None
        return shares, market_value,current_price



if __name__ == "__main__":

    API_KEY='{API Key goes Here}'
    Secret_Key='{Secret Key goes Here}'
    stock_array= [] # Example: ['AAPL', 'NVDA', 'AMZN',  'TSLA', 'NVAX', 'MRNA', 'FB',  'DKS', 'AAL', 'W', 'CHWY', 'PLAY', 'SAVE', 'CAKE', 'ANF', 'SHAK', 'AAPN', 'DKS', 'BIG', 'GOOGL', 'CCL', 'FSLY', 'WKHS', 'OSTK', 'TUP', 'ZM', 'FTCH', 'BJ', 'FSLR']
    My_Strategy=Strategy(Secret_Key,API_KEY,stock_array)
    My_Strategy.run()
