# link database to use date and time
import datetime
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.api import events

#users
class users(db.Model):
	
	# general info
	fname = db.StringProperty(Required=True)
	sname = db.StringProperty(Required=True)
	password = db.StringProperty(Required=True)
	role = db.StringProperty(Required=True,
																												choices=set(["treasurer","eventManager","user"]))
	email = db.StringProperty(Required=True)
	photo = db.blob(default=None)
	credit = db.IntegerProperty(default=0)
	registrationDate = DateProperty()
						
	# emergancy contact
	emergencyName = db.StringProperty(Required=True)
	emergencyEmail = db.StringProperty(Required=True)

#events
class events(db.Model):
	
	# general info
	eventName = db.StringProperty(Required=True)
	date = DateProperty()
	location = PostalAddress()
	description = db.Text()
