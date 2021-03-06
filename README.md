# Foreign Exchange Rate Viewer

This application will display exchange rates sourced from the [US
Federal Reserve](https://www.federalreserve.gov/).

The latest available rates are displayed relative to the Euro by
default.  This can be changed by selecting a different *base
currency*.  A timeseries of exchange rates of a single *target
currency* relative to the base is displayed graphically.  The target
can be changed by selecting one of current rates.  The time range of
the graph is selectable also.

The exchange timeseries values are displayed in a table and there is a
link that allows this selected time series to be downloaded in *CSV*
format.

Current financial news is displayed in a sidebar next to the exchnage
rate data.

## Installation

1. Clone this repository.

```
$ git clone https://github.com/inyotech/django-forex
```

2. (optional) create and activate a local python virtual environment
for python dependencies.

```
$ python -m venv venv

$ source venv/bin/activate
```

3. Install the required packages.

```
$ pip install -r requirements.txt
```

4. Configure the settings.

```
$ pushd forex/forex
$ cp settings.py.dist settings.py
# Edit settings.py as required
$ popd
```

5. Initialize the application database and download data.

```
$ python initialize.py
```
