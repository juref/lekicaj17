#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import jinja2
import webapp2


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("index.html")

    def post(self):
        number = int(self.request.get("number"))
        convert = self.request.get("convert")
        display = 0
        km_2_mi = number * 0.621371192
        mi_2_km = number * 1.609344

        if convert == "km_2_mi":
            display = km_2_mi
        elif convert == "mi_2_km":
            display = mi_2_km

        params = {"number": number,
            "display": display,
            "convert": convert,
            }

        return self.render_template("message.html", params=params)


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
], debug=True)

