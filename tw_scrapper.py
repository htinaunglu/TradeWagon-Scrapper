import requests
import json
from dataclasses import dataclass,field,asdict
import argparse

@dataclass
class Trading:
    name: str
    margin: float
    ent_price: float
    profit: float
    leverage: int
    side: str
    percent: float = field(init=False, repr=False)
    def __post_init__(self):
        self.percent = (self.profit/self.margin)*100

def scrap(tid):
    url = f"https://www.traderwagon.com/v1/public/social-trading/lead-portfolio/get-position-info/{tid}"
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    return json.loads(response.text)['data']

def get_data(data,jam):
    return Trading(
        name=data[jam]['symbol'], 
        margin=float(data[jam]['initialMargin']), 
        ent_price=float(data[jam]['entryPrice']), 
        profit=float(data[jam]['unrealizedProfit']), 
        leverage=int(data[jam]['leverage']), 
        side=data[jam]['positionSide'])

def get_batch_data(data):
    trade_list = []
    for i in range(len(data)):
        trade_info = get_data(data,i)
        trade_list.append(trade_info)
    return trade_list

def point_out_trade(trade_list):
    number_of_potential_trades = 0
    for something in trade_list:
        if something.profit < 0:
            number_of_potential_trades += 1
            print("*"*20)
            print(f"The trading pair {something.name} is now losing by {something.profit}, which is {something.percent:.3f}% in {something.side} position, the entry price was {something.ent_price}")
    print(f"\nThe total number of potential trades: {number_of_potential_trades}")
def main(args):
    tid = args.id
    data = scrap(tid)
    trade_list = get_batch_data(data)
    point_out_trade(trade_list)

    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--id", type = int, default = 3838, metavar = "portfolio id", help = "id of the portfolio"
    )
    args, _ = parser.parse_known_args()
    main(args)