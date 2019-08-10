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

    # Convert list to json
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

    # Convert list to json
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
    # days = 30(days) * 12 = 1 year
    month_12_ago = datetime.datetime.strptime(
        most_recent_date[0], '%Y-%m-%d')-datetime.timedelta(days=30*12)

    result_12_months = session.query(Measurement.tobs, Measurement.date).\
        filter(Measurement.date >= month_12_ago,
               Measurement.date <= most_recent_date[0]).all()
    # Convert list of tuples into normal list
    #all_names = list(np.ravel(results))
    list_temp = []
    for x in result_12_months:
        temp_dic = {}
        temp_dic["date"] = x[1]
        temp_dic["tobs"] = x[0]
        list_temp.append(temp_dic)
    return jsonify(list_temp)


@app.route("/api/v1.0/<start>")
def start(start):
    """Return a list of all measure greater than start"""
    # Query all passengers
    session = Session(engine)
    try:
        results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).all()

    # Convert list to json
        list_meas = []
        for x in results:
            stat_dic = {}
            stat_dic["min"] = x[0]
            stat_dic["avg"] = x[1]
            stat_dic["max"] = x[2]
            list_meas.append(stat_dic)

        return jsonify(list_meas)
    except:
        return jsonify({"error": f"not found."}), 404


@app.route("/api/v1.0/<start>/<end>")
def startEnd(start, end):
    """Return a list of all measure greater than start and less than end date"""
    # Query all passengers
    session = Session(engine)
    try:
        results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start, Measurement.date <= end).all()

    # Convert list of tuples into normal list
    #all_names = list(np.ravel(results))
        list_meas = []
        for x in results:
            stat_dic = {}
            stat_dic["min"] = x[0]
            stat_dic["avg"] = x[1]
            stat_dic["max"] = x[2]

            list_meas.append(stat_dic)

        return jsonify(list_meas)
    except:
        return jsonify({"error": f"not found."}), 404


if __name__ == '__main__':
    app.run(debug=True)
