import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


DEFAULT_ORG_NAME = "freedivers_brisbane"

def org_key(org_name=DEFAULT_ORG_NAME):
    #Constructs a Datastore key for a freediving organisation entity.
    #We use org_name as the key.

    return ndb.Key('Organisation',org_name)

def diverUser_key(userId):
    return ndb.Key('DiverUser',userId)


class DiverUser(ndb.Model):
    #stores info about users
    userId = ndb.StringProperty(indexed=True)
    fruit = ndb.StringProperty(indexed=False)
    isTreasurer = ndb.BooleanProperty(indexed=False)

class MainPage(webapp2.RequestHandler):

    def get(self):
        org_name = self.request.get('org_name',
                                          DEFAULT_ORG_NAME)
        #greetings_query = Greeting.query(
        #    ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
        #greetings = greetings_query.fetch(10)
		
	
        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'isTreasurer':True
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))
	


class Events(webapp2.RequestHandler):

	def get(self):
		self.response.write("EVENTS")
		
		
	
class UserCreate(webapp2.RequestHandler):
    def post(self):
        #capture the form data and save to db
        user = users.get_current_user()
        userId = user.user_id()
        #if user:
        #        userId = user.user_id()
        #else:
        #        self.redirect(users.create_login_url(self.request.uri))
        
        org_name = DEFAULT_ORG_NAME
        newUser = DiverUser(parent=org_key(org_name))
        
        newUser.fruit = self.request.get('fruit')
        newUser.userId = userId
        newUser.put()

        query_params = {'org_name': org_name}
        self.redirect('/?' + urllib.urlencode(query_params))

class UserUpdate(webapp2.RequestHandler):
    def post(self):
        
        googleUser = users.get_current_user()
        userId = googleUser.user_id()
        #userKey = diverUser_key(userId)
        #diverUser = userKey.get()

        #greetings_query = Greeting.query(
        #    ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
        #greetings = greetings_query.fetch(10)

        
        diverUserQuery = DiverUser.gql("WHERE userId = :1", userId)
        diverUser = diverUserQuery.get()
        msg = "not set"
        if diverUser:
            diverUser.fruit = self.request.get('fruit')
            diverUser.put()
            msg = "put"
        else:
            msg = "not put"
        query_params = {'msg': msg}
        self.redirect('/?' + urllib.urlencode(query_params))
    
class Users(webapp2.RequestHandler):

	def get(self):
            name = self.request.get('name')
            reps = int(self.request.get('reps'))
            
            user = users.get_current_user()

            currentUserId = user.user_id()
            
            if user:
                    name = user.nickname()
            else:
                    self.redirect(users.create_login_url(self.request.uri))
            
            template_values = {
                    'name':name,
                    'reps':reps
            }
            template = JINJA_ENVIRONMENT.get_template('users.html')
            self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
        ('/',MainPage),
        ('/events',Events),
        ('/users',Users),
        ('/userCreate',UserCreate),
        ('/userUpdate',UserUpdate)
], debug = True)
