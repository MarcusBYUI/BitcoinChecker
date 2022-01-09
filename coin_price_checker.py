"""

    Significant Program Proposal(Total hours: 16hrs)

(This is a proposal. All proposals are written with our best knowledge
at the beginning of a project. As we progress from the beginning to the
end of a project, we gain more knowledge, and some of the ideas we
proposed change. This is part of completing any project and is fine.
However, we still must write a proposal so that our teachers or
supervisors know what we intend to do. Please answer each of the
following questions to the best of your knowledge.)

1. What is the title of your program?
    Coin Tracker

2. What real world problem will your program address or help to solve?
I would create a program using the kivy module for the GUI and what this program does is to get a coin name from the user, then queries
an API from (coingecko.com) then prints our the current price of the coin, market cap and other informations. This helps solves problem of having to
visit the new to find coin prices and data

3. What will you learn from developing this program?
    I will have to learn to use the kivy module, how to request from a server and process that request and more

4. What Python modules will your program use? (Some examples are: csv,
datetime, functools, matplotlib, math, pandas, pytest, random, requests,
and tkinter.)
    Kivy, requests

5. Will you separate your Python program into functions that each
perform a single task?
    Yes

6. Will you write test functions to test many of your program functions?
    Yes
"""

#impoert needed dependencies
from pycoingecko import CoinGeckoAPI
from requests.sessions import TooManyRedirects
from typing import Text
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty




#the layout class
class FloatLayout(FloatLayout):
    input_name = ObjectProperty()
    coin_name = StringProperty()
    coin_price = StringProperty()
    coin_mcap = StringProperty()
    coin_advice = StringProperty()
    coin_warning = StringProperty() 
    check_state = StringProperty("Check Coin") 

    #funtion to change the button text when clicked
    def change_label(self):
        self.check_state = "Fetching Coin"
        
    #Function that makes a fetch to the coingecko api the name received from the user as an argument 
    #then returns the coin if found or an exception happens which is caught
    def check_coin(self):
        name = self.input_name.text
        
        #personal investment advise based on teh market cap of the token investigated
        advice = "High Market Cap, This Means Longterm Investment"

        #To clear the display grid of previous output on each click
        self.coin_name = ""
        self.coin_price = ""
        self.coin_mcap = ""
        self.coin_advice = ""
        self.coin_warning = ""

        try:
            cg = CoinGeckoAPI()
            name = name.lower()
            cg_response = cg.get_price(ids=name, vs_currencies='usd', include_market_cap='true')

            value = cg_response[name]

            price = value["usd"]
            market_cap = value["usd_market_cap"]
            if market_cap <= 1000000 and market_cap > 5000:
                advice = "Moderate Market Cap, This Means A Good Buy"
            elif market_cap < 5000:
                advice ="Market Cap Is Too Low To Invest"

            #passing the values to the front end
            self.coin_name = f"Name: {name.upper()}"
            self.coin_price = f"Price: ${price:.2f}"
            self.coin_mcap = f"Market Cap: ${market_cap:.2f}"
            self.coin_advice = f"Our Advice: {advice}"


        except KeyError:
            print(f"The coin: '{name.upper()}' cannot be found")
            self.coin_warning = f"The coin: '{name.upper()}' cannot be found"
        except (ConnectionError, TimeoutError, TooManyRedirects) as e:
            print(e)

        #returns the textbox to a blank state
        self.input_name.text = ""
        self.check_state = "Check Coin"
        

            
class CryptoCoinTrackerApp(App):
    
    def build(self):
        return FloatLayout()



if __name__ == "__main__":
    CryptoCoinTrackerApp().run()

