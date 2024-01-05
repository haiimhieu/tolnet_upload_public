import requests
import os,glob
 
class SessionWithHeaderRedirection(requests.Session):

    AUTH_HOST = 'urs.earthdata.nasa.gov'
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
 
all_files = glob.glob(r'C:\Users\kimqu\OneDrive\Desktop\TOLNet-Surface files\TOLNet-SurfaceObs_GSFC_20230814_R0.ict')

print(all_files)
 
# create session with the user credentials that will be used to authenticate access to the data
 
username = "trong_nguyen_gsfc"
 
password= "Tr6218517719!"


 
session = SessionWithHeaderRedirection(username, password)

t = session.get('https://tolnet.larc.nasa.gov/api/auth/login')
t1 = session.get('https://tolnet.larc.nasa.gov/api/auth/ident')

for file in all_files:
    files = {
        'public': (None, 'true'),
        'nearRealTime': (None, 'false'),
        'scanOnly': (None, 'false'),
        'file': open(file, 'rb'),
    }

    response = session.post('https://tolnet.larc.nasa.gov/api/data/upload', files=files, verify=False)

    print(response.text)
    print(response.status_code)

 