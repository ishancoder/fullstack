from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi,urllib2


#session.rollback()

class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith('/hello'):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()

                output = "<html><body>HEllo worlds<br>"
                output += "<form method='POST' enctype='multipart/form-data' action='/hello'>\
                        <h2>What world you like me to say?</h2> <input name='message'\
                        type='text'><input type='submit' value='SUBMIT'></form>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return
            if self.path.endswith('/hola'):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()

                output = "<html><body>Hola!<a href='/hello'>Back to hello</a><br>"
                output += "<form method='POST' enctype='multipart/form-data' action='/hello'>\
                        <h2>What world you like me to say?</h2> <input name='message'\
                        type='text'><input type='submit' value='SUBMIT'></form>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return
            if self.path.endswith('/restaurants'):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                retaurent = session.query(Restaurant).all();
                output = "<h1><a href='/restaurants/new'>Make New Restaurent</a></h1>"
                for each in retaurent:
                    output += "<h3>" + each.name + "</h3><a href='/restaurants/%s/edit'>Edit</a><br><a href='/restaurants/%s/delete'>Delete</a><br>"%(each.id,each.id)
                self.wfile.write(output)
                return
            if self.path.endswith('/restaurants/new'):
                self.send_response(200)
                self.send_header('Conetent-type','text-html')
                self.end_headers()
                output = "<html><body><form method='POST' enctype='multipart/form-data' action='/restaurants/new'>\
                        <h2>What world you like me to say?</h2> <input name='restname'\
                        type='text'><input type='submit' value='SUBMIT'></form></body></html>"
                self.wfile.write(output)
                return
            if self.path.endswith('/edit'):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                output = "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit'>\
                        <h2>Rename the hotel!</h2> <input name='hotelnewname'\
                        type='text'><input type='submit' value='RENAME'></form>"%self.path.split('/')[2]
                self.wfile.write(output)
##                restaurantIDPath =  self.path.split("/")[2]  
##                myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
##                print myRestaurantQuery
##                if myRestaurantQuery != [] :
##                    self.send_response(200)
##                    self.send_header('Content-type',    'text/html')
##                    self.end_headers()
##                    output = ""
##                    output += myRestaurantQuery.name
##                    output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit' >" % restaurantIDPath
##                    output += "<input name= 'newRestaurantName' type='text' placeholder = '%s' >" % myRestaurantQuery.name
##                    output += "<input type= 'submit' value='Rename'>"
##                    output += "</form>"
##
##                    self.wfile.write(output)
##                else:
##                    print "empty query!"
                
            if self.path.endswith('/delete'):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                #queryId = session.query(Restaurant).filter_by(id = self.path.split('/')[2]).one()
                output = "<html><body><form method='POST' enctype='multipart/form-data' action='/restaurants/%s/delete'>\
                        <h2>DELETE the hotel!</h2><input type='submit' value='SUBMIT'></form></body></html>"%self.path.split('/')[2]
                self.wfile.write(output)
                print self.path.split('/')[2]
                
                
        except IOError:
            self.send_error(404, "File not found %s"%self.path)

    def do_POST(self):
        try:
            if self.path.endswith('/restaurants/new'):
                self.send_response(302)
                
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                restname = fields.get('restname')
                restaurent = Restaurant(name=restname[0])
                session.add(restaurent)
                session.commit()
                self.send_header('Location','/restaurants')
                self.end_headers()
                
            if self.path.endswith('/edit'):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                name_of_hotel = fields.get('hotelnewname')[0]
                path = self.path.split("/")[2]
                found = session.query(Restaurant).filter_by(id = path).one()
                if found != []:
                    found.name = name_of_hotel
                    session.add(found)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location','/restaurants')
                    self.end_headers()
              
##            if self.path.endswith("/edit"):
##                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
##                if ctype == 'multipart/form-data':
##                    query=cgi.parse_multipart(self.rfile, pdict)
##                upfilecontent = query.get('hotelnewname')#newRestaurantName
##               
##                restaurantPath =  self.path.split("/")[2]
##                print restaurantPath
##                myRestaurant = urllib2.unquote(restaurantPath)
##                myRestaurantQuery = session.query(Restaurant).filter_by(id = myRestaurant).one() 
##                if myRestaurantQuery != [] :
##                    myRestaurantQuery.name = upfilecontent[0]
##                    session.add(myRestaurantQuery)
##                    session.commit()
##                    self.send_response(301)
##                    self.send_header('Content-type',    'text/html')
##                    self.send_header('Location', '/restaurants')
##                    self.end_headers()
                
            if self.path.endswith('/delete'):
                rest = session.query(Restaurant).filter_by(id = self.path.split('/')[2]).one()
                if rest != []:
                    session.delete(rest)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type','text/html')
                    self.send_header('Location','/restaurants')
                    self.end_headers()   
        except:
            pass
                

def main():
    try:
        port = 8080
        server = HTTPServer(('',port), webserverHandler)
        print "Web Server running on port %s"%port
        server.serve_forever()
    except KeyboardInterrupt:
        print "Stopping server ^C HIT..."
        server.socket.close()


if __name__ == '__main__':
    main()
