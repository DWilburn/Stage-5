
import os
import urllib


from google.appengine.api import users
from google.appengine.ext import ndb


import jinja2
import webapp2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)


default_guestbook_name = 'default_guestbook'

error =""

def guestbook_key(guestbook_name=default_guestbook_name):
    return ndb.Key('Guestbook', guestbook_name)

class Author(ndb.Model):
    """Sub model for representing an author."""
    identity = ndb.StringProperty(indexed=False)
    email = ndb.StringProperty(indexed=False)


class Greeting(ndb.Model):
    """A main model for representing an individual Guestbook entry."""
    title = ndb.StringProperty(indexed = False)
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)



class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class MainPage(Handler):
    def get(self):

        lessons=["Stage 5: Making Pages Look Good"]

        sub_topic=["Intro to JavaScript"]

        sub_topic2=["Use of JavaScript"]

        sub_topic3=["Replace and Append Functions"]

        sub_topic4=["Final Thoughts"]

        sub_topic_list=["JavaScript is the programming language of the web. It can change HTML content and attribitutes, it can make changes to CSS style, and it can be used to validate inpute. It gives immediate visual results from your code and runs natively in the browser. We can easily inspect our code simply by opening the JavaScript Console in the tools section of the browser.Using console.log(variablename) prints whaever information it receives to the console browser making it a very good debugging tool, especially for new developers."] 
                        

        sub_topic_list2=['Like other programming languages, JavaScript allows us to save data in the form of variables. The syntax is in s simpler form and easier to manipulate. The syntax is basic, just the keyword var, variable name equals some value.  It looks like this: var age = 35;. Arrays, functions and even objects use the same var syntax.', 'Arrays are used to store multiple values in a single variable.They are referenced as zero index meaning the first entry in an array is in position 0.', 'Objects are variables too, but objects can contain many values. JavaScript objects are containers for named values. Using objects allows us to assign many values to the variable we defined.  If we did a var name of John we could assign John an age, eye color, height and so on.']

        sub_topic_list3=['JavaScript String Object has a handy function that lets you replace words that occur within the string. This comes in handy if you have a form letter with a default reference of "username". With the replace function you could grab get the persons name with an HTML form or JavaScript prompt and then replace all occurrences of "username" with the value that they entered. Examples can be found in my codepen.', 'The append() method inserts specified content at the end of the selected elements. We can also insert content at the beginning of the selected elements, using the prepend() method. The syntax is $(selector).append(content,function(index,html)).']
        sub_topic_list4=['JavaScript and related tools such as jQuery, which is a Javascript Library that simplifies implementing JavaScript, makes website design and manipulation easy. jQuery greatly simplifies JavaScript programming.']
               

        items = self.request.get_all("words")
        self.render("html-div-lists.html", items = items,lessons=lessons,sub_topic=sub_topic, sub_topic_list=sub_topic_list, sub_topic_list2=sub_topic_list2, sub_topic2=sub_topic2, sub_topic3=sub_topic3, sub_topic_list3=sub_topic_list3, sub_topic4=sub_topic4, sub_topic_list4=sub_topic_list4)

class codepenHandler(webapp2.RequestHandler):
    def get(self):
        template_values={
            'title': 'Notes To Intro Programming',
                }

        template=jinja_env.get_template('codepen.html',)

        self.response.out.write(template.render(template_values))





#This code identifies the name of the wall
class guestbookHandler(Handler):
    def get(self):
        guestbook_name = self.request.get('guestbook_name',
                                          default_guestbook_name)
        notes_query = Greeting.query(
            ancestor = guestbook_key(guestbook_name)).order(-Greeting.date)
        notes_query_number=10
        notes = notes_query.fetch(notes_query_number)

        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'user' : user ,
            'notes' : notes ,
            'url' : url ,
            'url_linktext' : url_linktext ,
            'error' : error             
        }

        template = jinja_env.get_template('guestbook.html')
        self.response.write(template.render(template_values))



class Validation(webapp2.RequestHandler):
    def post(self):
        guestbook_name = self.request.get('guestbook_name',
                                         default_guestbook_name)
        note = Greeting(parent = guestbook_key(guestbook_name))

        
        if not (self.request.get('content') and self.request.get('title')):
            global error
            error = "Please Leave Your Name and Comment!"
        else:
            global error
            error = ""
            note.content = self.request.get('content')
            note.title = self.request.get('title')
            note.put()

        query_params = {'guestbook_name': guestbook_name}
        self.redirect('/guestbook.html?' + urllib.urlencode(query_params))
        






app=webapp2.WSGIApplication([('/', MainPage),
    ('/codepen.html', codepenHandler),
    ('/guestbook.html', guestbookHandler),
    ('/notes', Validation)
    ], 
    debug=True)
