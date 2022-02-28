# from asyncio.windows_events import NULL
# from dataclasses import dataclass
from symtable import Symbol
import requests
import json
import psycopg2
import os
import uuid
from flask import jsonify
from flask import Flask, request
# from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

# DATABASE_HOST = os.getenv("DATABASE_HOST")
# DATABASE_USER = os.getenv("DATABASE_USER")
# DATABASE_PASS = os.getenv("DATABASE_PASS")
# DATABASE_SCHM = os.getenv("DATABASE_SCHM")


# test = requests.get('https://crypto-banksters-wallet-api.azurewebsites.net/wallet')
# test = requests.get('https://crypto-banksters-rewards-account.azurewebsites.net/InvestmentAccount')
# print(test)
# print(test.content)



def get_db_connection():
    return psycopg2.connect("host=cloudathoncryptodb.postgres.database.azure.com port=5432 dbname=cloudathon user=cloud_admin password=CheeseOnToast64! sslmode=require")
    # if __debug__:
    #   return psycopg2.connect("host=cloudathoncryptodb.postgres.database.azure.com port=5432 dbname=cloudathon user=cloud_admin password=CheeseOnToast64! sslmode=require")

    # else:
    #   return psycopg2.connect(
    #       host=DATABASE_HOST,
    #       user=DATABASE_USER,
    #       password=DATABASE_PASS,
    #       dbname=DATABASE_SCHM
    # )

#This shouldn't live here. Will move later
@app.route('/CyptoValueInUSD/<string:Symbol>')
def CyptoValueInUSD(Symbol: str):
    url = 'https://data.messari.io/api/v1/assets/%s/metrics/market-data' % Symbol  
    response = requests.get(url)
    cryptoData = json.loads(response.content)
    valueInUSD = cryptoData['data']['market_data']['price_usd']
    print(valueInUSD)
    return str(valueInUSD)


@app.route('/InvestmentAccount')
def Test():
    return "BIG TEST"


@app.route('/InvestmentAccount/<string:UserID>')
def GetInvestmentAccount_byuser(UserID: str):
    # First user ID is "GetInvestmentAccountsAssociatedWithUser/4aa9777c-f2e9-4812-9270-5f3b4c178d89"
    currentDir = os.getcwd()
    # queryPath = currentDir + "\crypto_cloudathon_rewards_account_api\SQL_Queries\GetInvestmentAccountsAssociatedWithUser.sql"    
    queryPath = currentDir + "\crypto_cloudathon_rewards_account_api\SQL_Queries\GetInvestmentAccountsAssociatedWithUser.sql" 
    try:
      with open(queryPath) as f:
        queryPath = f.read()
        queryPath = queryPath.format(UserID = UserID)
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(queryPath)
        print(cursor.statusmessage)
        allInvestmentAccounts = cursor.fetchall()
        cursor.close()
        conn.close()
        
        results = []
        for investmentAccount in allInvestmentAccounts:
          print(investmentAccount)
          CryptoCurrencySymbol = investmentAccount[2]
          if CryptoCurrencySymbol == "BCY":
            CryptoCurrencySymbol = "BTC"


          valueInUSD = float(CyptoValueInUSD(CryptoCurrencySymbol))          
          
          totalValueOfCurrency = valueInUSD * investmentAccount[0]

          result={}
          result['Coin']= investmentAccount[1]
          result['NumberCoins']= investmentAccount[0]
          result['UserID']= investmentAccount[3]
          result['ValueUSD']= totalValueOfCurrency
          results.append(result)
        return jsonify(results)

    except Exception as err:
      return str(err) 



# @app.route('/InvestmentAccount/InterestPayments')
# def InvestmentAccount_InterestPayments():    
#     transferringToInterestAccountQuery = os.getcwd() + "\SQL_Queries\AddingInterestToInvestmentAccounts.sql"
#     with open(transferringToInterestAccountQuery) as f:
#       transferringToInterestAccountQuery = f.read()
#       print(transferringToInterestAccountQuery)
#       conn = get_db_connection()
#       cursor = conn.cursor()
      
#       try:
#         cursor.execute(transferringToInterestAccountQuery)
#         print(cursor.statusmessage)
#         conn.commit()
#         cursor.close()
#         conn.close()
#         return "SUCCESS"
#       except Exception as err:
#         return jsonify(err)

# @app.route('/InvestmentAccount/TransfersTo/<float(signed=True):Quantity>/<string:UserID>/<string:ChainID>')
# def InvestmentAccount_TransfersTo(Quantity, UserID, ChainID):  

#     InterestAccountID = str(uuid.uuid4())  
#     InterestTransactionsId = str(uuid.uuid4())  
    
#     transferringToInterestAccountQuery = os.getcwd() + "\\SQL_Queries\TransferringToInterestAccount.sql"
#     with open(transferringToInterestAccountQuery) as f:
#       transferringToInterestAccountQuery = f.read()
#       transferringToInterestAccountQuery = transferringToInterestAccountQuery.format(ChainID = ChainID, UserID = UserID, Quantity = Quantity, InterestAccountID = InterestAccountID, InterestTransactionsId = InterestTransactionsId)
#       print(transferringToInterestAccountQuery)
#       conn = get_db_connection()
#       cursor = conn.cursor()
      
#       try:
#         cursor.execute(transferringToInterestAccountQuery)
#         print(cursor.statusmessage)
#         conn.commit()
#         cursor.close()
#         conn.close()
#         return "SUCCESS"
#       except Exception as err:
#         return jsonify(err)

# @app.route('/InvestmentAccount/TransfersFrom/<float(signed=True):Quantity>/<string:InterestAccountID>')
# def InvestmentAccount_TransfersFrom(Quantity, InterestAccountID):    
#     transferringToInterestAccountQuery = os.getcwd() + "\\SQL_Queries\TransferringOutOfInterestAccount.sql"
    
    
#     with open(transferringToInterestAccountQuery) as f:
#       transferringToInterestAccountQuery = f.read()
#       transferringToInterestAccountQuery = transferringToInterestAccountQuery.format(Quantity = str(Quantity),  InterestAccountID = InterestAccountID)
#       conn = get_db_connection()
#       cursor = conn.cursor()
      
#       try:
#         cursor.execute(transferringToInterestAccountQuery)
#         print(cursor.statusmessage)
#         conn.commit()
#         cursor.close()
#         conn.close()
#         return "SUCCESS"
#       except Exception as err:
#         return jsonify(err)


# sched = BackgroundScheduler(daemon=True)
# sched.add_job(InvestmentAccount_InterestPayments,'cron',minute='*')
# sched.start()


# def CreateTransaction(fromUser, symbol):
#     # walletsUrl = 'https://crypto-banksters-wallet-api.azurewebsites.net/wallets/user/{UserID}'
#     # walletsUrl = 'http://127.0.0.1:5000/wallets/user/{UserID}'
#     # url = walletsUrl.format(UserID = fromUser)
#     # response = requests.get(url)
#     # wallets = json.loads(response.content)

#     # fromWalletID = NULL
#     # for wallet in wallets:
#     #   if symbol == "BCY":
#     #     wallet['symbol'] = wallet
#     #     fromWalletID = wallet['wallet_id']
#     #     break
    


    



#     # conn = get_db_connection()
#     # cursor = conn.cursor()
    
#     try:
#       # toSQLQuery = "select crypto_connection_details.public_address from wallet inner join crypto_connection_details on wallet.connection_id = crypto_connection_details.connection_id where wallet.user_id = '{UserID}'";
#       # toSQLQuery = toSQLQuery.format(UserID = '5265948e-0ae1-4c2f-a093-4ee742d66507')
#       # cursor.execute(toSQLQuery)
#       # print(cursor.statusmessage)
#       # toWalletQueryResult = cursor.fetchall()
#       # toAddress = toWalletQueryResult[0][0]

#       requestObject = {}
#       # requestObject['fromWalletId'] = fromWalletID
#       # requestObject['toAddress'] = 'CFpCVuNRfVq828yx2wPn73GTXj388NjrU9'
#       # requestObject['amount'] = 10

#       # requestObject['fromWalletId'] = "cd6076fc-e4bc-4f34-800b-1fdf8c64e884"
#       # requestObject['toAddress'] = "BsCBSiUzqnTQgnHrSejfg5ac1syQewExGw"
#       # requestObject['amount'] = 500

#       requestObject = {
#         "fromWalletId": "cd6076fc-e4bc-4f34-800b-1fdf8c64e884",
#         "toAddress": "BsCBSiUzqnTQgnHrSejfg5ac1syQewExGw",
#         "amount": 500
#       }

#       requestBody = json.dumps(requestObject) 
#       print(requestBody)
#       headers = {'Content-Type': 'application/json'}

#       r = requests.put('http://127.0.0.1:5000/transaction', json=requestObject, headers=headers)
      
 
#       # check status code for response received
#       # success code - 200
#       print(r)
      
#       # print content of request
#       print(r.content)





#       cursor.close()
#       conn.close()
        
#       return result

#     except Exception as err:
#       print ("Oops! An exception has occured:")
#       print ("Exception TYPE:")
#       return "ERROR: " + err

# CreateTransaction("e16666ff-c559-4aab-96eb-f0a5c2c77b18", "BCY")



# def GetFirstUser():
#     conn_string = "host=cloudathoncryptodb.postgres.database.azure.com port=5432 dbname=cloudathon user=cloud_admin password=CheeseOnToast64! sslmode=require"
#     conn = psycopg2.connect(conn_string)
#     print("Connection established")
#     cursor = conn.cursor()
    
#     try:
#       # cursor.execute("select user_id from users;")
#       cursor.execute("select * from users;")
#       print(cursor.statusmessage)
#       result = cursor.fetchall()
#       cursor.close()
#       conn.close()
        
#       return result[0][0]

#     except Exception as err:
#       print ("Oops! An exception has occured:")
#       print ("Exception TYPE:")
#       return "ERROR: " + err

# GetFirstUser()

    
# def ChainID():
#     conn_string = "host=cloudathoncryptodb.postgres.database.azure.com port=5432 dbname=cloudathon user=cloud_admin password=CheeseOnToast64! sslmode=require"
#     conn = psycopg2.connect(conn_string)
#     print("Connection established")
#     cursor = conn.cursor()
    
#     try:
#       cursor.execute("select chain_id from supported_chains")
#       print(cursor.statusmessage)
#       result = cursor.fetchall()
#       cursor.close()
#       conn.close()
      
      
#       return result[0][0]

#     except Exception as err:
#       print ("Oops! An exception has occured:")
#       print ("Exception TYPE:")
#       return "ERROR: " + err

if __name__ == '__main__':
    app.run()

