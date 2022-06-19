import http.server
import socketserver
from unicodedata import name
from urllib.parse import urlparse
from urllib.parse import parse_qs
import os

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):

    def errorC(parameters):
        print(parameters)

    def find_files(filename, search_path):
        # Walking top-down from the root
        for root,dir, files in os.walk(search_path):
            if filename in files:
                return os.path.join(root, filename)

    def Registration(information):
            name = str(information[0]).replace("-"," ")
            tripId = str(information[1]).replace("-"," ")
            date = str(information[2]).replace("-"," ")
            numOfPeople = str(information[3]).replace("-"," ")
            cost = str(information[4]).replace("-"," ")
            location = str(information[5]).replace("-"," ")
            #paidBack = "0"

            # Save in CSV format
            order="name:"+ name +"\ntripId:"+tripId + "\ndate:"+date+ "\nnumOfPeople:"+numOfPeople+"\ncost:"+cost+"\nlocation:"+location + "\n" #+"\npaidBack:"+paidBack + " "
            f = open((name)+"_"+(tripId) +".txt", "w")
            f.write(order)
            f.close()

            return information


    def findTrip(information):
        global possibleInstructions
            #d = {
            #    'name' : "",
            #    'tripId' :  "",
            #    'numOfPeople' :  "",
            #    'location' :  "",
            #    'date' :  "",
            #    'cost' :  "",
            #    'paidBack' : ""
            #}

        name = information[0]
        tripId = information[1]
        d = []
        with open(str(name)+"_"+str(tripId) +".txt",'r') as new_file:
            for i in new_file:
                i = i[:len(i)-1]
                j=i.rsplit(":")
                #d[j[0]]=j[1]
                d.append(j[1])
        return d

    def addCost(val):
        global possibleInstructions
        # send name, id, cost either negative or positive
        information = possibleInstructions.get('getInfo')([val[0],val[1]])
        if int(val[2])>0:
            information[4] = str(float(information[4])+float(val[2]))
        else:
            information[4] = str(float(information[4])-float(val[2]))
        return possibleInstructions.get('registrationinfo')(information)


    def addPerson(val):
        global possibleInstructions
        # send name, id
        information = possibleInstructions.get('getInfo')([val[0],val[1]])
        information[3] = str(1+int(information[3]))
        return possibleInstructions.get('registrationinfo')(information)

    def removePerson(val):
        global possibleInstructions
        # send name, id
        information = possibleInstructions.get('getInfo')([val[0],val[1]])
        information[3] = str(int(information[3])-1)
        return possibleInstructions.get('registrationinfo')(information)

    #def payBack(val):
    #    global possibleInstructions
    #    # send name, id, value
    #    information = possibleInstructions.get('findTrip')([val[0],val[1]])
    #    information[6] += val[2]
    #    return possibleInstructions.get('updateData')(information)


    global possibleInstructions
    possibleInstructions = {
        'registrationinfo' : Registration,
        'getInfo' : findTrip,
        'addcost' : addCost,
        'addperson' : addPerson,
        'removeperson' : removePerson,
        #'payBack' : payBack,
        'default' : errorC,

        #internal methods
        'findFiles' : find_files
         }
    def do_GET(self):
        # Sending an '200 OK' response
        self.send_response(200)

        # Setting the header
        self.send_header("Content-type", "text/html")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods','GET,POST,PATCH,OPTIONS')

        # Whenever using 'send_header', you also have to call 'end_headers'
        self.end_headers()

        global possibleInstructions
        url = self.path
        instructions = url[1:url.rfind(":")]
        parameters = url[url.rfind(":") + 1:].replace("-"," ")
        values = parameters.split(",")
        possibleInstructions.get(instructions, 'default')(values)

        updatedValues=possibleInstructions.get(instructions)(values)
        if (type(updatedValues) != bool):
            costPerUser = float(updatedValues[4])/float(updatedValues[3])
            sendToJS = str(updatedValues[2]).replace(" ","-")+","+str(updatedValues[5]).replace(" ","-")+","+str(updatedValues[4]).replace(" ","-")+","+str(costPerUser)
        else:
            print("THIS FUNCTION DOESNT RETURN ANHITNGNGGHIUISdssaifjpw")

        self.wfile.write(bytes(sendToJS, "utf8"))



    def do_POST(self):
        global possibleInstructions
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header("Content-type", "text/html")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods','GET,POST,PATCH,OPTIONS')
        self.end_headers()

        url = self.path
        instructions = url[1:url.rfind(":")]
        parameters = url[url.rfind(":") + 1:].replace("-"," ")
        values = parameters.split(",")

        possibleInstructions.get(instructions, 'default')(values)
# Create an object of the above class
handler_object = MyHttpRequestHandler

PORT = 8000
my_server = socketserver.TCPServer(("", PORT), handler_object)

# Star the server
my_server.serve_forever()