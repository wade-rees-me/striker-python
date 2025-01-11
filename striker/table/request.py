import http.client
import json
from urllib.parse import urlparse

class Request:
    def __init__(self):
        self.response_string = ""
        self.json_response = None

    def fetch_json(self, url):
        try:
            # Parse the URL
            parsed_url = urlparse(url)
            conn = http.client.HTTPSConnection(parsed_url.netloc)

            # Make the GET request
            conn.request("GET", parsed_url.path + ("?" + parsed_url.query if parsed_url.query else ""))
            response = conn.getresponse()

            # Check for HTTP errors
            if response.status < 200 or response.status >= 300:
                print(f"HTTP error: {response.status} {response.reason}")
                exit(-1)

            # Read the response data
            self.response_string = response.read().decode("utf-8")

            # Parse the JSON response
            self.json_response = json.loads(self.response_string)
        except http.client.HTTPException as e:
            print(f"HTTP request failed: {e}")
            exit(-1)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            exit(-1)
        finally:
            conn.close()

