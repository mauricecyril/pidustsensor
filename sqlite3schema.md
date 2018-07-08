Max Rows in SQLITE3 = 9,223,372,036,854,775,807
There are 1440 Minutes in a 24 hour day
The GROVE / Shinyei PPD42NS dust sensor gets a reading every 30 seconds (2 readings every minute), so anticipate 2880 readings a day. Which allows us to get readings for a maximum of 3,202,559,735,019,020 days, or 8,774,136,260,326 years.



Table			|Column Name		|Data Type			|Description
----------------|-------------------|-------------------|-------------------
airqualitylog	|timestamp			|Text
airqualitylog	|
airqualitylog	|
airqualitylog	|
airqualitylog	|
airqualitylog	|
airqualitylog	|
airqualitylog	|
airqualitylog	|
airqualitylog	|
airqualitylog	|
airqualitylog	|

	'Date Time Stamp',
'Ratio for PM2.5 (P2 or Pin4) (r25)',
'Raw Readings of PM2.5 Concentration (PCS per 0.01 cubic foot) (c25)',
'Ratio for PM1.0 (P1 or Pin2) (r10)',
'Raw readings of PM1.0 Concentration (PCS  per 0.01 cubic foot) (c10)',
'Concentration Count for Particles Greater than 1µg and Less than 2.5µ (PCS per 0.01 cubic foot) (PM25count = c10 - c25)',
'SI PM2.5 Concentration (PCS per cubic metre) (concentration_ugm3_pm25)',
'Concentration Count for Particles greater than 2.5 µg (PCS per 0.01 cubic foot) (PM10count = c25)',
'SI PM10 Concentration (PCS per cubic metre)(concentration_ugm3_pm10)',
'US AQI for PM2.5 (Should be average of a 24h reading)',
'US AQI for PM10 (Should be average of a 24h reading)'


timestamp, r25, int(c25), r10, int(c10), int(PM25count), int(concentration_ugm3_pm25), int(PM10count), int(concentration_ugm3_pm10), int(aqiPM25), int(aqiPM10)
CREATE TABLE IF NOT EXISTS projects (
 id integer PRIMARY KEY,
 name text NOT NULL,
 begin_date text,
 end_date text
);
