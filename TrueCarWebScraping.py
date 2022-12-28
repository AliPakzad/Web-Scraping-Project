from bs4 import BeautifulSoup

import requests

import mysql.connector

cnx = mysql.connector.connect(user='root', password='@lexander8891',
                              host='127.0.0.1',
                              database='infoDB')

#print("connected to DB")
cursor = cnx.cursor(buffered=True)

print("Please enter your brand: ")

brand = input()

url = 'https://www.truecar.com/used-cars-for-sale/listings/' + brand

#print(url)

webpage = requests.get(url)

soup = BeautifulSoup(webpage.text, 'html.parser')

result = soup.find_all("div", class_ = "card-content vehicle-card-body order-3 vehicle-card-carousel-body")


for i in range(20):
    vehicleMileage = result[i].find("div", attrs ={'class':"truncate text-xs", 'data-test':"vehicleMileage"}).text
    vehiclePrice = result[i].find("div", attrs ={'class':"heading-3 my-1 font-bold", 'data-qa':"Heading", 'data-test':"vehicleCardPricingBlockPrice"}).text
    #convert mileage and Price into integers
    vehicleMileageInt = int(vehicleMileage.split()[0].replace(",", ""))
    vehiclePriceInt = int(vehiclePrice.replace(",", "").replace("$", ""))
    cursor.execute("INSERT INTO cars VALUES(\'%s\', \'%i\', \'%i\')" %(brand, vehicleMileageInt, vehiclePriceInt))
    cnx.commit()
    #print(f"Mileage is {vehicleMileage} and price is {vehiclePrice}")
    #print()



#cursor.execute("CREATE TABLE cars(brand varchar(50), mileage INTEGER, price INTEGER)")

cursor.execute("SELECT * From cars;")
cnx.commit()

results = cursor.fetchall()

for row in results:
  print(row)

cnx.close()
