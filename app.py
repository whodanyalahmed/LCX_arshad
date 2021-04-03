import time,requests,os,csv,datetime
import pandas as pd

url = 'https://exchange-api.lcx.com/order/book'
coins = {1:'LCX/ETH',2:'LCX/USDC'}
totalBuy= []
totalSell= []
totalDf = []
timeInterval = input("Enter time interval(in seconds): ")
CsvInterval = input("Enter csv time: ")
while True:
    for k,i in coins.items():
        print(i)
        myobj = {'pair': i}
        print(myobj)
        x = requests.post(url,json=myobj).json()

        data = x['data']
        l = ['buy','sell']
        for BoS in l:
            if(BoS == 'buy'):
                for buy in data[BoS]:
                    buy.insert(0,"LCX")
                    buy.insert(1,k)
                    buy.insert(3," ")
            else:
                for sell in data[BoS]:
                    sell.insert(0,"LCX")
                    sell.insert(1,k)
                    sell.insert(2," ")
        totalBuy.append(data['buy'])
        totalSell.append(data['sell'])
        buyDF = pd.DataFrame(data['buy'],columns=["A","B", "C","D","E"])
        sellDF = pd.DataFrame(data['sell'],columns=["A","B", "C","D","E"])
        tempCombined = pd.concat([buyDF, sellDF], axis=0)
        totalDf.append(tempCombined)
        combined = pd.concat(totalDf,axis=0)
        pd.set_option("display.max_rows", None, "display.max_columns", None)
        combined.set_index('A', inplace=True)

        print(combined)

    # print(len(totalSell))
    if(len(totalSell)%int(CsvInterval) == 0):
        csvConfirmation = input("Want to create csv? (y/n) : ")
        if(csvConfirmation.lower() == "y"):
            currentDateTimeFile = str(datetime.datetime.now().strftime('%H.%M.%S %d-%m-%Y'))
            combined.to_csv(currentDateTimeFile+".csv", mode='a', header=False)
            totalDf = []
            # for i in range(len(totalBuy)):
            #     with open('file.csv',"a+",newline='', encoding='utf-8') as f:
            #         writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            #         writer.writerow()


    time.sleep(int(timeInterval))