tadoschedule
============

tado multi temperature scheduling utility

At the moment, the tado smart thermometer web and mobile apps only allow a single home temperature to be set.  This is a simple python3 script to allow the home temperature to be changed at defined times.

Having only learned python in the last day I'm sure this code can be massively improved!

Usage:  - copy tadocontrol.py3 and temperatures.db into your directory of choice
            - edit tadocontrol.py3 to set tado username/password, temperature and time preferences
            - run tadocontrol.py3 in a terminal to activate

Python package dependencies: httplib2, schedule, sqllite3, time

Tested with python v3.4.0 only
