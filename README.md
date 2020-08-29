# Alpaca-Trading-Bot
Alpaca is a sillicon valley based brokerage that focuses on algorithmic trading through its simple, easy-to-use API. The code in Trady_RVOL.py is for a Trading bot for the NYSE using Alpaca API. Please scroll down for a quick tutorial. 
## Strategy Explanation
This stock market strategy is derived from a simple volume based strategy. For each stock, we collect the volume at a given time for the past n (n can be changed under the calc_screen() function) trading days and append it to a list. For example: if today is friday at 10AM, our stock is TSLA, and n=4, our list will comprise of TSLA's volume at 10am on the previous monday, teusday, wednesday, and thursday. If the current volume is in the top 25% of volume in that list, we buy. If current volume is in the bottom 25%, we sell. Else, we hold. This code will continually run locally until trading hours are over. Feel free to look at the code and make changes as you wish. Thank you, and good luck trading!

## Getting Started
For those  of you that are new to programming, I would start by checking these tutorials/courses : <br />
* [Getting Started With Alpaca](https://alpaca.markets/docs/get-started-with-alpaca/tutorial-videos/) -- Intro to algo trading with Alpaca<br />
* [Intro to Python Programming Full Course](https://www.edx.org/course/cs50s-introduction-to-computer-science) Intro to object oriented programming by Harvard<br />
* [30 Days of Code](https://www.hackerrank.com/domains/tutorials/30-days-of-code) 30 days of learning how to code by HackerRank <br />

#### Step 1: Download Trade_RVOL.py or make a pull request in git. 

#### Step 2: Make sure you have installed all required packages as shown below.
```python
import requests, json
import pandas as pd
import pytz
from datetime import *
import time
import calendar

 ```


#### Step 3: Open the file, and under __name__=='__main__', enter your alpaca api_key, secret key, and input all the stocks you want to trade.

```python

  if __name__ == "__main__":

    API_KEY='{API Key goes here}'
    Secret_Key='{Secret Key goes here}'
    stock_array=["AAPL","AMZN","GOOGL","TSLA","FB","BA", etc...]
    My_Strategy=Strategy(Secret_Key,API_KEY,stock_array)
    My_Strategy.run()
 ```
 #### Step 4: Open terminal and run Trade.py in the folder in which you downloaded it. 
 This is how it looks when I run it in powershell. <br />
    ```C#
    PS C:\Users\somer> cd OneDrive\Documents\Atom_Projects\Buy_Low_Sell_High
    PS C:\Users\somer\OneDrive\Documents\Atom_Projects\Buy_Low_Sell_High> python Trade_RVOL.py  
    ```  <br />
     ```
    Sold 46 shares of AAPL ``` <br />
    ```Sold 8 shares of AMZN  ```<br />
   ``` Hold GOOGL ``` <br />
    ```Hold TSLA ```<br />
    ```Sold 12 shares of FB ```<br />
    ```... ```
  #### Step 5: Check your Alpaca dashboard and review your gains!
  Note: This image displays paper trading gains i.e. not real money. Simply change the api key and secret key if you want to trade on your real account. 
  
  ![](https://github.com/jacobsomer/Alpaca-Trading-Bot/blob/master/Screenshot%20(6).png)
