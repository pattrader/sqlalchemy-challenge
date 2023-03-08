import sqlalchemy
import numpy as np
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from flask import Flask, jsonify
from sqlalchemy import create_engine, func
import datetime as dt


# Database Setup

engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

#Classes from automap
Base.classes.keys()

#Tables from classes
measurement = Base.classes.measurement
station = Base.classes.station

session = Session(engine)

# Flask Setup
#################################################
app = Flask(__name__)

#Home page
@app.route('/')
def main():
    return (
        f'WELCOME TO YOUR HOME PAGE<br/>'
        f'Below are the avilable routes<br/>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
        f"/api/v1.0/<start><br>"
        f"/api/v1.0/<start>/<end><br>"
    )

#Pulling precipitation data and result in dictionary
@app.route("/api/v1.0/precipitation")
def prcp():
    oneyear = dt.date(2017,8,23)- dt.timedelta(days=365)
    prcp_d = session.query(measurement.date, measurement.prcp).filter(measurement.date >= oneyear).order_by(measurement.date).all()
    prcp_dict = dict(prcp_d)
    session.close()
    return jsonify(prcp_dict)

#Pulling station data and result in list
@app.route("/api/v1.0/stations")
def station():
    Station = session.query(measurement.station, func.count(measurement.station)).group_by(measurement.station).order_by(func.count(measurement.station).desc()).all()
    session.close()
    station = list(np.ravel(Station))
    return jsonify(list(station))

#Pulling temprature and result in list
@app.route("/api/v1.0/tobs")
def tobs():
    oneyear = dt.date(2017,8,23)- dt.timedelta(days=365)
    max = session.query(measurement.station, measurement.tobs).filter(measurement.date >= oneyear).filter(measurement.station == 'USC00519281').all()

    tobs_list = list(np.ravel(max))
    session.close()
    return jsonify(tobs_list)

#Creating function to calculate min, avg and max with dynamic start and finish
@app.route("/api/v1.0/<start>")
def start(start):
    result = session.query(func.min(measurement.tobs), func.avg(measurement.tobs),func.max(measurement.tobs)).filter(measurement.date >= start).all()
    
    session.close()
    data = []

    for min,avg,max in result:
        data_d = {}
        data_d["Min"] = min
        data_d["Average"] = avg
        data_d["Max"] = max
        data.append(data_d)
        
    return jsonify(data)

@app.route('/api/v1.0/<start>/<end>')
def start_end(start,end):
    queryresult = session.query(func.min(measurement.tobs), func.avg(measurement.tobs),func.max(measurement.tobs)).filter(measurement.date >= start).filter(measurement.date <= end).all()

   
    session.close()
    data = []
    for min,avg,max in queryresult:
        data_d = {}
        data_d["Min"] = min
        data_d["Average"] = avg
        data_d["Max"] = max
        data.append(data_d)

    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)



