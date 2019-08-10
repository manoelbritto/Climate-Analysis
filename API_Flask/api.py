import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as datetime
from dateutil.parser import parse

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start>/<br>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of all measures based on date (key) and precipt (valaue)"""
    # Query all passengers
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).all()

    # Convert list of tuples into normal list
    #all_names = list(np.ravel(results))
    list_meas = []
    for x in results:
        meas_dic = {}
        meas_dic[x[0]] = x[1]
        list_meas.append(meas_dic)
    return jsonify(list_meas)


@app.route("/api/v1.0/stations")
def station():
    """Return a list of all stations"""
    # Query all passengers
    session = Session(engine)
    results = session.query(Station.station, Station.name,
                            Station.latitude, Station.longitude).all()

    # Convert list of tuples into normal list
    #all_names = list(np.ravel(results))
    list_station = []
    for x in results:
        stat_dic = {}
        stat_dic["station"] = x[0]
        stat_dic["name"] = x[1]
        stat_dic["latitude"] = x[2]
        stat_dic["longitude"] = x[3]
        list_station.append(stat_dic)
    return jsonify(list_station)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of Temperature Observations (tobs) for the previous year."""
    # Query all passengers
    session = Session(engine)

    most_recent_date = session.query(Measurement.date)\
                            .order_by(Measurement.date.desc()).first()
    #days = 30(days) * 12 = 1 year
    month_12_ago = datetime.datetime.strptime(most_recent_date[0], '%Y-%m-%d')-datetime.timedelta(days=30*12) 
    
    result_12_months = session.query(Measurement.tobs, Measurement.date).\
        filter(Measurement.date>=month_12_ago, Measurement.date<=most_recent_date[0]).all()
    # Convert list of tuples into normal list
    #all_names = list(np.ravel(results))
    list_temp = []
    for x in result_12_months:
        temp_dic = {}
        temp_dic["date"] = x[1]
        temp_dic["tobs"] = x[0]
        list_temp.append(temp_dic)
    return jsonify(list_temp)
# @app.route("/api/v1.0/passengers")
# def passengers():
#     """Return a list of passenger data including the name, age, and sex of each passenger"""
#     # Query all passengers
#     session = Session(engine)
#     results = session.query(Passenger.name, Passenger.age, Passenger.sex).all()

#     # Create a dictionary from the row data and append to a list of all_passengers
#     all_passengers = []
#     for name, age, sex in results:
#         passenger_dict = {}
#         passenger_dict["name"] = name
#         passenger_dict["age"] = age
#         passenger_dict["sex"] = sex
#         all_passengers.append(passenger_dict)

#     return jsonify(all_passengers)


if __name__ == '__main__':
    app.run(debug=True)
