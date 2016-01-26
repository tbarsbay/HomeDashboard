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
        route19 = buildRouteArrivalsObject(route19Name)
        route48 = buildRouteArrivalsObject(route48Name)
        values = {}
        if route19 and route48:
            values['route1Name'] = route19.name
            values['route1Dir'] = route19.direction
            values['route1StopName'] = route19.stopName
            values['route1Arrivals'] = route19.arrivals

            values['route2Name'] = route48.name
            values['route2Dir'] = route48.direction
            values['route2StopName'] = route48.stopName
            values['route2Arrivals'] = route48.arrivals

            values['messageText'] = "Hope you have a great day at work! Don't forget your lunch!"
            values['messageSenderName'] = "Tamer"
            values['messageTimestamp'] = "7:26am"
        self.response.out.write(template.render("index.html", values))

    def post(self):
        customMessage = self.request.get('customMessage')
        values = {'customMessage': customMessage}
        self.response.out.write(template.render("index.html", values))

class RouteArrivals:
    name = ""
    direction = ""
    stopName = ""
    arrivals = ""

    def __init__(self, name, direction, stopName, arrivals):
        self.name = name
        self.direction = direction
        self.stopName = stopName
        self.arrivals = arrivals

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/dashboard', DashboardHandler)
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

def buildRouteArrivalsObject(selectedRoute):
    routeXml = getRouteXml(selectedRoute)
    routeName = routeXml.getAttribute('Name')
    routeName = routeName[:routeName.index('-')]
    routeDir = routeXml.getElementsByTagName('RouteDirection')[0].getAttribute('Name')
    stopName = routeXml.getElementsByTagName('Stop')[0].getAttribute('name')
    arrivals = [str(arrivalTime.childNodes[0].nodeValue) + "m" for arrivalTime in routeXml.getElementsByTagName("DepartureTime")]
    arrivals = ", ".join(arrivals)
    return RouteArrivals(routeName, routeDir, stopName, arrivals)

def buildMuniArrivalsEndpoint(stopCode):
    return "http://services.my511.org/Transit2.0/GetNextDeparturesByStopCode.aspx?token=" + muniAuthToken + "&stopcode=" + stopCode