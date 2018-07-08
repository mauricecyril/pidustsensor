# Instructions for Setting Up SQLite3 Database for Data Logging

Max Rows in SQLITE3 = 9,223,372,036,854,775,807

There are 1440 Minutes in a 24 hour day

The GROVE / Shinyei PPD42NS dust sensor gets a reading every 30 seconds (2 readings every minute), so anticipate 2880 readings a day. Which allows us to get readings for a maximum of 3,202,559,735,019,020 days, or 8,774,136,260,326 years. So no need to worry about filling up the database.

### SQL Table Layout

Table Name		|Column Name		            |Data Type			    |Description
--------------|---------------------------|-------------------|----------------------------------------------
airqualitylog	|datetimestamp			        |Text               |Date Time Stamp
airqualitylog	|r25                        |Integer            |Ratio for PM2.5 (P2 or Pin4) (r25)
airqualitylog	|c25                        |Integer            |Raw Readings of PM2.5 Concentration (PCS per 0.01 cubic foot) (c25)
airqualitylog	|r10                        |Integer            |Ratio for PM1.0 (P1 or Pin2) (r10)
airqualitylog	|c10                        |Integer            |Raw readings of PM1.0 Concentration (PCS  per 0.01 cubic foot) (c10)
airqualitylog	|PM25count                  |Integer            |Concentration Count for Particles Greater than 1µg and Less than 2.5µ (PCS per 0.01 cubic foot) (PM25count = c10 - c25)
airqualitylog	|concentration_ugm3_pm25    |Integer            |SI PM2.5 Concentration (PCS per cubic metre) (concentration_ugm3_pm25)
airqualitylog	|PM10count                  |Integer            |Concentration Count for Particles greater than 2.5 µg (PCS per 0.01 cubic foot) (PM10count = c25)
airqualitylog	|concentration_ugm3_pm10    |Integer            |SI PM10 Concentration (PCS per cubic metre)(concentration_ugm3_pm10)
airqualitylog	|aqiPM25                    |Integer            |US AQI for PM2.5 (Should be average of a 24h reading)
airqualitylog	|aqiPM10                    |Integer            |US AQI for PM10 (Should be average of a 24h reading)


### Creating a New SQL Table

If creating a new SQL table, first make sure you have SQLite3 installed:
```shell
$ sudo apt-get install sqlite3 
```

Run the SQLite3 Command Prompt:
```shell
$ sqlite3 
```

Insert the following lines from "CREATE TABLE..." onward:
```SQL
-- airqualitylog table
CREATE TABLE IF NOT EXISTS airqualitylog (
 datetimestamp text NOT NULL,
 r25 integer NOT NULL,
 c25 integer NOT NULL,
 r10 integer NOT NULL,
 c10 integer NOT NULL,
 PM25count integer NOT NULL,
 concentration_ugm3_pm25 integer NOT NULL,
 PM10count integer NOT NULL,
 concentration_ugm3_pm10 integer NOT NULL,
 aqiPM25 integer NOT NULL,
 aqiPM10 integer NOT NULL
);
```

#### If Importing Data from an Existing CSV file
If importing data from an existing CSV file make sure to delete the header row from the CSV file before importing.

The following commands import the airqualitylog.csv file into the airqualitylog table.

```
sqlite> .mode csv
sqlite> .import /home/pi/airqualitylog.csv airqualitylog
```

#### Exiting SQLite3 Command Prompt
Exit the SQLite3 Command Prompt by pressing "Ctrl-D"
