tadoschedule
============

tado multi temperature scheduling utility by Ian Atkin, January 2015

At the moment, the tado smart thermometer web and mobile apps only allow a single home temperature to be set.  This is a simple python3 script to allow the home temperature to be changed at defined times.

A simple non-authenticated web interface is also included.

Having only learned python in the last week I'm sure this code can be massively improved!

Usage:  
- copy tadocontrol.py3, make_table.tpl and temperatures.db into your directory of choice
- edit tadocontrol.py3 to set tado username/password, network settings for web interface, temperature and time preferences
- run tadocontrol.py3 in a terminal to activate

Python package dependencies: bottle, httplib2, schedule, sqllite3, time

Tested with python v3.4.0 only
