from flask import Flask, render_template, send_file, make_response
from coronaIndia import totalWorld, top20World, table, top20, datewise, ageWise, total
from flask import *
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import folium
import io
import random
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

app = Flask(__name__)


@app.route('/')
def show_tables():
    
    totalWorld1 = totalWorld()
    top20Worldfig = top20World()
    tableDisplay = table()
    top20fig = top20()
    dateWise = datewise()
    ageWiseDate = ageWise()
    totals=total()
    return render_template("index.html", total_WorldData=totalWorld1, top20Worldlist = top20Worldfig, returnList = tableDisplay, top20list=top20fig, dateWiseData=dateWise,
                    ageWiseData=ageWiseDate, total_data=totals)
    

if __name__ == "__main__":
    app.jinja_env.cache = {}
    app.run(debug=True)