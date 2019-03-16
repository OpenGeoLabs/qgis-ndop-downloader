# NDOP Downloader

NDOP Downloader je aplikace, která slouží ke stahování nálezů z
[Nálezové databáze ochrany přírody AOPK ČR](https://cs.wikipedia.org/wiki/N%C3%A1lezov%C3%A1_datab%C3%A1ze_ochrany_p%C5%99%C3%ADrody).
Aplikace je dostupná ve dvou formách, jako **QGIS zásuvný modul**, jehož
základ tvoří Python balíček *ndop-downloader* s nástrojem příkazové řádky **ndop**.

NDOP Downloader pouze zprostředkovává přístup k datům. Veškeré informace
o datech - fungování databáze, licenční podmínky, citační pravidla týkající
se dat naleznete na stránkách
[Nálezové databáze](https://portal.nature.cz/nd/).

**Pro použití** databáze je **nutné
[vytvořit účet](https://idm.nature.cz/idm/#/registration)** v informačním
systému AOPK (ISOP).


## QGIS Plugin - NDOP Downloader
Zásuvný modul slouží ke stahování dat z nálezové databáze AOPK. V
současné verzi je možné filtrovat na základě taxonu (druh,popř. rod)
a definovaných regionů (katastrální území, CHKO, PP, atd.).

Výstupem jsou dostupná data lokalizací (.shp komprimované v .zip)
a tabulková data (.csv) pro všechny záznamy. Lokalizace se po ukončení
stahování nahrají do projektu. Tabulková data se nahrají do projektu
jako `Oddělený text` a zobrazí se jako body (na základě souřadnic v
tabulce). Tato data obsahují body a centroidy většiny polygonů a linií.

![](static/images/main.png)

### Instalace a Spouštění

Zásuvný modul předpokládá verzi LTR QGIS 3.4. Instaluje se jako ostatní
moduly pomocí menu `Zásuvné moduly --> Spravovat a instalovat zásuvné moduly`.
Je ale nutné přidat externí repozitář OpneGeoLabs. V záložce nastavení klikneme
na tlačítko `Přidat...` a zadáme adresu:

    adresa k repozitáři

    screenshot

Aktualizujeme seznam modulů tlačítkem `Reload repository`. Nyní už uvidíme
zásuvný modul mezi ostatními v záložce `Nenainstalované` (nebo `Vše`.
Vyhledáme `NDOP Downloader`, a nainstalujeme pomocí tlačítka
`Instalvoat zásuvný modul`

    screenshot

Po instalaci se přidá do menu `Zásuvné moduly` položka `NDOP Downloader`
a pro rychlé spuštění se objeví ikonka v liště.

### Popis rozhraní

![](static/images/dialog.png)


#### Přihlášení

Zadejte přihlašovací údaje pro informačním systém AOPK (ISOP). Pokud
zaškrtnete položku `Uložit přihlašovací údaje`, údaje se uloží do
konfiguračního souboru a při dalším použití budou předvyplněny. V opačném
případě budou údaje uložené pouze v rámci běžící instance QGIS, při dalším
spuštění QGIS je bude potřeba zadat znovu.

    obrázek předvyplněých údajů

#### Taxon

Druh lze vybrat pomocí rolovací nabídky, nebo vepsáním názvu s funkcí
našeptávače. Lze zadávat česká i latinská jména.

![](static/images/filter_taxon.gif)   

#### Region

Obdobně jako u taxonu. V případě že položka zůstane nevyplněná, získáme
data z clého území ČR. Naopak, pokud vybyreme území regionu a necháme
prázdné políčko taxonu, získáme data všech taxonů ve vybraném regionu.

![](static/images/filter_region.png)

#### Výstupní složka


Vybereme výsupní složku kam se nám data uloží. Pokud ponecháme prázdné,
stáhnou se data do složky dočasných souborů. V případě, že nechceme
stahovat tabulková data zaškrtneme možnost `Nestahovat tabulková data`.

Stažené soubory se nahrají do projektu a ponesou název odvozený od
použitého filtru a typu dat.

Příklad:

- `Mantis_religiosa_shp_b` - bodová vrstva (.shp)
- `Mantis_religiosa_shp_p` - polygonová vrstva (.shp)
- `Mantis_religiosa_shp_l` - liniová vrstva (.shp)
- `Mantis_religiosa_tab` - tabulková data (.csv), v projektu se zobrazí
body (souřadnice ze sloupečků `X` a `Y`)

Pokud je do filtru zadán taxon, bude název odvozen od názvu druhu. Poukd
filtrujeme pouze podle regionu bude název odvozen od názvu regionu.

### Průběh stahování

Po potvrzení tlačítkem `Ok` se okno zavře a spustí se filtrace a
stahování. QGIS během stahování **nelze v současné době používat**.
Stejně jako při použití oficiální webové aplikace, stahování může trvat
několik minut, v závislosti na počtu záznamů, stažení tabulkových dat atd.

![](static/images/message.png)

V informačním panelu v horní části obrazovky uvidíte informace o průběhu
stahování. Při stahování se také vypíše počet záznamů a hrubý odhad doby
trvání konkrétního kroku. Po úspěšném stažení se objeví zelený panel s
odkazem na složku kam byla data stažena.

![](static/images/result.png)

### Plánované funkce - zpětná vazba

Výběr plánovaných funkcí:

- zadání oblasti tažením a použítím polygonu z vrstvy
- přidání filtru druhové ochrany
- automatické vytvoření relace tabulkových dat a lokalizací (1:n)

seznam aktuálně plánovaných funkcí [zde](https://github.com/OpenGeoLabs/qgis-ndop-downloader/issues?q=is%3Aopen+is%3Aissue+label%3Aenhancement) 

Pro připomínky, nápady a hlášení chyb můžete napsat email nebo použít [issues projektu na GitHub ](https://github.com/OpenGeoLabs/qgis-ndop-downloader/issues).

## Python balíček - ndop-downloader

Po nainstalování balíčku ndop-downloader lze pro stahování dat využít
nástroj příkazové řádky **ndop**, nebo lze baláček naimportovat do
python skriptu (`import ndop`)

    pip install ndop-downloader
    
    ndop --taxon "mantis religiosa"

    ndop -h

    usage: ndop [-h] [--user USER] [--password PASSWORD] [--output OUTPUT]
                [--taxon TAXON] [--region REGION] [--polygon POLYGON]
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
      --output OUTPUT       path with output filenames prefix
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

...
## Licence
...
## Reference
...
