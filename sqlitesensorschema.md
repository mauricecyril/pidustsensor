# Instructions for Setting Up SQLite3 Database for Data Logging from the Environment Sensors

### SQL Table Layout

Table Name		|Column Name		            |Data Type			    |Description
--------------|---------------------------|-------------------|----------------------------------------------
airqualitylog	|datetimestamp			        |Text               |Date Time Stamp
airqualitylog	|r25_db                     |Integer            |Ratio for PM2.5 (P2 or Pin4) (r25)
airqualitylog	|c25_db                     |Integer            |Raw Readings of PM2.5 Concentration (PCS per 0.01 cubic foot) (c25)
airqualitylog	|r10_db                     |Integer            |Ratio for PM1.0 (P1 or Pin2) (r10)
airqualitylog	|c10_db                     |Integer            |Raw readings of PM1.0 Concentration (PCS  per 0.01 cubic foot) (c10)
airqualitylog	|temp_db                    |Integer            |Temperature Readings from BME680 in Celsius 
airqualitylog	|pres_db                    |Integer            |Pressure Readings from BME680 in hPa
airqualitylog	|hum_db                     |Integer            |Humidity Readings from BME680 in %RH
airqualitylog	|gas_db                     |Integer            |Gas Resistance Readings from BME680 in Ohms


### Creating a New SQL Table

If creating a new SQL table, first make sure you have SQLite3 installed:
```shell
$ sudo apt-get install sqlite3 
```

Run the SQLite3 Command Prompt and create a new Database called "envirosensorlog.db":
```shell
$ sqlite3 envirosensorlog.db 
```

Insert the following lines from "CREATE TABLE..." onward:
```SQL
-- envirosensorlog table
CREATE TABLE IF NOT EXISTS envirosensorlog (
 datetimestamp text NOT NULL,
 r25_db integer NOT NULL,
 c25_db integer NOT NULL,
 r10_db integer NOT NULL,
 c10_db integer NOT NULL,
 temp_db integer NOT NULL,
 pres_db integer NOT NULL,
 hum_db integer NOT NULL,
 gas_db integer NOT NULL
);
```

or enter each line in the prompt as follows:
```
sqlite> CREATE TABLE IF NOT EXISTS envirosensorlog (
   ...>  datetimestamp text NOT NULL,
   ...>  r25_db integer NOT NULL,
   ...>  c25_db integer NOT NULL,
   ...>  r10_db integer NOT NULL,
   ...>  c10_db integer NOT NULL,
   ...>  temp_db integer NOT NULL,
   ...>  pres_db integer NOT NULL,
   ...>  hum_db integer NOT NULL,
   ...>  gas_db integer NOT NULL
   ...> );
```

#### If Importing Data from an Existing CSV file
If importing data from an existing CSV file make sure to delete the header row from the CSV file before importing.
```shell
$ cp envirosensorlog.csv envirosensorlog_noheader.csv
$ nano envirosensorlog_noheader.csv
```
Delete the first row of the file and save (Ctrl-W or Ctrl-X in Nano).


The following commands import the envirosensorlog_noheader.csv file into the envirosensorlog table.

```shell
$ sqlite3 envirosensorlog.db 
sqlite> .mode csv
sqlite> .import /home/pi/envirosensorlog_noheader.csv envirosensorlog
```

Optional: In some cases you might need to Drop the envirosensorlog table before importing data. WARNING: If you DROP the table it will purge all data from the table so this should only be done the very first time you are setting up the database for the dust sensor.
```shell
$ sqlite3 envirosensorlog.db 
sqlite> DROP TABLE IF EXISTS envirosensorlog;
sqlite> .mode csv
sqlite> .import /home/pi/envirosensorlog_noheader.csv envirosensorlog
```


#### Exiting SQLite3 Command Prompt
Exit the SQLite3 Command Prompt by pressing "Ctrl-D" or by typing .quit in the prompt
```shell
sqlite> .quit
```

### How to check data in the database table
```
$ sqlite3 envirosensorlog.db 
sqlite> select * from envirosensorlog
```
