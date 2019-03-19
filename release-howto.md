# Howto release NDOP Downloader

two different release packages:

- QGIS NDOP Downloader `ndop_downloader.py`- OpenGeoLabs QGIS plugins repo
- ndop `__init__.py`, `bin/ndop` - PyPi

## Releases numbering x.x.x

>Release process without bugfix backporting? (till some stable version)

- bugfix (x.x.+1)

    - only QGIS bug - release only QGIS NDOP Downloader
    - only ndop bug - release only ndop
    - if ndop bug affects QGIS - release both

- new functions (x.+1.x)

    - QGIS implementation of ndop function  - release only QGIS NDOP Downloader
    - ndop new function - release only ndop
    - release if releasing bugfixes but also new functionality commited before

    
- main release (+1.x.x)

    - release both (same number)
    - 0 - beta; 1< - stable
    - 1 - database in current state; 2 - refactoring when AOPK change database dramatically (migrate, API, etc.)


# QGIS NDOP Downloader
>todo

1. fix `metadata.txt` - new version etc.
2. fix repo `.xml` - new version etc. (port from `metadata.txt`)
3. make zip
```
pb_tool zip
``` 
4. update `.xml` on ogl repo 
5. upload `.zip` to ogl repo
    
6. changelog
7. create tag on git

# ndop `__init__.py`, `bin/ndop`

Visit https://packaging.python.org/tutorials/packaging-projects/ for further
details

## Requirements

`pip install` 

* setuptools
* wheel 
* twine 

## Steps needed


### Up-to-date configuration files

1. Fix `requirements.txt` file
2. Update `README.md` file
3. Check, if something is needed to be adjusted in `MANIFEST.in`
4. Check `setup.py`, fix the version and possibly packages

5.changelog

### Make package distribution

Create the package

```
python3 setup.py sdist bdist_wheel
```

Make sure, everything is in place

```
ls dist
```

### Upload the package to pypi.org

Do not forget to have account ready for the PyPi.org site

```
python3 -m twine upload dist/*
```

### Make sure, everything works fine

Check https://pypi.org/project/ndop-downloader make sure, available version
corresponds with your last change.

Try `pip install` the package and make sure, correct version is being installed


