__author__ = 'itamar'
import webapp2
from google.appengine.ext.webapp import template


class HomepageHandler(webapp2.RequestHandler):
    def get(self):
        html = template.render("web/html/Kazrin.html",1)
        self.response.write(html)

        # self.post(html)

    # def post(self, page):
    #     self.response.write(page)

page = webapp2.WSGIApplication([
    ('/', HomepageHandler)
], debug=True)