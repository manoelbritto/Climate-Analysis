# Project: Climate-Analysis
This project uses SQLAlchemy and API with Flask to:
1. Extract data from SQLite database
1. Plot results using data analytics tools
1. Expose data in JSON format to be viewed by external developers


## Getting started:
To run this code is necessary to have some libraries installed on your machine:<br>
**Anaconda:**<br>
https://www.anaconda.com/distribution/<br>

**Libraries:**
```
pip install pandas
pip install flask
```

**Execute the program:** <br>
python app.py<br>

## Implementaton: 

There are two parts to this project. The first one is Climate Analysis and Exploration. Also, the second one exposes the database content using API with Flask

**1. First part:** Climate Analysis and Exploration
Import SQLite:
```Python
# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

engine = create_engine("sqlite:///Resources/hawaii.sqlite")


```

This code mapping automatically the tables and columns inside the SQLite:

```Python
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
```

```Python
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
```

```Python
session = Session(engine)
```
Instead, to create an SQL statement, it is possible to use SQLAlchemy which abstract the way to do queries in any database. 


```Python
most_active = session.query(Measurement.station, func.count(Measurement.station)).\
                            group_by(Measurement.station).\
                            order_by(func.count(Measurement.station).desc()).all()
```

Using matplotib is possible to plot results, for instance, this one shows the preciptation in 12 months<br>
![plot](Images/precipitation.png)

To see more analysis, go to Jupyter notebook python code, or just click [here](climate_starter.ipynb)

**2. Second part:** Climate App<br>
design a Flask API based on the queries

## Routes

To see this developement using Flask, click [here](API_Flask/app.py)
```
/
```
*Home page.<br>
List all routes that are available.

![page](Images/initial_page.PNG)
```
/api/v1.0/precipitation
```
![page](Images/api_precipitation.PNG)

Convert the query results to a Dictionary using a date as the key and precipitation as the value.
Return the JSON representation of your dictionary.

```
/api/v1.0/stations
```
Return a JSON list of stations from the dataset.

![page](Images/api_stations.PNG)

```
/api/v1.0/tobs
```
![page](Images/api_tobs.PNG)

The query for the dates and temperature observations from a year from the last data point, it returns a JSON list of Temperature Observations (tobs) for the previous year.

```
/api/v1.0/<start>
```  
![page](Images/api_start.PNG)
  
```
/api/v1.0/<start>/<end>
```
![page](Images/start_end.PNG)

Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

# Features:
* Python with:
  * Sqlalchemy
  * Flask
  * Matplotlib
