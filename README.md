# Waypoint

Waypoint is an individual term project for CCGC-5003 Application Programming.

The project begins as a pure-Python object-oriented domain engine and later develops into a Django trail-finder website.

## Current development stage

Week 7 domain model completed.

## Week 7 features

The current domain engine includes:

- A validated `Distance` value type
- Kilometre and mile conversion
- Read-only distance accessors
- A validated `Trail` class
- Trail identity equality
- A class-level default distance unit
- A `Trail.from_dict()` alternate constructor
- Static validation methods
- An `Itinerary` containing an ordered collection of trails
- Total-distance calculation
- Independent itinerary trail collections

## Project structure

```text
waypoint-term-project/
├── waypoint_core/
│   ├── __init__.py
│   ├── distance.py
│   ├── itinerary.py
│   └── trail.py
├── tests/
│   ├── __init__.py
│   ├── test_distance.py
│   ├── test_itinerary.py
│   └── test_trail.py
├── demo_week7.py
├── .gitignore
└── README.md