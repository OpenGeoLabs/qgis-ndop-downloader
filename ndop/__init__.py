import pandas as pd
import requests
import configparser
import re
import urllib
import json

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
    Get list of values from list searching on web
    
    :param filt_attr: use some attribute ie. `rfTaxon` or `multiple`
    for search for regions names (CHKO, NP, EVL, cities)

    """
    
    s = requests.Session()
    url = ("https://portal.nature.cz/nd/nd_modals/"
           "modals.php?opener={}&promka={}").format(filt_attr, keyword)
    tax = s.get(url).text
    json_string = tax[9:-1]
    obj = json.loads(json_string)
        
    dt = []
    dt.append(list(obj[0].keys()))
    for i in obj:
        dt.append(list(i.values()))
    
    return(dt)

def read_config(path):
	config = configparser.ConfigParser()
	config.read(path)
	username = config.get('login', 'username')
	password = config.get('login', 'password')

	return (username, password)

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
        search_payload['parametryZakresu'] = polygon

    if region is not None:
        df = list_of_val('multiple', region)
        if len(df) == 2:
            reg_type = df[1][1]
            if reg_type == 'KU':
                search_payload['rfKatastr'] = df[1][0]
            elif reg_type == 'MZCHU':
                search_payload['rfMZCHU'] = df[1][0]
            elif reg_type == 'EVL':
                search_payload['rfEVL'] = df[1][0]
            elif reg_type == 'VZCHU':
                search_payload['rfVZCHU'] = df[1][0]
            elif reg_type == 'PO':
                search_payload['rfPO'] = df[1][0]
            print("Region: ", reg_type, " - ", df[1][0])
        else:
            print(("{} regions was found :\n").format(len(df)-1))
            for i in df:
                if i == df[0]:
                    print(i,"\n",50*"-")
                else:
                    print(i)
            print(("\nPlease specify the unique or exact input value"
                  " ie: '{}'").format(df[1][0])
                 )
            return None
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
