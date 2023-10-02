# -*- coding: utf-8 -*-
from odoo import api, fields, models
import json
import random
import urllib.request

HOST = 'localhost'
PORT = 8069
DB = 'odoo'
USER = 'admin'
PASS = 'admin'

class BreakingBadActor(models.Model):
    _name = 'breakingbad.actor'
    _description = 'Breaking Bad actors contacts'

    name = fields.Char(string='Name', required=True)
    address = fields.Text(string='Address', required=True)
    phone = fields.Integer(string='Phone', required=True)
    email = fields.Text(string='Email', required=True)

    def custom_button_method(self):
        def json_rpc(url, method, params):
            data = {
                "jsonrpc": "2.0",
                "method": method,
                "params": params,
                "id": random.randint(0, 100000000),
            }
            req = urllib.request.Request(url=url, data=json.dumps(data).encode(), headers={
                "Content-Type":"application/json",
            })
            reply = json.loads(urllib.request.urlopen(req).read().decode('UTF-8'))
            if reply.get("error"):
                raise Exception(reply["error"])
            return reply["result"]

        def call(url, service, method, *args):
            return json_rpc(url, "call", {"service": service, "method": method, "args": args})

        url = "http://%s:%s/jsonrpc" % (HOST, PORT)
        uid = call(url, "common", "login", DB, USER, PASS)

        i = 1
        res = call(url, "object", "execute", DB, uid, PASS, 'breakingbad.actor', 'read', [i])

        while len(res) == i:
            i += 1
            res.extend(call(url, "object", "execute", DB, uid, PASS, 'breakingbad.actor', 'read', [i]))

        with open('Breaking Bad Actors contacts.txt', 'w') as outfile:
            json.dump(res, outfile)    