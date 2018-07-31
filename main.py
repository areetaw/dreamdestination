import webapp2
import jinja2
import os
import sys
import logging
import time
from google.appengine.api import urlfetch
import json

from google.appengine.api import users
from google.appengine.ext import ndb

API_KEY = "650c77ad9e074e7c91aa8cdf38ee54e1"

env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=["jinja2.ext.autoescape"],
    autoescape=True)

locations = {
    231 : "Moscow, Russia",
    1210 : "Chicago, USA",
    2232 : "Beijing, China",
    3001 : "Sunnyvale, USA",
}

starting_point = "San Francisco, USA"

class User(ndb.Model):
    name = ndb.StringProperty()
    weather = ndb.IntegerProperty()
    transportation = ndb.StringProperty()
    cost = ndb.IntegerProperty()
    numOfPeople = ndb.IntegerProperty()

class HomePage(webapp2.RequestHandler):
    def get(self):
        template = env.get_template("templates/home.html")
        self.response.write(template.render())

class QuestionsPage(webapp2.RequestHandler):
    def post(self):
        template = env.get_template("templates/questions.html")
        self.response.write(template.render())

class Blog(webapp2.RequestHandler):
    def get(self):
        template = env.get_template("templates/blog.html")
        self.response.write(template.render())

class About(webapp2.RequestHandler):
    def get(self):
        template = env.get_template("templates/about.html")
        self.response.write(template.render())

class News(webapp2.RequestHandler):
    def get(self):
        template = env.get_template("templates/news.html")
        url = "https://newsapi.org/v2/everything?q=travel&apiKey=650c77ad9e074e7c91aa8cdf38ee54e1"
        response = urlfetch.fetch(url)  #gets the content of the api
        json_result = json.loads(response.content)  #loads the contents of api as a json object
        articles = json_result["articles"]
        photos = json_result["articles"["urlToImage"]]
        for photo in photos:
            if photo.status_code == 200:
                self.response.write(photo.content)
            else:
                urlToImage = ""
        templateVars = {
            "articles": articles,
        }
        self.response.write(template.render(templateVars))


class Contact(webapp2.RequestHandler):
    def get(self):
        template = env.get_template("templates/contact.html")

        self.response.write(template.render())

class ResultsPage(webapp2.RequestHandler):
    def get(self):
        template = env.get_template("templates/results.html")
        self.response.write(template.render())
    def post(self):
        template = env.get_template("templates/results.html")
        weather = self.request.get("question1")
        transportation = self.request.get("question2")
        cost = self.request.get("question3")
        numOfPeople = self.request.get("question4")


        location_string = weather + transportation + cost + numOfPeople
        location_number = int(location_string)

        result_of_city = 0
        min_diff = sys.maxint
        min_city = ""

        for cities in locations:
            city_sum = 0
            for num in range(4):
                copy_cities = cities
                last_num = location_number % 10
                location_number /= 10
                last_num_in_city = copy_cities % 10
                copy_cities /= 10
                final_location_num = abs(last_num - last_num_in_city)
                city_sum += final_location_num
        if city_sum < min_diff:
            min_diff = city_sum
            min_city = cities
            dreamLocation = locations[min_city]


        templateVars = {
            "weather": weather,
            "transportation": transportation,
            "cost": cost,
            "numOfPeople": numOfPeople,
            "dreamLocation": dreamLocation,
        }
        self.response.write(template.render(templateVars))

app = webapp2.WSGIApplication([
    ("/", HomePage),
    ("/questions", QuestionsPage),
    ("/results", ResultsPage),
    ("/blog", Blog),
    ("/about", About),
    ("/news", News),
    ("/contact", Contact),
], debug=True)
