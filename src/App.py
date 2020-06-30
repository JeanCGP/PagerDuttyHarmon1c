from flask import Flask, render_template, request, redirect, url_for, flash
import http.client, json


# initializations
app = Flask(__name__)

# VARIABLES 

class MyClassInc(object):
    def __init__(self,number,title,created_at,unacknowledg_at,acknowledgements_name,html_url):
        self.number = number
        self.title=title
        self.created_at=created_at
        self.unacknowledg_at=unacknowledg_at
        self.acknowledgements_name=acknowledgements_name
        self.html_url=html_url
  


# settings <- No tiene sentido guardar seccion por ahora...
app.secret_key = "mysecretkey"

# PD-settings
conn = http.client.HTTPSConnection("api.pagerduty.com")
headers = {
    'accept': "application/vnd.pagerduty+json;version=2",
    'authorization': "Token token=VqvWzGzb2YstCF4To7Tr"
    }

# routes
@app.route('/')
def Index():
    conn.request("GET", "/incidents?statuses%5B%5D=acknowledged&team_ids%5B%5D=PL09PSG&time_zone=UTC", headers=headers)
    res = conn.getresponse()
    data_bytes = res.read()
    data = json.loads(data_bytes)
    my_list=[]
    for incidents in data['incidents']:
            text1aux=""
            text2aux=""
            for unacknowledge in incidents['pending_actions']:
                text1aux=unacknowledge['at']
            for acknowledgements in incidents['acknowledgements']:
                acknowledger_dict=acknowledgements['acknowledger']
                text2aux=acknowledger_dict['summary']
            my_list.append([MyClassInc(incidents['incident_number'],incidents['title'],incidents['created_at'],text1aux,text2aux,incidents['html_url'])])
    #return "hello-words"
    return render_template('index.html', incidents=my_list)

# starting the app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)