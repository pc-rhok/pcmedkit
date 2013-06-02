import cgi
import os
import webapp2
from datetime import datetime
from google.appengine.api import search
from google.appengine.api import users
import models
import render

import jinja2


class main(webapp2.RequestHandler):
    def get(self):
        template_values = {
            'position': 'Peace Corps Volunteer',
            'verb': 'extremely enjoy'
        }
        html = render.page(self, "templates/siteadmin/home.html",template_values)
        self.response.out.write(html)

class form(webapp2.RequestHandler):
    def get(self):
        template_values = {
            'position': 'Peace Corps Volunteer',
            'verb': 'extremely enjoy'
        }
        html = render.page(self, "templates/siteadmin/medbox_form.html",template_values)
        self.response.out.write(html)

class boxform(webapp2.RequestHandler):
    def get(self):
        template_values = {
            'position': 'Medical Officer',
            'verb': 'extremely enjoy'
        }
        html = render.page(self, "templates/siteadmin/postsupplyform.html",template_values)
        self.response.out.write(html)