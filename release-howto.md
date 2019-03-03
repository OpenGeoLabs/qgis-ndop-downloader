# Howto release NDOP Downloader

Visit https://packaging.python.org/tutorials/packaging-projects/ for further
details

## Requirements

`pip install` 

* setuptools
* wheel 
* twine 

## Steps needed


## Up-to-date configuration files

1. Fix `requirements.txt` file
2. Update `README.md` file
3. Check, if something is needed to be adjusted in `MANIFEST.in`
4. Check `setup.py`, fix the version and possibly packages

## Make package distribution

Create the package

```
python3 setup.py sdist bdist_wheel
```

Make sure, everything is in place

```
ls dist
```

## Upload the package to pypi.org

Do not forget to have account ready for the PyPi.org site

```
python3 -m twine upload dist/*
```

## Make sure, everything works fine

Check https://pypi.org/project/ndop-downloader make sure, available version
corresponds with your last change.

Try `pip install` the package and make sure, correct version is being installed


