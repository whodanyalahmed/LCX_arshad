import time,requests,os,csv,datetime
import pandas as pd

url = 'https://exchange-api.lcx.com/order/book'
coins = ['LCX/ETH']
totalBuy= []
totalSell= []
while True:
    for i in coins:
        print(i)
        myobj = {'pair': i}
        print(myobj)
        x = requests.post(url,json=myobj).json()

        data = x['data']
        l = ['buy','sell']
        for BoS in l:
            if(BoS == 'buy'):
                for buy in data[BoS]:
                    buy.insert(0,str(datetime.datetime.now()))
                    buy.insert(2," ")
            else:
                for sell in data[BoS]:
                    sell.insert(0,str(datetime.datetime.now()))
                    sell.insert(1," ")
        totalBuy.append(data['buy'])
        totalSell.append(data['sell'])
        buyDF = pd.DataFrame(data['buy'],columns=["Time", "Buy","Sell","Quantity"])
        sellDF = pd.DataFrame(data['sell'],columns=["Time", "Buy","Sell","Quantity"])
        combined = pd.concat([buyDF, sellDF], axis=0)
        print(combined)

    if(len(totalSell)%5 == 0):
        csvConfirmation = input("Want to create csv? (y/n) : ")
        if(csvConfirmation.lower() == "y"):
            if os.path.isfile('file.csv'):
                print ("info : File already exist")
            else:
                print ("info : File not exist... will create new file")
                with open("file.csv","w+",newline='', encoding='utf-8') as f:
                    writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow(['Time',"Buy","Sell","Quantity"])
                
            # for i in range(len(totalBuy)):
            #     with open('file.csv',"a+",newline='', encoding='utf-8') as f:
            #         writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            #         writer.writerow()

    print(len(totalSell))

    time.sleep(3)