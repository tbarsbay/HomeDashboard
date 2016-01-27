#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import urllib2
import json
from xml.dom import minidom
from google.appengine.ext.webapp import template

muniAuthToken = "4eaad5aa-05b7-477e-b75b-c57e78c89d57"
route19Name = "19-Polk"
route19ShortName = "19"
route48Name = "48-Quintara 24th Street"
route48ShortName = "48"

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')

class DashboardHandler(webapp2.RequestHandler):
    def get(self):
        values = {}
        self.response.out.write(template.render("index.html", values))

    def post(self):
        customMessage = self.request.get('customMessage')
        values = {'customMessage': customMessage}
        self.response.out.write(template.render("index.html", values))

class ArrivalsHandler(webapp2.RequestHandler):
    def get(self):
        # make it so that get request takes in params for all the routes wanted, and then builds response from there
        route19json = buildRouteArrivalsJson(route19Name)
        route48json = buildRouteArrivalsJson(route48Name)
        response = []
        response.append(route19json)
        response.append(route48json)
        self.response.out.write(json.dumps(response))

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/dashboard', DashboardHandler),
    ('/arrivals', ArrivalsHandler)
], debug=True)

def getArrivalTimes(route):
    selectedRouteXml = getRouteXml(route)
    if (selectedRouteXml):
        # Found the xml for our specified route
        arrivalTimesXml = selectedRouteXml.getElementsByTagName("DepartureTime")
        arrivalTimes = [str(arrivalTime.childNodes[0].nodeValue) for arrivalTime in arrivalTimesXml]
        return arrivalTimes

def getBaseXml():
    url = buildMuniArrivalsEndpoint("16199") #TODO need to parametrize stopCode
    return minidom.parse(urllib2.urlopen(url))

def getRouteXml(selectedRoute):
    allRoutesXml = getBaseXml().getElementsByTagName("Route")
    for route in allRoutesXml:
        if route.getAttribute('Name') == selectedRoute:
            return route

def buildRouteArrivalsJson(selectedRoute):
    routeXml = getRouteXml(selectedRoute)
    routeName = routeXml.getAttribute('Name')
    routeName = routeName[:routeName.index('-')]
    routeDir = routeXml.getElementsByTagName('RouteDirection')[0].getAttribute('Name')
    stopName = routeXml.getElementsByTagName('Stop')[0].getAttribute('name')
    arrivals = [str(arrivalTime.childNodes[0].nodeValue) + "m" for arrivalTime in routeXml.getElementsByTagName("DepartureTime")]
    arrivals = ", ".join(arrivals)
    return {
        'routeName': str(routeName),
        'routeDirection': str(routeDir),
        'stopName': str(stopName),
        'arrivals': str(arrivals)
    }

def buildMuniArrivalsEndpoint(stopCode):
    return "http://services.my511.org/Transit2.0/GetNextDeparturesByStopCode.aspx?token=" + muniAuthToken + "&stopcode=" + stopCode