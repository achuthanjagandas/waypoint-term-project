# Waypoint

Waypoint is my individual term project for CCGC-5003 Application Programming.

I began the project as a pure-Python object-oriented domain engine and am developing it into a Django trail-finder website.

## Current development stage

Week 9 Django project setup.

## Domain-engine features

The current domain engine includes:

- A validated `Distance` value type
- Kilometre and mile conversion
- Read-only distance accessors
- Distance addition and subtraction
- Distance equality and ordering
- Distance sorting
- Readable `str` and developer-focused `repr`
- An abstract `Trail` base class
- Abstract `estimated_time()` and `summary()` methods
- `DayHike`, `BackpackingRoute`, and `TrailRun`
- A further subclass named `GuidedDayHike`
- Method overriding and `super()`
- `ElevationMixin` and `RatingMixin`
- A Method Resolution Order demonstration
- A polymorphic estimated-time loop
- A duck-typed `FakeTrail`
- A validated `Itinerary`
- Independent itinerary trail collections
- Total-distance calculation

## Django setup

The project now includes:

- Python 3.12
- A virtual environment named `env`
- Django 4.2.30
- A `requirements.txt` dependency file
- The Django project package named `waypoint`
- The Django management script `manage.py`
- SQLite for local development
- The existing importable `waypoint_core` package

## Project structure

```text
waypoint-term-project/
├── waypoint/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── waypoint_core/
├── tests/
├── demo_week7.py
├── demo_week8.py
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md

## Python version

I use Python 3.12 because it is compatible with the required Django 4.2 release.

## Setup from a fresh clone

Clone the repository and enter the project folder:

```powershell
git clone https://github.com/achuthanjagandas/waypoint-term-project.git
Set-Location waypoint-term-project
```

Create the required virtual environment:

```powershell
py -3.12 -m venv env
```

Activate the virtual environment:

```powershell
.\env\Scripts\Activate.ps1
```

Install the dependencies:

```powershell
python -m pip install -r requirements.txt
```

Apply the Django migrations:

```powershell
python manage.py migrate
```

Check the Django configuration:

```powershell
python manage.py check
```

Start the development server:

```powershell
python manage.py runserver
```

Open this address in a browser:

```text
http://127.0.0.1:8000/
```

Stop the server by pressing `Ctrl + C` in the terminal.

## Run the demonstrations

Run the Week 7 demonstration:

```powershell
python demo_week7.py
```

Run the Week 8 demonstration:

```powershell
python demo_week8.py
```

## Run the pure-Python tests

```powershell
python -m unittest discover -s tests -v
```

## Estimated-time formulas

### DayHike

I calculate the estimated time by dividing the distance in kilometres by the hiking pace and adding one hour for every 600 metres of elevation gain.

### BackpackingRoute

I calculate the estimated time by dividing the distance in kilometres by the backpacking pace, adding one hour for every 500 metres of elevation gain, 
and adding 30 minutes for each overnight stop.

### TrailRun

I calculate the estimated time by dividing the distance in kilometres by the running pace and adding one hour for every 900 metres of elevation gain.

### GuidedDayHike

I use the normal `DayHike` estimate and add 30 minutes for a safety briefing.

## Mixed-unit policy

When arithmetic or comparisons involve kilometres and miles, I convert the right-hand `Distance` into the left-hand object’s unit.

Examples:

- `Distance(5, "km") + Distance(1, "mi")` returns kilometres.
- `Distance(5, "mi") + Distance(1, "km")` returns miles.
- Equality and ordering convert the right-hand value before comparing.
- Subtraction raises `ValueError` when it would produce a negative distance.

The itinerary follows the same principle by converting every trail into the requested total-distance unit before adding the magnitudes.

## AI-assistance disclosure

I used substantial AI assistance for project planning, implementation guidance, code explanations, test design, documentation, and error troubleshooting. 
I personally ran and verified all commands and tests recorded as completed.