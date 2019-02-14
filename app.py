
##Alice Surfs Up App
app = Flask(__name__)
@app.route("/")
def home():
  usage = """/api/v1.0/precipitation for precipitation data <br>
        /api/v1.0/stations for stations data <br>
        /api/v1.0/tobs for last years' temperature data <br>
        /api/v1.0/date?start=YYYY-MM-DD for stats from that date forward <br>
        /api/v1.0/date?start=YYYY-MM-DD&end=YYYY-MM-DD for stats between those dates"""
​
  return usage
​
@app.route("/api/v1.0/precipitation")
def precipitation():
​
  engine = create_engine("sqlite:///Resources/hawaii.sqlite") 
​
  prcp_last_year = text("""SELECT * FROM MEASUREMENT \
              WHERE DATE BETWEEN '2016-08-23' and '2017-08-23'""")
​
  prcp_last_year_df = pd.read_sql(prcp_last_year, engine)
​
  prcp_last_year_df["date"] = pd.to_datetime(prcp_last_year_df["date"])
  
  json_data = prcp_last_year_df[["date","prcp"]].to_json(orient ="records")
​
  return json_data
  
​
@app.route("/api/v1.0/stations")
def stations():
  
  engine = create_engine("sqlite:///Resources/hawaii.sqlite") 
​
  active = text("""SELECT * FROM MEASUREMENT""")
​
  df = pd.read_sql(active, engine).groupby("station")["id"].count().sort_values(ascending=False).reset_index()
​
  df = df.rename(columns={"id":"count"})
​
  json_data = df.to_json(orient="records")
​
  return json_data
​
@app.route("/api/v1.0/tobs")
def tobs():
​
  engine = create_engine("sqlite:///Resources/hawaii.sqlite")
​
  hist = text("""SELECT STATION, TOBS, DATE FROM MEASUREMENT \
        WHERE DATE BETWEEN '2016-08-23' and '2017-08-23'""")
​
  df = pd.read_sql(hist, engine)
​
  json_data = df.to_json(orient="records")
​
  return json_data
​
  
@app.route("/api/v1.0/date")
def start():
  start_date_key = request.args.get('start')
  start_date = '''{}'''.format(start_date_key)
​
  end_date_key = request.args.get('end')
  end_date = '''{}'''.format(end_date_key)
  
  engine = create_engine("sqlite:///Resources/hawaii.sqlite")
​
  if end_date is not None:
    temp = text(f"""SELECT STATION, TOBS FROM MEASUREMENT \
      WHERE DATE BETWEEN '{start_date}' AND '{end_date}'""") 
​
  else:
    temp = text(f"""SELECT STATION, TOBS FROM MEASUREMENT \
        WHERE DATE >= '{start_date}'""")
​
  temp_df = pd.read_sql(temp, engine)
​
  max_temp = temp_df["tobs"].max()
​
  min_temp = temp_df["tobs"].min()
​
  mean_temp = temp_df["tobs"].mean()
​
  df = pd.Series({"Max Temp": max_temp,
      "Min Temp": min_temp,
      "Mean Temp": mean_temp,   
      })
​
  json_data = df.to_json()
  
  return json_data
  
if __name__ == "__main__":
  app.run()



