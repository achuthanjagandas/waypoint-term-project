# Waypoint

Waypoint is my individual term project for CCGC-5003 Application Programming.

I began the project as a pure-Python object-oriented domain engine and am developing it into a Django trail-finder website.

## Current development stage

Week 12 database-backed trails, migrations, Django admin, and ORM catalog queries.

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

The project currently includes:

- Python 3.12
- A virtual environment named `env`
- Django 4.2.30
- A `requirements.txt` dependency file
- The Django project package named `waypoint`
- The Django management script `manage.py`
- SQLite for local development
- The existing importable `waypoint_core` package
- Project-level templates
- Project-level static files
- Django forms
- Named URL routes
- Automated pure-Python and Django tests
- A registered Django app named `trails`
- A committed database migration
- Django admin configuration

## Week 10 web features

I added the following Django web features:

- A styled Waypoint homepage
- Shared project-level templates and static CSS
- Context variables rendered in the homepage template
- Named URL routes
- A Django trail-report form
- Required-field and email validation
- CSRF protection
- A personalized report-confirmation page
- A trail-name search view
- Safe handling when the `q` query parameter is missing
- Search results and no-results messages

## Week 11 template and catalog features

I added a shared Django template layout and a data-driven trail catalog.

The Week 11 work includes:

- A shared `base.html` template
- A reusable navbar partial
- A reusable footer partial
- Existing pages refactored to extend the shared base template
- A catalog page rendered through a Django template loop
- Six temporary trail dictionaries
- Automatic row numbering with `forloop.counter`
- Conditional `CLOSED`, `HARD`, and difficulty badges
- Distance formatting with the `floatformat:1` template filter
- Shared navigation across the homepage, catalog, search page, report page, and confirmation page
- Django tests for catalog content, formatting, badges, numbering, and shared navigation

The temporary Week 11 dictionaries were replaced by database-backed model records during Week 12.

## Week 12 ORM and admin features

I replaced the temporary Week 11 catalog dictionaries with database-backed Django model records.

The Week 12 work includes:

- A registered Django app named `trails`
- A database-backed `Trail` model
- A `DecimalField` for trail distance
- An integer field for elevation gain
- Difficulty choices for Easy, Moderate, and Expert
- An `is_open` availability field
- An automatically generated `added` timestamp
- Minimum-value validators for distance and elevation gain
- A readable `__str__()` representation
- A committed initial migration
- Django admin registration
- Admin list columns
- Trail-name searching in Django admin
- Admin filters for difficulty and availability
- Alphabetical admin ordering
- App-level URLs mounted under `/trails/`
- An ORM query that returns only open trails
- Database records ordered by distance
- Reuse of the Week 11 catalog template with Django model instances
- Automated model, routing, query, formatting, catalog, and navigation tests

The public catalog uses this ORM query:

```python
Trail.objects.filter(is_open=True).order_by("distance_km")
```

Closed trails remain manageable through Django admin but are excluded from the public catalog.

## Website routes

- `/` displays the Waypoint homepage.
- `/trails/` displays open database trails ordered by distance.
- `/report/` displays and processes the trail-report form.
- `/search/` displays the trail search page.
- `/search/?q=Lake` searches the temporary trail-name data.
- `/admin/` displays the Django administration login page.
- `/admin/trails/trail/` allows an administrator to manage trail records.

## Project structure

```text
waypoint-term-project/
├── static/
│   └── style.css
├── templates/
│   ├── partials/
│   │   ├── footer.html
│   │   └── navbar.html
│   ├── base.html
│   ├── catalog.html
│   ├── home.html
│   ├── report_form.html
│   ├── report_thanks.html
│   └── search.html
├── tests/
│   ├── __init__.py
│   ├── test_distance.py
│   ├── test_distance_operators.py
│   ├── test_itinerary.py
│   ├── test_trail.py
│   └── test_week8_mixins.py
├── trails/
│   ├── migrations/
│   │   ├── __init__.py
│   │   └── 0001_initial.py
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── waypoint/
│   ├── __init__.py
│   ├── asgi.py
│   ├── forms.py
│   ├── settings.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── wsgi.py
├── waypoint_core/
│   ├── __init__.py
│   ├── distance.py
│   ├── guided.py
│   ├── itinerary.py
│   ├── mixins.py
│   ├── polymorphism.py
│   └── trail.py
├── demo_week7.py
├── demo_week8.py
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md
```

The local `env/`, `db.sqlite3`, `__pycache__/`, and compiled Python files are intentionally excluded from Git.

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

Activate the virtual environment in Windows PowerShell:

```powershell
.\env\Scripts\Activate.ps1
```

For Command Prompt:

```text
env\Scripts\activate.bat
```

For macOS or Linux:

```bash
source env/bin/activate
```

Install the dependencies:

```powershell
python -m pip install -r requirements.txt
```

Check the Django configuration:

```powershell
python manage.py check
```

Apply the Django migrations:

```powershell
python manage.py migrate
```

Confirm the `trails` migration:

```powershell
python manage.py showmigrations trails
```

Expected migration status:

```text
trails
 [X] 0001_initial
```

Run the complete test suite:

```powershell
python manage.py test
```

Start the development server:

```powershell
python manage.py runserver
```

Open the homepage:

```text
http://127.0.0.1:8000/
```

Open the public trail catalog:

```text
http://127.0.0.1:8000/trails/
```

Stop the server by pressing `Ctrl + C` in the terminal.

A fresh clone contains the database schema after migration but does not contain the trail records created in another local database. Trail records can be added through Django admin after creating a local superuser.

## Create a local administrator account

Create a superuser:

```powershell
python manage.py createsuperuser
```

Django will request a username, email address, and password.

Start the server:

```powershell
python manage.py runserver
```

Open Django admin:

```text
http://127.0.0.1:8000/admin/
```

The superuser and trail records are stored only in the local `db.sqlite3` database, which is excluded from Git.

## Run the demonstrations

Run the Week 7 demonstration:

```powershell
python demo_week7.py
```

Run the Week 8 demonstration:

```powershell
python demo_week8.py
```

## Run only the pure-Python tests

The following command runs the domain-engine tests stored in the top-level `tests` directory:

```powershell
python -m unittest discover -s tests -v
```

The current project contains 56 pure-Python tests.

## Run the complete test suite

The following command runs the pure-Python tests and the Django tests together:

```powershell
python manage.py test
```

The current project contains 63 tests.

Django creates a temporary test database while running the Django tests and destroys it when the tests finish.

## Trail catalog behaviour

The public trail catalog:

- Uses records stored in the database
- Displays only trails where `is_open=True`
- Orders visible trails from shortest to longest
- Formats distance values to one decimal place
- Displays `HARD` for open expert trails
- Uses the shared Week 11 catalog template
- Updates automatically when trail records are changed in Django admin

Closed trails do not appear on the public catalog.

## Estimated-time formulas

### DayHike

I calculate the estimated time by dividing the distance in kilometres by the hiking pace and adding one hour for every 600 metres of elevation gain.

### BackpackingRoute

I calculate the estimated time by dividing the distance in kilometres by the backpacking pace, adding one hour for every 500 metres of elevation gain, and adding 30 minutes for each overnight stop.

### TrailRun

I calculate the estimated time by dividing the distance in kilometres by the running pace and adding one hour for every 900 metres of elevation gain.

### GuidedDayHike

I use the normal `DayHike` estimate and add 30 minutes for a safety briefing.

## Mixed-unit policy

When arithmetic or comparisons involve kilometres and miles, I convert the right-hand `Distance` into the left-hand object's unit.

Examples:

- `Distance(5, "km") + Distance(1, "mi")` returns kilometres.
- `Distance(5, "mi") + Distance(1, "km")` returns miles.
- Equality and ordering convert the right-hand value before comparing.
- Subtraction raises `ValueError` when it would produce a negative distance.

The itinerary follows the same principle by converting every trail into the requested total-distance unit before adding the magnitudes.

## Troubleshooting

### PowerShell blocks virtual-environment activation

Run this command for the current terminal session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate the environment again:

```powershell
.\env\Scripts\Activate.ps1
```

### `django-admin` or Django is unavailable

Confirm that the virtual environment is active. The terminal prompt should begin with:

```text
(env)
```

Then reinstall the requirements if necessary:

```powershell
python -m pip install -r requirements.txt
```

### `TemplateDoesNotExist`

Confirm that the project-level template directory is configured in `waypoint/settings.py` and that the required file exists inside `templates/`.

### The trail catalog is empty after a fresh clone

This is expected because `db.sqlite3` is not committed.

Apply the migrations:

```powershell
python manage.py migrate
```

Create a superuser:

```powershell
python manage.py createsuperuser
```

Then add trail records through:

```text
http://127.0.0.1:8000/admin/trails/trail/
```

### A POST request returns `403 Forbidden`

Confirm that the form contains:

```django
{% csrf_token %}
```

Django rejects a POST request without a valid CSRF token to protect the application from cross-site request-forgery attacks.

## AI-assistance disclosure

I used substantial AI assistance for project planning, implementation guidance, code explanations, test design, documentation, and error troubleshooting.
I personally ran and verified all commands and tests recorded as completed.