#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import csv

def get_cdb(filt_par):
    s = requests.Session()
    url = ("https://portal.nature.cz/nd/nd_modals/"
           "modals.php?opener={}&promka=").format(filt_par)
    ls = s.get(url).text
    json_string = ls[9:-1]
    cdb = json.loads(json_string)
    
    keys = cdb[0].keys()
    with open(filt_par+'.csv', 'w') as f:
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writeheader()
        dict_writer.writerows(cdb)

get_cdb("rfTaxon")
get_cdb("multiple")



