#!/usr/bin/env python
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
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("kalkulator.html")

class BlogHandler(BaseHandler):
    def post(self):
        first_num = self.request.get("first_num")
        second_num = self.request.get("second_num")
        sum = float(first_num) + float(second_num)


        dodatne_stvari = {
            "sporocilo": "resultat je:",
            "tisto_kar_sem_vnesel_plus_nekaj": str(first_num) +  " + " + str(second_num) + " = " + str(int(sum))
        }

        return self.render_template("kalkulator.html", params=dodatne_stvari)

    def get(self):
        dodatne_stvari = {
            "ime": "Janez",
            # "priimek": "Novak"
        }

        return self.render_template("kalkulator.html", params=dodatne_stvari)

class FakebookHandler(BaseHandler):
    def get(self):
        return self.render_template("fakebook1.html")

app = webapp2.WSGIApplication([
    # webapp2.Route('/', MainHandler),
    webapp2.Route('/', BlogHandler),
    # webapp2.Route('/fakebook', FakebookHandler),

], debug=True)