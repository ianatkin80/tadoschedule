# tado multi temperature scheduler script v2.0.2
# Ian Atkin, January 2015
# Released under MIT licence
# Ensure make_table.tpl and temperatures.db are in this script's directory

import httplib2
import schedule
import time
import sqlite3 as lite
from bottle import Bottle, run, template, request
import threading

# Temperature in degrees Celsius
# Entries 1-7 set home temperature at 00:01 on that day (time can be changed below)
# Entry 8 sets home temperature at 16:00 every day, allowing a higher evening temperature (time can be changed below)
temperatureDefaults = (
    (1, 'Monday', '18.0'),
    (2, 'Tuesday','18.0'),
    (3, 'Wednesday', '18.0'),
    (4, 'Thursday', '18.0'),
    (5, 'Friday', '18.0'),
    (6, 'Saturday', '19.7'),
    (7, 'Sunday', '19.7'), 
    (8,  'Every evening', '19.7')
)

# Tado username and password
user = "USERNAME"
passw = "PASSWORD"

# Initialises web app and database instances
webapp = Bottle()
h = httplib2.Http(".cache")

# Populates database with default values
con = lite.connect('temperatures.db')
with con:
    cur = con.cursor()    
    cur.execute("DROP TABLE IF EXISTS Temperatures")
    cur.execute("CREATE TABLE Temperatures(Id INT, Day TEXT, SetTemp TEXT)")
    cur.executemany("INSERT INTO Temperatures VALUES(?, ?, ?)", temperatureDefaults)
    print ("Default temperatures loaded")

# ---------------------------------
# Scheduler section
# ---------------------------------

# When schedule triggers temperature change, finds correct temperature in database
def setHomeTemp(id):
    con = lite.connect('temperatures.db')
    with con:
        cur = con.cursor()    
        cur.execute("SELECT SetTemp FROM Temperatures WHERE Id=:Id", {"Id": id})        
        con.commit()
        row = cur.fetchone()
        print ("Changing temperature to " + row[0])
        sendHomeTemp(row[0])

# Sends data update request to tado server
def sendHomeTemp(newTemp):
    (resp_headers, content) = h.request("https://my.tado.com/mobile/1.4/updateThermostatSettings?username=" + user + "&password=" + passw + "&homeTemp=" + newTemp,  "GET", headers={'cache-control':'no-cache'})

# Following print statements are for debugging purposes to show temperature is changing at desired time
    print(time.ctime())
    print(content)

# Initialise scheduler instance
scheduler = schedule.Scheduler()

# Change 00:01 to desired time for daytime temperature to begin each day (24 hour format)
scheduler.every().monday.at("00:01").do(setHomeTemp, 1)
scheduler.every().tuesday.at("00:01").do(setHomeTemp, 2)
scheduler.every().wednesday.at("00:01").do(setHomeTemp, 3)
scheduler.every().thursday.at("00:01").do(setHomeTemp, 4)
scheduler.every().friday.at("00:01").do(setHomeTemp, 5)
scheduler.every().saturday.at("00:01").do(setHomeTemp, 6)
scheduler.every().sunday.at("00:01").do(setHomeTemp, 7)

# Change 16:00 to desired time for evening temperature to begin every day (24 hour format)
scheduler.every().day.at("16:00").do(setHomeTemp, 8)

# Runs scheduler in a separate thread
class ScheduleThread(threading.Thread):
    @classmethod
    def run(cls):
        while True:
            scheduler.run_pending()
            time.sleep(1)

continuous_thread = ScheduleThread()
continuous_thread.start()

# ---------------------------------
# Web interface section
# ---------------------------------

# Calls web interface page, defaults to <hostname>/tado
@webapp.route('/tado')
def displayWeb():
    con = lite.connect('temperatures.db')
    with con:
        cur = con.cursor()    
        cur.execute("SELECT * FROM Temperatures")        
        con.commit()
        output = cur.fetchall()
# Send table of current temperature settings to web page defined by make_table.tpl    
    return template('make_table', rows=output)

# Calls data update page (when 'Save changes' clicked on main web page)
@webapp.route('/update', method='GET')
def edit_item():
    newTemp = [None] * 9
    for id in range(1, 9):
        newTemp[id]= request.GET.get(str(id),'').strip()
        print(newTemp[id] + ' ' + str(id))
        con = lite.connect('temperatures.db')
        with con:
            cur = con.cursor()
            cur.execute("UPDATE temperatures SET SetTemp = ? WHERE id LIKE ?", (newTemp[id],id))
    
    con.commit()
    return '<p>Updated</p>'

# Set interface and port for web interface here (0.0.0.0 = listen on all interfaces)
# Access web interface at http://<ip address>:<port>/tado
run(webapp, host='0.0.0.0', port=8080)
