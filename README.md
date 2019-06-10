# Twitter_Bots_Detector
The Python bot detector that will fetch the user information from the Twitter database using RESTful API to calculate some mathematical parameters and flag how likely the user account is being handled by a bot.

To Deploy the project follow below steps:

1. Install flask - pip install flask You need Microsoft Visual C++ 14.0 or above version and Visual C++ build tools installed in your machine

2. Install flask-mysqldb - pip install flask-mysqldb Sometimes you get error: failed to build wheel inthat case you can follow below steps:
  - Go to https://www.lfd.uci.edu/~gohlke/pythonlibs/#twisted
  - Download mysqlclient‑1.4.2‑cp37‑cp37m‑win32.whl from the list. You may need another version based on your system and python version
  pip install /Downloads/mysqlclient‑1.4.2‑cp37‑cp37m‑win32.whl After this your flask-mysqldb must get installed correctly
  - Download MySQL Workbench, MySQL Server and Connector/Python.

3. Start MySQL Server, Query the contents of CreateDB.sql in MYSQL Workbench and execute it

4. Make sure Server connection is on

5. Run python twitterBots.py

Sometime you might get error "Authentication plugin 'chaching-sha2-password' cannot be loaded" Then follow below SQL command:

ALTER USER 'yourusername'@'localhost' IDENTIFIED WITH mysql_native_password BY 'youpassword';

The program should run on http://localhost:5000/home

You can use command select * from user; to check the contents of the database.
