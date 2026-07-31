# Waypoint

Waypoint is an individual term project for CCGC-5003 Application Programming.

The project begins as a pure-Python object-oriented domain engine and later develops into a Django trail-finder website.

## Current development stage

Week 8 domain hierarchy, polymorphism, mixins, and operators.

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
- Method Resolution Order demonstration
- A polymorphic estimated-time loop
- Duck-typed `FakeTrail`
- A validated `Itinerary`
- Independent itinerary trail collections
- Total-distance calculation

## Python version

Python 3.12 is used for compatibility with the Django 4.2 portion of the project.

## Activate the virtual environment

Windows PowerShell:

`.\env\Scripts\Activate.ps1`

## Run the demonstrations

Week 7:

`python demo_week7.py`

Week 8:

`python demo_week8.py`

## Run the tests

From the project root:

`python -m unittest discover -s tests -v`

## Estimated-time formulas

### DayHike

Distance in kilometres divided by hiking pace, plus one hour for every 600 metres of elevation gain.

### BackpackingRoute

Distance in kilometres divided by backpacking pace, plus one hour for every 500 metres of elevation gain, plus 30 minutes for each overnight stop.

### TrailRun

Distance in kilometres divided by running pace, plus one hour for every 900 metres of elevation gain.

### GuidedDayHike

Uses the normal `DayHike` estimate and adds 30 minutes for a safety briefing.

## Mixed-unit policy

When arithmetic or comparisons involve kilometres and miles, the right-hand `Distance` is automatically converted into the left-hand object's unit.

Examples:

- `Distance(5, "km") + Distance(1, "mi")` returns kilometres.
- `Distance(5, "mi") + Distance(1, "km")` returns miles.
- Equality and ordering also convert the right-hand value before comparing.
- Subtraction raises `ValueError` when it would produce a negative distance.

The itinerary uses the same conversion principle by converting every trail into the requested total-distance unit before adding the magnitudes.

## AI-assistance disclosure

I used substantial AI assistance for project planning, implementation guidance, code explanations, test design, documentation, and error troubleshooting. 
I personally ran and verified all commands and tests recorded as completed.