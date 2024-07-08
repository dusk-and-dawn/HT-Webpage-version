****************
## Welcome to HabIT
****************
# HabIT 

## Introduction 
This habit tracking app was created for an object-oriented and functional programming course. 
It can record habits in general as well as concrete instances of them and then process the habit data to generate minor insights. 

## Before first use

__Python__

HabIT has been implemented using Python 3. Hence, a Python 3 installation is required to use the application. 

Python can be downloaded here: https://www.python.org/downloads/ 

A detailed guide helping you with the installation process can be found here: https://wiki.python.org/moin/BeginnersGuide/Download 

__Dependencies__

However, to run HabIT, all dependencies must also be installed, which includes: 

-Flask

-datetime 

-sqlite3

-pytest 

All of these can be installed using the pip installer, which itself comes with Python, if python was installed from the python.org webpage. 
To install the dependecies please simply open a terminal, navigate to the directory in which HabIT has been saved and run the following commands: 

pip install flask

pip install datetime 

pip install sqlite

pip install pytest 

## General structure

App.py controls the system logic, the datastreams and most else. 
Analysis.py separates between daily and weekly habits and is mostly used to supply any and all analytical functions. 
Within the templates folder all html templates can be found, each one corresponding to a Flask route in app.py. 
Also, there is a testsuite which can be adapted in the test_app.py and test_database.py files. 

## Unit tests

A significant number of functionalities can be tested via unittests. These can be executed by using the following command: 

python3 -m pytest 

## Credits 

This app was coded by David Koeller in his function as a student of the Applied Artificial Intelligence B.Sc. at the International University for Applied Sciences. 

## License 

Copyright 2024 David Koeller 

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
