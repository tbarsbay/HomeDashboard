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
route10Name = "10-Townsend"
route19Name = "19-Polk"
route48Name = "48-Quintara 24th Street"

trelloApiKey = "5c8418656e2cf0ff016be1ef98fee2ae"
trelloPersonalBoardId = "ayldRlvY"
trelloListId = "55e5140b0ab26cbcb8ed4e67"
trelloToken = "10e0945667de140dc0681e748bf52d253c549704e8290901982e7f7c1e1d53de"
trelloBoardFields = "name"
trelloCardFields = "name,labels,due,idChecklists"
trelloBaseListsUrl = "https://api.trello.com/1/lists/"
trelloFullUrl = trelloBaseListsUrl + trelloListId + "?fields=" + trelloBoardFields + "&cards=open" + "&card_fields=" + trelloCardFields + "&key=" + trelloApiKey + "&token=" + trelloToken

class MainHandler(webapp2.RequestHandler):
    def get(self):
        values = {}
        self.response.out.write(template.render("index.html", values))

    def post(self):
        customMessage = self.request.get('customMessage')
        values = {'customMessage': customMessage}
        self.response.out.write(template.render("index.html", values))

class WeatherHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write(getCurrentAtlantaWeatherJson())

class TrelloHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write(getTrelloListJson())

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    # ('/arrivals', ArrivalsHandler),
    ('/weather', WeatherHandler),
    ('/trello', TrelloHandler)
], debug=True)

def getCurrentAtlantaWeatherJson():
    url = "http://api.openweathermap.org/data/2.5/weather?id=4180439&APPID=7a7167bed31c6a147d7dd7de26c20fe8"
    return urllib2.urlopen(url).read()

def getTrelloListJson():
    return urllib2.urlopen(trelloFullUrl).read()
