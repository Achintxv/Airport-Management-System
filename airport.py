import sys
import mysql.connector
import time

def createCursor():
          global myConnect

          try:
                    myConnect=mysql.connector.connect(
                              host="localhost",
                              user="root",
                              password="Ac.root123",
                              database="airport"
                              )

          except Exception:
                    sys.exit("databse connection not successful")

          if myConnect.is_connected():
                    print("Connection successfull")

          else:
                    sys.exit("databse connection not successful")

          global mycursor
          mycursor= myConnect.cursor()

def updatePassword():
          newpass=input("Enter new password:")
          repass=input("Re-Enter new password:")

          if newpass==repass:
                    global mycursor, myConnect
                    mycursor.execute("update user set password='{}' where username='Admin'".format(newpass))
                    myConnect.commit()
                    print("Password successfully changed")
                    print("Please login again to continue")
                    return True
          else:
                    print("Password does not match")
                    print("Password change unsuccessful")
                    return False


def menu():
          print("Welcome to management portal")
          print("Enter admin password to proceed")
          password=input("Password:")
          checkUser(password)

          while True:
                    print()
                    print("Main menu")
                    print("1.To Update the password")
                    print("2.Manage country")
                    print("3.Manage flight")
                    print("0.To Exit")
                    
                    choice = int(input("Enter your choice:"))
                    if choice ==1:
                              success= updatePassword()
                              if success:
                                        break
                    elif choice==2:
                              manageCountries()
                              
                    elif choice==3:
                              manageFlights()
                              
                    elif choice==0:
                              print("Have a great day.")
                              print("Logged off successfully.")
                              break
                    
                    else:
                              print("Choose a correct option")
                    
                    
                      
def checkUser(password):
          global mycursor
          mycursor.execute("select password from user where username='admin'")
          data=mycursor.fetchone()
          if password==data[0]:
                    print('login successful')
          else:
                    sys.exit("incorrect password")

def manageCountries():
          while True:
                    print("1.Add a country")
                    print("2.Search a country code")
                    print("0.Go back to main menu")
                    choice = int(input("Enter your choice:"))
                    if choice==1:
                              addCountry()
                    elif choice==2:
                              searchCountry()
                    elif choice==0:
                              return
                    else:
                              print("Choose a correct option")

def manageFlights():
          while True:
                    print("1.Add a flight")
                    print("2.Modify a flight")
                    print("3.Delete a flight")
                    print("4.Search a flight")
                    print("0.Go back to main menu")
                    choice=int(input("Enter your choice:"))
                    if choice==1:
                              addFlight()
                    elif choice==2:
                              modifyFlight()
                    elif choice==3:
                              deleteFlight()
                    elif choice==4:
                              searchFlight()
                    elif choice==0:
                              return
                    else:
                              print("Choose a correct option!")

def addCountry():
          country=input("Enter Country Name:")
          code=int(input("Enter Country Code:"))
          global mycursor, myConnect
          try:
                    mycursor.execute("insert into country values('{}','{}')".format(code,country))
                    myConnect.commit()
                    print("Country added successfully")
          except Exception as e:
                    print(e)

def addFlight():
          fid=input("Enter flight ID:")
          tocode=input("Enter To country code:")
          fromcode=input("Enter from country code:")
          if validCode(tocode) and validCode(fromcode):
                    datentime = getDateTime()
                    global mycursor, myConnect
                    try:
                              if validCode(tocode) and validCode(fromcode):
                                        query="insert into flight values('{}','{}','{}',STR_TO_DATE('{}','%Y-%m-%d %H:%i:%s'))".format(fid,tocode,fromcode,datentime)
                                        mycursor.execute(query)
                                        myConnect.commit()
                                        print("Flight successfully added")
                                        
                    except Exception as e:
                              print(e)

          else:
                    print("Enter a valid code")

def getDateTime():
          y=input("Year(YYYY):")
          d=input("Day(DD):")
          m=input("Month(MM):")
          hr=input("Hours(HH):")
          mins=input("Minutes(MM):")
          datetime_str = '{:0>4}-{:0>2}-{:0>2}{:0>2}:{:0>2}:00'.format(y,m,d,hr,mins)
          return datetime_str

def validCode(code):
          global mycursor
          mycursor.execute("select country from country where countrycode='{}'".format(code))
          mycursor.fetchall()
          if mycursor.rowcount>=1:
                    return True
          else:
                    return False

def validFlight(code):
          global myCursor
          mycursor.execute("select flightid from flight where flightid='{}'".format(code))
          mycursor.fetchall()
          if mycursor.rowcount>=1:
                    return True
          else:
                    return False

def modifyFlight():
          fid=int(input("Enter flight id to modify:"))
          if not validFlight(fid):
                    print("Enter a valid id")
                    return
          tocode=input("Enter To country code:")
          fromcode=input("Enter from country code:")
          if validCode(tocode) and validCode(fromcode):
                    datentime = getDateTime()
                    global mycursor, myConnect
                    try:
                              if validCode(tocode) and validCode(fromcode):
                                        query="update flight set toflight='{}',fromflight='{}',datentime=STR_TO_DATE('{}','%Y-%m-%d %H:%i:%s')where flightid='{}'" .format(tocode,fromcode,datentime,fid)
                                        mycursor.execute(query)
                                        myConnect.commit()
                                        print("Flight successfully modified")
                                        
                    except Exception as e:
                              print(e)

          else:
                    print("Enter a valid code")

def deleteFlight():
          fid=input("Enter flight id to delete:")
          if not validFlight(fid):
                    print("Enter a valid id")
                    return
          global mycursor, myConnect
          try:
                    query="delete from flight where flightid='{}'".format(fid)
                    mycursor.execute(query)
                    myConnect.commit()
                    print("Flight deleted successfully")
          except Exception as e:
                    print(e)

def searchFlight():
          tocode=input("Enter To country code:")
          fromcode=input("Enter from country code:")
          if validCode(tocode) and validCode(fromcode):
                    global mycursor
                    try:
                              if validCode(tocode) and validCode(fromcode):
                                        query="select * from flight where toflight='{}' and fromflight='{}'".format(tocode,fromcode)
                                        mycursor.execute(query)
                                        flights = mycursor.fetchall()
                                        for flight in flights:
                                                  flight=list(flight)
                                                  flight[3]=str(flight[3])
                                                  print(flight)
                                        
                    except Exception as e:
                              print(e)

          else:
                    print("Enter a valid code")


def searchCountry():
          country=input("Enter country Name:")
          global mycursor
          try:
                    query="select * from country where country='{}'".format(country)
                    mycursor.execute(query)
                    cont= mycursor.fetchall()
                    if mycursor.rowcount >=1:
                              for c in cont:
                                        print(c)
                    else:
                              print("Enter a valid code")

          except Exception as e:
                    print(e)

                    
createCursor()
menu()
