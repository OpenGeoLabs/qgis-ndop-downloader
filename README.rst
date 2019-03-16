NDOP Downloader
===============

NDOP Downloader is an application for downloading of records of species
occurence from official database of the Nature Conservation Agency of
the Czech Republic `Nálezová databáze ochrany přírody AOPK ČR
<https://portal.nature.cz/nd/>`_. This package only provides access
to the data, please visit the official databse site for additional
information about the data, the database, license terms and reference
rules.

To use the database, it is **necessary** to `create an account
<https://idm.nature.cz/idm/#/registration>`_ in the AOPK (ISOP)
information system.

Download data (.csv, .shp) from NDOP based on input parametres. Unlike
the offical web filter, its possible to input polygon layer (EPSG:5514)
for search in area and amount of results is not limited. Login can be
stored in configuration file ".ndop.cfg".

This package is a part of NDOP Downloader QGIS plugin. Whole project is
maintained on `GitHub <https://github.com/OpenGeoLabs/qgis-ndop-downloader>`_
