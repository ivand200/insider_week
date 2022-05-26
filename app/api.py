import json

from .main import app
from flask import jsonify, request, render_template

from database.models import Asset, db

import gspread
from .creds import credentials
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px

@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/sheet/", methods=["GET"])
def test_table():
    """
    Update data from google sheet
    """
    gc = gspread.service_account_from_dict(credentials)
    sh = gc.open("Asset")
    worksheet = sh.sheet1
    dataframe = pd.DataFrame(worksheet.get_all_records())
    dataframe.columns = ["ticker", "date", "open", "high", "low", "close"]
    dataframe.to_sql("asset", con=db.engine, if_exists="replace", index=False)
    print(dataframe)
    return jsonify({"status": "ok"})


@app.route("/sheet/candles/", methods=["GET"])
def candle_grapth():
    """
    Chart with candles
    all time
    """
    data = pd.read_sql("SELECT ticker, date, open, high, low, close FROM asset", con=db.engine, parse_dates=["date"])
    fig = go.Figure(data=go.Candlestick(x=data["date"], open=data["open"], high=data["high"], low=data["low"], close=data["close"]))
    fig.update_layout(xaxis_rangeslider_visible=False)
    fig.write_html("app/templates/candles.html")
    return render_template("candles.html")


# @app.route("/sheet/line/", methods=["GET"])
# def line_grapth():
#     data = pd.read_sql("SELECT ticker, date, open, high, low, close FROM asset", con=db.engine, parse_dates=["date"])
#     fig = go.Figure([go.Scatter(x=data["date"], y=data["close"])])
#     fig.show()
#     return "Line chart"


@app.route("/sheet/times/", methods=["GET"])
def times_chart():
    """
    Chart with time series choice
    1m, YTD, 1y, all
    """
    data = pd.read_sql("SELECT ticker, date, open, high, low, close FROM asset", con=db.engine, parse_dates=["date"])
    fig = px.line(data, x="date", y="close", title="Time series chart")
    fig.update_xaxes(rangeslider_visible=True, rangeselector=dict(buttons=list([
        dict(count=1, label="1m", step="month", stepmode="backward"),
        dict(count=1, label="YTD", step="year", stepmode="todate"),
        dict(count=1, label="1y", step="year", stepmode="backward"),
        dict(step="all")
    ]))
    )
    fig.write_html("app/templates/times_series.html")
    return render_template("times_series.html")