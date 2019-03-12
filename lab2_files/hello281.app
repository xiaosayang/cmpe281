import webapp2

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, Welcome to my homepage for CMPE281 lab2!')

app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
