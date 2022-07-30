# Importing the required libraries
from flask import Flask, render_template, Response, request
import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from PIL import Image

#Stops flask from dying whenever a graph is generated
matplotlib.use('Agg')

#Reading .csv file
df = pd.read_csv('HIV_Data.csv')

#Cleaning data
df.dropna(inplace = True)

countrylist = df['Country'].values.tolist()

def getIndexes(dfObj, value):

    listOfPos = []

    result = dfObj.isin([value])

    seriesObj = result.any()

    columnNames = list(seriesObj[seriesObj == True].index)

    for col in columnNames:
        rows = list(result[col][result[col] == True].index)
 
        for row in rows:
            listOfPos.append((row, col))

    return listOfPos

#Initiating app
app = Flask(__name__)

#Defining home page function
@app.route("/", methods = ['GET', 'POST'])
def home():
    return render_template('home.html')

#Defining bar graph input function
@app.route("/bar-graph-input")
def bargraph_input():
    return render_template('bar-graph-input.html', name = 'bargraph_input', bar_url ='static/images/bargraph.png', countrylist=countrylist)

#Defining bar graph function
@app.route("/bar-graph", methods = ['GET', 'POST'])
def bargraph():
    plt.cla()
    plt.clf()
    df['Reported number of people receiving ART'] = pd.to_numeric(df['Reported number of people receiving ART'])
    plt.bar(df['Country'].tail(5),df['Reported number of people receiving ART'].tail(5))
    plt.savefig('static/images/bargraph.png')
    image = Image.open('static/images/bargraph.png')
    image = image.resize((1000,1000))
    image.save('static/images/bargraph.png')
    return render_template('bar-graph.html', name = 'bargraph', bar_url ='static/images/bargraph.png')

#Defining scatter graph function
@app.route("/scatter-graph", methods = ['GET', 'POST'])
def scattergraph():
    plt.cla()
    plt.clf()
    df['Reported number of people receiving ART'] = pd.to_numeric(df['Reported number of people receiving ART'])
    a, b = np.polyfit(df['Reported number of people receiving ART'].head(20), df['Estimated number of people living with HIV_median'].head(20), 1)
    plt.scatter(df['Reported number of people receiving ART'].head(20), df['Estimated number of people living with HIV_median'].head(20))
    plt.plot(df['Reported number of people receiving ART'].head(20), a*df['Reported number of people receiving ART'].head(20)+b)
    plt.xlabel('Reported number of people receiving ART')
    plt.ylabel('Median number of people living with HIV')
    plt.savefig('static/images/scattergraph.png')
    image = Image.open('static/images/scattergraph.png')
    image = image.resize((1000,1000))
    image.save('static/images/scattergraph.png')
    return render_template('scatter-graph.html', name = 'scattergraph', scatter_url ='static/images/scattergraph.png')

#defining action for the bar graph
@app.route("/bar-graph-action", methods = ['GET', 'POST'])
def bar_graph_action():
    plt.cla()
    plt.clf()
    #print(request.form['bar-graph-input'])
    country1 = request.form.get("country1")
    country2 = request.form.get("country2")
    country3 = request.form.get("country3")
    country4 = request.form.get("country4")
    country5 = request.form.get("country5")
    print(country1)
    xaxis = np.array([country1, country2, country3, country4, country5])
    list1 = getIndexes(df,country1)
    list2 = getIndexes(df,country2)
    list3 = getIndexes(df,country3)
    list4 = getIndexes(df,country4)
    list5 = getIndexes(df,country5)
    print(list1[0][0])
    loc1 = int(list1[0][0])
    loc2 = int(list2[0][0])
    loc3 = int(list3[0][0])
    loc4 = int(list4[0][0])
    loc5 = int(list5[0][0])

    yaxis = [int(df.iat[loc1,'Reported number of people receiving ART']),int(df.iat[loc2,'Reported number of people receiving ART']),int(df.iat[loc3,'Reported number of people receiving ART']),int(df.iat[loc4,'Reported number of people receiving ART']),int(df.iat[loc5,'Reported number of people receiving ART'])]
    yaxis.append(df.iat[loc1,'Reported number of people receiving ART'])
    print(loc1)
    plt.bar(xaxis, yaxis)

    plt.savefig('static/images/bargraph.png')
    image = Image.open('static/images/bargraph.png')
    image = image.resize((1000,1000))
    image.save('static/images/bargraph.png')
    return render_template('bar-graph.html', name = 'bargraph', bar_url ='static/images/bargraph.png')
    

#Running flask server
if __name__ == "__main__":
    app.run(debug=True)