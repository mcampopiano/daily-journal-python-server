from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from moods import get_all_moods
from notes import get_all_notes, get_single_note, delete_note, get_note_by_search_term, create_note, update_note


# Here's a class. It inherits from another class.
# For now, think of a class as a container for functions that
# work together for a common purpose. In this case, that
# common purpose is to respond to HTTP requests from a client.
class HandleRequests(BaseHTTPRequestHandler):
    def parse_url(self, path):
        # Just like splitting a string in JavaScript. If the
        # path is "/animals/1", the resulting list will
        # have "" at index 0, "animals" at index 1, and "1"
        # at index 2.
        path_params = path.split("/")
        resource = path_params[1]

         # Check if there is a query string parameter
        if "?" in resource:
            # GIVEN: /notes?q=${searchTerm}

            param = resource.split("?")[1]  # q=${searchTerm}
            resource = resource.split("?")[0]  # 'notes'
            pair = param.split("=")  # [ 'q', '${searchTerm}' ]
            key = pair[0]  # 'q'
            value = pair[1]  # '${searchTerm}'

            return ( resource, key, value )
        else:
            id = None

        # Try to get the item at index 2
        try:
            # Convert the string "1" to the integer 1
            # This is the new parseInt()
            id = int(path_params[2])
        except IndexError:
            pass  # No route parameter exists: /animals
        except ValueError:
            pass  # Request had trailing slash: /animals/

        return (resource, id)  # This is a tuple

    # Here's a class function
    def _set_headers(self, status):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    # Here's a method on the class that overrides the parent's method.
    # It handles any GET request.
    def do_GET(self):
        self._set_headers(200)
        response = {}  # Default response

        # Parse URL and store entire tuple in a variable
        parsed = self.parse_url(self.path)
        
        # Response from parse_url() is a tuple with 2
        # items in it, which means the request was for
        # `/animals` or `/animals/2`
        if len(parsed) == 2:
            ( resource, id ) = parsed

            if resource == "notes":
                if id is not None:
                    response = f"{get_single_note(id)}"

                else:
                    response = f"{get_all_notes()}"
            elif resource == "moods":
                response = f"{get_all_moods()}"
        # Response from parse_url() is a tuple with 3
        # items in it, which means the request was for
        # `/resource?parameter=value`
        elif len(parsed) == 3:
            ( resource, key, value ) = parsed

            # Is the resource `customers` and was there a
            # query parameter that specified the customer
            # email as a filtering value?
            if key == "q" and resource == "notes":
                response = get_note_by_search_term(value)
        

        self.wfile.write(response.encode())

    # Here's a method on the class that overrides the parent's method.
    # It handles any POST request.
    def do_POST(self):
        # Set response code to 'Created'
        self._set_headers(201)

        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

         # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Initialize new note
        new_entry = None
        # Initialize new location

        # Add a new note to the list. Don't worry about
        # the orange squiggle, you'll define the create_note
        # function next.
        if resource == "notes":
            new_entry = create_note(post_body)
        # response = f"received post request:<br>{post_body}"
        self.wfile.write(f"{new_entry}".encode())

    def do_DELETE(self):
        # Set a 204 response code
        self._set_headers(204)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

         # Delete a single note from the list
        if resource == "notes":
            delete_note(id)
        # elif resource == "locations":
        #     delete_location(id)
        # elif resource == "employees":
        #     delete_employee(id)
        # elif resource == "customers":
        #     delete_customer(id)

        # Encode the new animal and send in response
        self.wfile.write("".encode())


    # Here's a method on the class that overrides the parent's method.
    # It handles any PUT request.
    def do_PUT(self):
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        success = False

        
        if resource == "notes":
           success = update_note(id, post_body)
        
        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

        # Encode the new animal and send in response
        self.wfile.write("".encode())


# This function is not inside the class. It is the starting
# point of this application.
def main():
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()

if __name__ == "__main__":
    main()