from time import localtime, strftime, time

from flask import Flask
from flask import render_template
import requests
import xml.etree.ElementTree as ET

app = Flask(__name__)

lastupdated = 0
_tree = None
def parseXML():
    global lastupdated
    global _tree
    print "{} {}".format(lastupdated, _tree)
    if time() - 30 > lastupdated:
        response = requests.get('https://tfl.gov.uk/tfl/syndication/feeds/cycle-hire/livecyclehireupdates.xml')
        xmldata = response.text
        _tree = ET.fromstring(xmldata)
        lastupdated = time()
    return (_tree,lastupdated)

@app.route('/')
def page():
    (tree, lastupdated) = parseXML()
    results = [ parse(item) for item in tree if detect(item) ]
    now = strftime("%a %H:%M:%S %Z", localtime(lastupdated))
    data = {
            "stations": results,
            "now": now
            }
    return render_template('bikes.html', data = data)

targets = { "154","361","374", "32" }

def detect(item):
    return item.find("id").text in targets

def parse(item):
    name = item.find("name").text
    bikes = item.find("nbBikes").text
    docks = item.find("nbDocks").text
    return { "name": name, 
             "bikes": bikes,
             "docks": docks }

