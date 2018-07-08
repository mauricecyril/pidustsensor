# Instructions for Setting Up SQLite3 Database for Data Logging

Max Rows in SQLITE3 = 9,223,372,036,854,775,807

There are 1440 Minutes in a 24 hour day

The GROVE / Shinyei PPD42NS dust sensor gets a reading every 30 seconds (2 readings every minute), so anticipate 2880 readings a day. Which allows us to get readings for a maximum of 3,202,559,735,019,020 days, or 8,774,136,260,326 years. So no need to worry about filling up the database.

### SQL Table Layout

Table Name		|Column Name		            |Data Type			    |Description
--------------|---------------------------|-------------------|----------------------------------------------
airqualitylog	|datetimestamp			        |Text               |Date Time Stamp
airqualitylog	|r25_db                     |Integer            |Ratio for PM2.5 (P2 or Pin4) (r25)
airqualitylog	|c25_db                     |Integer            |Raw Readings of PM2.5 Concentration (PCS per 0.01 cubic foot) (c25)
airqualitylog	|r10_db                     |Integer            |Ratio for PM1.0 (P1 or Pin2) (r10)
airqualitylog	|c10_db                     |Integer            |Raw readings of PM1.0 Concentration (PCS  per 0.01 cubic foot) (c10)
airqualitylog	|PM25count_db               |Integer            |Concentration Count for Particles Greater than 1µg and Less than 2.5µ (PCS per 0.01 cubic foot) (PM25count = c10 - c25)
airqualitylog	|concentration_ugm3_pm25_db |Integer            |SI PM2.5 Concentration (PCS per cubic metre) (concentration_ugm3_pm25)
airqualitylog	|PM10count_db               |Integer            |Concentration Count for Particles greater than 2.5 µg (PCS per 0.01 cubic foot) (PM10count = c25)
airqualitylog	|concentration_ugm3_pm10_db |Integer            |SI PM10 Concentration (PCS per cubic metre)(concentration_ugm3_pm10)
airqualitylog	|aqiPM25_db                 |Integer            |US AQI for PM2.5 (Should be average of a 24h reading)
airqualitylog	|aqiPM10_db                 |Integer            |US AQI for PM10 (Should be average of a 24h reading)


### Creating a New SQL Table

If creating a new SQL table, first make sure you have SQLite3 installed:
```shell
$ sudo apt-get install sqlite3 
```

Run the SQLite3 Command Prompt and create a new Database called "airqualitylog.db":
```shell
$ sqlite3 airqualitylog.db 
```

Insert the following lines from "CREATE TABLE..." onward:
```SQL
-- airqualitylog table
CREATE TABLE IF NOT EXISTS airqualitylog (
 datetimestamp text NOT NULL,
 r25_db integer NOT NULL,
 c25_db integer NOT NULL,
 r10_db integer NOT NULL,
 c10_db integer NOT NULL,
 PM25count_db integer NOT NULL,
 concentration_ugm3_pm25_db integer NOT NULL,
 PM10count_db integer NOT NULL,
 concentration_ugm3_pm10_db integer NOT NULL,
 aqiPM25_db integer NOT NULL,
 aqiPM10_db integer NOT NULL
);
```

or enter each line in the prompt as follows:
```
sqlite> CREATE TABLE IF NOT EXISTS airqualitylog (
   ...>  datetimestamp text NOT NULL,
   ...>  r25_db integer NOT NULL,
   ...>  c25_db integer NOT NULL,
   ...>  r10_db integer NOT NULL,
   ...>  c10_db integer NOT NULL,
   ...>  PM25count_db integer NOT NULL,
   ...>  concentration_ugm3_pm25_db integer NOT NULL,
   ...>  PM10count_db integer NOT NULL,
   ...>  concentration_ugm3_pm10_db integer NOT NULL,
   ...>  aqiPM25_db integer NOT NULL,
   ...>  aqiPM10_db integer NOT NULL
   ...> );
```

#### If Importing Data from an Existing CSV file
If importing data from an existing CSV file make sure to delete the header row from the CSV file before importing.
```shell
$ cp airqualitylog.csv airqualitylog_noheader.csv
$ nano airqualitylog_noheader.csv
```
Delete the first row of the file and save (Ctrl-W or Ctrl-X in Nano).


The following commands import the airqualitylog_noheader.csv file into the airqualitylog table.

```shell
$ sqlite3 airqualitylog.db 
sqlite> .mode csv
sqlite> .import /home/pi/airqualitylog_noheader.csv airqualitylog
```

Optional: In some cases you might need to Drop the airqualitylog table before importing data. WARNING: If you DROP the table it will purge all data from the table so this should only be done the very first time you are setting up the database for the dust sensor.
```shell
$ sqlite3 airqualitylog.db 
sqlite> DROP TABLE IF EXISTS airqualitylog;
sqlite> .mode csv
sqlite> .import /home/pi/airqualitylog_noheader.csv airqualitylog
```


#### Exiting SQLite3 Command Prompt
Exit the SQLite3 Command Prompt by pressing "Ctrl-D" or by typing .quit in the prompt
```shell
sqlite> .quit
```
