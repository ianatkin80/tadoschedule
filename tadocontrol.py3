import httplib2
import schedule
import time
import sqlite3 as lite

temperatureDefaults = (
    (1, 'Monday', '18.0'),
    (2, 'Tuesday','18.0'),
    (3, 'Wednesday', '18.0'),
    (4, 'Thursday', '18.0'),
    (5, 'Friday', '18.0'),
    (6, 'Saturday', '19.7'),
    (7, 'Sunday', '19.7'), 
    (8,  'Evening', '19.7')
)
user = "USERNAME"
passw = "PASSWORD"
h = httplib2.Http(".cache")
con = lite.connect('temperatures.db')

with con:
    cur = con.cursor()    
    cur.execute("DROP TABLE IF EXISTS Temperatures")
    cur.execute("CREATE TABLE Temperatures(Id INT, Day TEXT, SetTemp TEXT)")
    cur.executemany("INSERT INTO Temperatures VALUES(?, ?, ?)", temperatureDefaults)
    print ("Default temperatures loaded")

def setHomeTemp(id):
    with con:
        cur = con.cursor()    
        cur.execute("SELECT SetTemp FROM Temperatures WHERE Id=:Id", {"Id": id})        
        con.commit()
        row = cur.fetchone()
        print ("Changing temperature to " + row[0])
        sendHomeTemp(row[0])

def sendHomeTemp(newTemp):
    (resp_headers, content) = h.request("https://my.tado.com/mobile/1.4/updateThermostatSettings?username=" + user + "&password=" + passw + "&homeTemp=" + newTemp,  "GET", headers={'cache-control':'no-cache'})
    print(time.ctime())
    print(content)

schedule.every().monday.at("00:01").do(setHomeTemp, 1)
schedule.every().tuesday.at("00:01").do(setHomeTemp, 2)
schedule.every().wednesday.at("00:01").do(setHomeTemp, 3)
schedule.every().thursday.at("00:01").do(setHomeTemp, 4)
schedule.every().friday.at("00:01").do(setHomeTemp, 5)
schedule.every().saturday.at("00:01").do(setHomeTemp, 6)
schedule.every().sunday.at("00:01").do(setHomeTemp, 7)
schedule.every().day.at("16:00").do(setHomeTemp, 8)

while True:
    schedule.run_pending()
    time.sleep(1)
