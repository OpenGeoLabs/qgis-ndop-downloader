#!/usr/bin/python3
# -*- coding: utf-8 -*-

# TODO
#   * popis/napoveda/dokumentace
#   * dalsi parametry zdroju
#   * pridat casy odezvy serveru
#   * zpracovani vystupu
#   * vytvorit konfiguracni soubor s prihlasovacimi udaji
#   * transformace souřadnic z vektorové vrstvy

import requests
import re
import urllib
import pandas as pd
import argparse
import json
import sys
from pathlib import Path
import configparser

LOGIN_URL = 'https://login.nature.cz/login.php?appid=59'
SEARCH_URL = ('https://portal.nature.cz/nd/find.php?akce=seznam&opener='
             '&vztazne_id=0')
LOCATIONS_URL = 'https://portal.nature.cz/nd/export_lokalizaci.php'

class NBException(Exception):
    pass

def fail(message):
    """fail program for some reason. 

    for most of the code, you should be using NBException

    :param message: message to be printed to the user
    """

    sys.stderr.write("ERROR: {}\n".format(message))
    sys.exit(1)

def list_of_val(filt_attr, keyword):
    """
    Get list of values
    """
    
    s = requests.Session()
    keyword = keyword
    url = ("https://portal.nature.cz/nd/nd_modals/"
           "modals.php?opener={}&promka={}").format(filt_attr, keyword)
    tax = s.get(url).text
    json_string = tax[9:-1]
    obj = json.loads(json_string)
    dt = pd.DataFrame.from_dict(obj)
    
    return(dt)

def args_parser():
    """
    Parse command line arguments
    """
    parser = argparse.ArgumentParser(
        description=('Download data (.csv, .shp) from NDOP based on input '
                    'parametres. Unlike the offical web filter, its possible '
                    'to input polygon layer for search in area and amount of '
                    'results is not limited. Login can be stored in '
                    'configuration file ".ndop.cfg".')
    )

    parser.add_argument(
        '--user', help='login (user name or email)'
    )
    parser.add_argument(
        '--password', help='ISOP password'
    )
    parser.add_argument(
        '--output', help='path with output filenames prefix',
        default=str(Path(Path.cwd(),"data"))
    )

    parser.add_argument(
        '--taxon', help='taxon name (i.e. "mantis religiosa")'
    )

    parser.add_argument(
        '--region', help='region of iterest (i.e. town , protected area)'
    )
    parser.add_argument(
        '--polygon', help='path to poygon layer (EPSG:5514) that define the'
        'search area. Function takes first feature of the layer'
    )

    parser.add_argument(
        '--month_from', help='get data only from a certain month in season '
        '(number)'
    )
    parser.add_argument(
        '--month_to', help='get data only to a certain month in season '
        '(number)'
    )
    parser.add_argument(
        '--date_from', help='get data from a certain date (d.m.yyyy)'
    )
    parser.add_argument(
        '--date_to', help='get data only to a certain date (d.m.yyyy)'
    )

    parser.add_argument(
        '--author', help='author surname and firstname (i.e. "Kaláb Oto")'
    )

    parser.add_argument(
        '--config',
        help='path to the config file with login and password.'
        ' Default path for file is: "{}"'.format(Path(Path.home(),
        ".ndop.cfg")), default=Path(Path.home(), ".ndop.cfg")
    )


    args = parser.parse_args()

    def read_config(path):
        config = configparser.ConfigParser()
        config.read(args.config)
        username = config.get('login', 'username')
        password = config.get('login', 'password')

        return (username, password)

    if args.user and args.password:
         pass
    elif args.user and not args.password or \
          not args.user and args.password:
         fail("Input username and password")
    elif args.config:
         if not Path.is_file(Path(args.config)):
             fail("Configuration file {} not found".format(args.config))
         else:
              args.user, args.password = read_config(args.config)
    elif Path.is_file(Path.home(), '.ndop.cfg'):
             args.user, args.password = read_config(Path(Path.home(),
             '.ndop.cfg'))
    else:
         fail("There is no username and password or config file")  

    return args


def poly (polygon):
    """
    Parse geometry of polygon layers first feature to NDOP input format
    """
    import fiona

    shape = fiona.open(polygon)
    first = next(iter(shape))
    bb = shape.bounds

    polygon = '{},"xmin":{},"xmax":{},"ymin":{},"ymax":{} {}'.format(
        str(first['geometry']).replace("(","[").replace(")","]") \
        .replace("'","\"")[:-1],
        bb[0],bb[2],bb[1],bb[3],"}"
    )

    return polygon

def get_search_pars(
        author='', taxon='', region=None, polygon=None, date_to='',
        date_from='', month_to='', month_from=''):

    """
    :param taxon: taxon
    :param author: author
    :param region: region name
    :param polygon: polygon layer
    :param date_to: date to
    :param date_from: date from
    :param month_to: month to
    :param month_from: month from

    :return: dict with search parameters
    """

    if taxon is None:
        taxon = ''
    if author is None:
        author = ''
    if date_to is None:
        date_to = ''
    if date_from is None:
        date_from = ''
    if month_to is None:
        month_to = ''
    if month_from is None:
        month_from = ''

    search_payload = {
        'rfTaxon': taxon,
        'lname': '',
        'count': '',
        'region-setter': '',
        'from': '',
        'rfAutor': author,
        'rfMetadata': '',
        'rfProjekt': '',
        'rfZdroj': '',
        'fromHome': '',
        'rfPozitivni': '',
        'count': '',
        'existujeZakres': '',
        'idAkce': '',
        'karta_id': '',
        'karta_vztazne_id': '',
        'lpass': '',
        'parametryZakresu': '',
        'rfCeledi': '',
        'rfDatumDo': date_to,
        'rfDatumOd': date_from,
        'rfKategorie': '',
        'rfKraj': '',
        'rfKvadrat': '',
        'rfMesiceDo': month_to,
        'rfMesiceOd': month_from,
        'rfSpatial': '',
        'rfSpatialX': '',
        'but_action': 'Filtrovat',
        'but_co': 'rf',
        'pagesizeX': 500
    }

    if polygon is not None:
        search_payload['parametryZakresu'] = poly(polygon) 

    if region is not None:
        df = list_of_val('multiple', region)
        if df.shape[0] == 1:
            reg_type = df['type'][0]
            if reg_type == 'KU':
                search_payload['rfKatastr'] = df['val'][0]
            elif reg_type == 'MZCHU':
                search_payload['rfMZCHU'] = df['val'][0]
            elif reg_type == 'EVL':
                search_payload['rfEVL'] = df['val'][0]
            elif reg_type == 'VZCHU':
                search_payload['rfVZCHU'] = df['val'][0]
            elif reg_type == 'PO':
                search_payload['rfPO'] = df['val'][0]
            print("Region: ", reg_type, " - ", df['val'][0])
        else:
            return df.to_string()

    return search_payload


def get_ndop_data(username, password, search_payload, output_name):
    """
    Login and download data based on search payload dict
    """

    login_payload = {
        'isop_user': username,
        'isop_password': password,
        'isop_login': '+Přihlásit+se+'
    }

    s = requests.Session()

    print("Login...")
    s.post(LOGIN_URL, data=login_payload)

    if not "isop_loginhash" in s.cookies:
        raise NBException("Login failed")

    print("Filtering...")
    filter_page = s.post(SEARCH_URL, data=search_payload)

    if re.search("Seznam výsledků je prázdný", filter_page.text) is not None:
        print("No results found")
        sys.exit(0)

    num_rec = int(re.findall('záznam ze \d+', filter_page.text)[0][10:])

    print("The number of records:{}".format(num_rec))
    ndtsearch = re.search(
        'ndtoken=.+?"', s.post(SEARCH_URL, data=search_payload).text
    )
    ndtoken = ndtsearch.group(0)[8:40]

    table_payload = {
        'meziexport_druh': 'nalezy',
        'meziexport_sloupec_CXAKCE_AUTOR': 1,
        'meziexport_sloupec_CXAKCE_DATI_DO': 1,
        'meziexport_sloupec_CXAKCE_DATI_OD': 1,
        'meziexport_sloupec_CXAKCE_ZDROJ': 1,
        'meziexport_sloupec_CXEVD': 1,
        'meziexport_sloupec_CXKATASTR_NAZEV': 1,
        'meziexport_sloupec_CXLOKAL_ID': 1,
        'meziexport_sloupec_CXLOKAL_KVADRAT_XY': 1,
        'meziexport_sloupec_CXLOKAL_NAZEV': 1,
        'meziexport_sloupec_CXLOKAL_POZN': 1,
        'meziexport_sloupec_CXLOKAL_X': 1,
        'meziexport_sloupec_CXLOKAL_Y': 1,
        'meziexport_sloupec_CXLOKAL_Z': 1,
        'meziexport_sloupec_CXMTD_DTB': 1,
        'meziexport_sloupec_CXOSOBY_ZAPSAL': 1,
        'meziexport_sloupec_CXPRESNOST': 1,
        'meziexport_sloupec_CXPROJ_NAZEV': 1,
        'meziexport_sloupec_CXREDLIST': 1,
        'meziexport_sloupec_CXTAXON_IDX_CATEG': 1,
        'meziexport_sloupec_CXTAXON_NAME': 1,
        'meziexport_sloupec_CXVALIDACE': 1,
        'meziexport_sloupec_CXVYHL': 1,
        'meziexport_sloupec_HOD_VEROH': 1,
        'meziexport_sloupec_ID_ND_NALEZ': 1,
        'meziexport_sloupec_NEGATIVNI': 1,
        'meziexport_sloupec_ODHAD': 1,
        'meziexport_sloupec_POCET': 1,
        'meziexport_sloupec_POKRYVNOST': 1,
        'meziexport_sloupec_POP_POC': 1,
        'meziexport_sloupec_POZ_HAB': 1,
        'meziexport_sloupec_POZ_HABLOK': 1,
        'meziexport_sloupec_POZNAMKA': 1,
        'meziexport_sloupec_REL_POC': 1,
        'meziexport_sloupec_STRUKT_POZN': 1,
        'meziexport_sloupec_TAX_NOTE': 1,
        'meziexport_sloupec_VEROH': 1,
        'meziexport_tlacitko': 'Exportovat',
        'meziexport_typ_exportu': 'csv',
        'ndtokenexport': ndtoken
    }

    frames = []

    print("Downloading records: ")

    for i in range(0, num_rec, 500):
        print("{} - {}".format(str(i), str(i+500)))
        table_url = (
            'https://portal.nature.cz/nd/find.php?'
            'akce=seznam&opener=&vztazne_id=0&order=ID_ND_NALEZ'
            '&orderhow=DESC&frompage={frompage}&pagesize=500&'
            'filtering=&searching=&export=1&ndtoken={ndtoken}'
        ).format(frompage=str(i), ndtoken=ndtoken)

        req = s.post(url=table_url, data=table_payload)
        req.encoding = 'cp1250'
        s_clean = pd.compat.StringIO(req.text)
        df = pd.read_csv(s_clean, sep=";")
        frames.append(df)

    df = pd.concat(frames)
    df.to_csv(output_name+"_csv.csv")
    print("CSV table downloaded: {}_csv.csv".format(output_name))

    print("Localization downloading ...")
    local = s.get(LOCATIONS_URL).text
    if local == '\n\n\n\n\n\n':
        print("No localization")
    else:
        m = re.findall('http.[^>]*zip', local)
        for i in m:
#             filename = str(Path(
#                 '.', "{}_shp_{}.zip".format(output_name, str(i[34]))
#             ))
            filename = "{}_shp_{}.zip".format(output_name, str(i[34]))
            
            urllib.request.urlretrieve(i, filename)
            print("SHP downloaded: " + filename)
    print("Done")

def main():

    args = args_parser()
    search_parameters = get_search_pars(args.author, args.taxon, args.region,
                                        args.polygon, args.date_to,
                                        args.date_from, args.month_to,
                                        args.month_from)

    if type(search_parameters) is not dict:
        print(
            ("More than one region was found :\n {} "
             "\n\nSpecify the input value (name or code)"
             ).format(search_parameters)
        )
    else:
        get_ndop_data(
            args.user,
            args.password,
            search_parameters,
            args.output
        )

if __name__ == "__main__":

    main()
