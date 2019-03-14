# -*- coding: utf-8 -*-
"""
/***************************************************************************
 NDOPDownloader
                                 A QGIS plugin
 downlaoder
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2018-12-14
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Oto Kaláb
        email                : oto.kalab@opengeolabs.cz
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt5.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QWidget, QApplication, QCompleter, QComboBox

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .ndop_downloader_dialog import NDOPDownloaderDialog
import os.path
from pathlib import Path
from qgis.utils import iface
from . import ndop
from qgis.core import Qgis

# from PyQt5.QtWidgets import QPushButton
import requests
import tempfile
import csv

class NDOPDownloader:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'NDOPDownloader_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = NDOPDownloaderDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&NDOP Downloader')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'NDOPDownloader')
        self.toolbar.setObjectName(u'NDOPDownloader')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('NDOPDownloader', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/ndop_downloader/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'NDOP Downloader'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&NDOP Downloader'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar
        

    def run(self):
        """Run method that performs all the real work"""
        plugin_path = Path(os.path.dirname(os.path.realpath(__file__)))
        try:
            username, password = ndop.read_config(Path(
                                                  plugin_path,
                                                 '.ndop.cfg'
                                                )
            )
            self.dlg.line_user.setPlaceholderText(username)
            self.dlg.line_pass.setPlaceholderText(10*u"\u25CF")
        except:
            pass

        #stažení číselníku - dá se úplně bokem a vytvoří se soubor s číselníky
        import json

        # def get_numberer(filt_par):
            # s = requests.Session()
            # url = ("https://portal.nature.cz/nd/nd_modals/"
                   # "modals.php?opener={}&promka=").format(filt_par)
            # ls = s.get(url).text
            # json_string = ls[9:-1]
            # num_dict = json.loads(json_string)
            
            # return num_dict

        def get_numberer(filt_par):
            with open(Path(plugin_path,'cdb',filt_par+'.csv')) as f:
                reader = csv.DictReader(f)
                num_dict = list(reader)    

                return num_dict

        # num_t = ["abcde","cdeef","1524654 abcd"]

        # self.dlg.combo_taxon.addItems([""]+num_t)
        
        num_t = get_numberer("rfTaxon")
        self.dlg.combo_taxon.clear()
        self.dlg.combo_taxon.completer().setCompletionMode(0)
        self.dlg.combo_taxon.addItems([""]+[d['col1'] for d in num_t])
        
        num_reg = get_numberer("multiple")
        self.dlg.combo_region.clear()
        self.dlg.combo_region.completer().setCompletionMode(0)
        self.dlg.combo_region.addItems([""]+[d['col1']+' - '+ d['type'] for d in num_reg])

        self.dlg.mQgsFileWidget.setStorageMode(1)
        mQgsFileWidget_def = "Uložit do dočasných souborů"
        self.dlg.mQgsFileWidget.setFilePath(mQgsFileWidget_def)
        
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed

        if result:
            try:
                username, password = ndop.read_config(Path(
                                                      plugin_path,
                                                     '.ndop.cfg'
                                                    )
                )
            except:
                username = self.dlg.line_user.text()
                password = self.dlg.line_pass.text()
                if self.dlg.pass_check.isChecked():
                    import configparser
                    config = configparser.ConfigParser()
                    config['login'] = {'username': username,'password': password}
                    with open(Path(plugin_path,'.ndop.cfg'), 'w') as configfile:
                        config.write(configfile)

            taxon = self.dlg.combo_taxon.currentText()
            region = self.dlg.combo_region.currentText()

#           polygon=self.dlg.mMapLayerComboBox.currentLayer()

            search_payload = ndop.get_search_pars(taxon=taxon)
            
            if region == '':
                region = None
            else:
                #toto je zatím tady protože to v bin/ndop nefunguje pro
                # plugintak jak má kvůli konkrétnímu výběru v comboboxu.
                # Funkce se tam musí doladit.
                for i in num_reg:
                    if i['col1'] == region.startswith(i['col1']):
                        region = i
                        reg_type = i['type']
                        if reg_type == 'KU':
                            search_payload['rfKatastr'] = i['val']
                        elif reg_type == 'MZCHU':
                            search_payload['rfMZCHU'] = i['val']
                        elif reg_type == 'EVL':
                            search_payload['rfEVL'] = i['val']
                        elif reg_type == 'VZCHU':
                            search_payload['rfVZCHU'] = i['val']
                        elif reg_type == 'PO':
                            search_payload['rfPO'] = i['val']

                        
            if self.dlg.mQgsFileWidget.filePath () == mQgsFileWidget_def:
                self.dlg.mQgsFileWidget.setFilePath(tempfile.gettempdir())

            data_path = self.dlg.mQgsFileWidget.filePath()

            # data_path = Path(plugin_path,"downloaded_data")



            def mess_bar (head,desc,level,duration=5):
                iface.messageBar().clearWidgets()
                iface.messageBar().pushMessage(head, desc, level, duration)
                self.iface.mainWindow().repaint()

            # def show_cancel():
                # iface.messageBar().clearWidgets()
                # return iface.messageBar().pushMessage("Přerušeno", "Akce přerušena uživatelem", level=Qgis.Warning)

            # def mess_bar_butt (head,desc,level,duration):
                # iface.messageBar().clearWidgets()
                # widget = iface.messageBar().createMessage(head,desc)
                # print(widget)
                # button = QPushButton(widget)
                # button.setText("Zrušit")
                # button.pressed.connect(show_cancel)
                # widget.layout().addWidget(button)
                # iface.messageBar().pushWidget(widget, level, duration)
                # self.iface.mainWindow().repaint()

            # mess_bar("Testování dotazu", "Hledám zadané parametry v číselnících", level=Qgis.Info, duration = 0)

            # if taxon != "":
                # if taxon.lower() not in ls_t.lower():
                    # return mess_bar("Taxon nenalezen!"
                                    # , "Neplatný název taxonu. Zadejte prosím přesný název"
                                    # ,Qgis.Warning
                                    # ,5
                    # )

            mess_bar("Přihlašování", "Přihlášení do systému ISOP", level=Qgis.Info, duration = 0)
      
            try:
                s = ndop.login(username, password)
            except:
                return mess_bar("Hups", "Přihlášení selhalo ", level=Qgis.Critical)

            mess_bar("Filtrování", "Dotazování databáze (odhadovaná doba: 1 minuta)", level=Qgis.Info, duration = 0)
            # mess_bar_butt("Stahování", "Dotazování databáze (odhadovaná doba: 1 minuta)", Qgis.Info, 0)
            
            try:
                table_payload, num_rec = ndop.search_filter(s,search_payload)

            except:
                return mess_bar("Hups", "Filtrování selhalo", level=Qgis.Critical)

            def showError():
                return mess_bar("Konec", "Akce zrušena", level=Qgis.Warning)

            mess_bar("Stahování", "Stahování lokalizací - počet záznamů: "+str(num_rec)+" (odhadovaná doba: 1 minuta)", Qgis.Info, 0)
            # mess_bar_butt("Stahování", "Stahování lokalizací - počet výsledků: "+str(num_rec)+" (odhadovaná doba: 1 minuta)", Qgis.Info, 0)

            if taxon != "":
                file_names = taxon.replace(" ", "_")
            else:
                file_names = region['val'].replace(" ", "_").replace(":","")
                
            try:
                ndop.get_ndop_shp_data(s,str(Path(data_path,file_names)))
            except:
                return mess_bar("Hups", "Stahování selhalo", level=Qgis.Critical)

            mess_bar("Stahování", "Stahování tabulek - počet záznamů: "
                    + str(num_rec)
                    + " (odhadovaná doba: "
                    + str((int(num_rec/500)+(num_rec % 500 > 0))*30/60.0)
                    + " minuty)"
                    , level=Qgis.Info, duration = 0
            )

            try:
                ndop.get_ndop_csv_data(s,num_rec,table_payload,str(Path(data_path,file_names)))
            except:
                return mess_bar("Hups", "Stahování selhalo", level=Qgis.Critical)

            for filename in os.listdir(data_path):
                if filename.endswith("zip") and filename.startswith(file_names):
                    layer = iface.addVectorLayer(str(Path(data_path,filename)), "", "ogr")
                    if not layer:
                        print("Layer failed to load!")
                
                if filename.endswith(".csv") and filename.startswith(file_names):
                    uri = (
                        'file://{}?type=csv&detectTypes=yes&crs={}&'
                        'delimiter={}&xField={}&yField={}&decimalPoint={}'
                    ).format(
                        str(Path(data_path,filename)),
                        "EPSG:5514", ",", "X", "Y", ","
                    )
                    layer = iface.addVectorLayer(
                        uri, "centroids_"+filename, "delimitedtext"
                    )

            mess_bar("Hotovo", "Data stažena do složky: <a href='file://{0}'>{0}/</a>".format(data_path), level=Qgis.Success, duration = 10)
