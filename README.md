# dublin-bikes-timeseries-analysis
Clustering of Dublin Bikes stations based on their average weekday usage.

dublin-bikes-time-series-clustering-and-mapping.ipynb is self explanatory - a Python 3 notebook for data ETL, analysis and visualisation.

scraper.py accesses the Dublin bikes API and weather.com's API (using the library pywapi) and was run as a cronjob.

Dataset comprises of bike station and weather observations at 2 minute intervals from January 2017 - August 2017. There is also a complete set of station Lat/Lons saved in station_locations.csv. 

Full dataset of daily Dublin Bikes usage data and weather data is contained in data.tar.gz and some uncompressed files are in example_data/
