import psycopg2
import pandas as pd
import os

con = psycopg2.connect(
database="customerdb",
user="admin",
password="postgres",
host="localhost",
port= '5432'
)
mycursor = con.cursor()

phonenum= input("put phone num ")
def queryuser():
    try:
        namequery = "SELECT phone FROM customerdetails WHERE {}=phone"
        formatted = namequery.format(phonenum)
        queryresult = pd.read_sql(formatted, con=con,)
        if len(queryresult) == 0:
          print('Not a valid phone, would you like to create an account with NEXTBANK?? \n 1. YES 2. NO')
          createacct = input()
          if createacct == "1":
             print("craeting an acct for you")
          elif createacct =="2":
             print("thanks, hope to see you soon")
          print("Exiting We are done")
          os.system(exit())
        else:
          print("WELCOME TO NEXT BANK \n \n")

    except Exception as e:
        print(f"Error: {e}")

def acctbal():
    try:
        acctquery = "SELECT acctbal FROM customerdetails WHERE {}=phone"
        formatted = acctquery.format(phonenum)
        queryresult = pd.read_sql(formatted, con=con,)
        if len(queryresult) == 0:
          print('Not a valid phone')
        else:
          print("your balance is \n \n", queryresult)

    except Exception as e:
        print(f"Error: {e}")
def airtimerecharge():
    try:
        recharge_value = int(input("Enter Amount: "))
        recharge_query = "SELECT recharge FROM customerdetails WHERE {}=phone"
        recharge_format = recharge_query.format(phonenum)
        recharge_bal = pd.read_sql(recharge_format, con=con)['recharge'][0]
        print(recharge_bal)
        acctquery = "SELECT acctbal FROM customerdetails WHERE {}=phone"
        formatted = acctquery.format(phonenum)
        queryresult = pd.read_sql(formatted, con=con)
        acct_bal_value = queryresult['acctbal'][0]
        final_acct_bal = acct_bal_value - recharge_value
        final_recharge_bal = recharge_value + recharge_bal
        print(final_acct_bal)
        if recharge_value > acct_bal_value:
           print("Insufficient acct balance")
           os.system(exit())
        else:
           update_recharge = "UPDATE customerdetails SET recharge = {} WHERE {}=phone"
           f_update_recharge = update_recharge.format(final_recharge_bal, phonenum)
           mycursor.execute(f_update_recharge)
           con.commit()
           update_acctbal = "UPDATE customerdetails SET acctbal = {} WHERE {}=phone"
           f_update_acctbal = update_acctbal.format(final_acct_bal, phonenum)
           mycursor.execute(f_update_acctbal)
           con.commit()
        #    reduce_acct_num()
    except Exception as e:
        print(f"Error: {e}")

def transfer():
   print("transfer money")
   transfer_amt = int(input("How much are you sending:  "))
   account_number=int(input("Iput acct number:  "))
   acctquery = "SELECT acctbal FROM customerdetails WHERE {}=phone"
   formatted = acctquery.format(phonenum)
   debit_queryresult = pd.read_sql(formatted, con=con,)["acctbal"][0]
   final_debit_bal = debit_queryresult - transfer_amt
   c_credit_query= "SELECT acctbal FROM customerdetails where {}=acctnum"
   f_c_credit_query = c_credit_query.format(account_number)
   credit_acct_result = pd.read_sql(f_c_credit_query, con=con)["acctbal"][0]
   final_credit_bal = credit_acct_result + transfer_amt
   if transfer_amt > debit_queryresult:
      print("insufficient funds")
      os.system(exit())
   else:
      print("check account details")
      acct_check = "SELECT acctnum FROM customerdetails WHERE {}=acctnum"
      f_acct_num = acct_check.format(account_number)
      acct_credit_query = pd.read_sql(f_acct_num, con=con)
      if len(acct_credit_query) == 0:
         print("confirm the acct number and try again")
         os.system(exit())

      else:
        debit_update = "UPDATE customerdetails SET acctbal={} WHERE {}=phone"
        f_debit_update = debit_update.format(final_debit_bal, phonenum)
        mycursor.execute(f_debit_update)
        con.commit()
        credit_update = "UPDATE customerdetails SET acctbal={} WHERE {}=acctnum"
        f_credit_update = credit_update.format(final_credit_bal, account_number)
        mycursor.execute(f_credit_update)
        con.commit()
        print("suucessful transaction")


def ussdapp():

  queryuser()
  myUssdcode = input('INPUT USSD CODE: ')

  if myUssdcode == '*212#' :
    print(" \n Welcome to NextBank ussd services \n 1. check balance \n 2. Airtime \n 3. Transfer services \n 4. Buy Data \n 5. Payments \n 6. Get Loans \n 7. Get account statements \n \n")
    print("\n SELECT A SERVICE")
    service = input('SELECT THE SERVICE YOU WANT TO USE:   ')
    if service == "1":
      print('Getting your account balance')
      acctbal()
    elif service == "2":
       print("LOADING AIRTIME:  ")
       airtimerecharge()
    elif service == "3":
       print(" TRANSFERING FUNDS")
       transfer()
  else:
    print('put valid ussd code')
ussdapp()

