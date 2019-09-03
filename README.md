# Climate-Analysis
Python: SQLAlchemy and Flask (API)

Import SQLite:
```Python
# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func,inspect

engine = create_engine("sqlite:///Resources/hawaii.sqlite")


```

This code mapping automaticaly the tables and columns inside the SQLite:
```
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
Instead to create sql statement, it is possible to use SQLAlchemy which abstract the way to do queries in any kind of database. 


```Python
most_active = session.query(Measurement.station, func.count(Measurement.station)).\
                            group_by(Measurement.station).\
                            order_by(func.count(Measurement.station).desc()).all()
```

Using matplotib is possible to plot results, for instance, this one shows the preciptation in 12 months<br>
![plot](Images/precipitation.png)

To see more analysis, go to jupyter notebook python code, or just click [here](climate_starter.ipynb)
