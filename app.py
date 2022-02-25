from symtable import Symbol
import requests
import json
import psycopg2
import os
import uuid
from flask import jsonify
from flask import Flask, request

app = Flask(__name__)

DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASS = os.getenv("DATABASE_PASS")
DATABASE_SCHM = os.getenv("DATABASE_SCHM")


def get_db_connection():
    if __debug__:
      return psycopg2.connect("host=cloudathoncryptodb.postgres.database.azure.com port=5432 dbname=cloudathon user=cloud_admin password=CheeseOnToast64! sslmode=require")

    else:
      return psycopg2.connect(
          host=DATABASE_HOST,
          user=DATABASE_USER,
          password=DATABASE_PASS,
          dbname=DATABASE_SCHM
    )


@app.route('/CyptoValueInUSD/<string:Symbol>')
def CyptoValueInUSD(Symbol: str):
    url = 'https://data.messari.io/api/v1/assets/%s/metrics/market-data' % Symbol  
    response = requests.get(url)
    cryptoData = json.loads(response.content)
    valueInUSD = cryptoData['data']['market_data']['price_usd']
    print(valueInUSD)
    return str(valueInUSD)




@app.route('/TransferringToInterestAccount')
def TransferringToInterestAccount():
    
    # To be removed
    firstUser = GetFirstUser()
    chainID = ChainID()



    InterestAccountID = str(uuid.uuid4())  
    InterestTransactionsId = str(uuid.uuid4())  
    
    transferringToInterestAccountQuery = os.getcwd() + "\\SQL_Queries\TransferringToInterestAccount.sql"
    with open(transferringToInterestAccountQuery) as f:
      transferringToInterestAccountQuery = f.read()
      transferringToInterestAccountQuery = transferringToInterestAccountQuery.format(ChainID = chainID, UserID = firstUser, Quantity = 100, InterestAccountID = InterestAccountID, InterestTransactionsId = InterestTransactionsId)
      print(transferringToInterestAccountQuery)
      conn = get_db_connection()
      cursor = conn.cursor()
      
      try:
        cursor.execute(transferringToInterestAccountQuery)
        print(cursor.statusmessage)
        conn.commit()
        cursor.close()
        conn.close()
      except Exception as err:
        print ("Oops! An exception has occured:")
        print ("Exception TYPE:")


      return "I LIKE PIZZA"


@app.route('/GetInvestmentAccountsAssociatedWithUser/<string:UserID>')
def GetInvestmentAccountsAssociatedWithUser(UserID: str):
    # First user ID is "4aa9777c-f2e9-4812-9270-5f3b4c178d89"
    
    queryPath = os.getcwd() + "\SQL_Queries\GetInvestmentAccountsAssociatedWithUser.sql"
    with open(queryPath) as f:
      queryPath = f.read()
      queryPath = queryPath.format(UserID = UserID)
      conn = get_db_connection()
      cursor = conn.cursor()
      
      try:
        cursor.execute(queryPath)
        print(cursor.statusmessage)
        allInvestmentAccounts = cursor.fetchall()
        cursor.close()
        conn.close()
        
        results = []
        for investmentAccount in allInvestmentAccounts:
          print(investmentAccount)
          CryptoCurrencySymbol = investmentAccount[2]
          valueInUSD = float(CyptoValueInUSD(CryptoCurrencySymbol))          
          
          totalValueOfCurrency = valueInUSD * investmentAccount[0]

          result={}
          result['Coin']= investmentAccount[1]
          result['NumberCoins']= investmentAccount[0]
          result['ValueUSD']= totalValueOfCurrency
          results.append(result)
        return jsonify(results)

      except Exception as err:
        print ("Oops! An exception has occured:")
        print ("Exception TYPE:")
        return "ERROR: " + err


def GetFirstUser():
    conn_string = "host=cloudathoncryptodb.postgres.database.azure.com port=5432 dbname=cloudathon user=cloud_admin password=CheeseOnToast64! sslmode=require"
    conn = psycopg2.connect(conn_string)
    print("Connection established")
    cursor = conn.cursor()
    
    try:
      cursor.execute("select user_id from users;")
      print(cursor.statusmessage)
      result = cursor.fetchall()
      cursor.close()
      conn.close()
      
      
      return result[0][0]

    except Exception as err:
      print ("Oops! An exception has occured:")
      print ("Exception TYPE:")
      return "ERROR: " + err
    
def ChainID():
    conn_string = "host=cloudathoncryptodb.postgres.database.azure.com port=5432 dbname=cloudathon user=cloud_admin password=CheeseOnToast64! sslmode=require"
    conn = psycopg2.connect(conn_string)
    print("Connection established")
    cursor = conn.cursor()
    
    try:
      cursor.execute("select chain_id from supported_chains")
      print(cursor.statusmessage)
      result = cursor.fetchall()
      cursor.close()
      conn.close()
      
      
      return result[0][0]

    except Exception as err:
      print ("Oops! An exception has occured:")
      print ("Exception TYPE:")
      return "ERROR: " + err

if __name__ == '__main__':
    app.run()

