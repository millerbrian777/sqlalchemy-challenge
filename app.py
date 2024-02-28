# Import the dependencies.
import numpy as np
import datetime as dt

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask,jsonify






#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
M = Base.classes.measurement
S = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)





#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    return(
        f"Welcome to Hawaii Analysis<br/>"
        f"Available Route:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stattions<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
        f"<p>'start' and 'end' date should be in the format MMDDYYYY<br/>"


    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the precipitation for the last year"""
    prev_year = dt.date(2017, 8,23) - dt.timedelta(days=365)
    precipitation = session.query(M.date,M.prcp).\
        filter(M.date>= prev_year).all()
    session.close()

    precip = {date:prcp for date, prcp in precipitation}
    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(S.station).all()
    session.close()
    stations = list(np.ravel(results))
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    prev_year = dt.date(2017, 8,23) - dt.timedelta(days=365)

    results= session.query(M.tobs).\
        filter(M.station == 'USC00519281').\
        filter(M.date >= prev_year).all()
    session.close()

    temps = list(np.ravel(results))

    return jsonify(temps=temps)


@app.route ("/api/v1.0/temp<start>")
@app.route ("/api/v1.0/temp<start>/<end>")
def stats(start,end=None):

    sel=[func.min(M.tobs),func.max(M.tobs), func.avg(M.tobs)]
    start = dt.datetime.strptime(start,"%m%d%Y")

    if end == None:
        results = session.query(*sel).\
            filter(M.date>= start).all()

        session.close()
        temps = list(np.ravel(results))
        return jsonify(temps)
    
    end = dt.datetime.strptime(start,"%m%d%Y")

    results = session.query(*sel).\
    filter(M.date>= start).\
    filter(M.date<= end).all()

    session.close()
    temps = list(np.ravel(results))
    return jsonify(temps)





if __name__ == '__main__':
    app.run()