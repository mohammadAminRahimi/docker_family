import time
from locust import HttpUser, task, between
import random 
import string
import json

class QuickstartUser(HttpUser):
    wait_time = between(1, 2.5)

    token = str()
    child_name = str()


    def on_start(self):

        # register a new person
        uname = ''.join(random.choice(string.ascii_uppercase  ) for _ in range(5))
        pas = ''.join(random.choice(string.ascii_uppercase  ) for _ in range(5))
        fname = ''.join(random.choice(string.ascii_uppercase  ) for _ in range(5))
        lname = ''.join(random.choice(string.ascii_uppercase  ) for _ in range(5))
        pnumber = ''.join(random.choice(string.ascii_uppercase  ) for _ in range(5))
        data = '{{ "username": "{uname}","password": "{password}","firstname": "{fname}","lastname": "{lname}","phone_number": "{pnumber}","gender": "m"}}'
        res = self.client.post("/register",data=data.format(uname=uname, password=pas, fname=fname, lname=lname, pnumber=pnumber), headers={'Content-Type': "application/json"})
        self.token = json.loads(res.text)["token"]

        #register its child
        cname = ''.join(random.choice(string.ascii_uppercase  ) for _ in range(5))
        pas = ''.join(random.choice(string.ascii_uppercase  ) for _ in range(5))
        fname = ''.join(random.choice(string.ascii_uppercase  ) for _ in range(5))
        lname = ''.join(random.choice(string.ascii_uppercase  ) for _ in range(5))
        pnumber = ''.join(random.choice(string.ascii_uppercase  ) for _ in range(5))
        data = '{{ "username": "{uname}","password": "{password}","firstname": "{fname}","lastname": "{lname}","phone_number": "{pnumber}","gender": "m"}}'
        res = self.client.post("/register",data=data.format(uname=cname, password=pas, fname=fname, lname=lname, pnumber=pnumber), headers={'Content-Type': "application/json"})
        self.child_name = cname

        #register a new family
        data = '{{ "parents_username": ["{pname}" ], "childs_username": ["{cname}"]}}'
        res = self.client.post("/create-family",data=data.format(pname=uname, cname=cname), headers={'Authorization': ("token " + self.token), 'Content-Type': "application/json" })

    @task
    def selecting_package(self):
        data = '{{ "child_username": "{cname}", "package_type": "A" }}'.format(cname=self.child_name)
        res = self.client.post('/package-selection', data=data, headers={'Authorization': ("token " + self.token), 'Content-Type': "application/json"})

    @task
    def changing_package(self):
        codata = '{{ "child_username": "{cname}", "package_type": "A" }}'.format(cname=self.child_name)
        res = self.client.post('/package-change', data=data, headers={'Authorization': ("token " + self.token), 'Content-Type': "application/json"})

    @task
    def changing_package(self):
        data = '{{ "child_username": "{cname}" }}'.format(cname=self.child_name)
        res = self.client.post('/package-delete', data=data, headers={'Authorization': ("token " + self.token), 'Content-Type': "application/json"})
