# Upload codes for the tolnet archive website
# As of February 14th, 2023 needed to be on the NASA VPN.
# Work for python 3+

import requests
import os,glob
 
class SessionWithHeaderRedirection(requests.Session):
    """
    Session class provided through NASA, this will ensure that your session will stay the same
    throughout the uploading process. 
    """
    AUTH_HOST = 'uat.urs.earthdata.nasa.gov'
    def __init__(self, username, password):
        super().__init__()
        self.auth = (username, password)
  
   # Overrides from the library to keep headers when redirected to or from 
   # the NASA auth host.
 
    def rebuild_auth(self, prepared_request, response):
        headers = prepared_request.headers
        url = prepared_request.url
 

        if 'Authorization' in headers:
            original_parsed = requests.utils.urlparse(response.request.url)
            redirect_parsed = requests.utils.urlparse(url)
 
            if (original_parsed.hostname != redirect_parsed.hostname) and (redirect_parsed.hostname != self.AUTH_HOST) and (original_parsed.hostname != self.AUTH_HOST):
                del headers['Authorization']
        return
 


def upload_file(username, password, file):
    """
    Upload file function that is used to upload the file to the website. 
    Parameters:
    username = your earthdata username as a string
    password = your earthdata password as a string
    file = the path of the file where you want to upload as a string
    """    
    
    session = SessionWithHeaderRedirection(username, password)

    t = session.get('https://test-tolnet.nasa.gov/api/auth/login', verify = False)
    t1 = session.get('https://test-tolnet.nasa.gov/api/auth/ident', verify = False)

    files = {
        'public': (None, 'true'),
        'nearRealTime': (None, 'false'),
        'scanOnly': (None, 'false'),
        'file': open(file, 'rb'),
    }

    response = session.post('https://test-tolnet.nasa.gov/api/data/upload', files=files, verify=False)

    status = response.status_code
    print(status)
    # If status code is 200, then file is uploaded successfully



 