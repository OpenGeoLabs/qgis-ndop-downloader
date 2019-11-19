
Plánované funkce - zpětná vazba
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Výběr plánovaných funkcí:

-  zadání oblasti tažením a použítím polygonu z vrstvy
-  přidání filtru druhové ochrany
-  automatické vytvoření relace tabulkových dat a lokalizací (1:n)

seznam aktuálně plánovaných funkcí
`zde <https://github.com/OpenGeoLabs/qgis-ndop-downloader/issues?q=is%3Aopen+is%3Aissue+label%3Aenhancement>`__

Pro připomínky, nápady a hlášení chyb můžete napsat email nebo použít
`issues projektu na
GitHub <https://github.com/OpenGeoLabs/qgis-ndop-downloader/issues>`__.

Python balíček - ndop-downloader
--------------------------------

Pro stahování dat lze využít nástroj příkazové řádky **ndop** , který se
nainstaluje se zásuvným modulem do složky ``bin/ndop``. Tento nástroj má
více možností filtrů (viz nápověda modulu), a mimo jiné umožňuje
stahování na základě polygonové vrstvy (vezme první polygon z vrstvy).
Přihlašovací údaje lze zadat přímo do příkazu (``--user``,
``--password``), nebo je načíst z konfiguračního souboru ``.ndop.cfg`` v
domovském adresáři. Konfigurační soubor lze nechat vygenerovat použitím
argumentu ``-s``. Nástroj lze spustit z adresáře QGIS pluginu:

nápověda:

::

    python3 bin/ndop -h

použití:

::

    python3 bin/ndop --taxon "mantis religiosa"

Python balíček lze také stánout zcela samostatně z `PyPi <https://pypi.org/project/ndop-downloader/>`__:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    pip3 install ndop-downloader

Poté můžeme rovnou spustit:

::

    ndop --taxon "mantis religiosa"

Nebo naimportovat modul do vlastního skriptu pomocí:

.. code:: python

    import ndop

Nápověda:

::

    ndop -h

    usage: ndop [-h] [--user USER] [--password PASSWORD] [-s] [--output OUTPUT]
                [-loc_only] [--taxon TAXON] [--region REGION] [--polygon POLYGON]
                [--month_from MONTH_FROM] [--month_to MONTH_TO]
                [--date_from DATE_FROM] [--date_to DATE_TO] [--author AUTHOR]
                [--project PROJECT] [--source SOURCE] [--d_source D_SOURCE]
                [--config CONFIG]

    Download data (.csv, .shp) from NDOP based on input parametres. Unlike the
    offical web filter, its possible to input polygon layer for search in area and
    amount of results is not limited. Login can be stored in configuration file
    ".ndop.cfg".

    optional arguments:
      -h, --help            show this help message and exit
      --user USER           login (user name or email)
      --password PASSWORD   ISOP password
      -s                    store login and password in "/home/ok/.ndop.cfg"
      --output OUTPUT       path with output filenames prefix
      -loc_only             downloads only spatial data without tables(faster, but
                            only localisations with id)
      --taxon TAXON         taxon name (i.e. "mantis religiosa")
      --region REGION       region of iterest (i.e. town , protected area)
      --polygon POLYGON     path to poygon layer (EPSG:5514) that define thesearch
                            area. Function takes first feature of the layer
      --month_from MONTH_FROM
                            get data only from a certain month in season (number)
      --month_to MONTH_TO   get data only to a certain month in season (number)
      --date_from DATE_FROM
                            get data from a certain date (d.m.yyyy)
      --date_to DATE_TO     get data only to a certain date (d.m.yyyy)
      --author AUTHOR       author surname and firstname (i.e. "Kaláb Oto")
      --project PROJECT     for data obtained from specific project
      --source SOURCE       general source of data (i.e. "ND - Databáze BioLog")
      --d_source D_SOURCE   specific, more detailed source of data
      --config CONFIG       path to the config file with login and password.
                            Default file path is: "/home/ok/.ndop.cfg"

Licence
-------

`GNU General Public License
v3.0 <https://github.com/OpenGeoLabs/qgis-ndop-downloader/blob/master/LICENSE>`__
## Reference

Kaláb. O. (2019): NDOP Downloader - QGIS a Python modul, OpenGeoLabs

::

    @manual{,
      author   = {Oto Kaláb},
      title    = {NDOP Downloader - QGIS a Python modul},
      year     = {2019},
      organization = {OpenGeoLabs},
      url      = {https://github.com/OpenGeoLabs/qgis-ndop-downloader},
      keywords = {QGIS, Python, ecology, AOPK, species occurrence},
    }

Pro citaci použitých dat postupujte podle `Citačních pravidlel
ND <https://portal.nature.cz/publik_syst/ctihtmlpage.php?what=4910&X=X>`__
