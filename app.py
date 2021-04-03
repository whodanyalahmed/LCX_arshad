import time,requests,os,csv,datetime
import pandas as pd

url = 'https://exchange-api.lcx.com/order/book'
coins = ['LCX/ETH']
totalBuy= []
totalSell= []
totalDf = []
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
                    buy.insert(0,str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M')))
                    buy.insert(1,str(len(totalBuy)+1))
                    buy.insert(3," ")
            else:
                for sell in data[BoS]:
                    sell.insert(0,str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M')))
                    sell.insert(1,str(len(totalBuy)+1))
                    sell.insert(2," ")
        totalBuy.append(data['buy'])
        totalSell.append(data['sell'])
        buyDF = pd.DataFrame(data['buy'],columns=["Time","No.", "Buy","Sell","Quantity"])
        sellDF = pd.DataFrame(data['sell'],columns=["Time","No.", "Buy","Sell","Quantity"])
        tempCombined = pd.concat([buyDF, sellDF], axis=0)
        totalDf.append(tempCombined)
        combined = pd.concat(totalDf,axis=0)
        pd.set_option("display.max_rows", None, "display.max_columns", None)
        combined.set_index('Time', inplace=True)

        print(combined)

    # print(len(totalSell))
    if(len(totalSell)%5 == 0):
        csvConfirmation = input("Want to create csv? (y/n) : ")
        if(csvConfirmation.lower() == "y"):
            if os.path.isfile('file.csv'):
                print ("info : File already exist")
            else:
                print ("info : File not exist... will create new file")
                with open("file.csv","w+",newline='', encoding='utf-8') as f:
                    writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow(["Time","No.", "Buy","Sell","Quantity"])
            combined.to_csv('file.csv', mode='a', header=False)

            # for i in range(len(totalBuy)):
            #     with open('file.csv',"a+",newline='', encoding='utf-8') as f:
            #         writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            #         writer.writerow()


    time.sleep(3)