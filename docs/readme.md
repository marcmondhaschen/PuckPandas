# **PuckPandas**

PuckPandas is a hobby database tool built to query, log, and transform data queried from the National Hockey League (NHL) API into a normalized, local database built for general-purpose hockey analysis. Once properly configured, PuckPandas helps you to get fast, up-to-date hockey data easily and simply.
________________________________________
### **Installation**

#### Requirements

As the name suggests, PuckPandas makes heavy use of the Pandas library to manage and store data. Further Python library requirements are described in the _‘..\PuckPandas\requirements.txt’_.  PuckPandas stores its data to a MySQL database which will need to be configured and running before PuckPandas is run.
MySQL Database
To properly use this release as distributed, users will need to configure and run a MySQL database. 

SQL scripts required to create all the of the application’s database schemas, users, tables, and indices are included in ‘..\PuckPandas\sql\mysql_localhost_create_statements.sql’. As the name implies, the script assumes users will use a server addressed as ‘localhost’ but is easily rewritten to suit users’ differing specifications. Users should overwrite the “YOURPASSWORDGOESHERE” text blocks with their own, intended passwords before attempting to use these scripts. 
Environment Files
This application uses the dotenv library to access users .env files. An example .env file has been included as _‘..\PuckPandas\sampledotenv.txt’_. Users should rewrite the PASSWORD fields with the passwords they chose in the database creation steps and save the file as “.env” (no filename, just the extension) in the same folder.
________________________________________
### **Documentation**

#### Standard Operation

Once configured, running PuckPandas is exceedingly simple.
As distributed, the project’s ‘main’ script will query its way through the history of games and players offered by the NHL in chronological order. Should the application’s connection be interrupted, it can safely be restarted at a minimum risk to data loss and obligation to re-query the API. 
Object Model
Underneath the covers, PuckPandas includes objects whose data attributes represent a single API call’s data (i.e. TeamsImport) or a sub-table nested within a single call’s data (i.e. RefereesImport). Methods given to these objects provide standard CRUD functionality. Most objects offer update_db , clear_db, query_db, query_api, and query_api_update_db (which runs query_api, clear_db, and update_db in succession) to query data from the API and log it to the local database. 

These API-querying methods are called in specific order, where the information in each call provides serializing information for the next set of calls. 
The order, timing, and necessity of these calls is maintained by a Scheduler object. Several logging objects are also provided, who support the Scheduler object’s ability to identify and query information not yet present in the local database. The Scheduler is built to be re-run as time progresses and more games played, generating more game and player data. The Scheduler is also built to recover reasonably politely if interrupted, generating a minimum of data loss and need for re-query.
________________________________________
### **Disclaimers**

"NHL" is registered mark of and belongs to the National Hockey League (NHL). Use of "NHL"
or any other National Hockey League owned marks within this software and its documentation is not
in any way an indication of the authors or this software’s affiliation with nor endorsement by the NHL.

