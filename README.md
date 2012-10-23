stockExperiments
================
A series of experiments aiming to put python into practice in the exploration of Statistis, AI and other tecniches while using stock market data.


### Features:
- None yet

### Installing:
- Setting the environment up
    Install Python 2.7
    Install bovespaParser
        easy_install bovespaparser
    Install mySql (=> 5.5) 
        ubuntu: sudo apt-get install mysql-server
    Install nose (for testing)
        easy_install nose
    [Optional] Instal qtStalker
        ubuntu: sudo apt-get install qtstalker
- Setting the database up
    Login
        mysql -u root -p
    Create a schema
        CREATE SCHEMA `stockexperiments` ;
    Create a user
        CREATE USER stockexperiments@localhost IDENTIFIED BY '';
    Add a database user
        GRANT ALL ON stockexperiments.* TO stockexperiments@localhost;
        FLUSH PRIVILEGES;

### Links:
- [Blog posts][1]

---------------------------------------
### Any feedback is always appreciated!
- Write to the author:  <rhlobo+stockExperiments@gmail.com>


[1]: http://how.i.drycode.it/search/label/stockExperiments