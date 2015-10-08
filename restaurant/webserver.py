from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
import re

####################### CRUD operation dependencies #######################

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            restaurants = session.query(Restaurant).all()
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<h1>Hello!</h1>"
                output += "<html><body>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What 
                would you like me to say?</h2><input name="message" type="text" >
                <input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>&#161 Hola !</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'>
                <h2>What would you like me to say?</h2><input name="message" type="text" >
                <input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            # Restaurants link

            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += '<a href = "/restaurants/new">Make a New Restaurant Here</a><br><br>'
                for restaurant in restaurants:
                    output += restaurant.name +'<br> <a href="' + 'restaurants/'+ str(restaurant.id) +'/edit' + '">Edit</a> <br> <a href="restaurants/%d/delete">Delete</a> <br><br>'%restaurant.id
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            # Restaurant item adding link

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>
                <h2>Make a New Restaurant</h2>
                <input name="restaurant" type="text" >
                <input type="submit" value="Create"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            # Restaurants edit link
            if self.path.endswith("/edit"):
                rest_id = self.path.split("/")[2]
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit'><h2>'''% rest_id + restaurants[int(rest_id)].name +'''</h2>
                <input name="newrestaurant" type="text" >
                <input type="submit" value="Rename"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            # Restaurants Delete link
            if self.path.endswith("/delete"):
                rest_id = self.path.split("/")[2]
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/delete'><h2>'''% rest_id + "Do you want to delete " + restaurants[int(rest_id)].name +'''</h2>
                <input type="submit" value="Delete"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return


        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)


    def do_POST(self):
        try:
            if self.path.endswith("restaurants/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    new_restaurant = fields.get('restaurant')
                restaurant1 = Restaurant(name = new_restaurant[0])
                session.add(restaurant1)
                session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location','/restaurants')
                self.end_headers()
                return

            elif self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    new_restaurant = fields.get('newrestaurant')
                rest_id = int(self.path.split("/")[2]) 
                restaurant_to_edit = session.query(Restaurant).filter_by(id=rest_id).one()
                restaurant_to_edit.name = new_restaurant[0]
                session.add(restaurant_to_edit)
                session.commit()
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location','/restaurants')
                self.end_headers()
                return

            elif self.path.endswith("/delete"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    new_restaurant = fields.get('delete')
                rest_id = int(self.path.split("/")[2]) 
                to_delete = session.query(Restaurant).filter_by(id = rest_id).one()
                session.delete(to_delete)
                session.commit()
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location','/restaurants')
                self.end_headers()
                return

            else:
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('message')
                output = ""
                output += "<html><body>"
                output += " <h2> Okay, how about this: </h2>"
                output += "<h1> %s </h1>" % messagecontent[0]
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'>
                <h2>What would you like me to say?</h2><input name="message" type="text" >
                <input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()