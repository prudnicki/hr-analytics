# Simple HR analytics app

## Getting started

Clone git repo to local directory:

```
$ git clone https://github.com/prudnicki/hr-analytics.git
```

## Prerequisites

This app uses `pipenv` for dependency management and virtual environments.
Make sure that `pipenv` is installed:

```
$ pip3 install -U pipenv
```

## Installing

Setup the environment:

```
$ pipenv lock
$ pipenv sync
```

This app uses SQLite3 by default. Create database and necessary tables by executing:

```
$ pipenv run flask db upgrade
```

## Run

Run the app by executing:

```
$ pipenv run flask run
```

Navigate to `http://127.0.0.1:5000` in your browser to see the application.


## Importing sample data

Application's database does not contain any data initially. You can populate it with some data by navigating to `Upload`
tab and providing it with a CSV file. Sample CSV fil is included in the repo: [sample_data.csv](./sample_data.csv).
To see the statistics make sure your start_date is around 2014.

   
## Approach

I chose web app with SQL backend for several reasons:
* nice user interface for querying the data as opposed to constructing some kind of query language
* leveraging SQL as durable data backend with enabling efficient development of future requirements
* to show extra effort :)

Even though requirements stated we need to answer different queries, at the time data is simple enough that I felt
like I can satisfy those requirements using single form and screen that shows count and conversion rates 
for all pipeline stages at once.

Analytics form: use of start_date and end_date fields is pretty obvious, but pipeline stages selection probably 
deserves additional explanation. Let's assume we are doing analysis on candidates that had a entry in pipeline database
in time period 01.01.2019 until 31.01.2019. Selecting a pipeline stage in form field will make sure that only candidates
that reached one of selected stages in given time period are taken into account. This allows us to analyze a subset
of candidates (like 'candidates that were interviewed or screened during given time period').  