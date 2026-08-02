# Waypoint

Waypoint is my individual term project for CCGC-5003 Application Programming.

I began the project as a pure-Python object-oriented domain engine and am developing it into a Django trail-finder website.

## Current development stage

Week 11 shared templates and data-driven trail catalog.

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
- Automated Django tests

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
- A catalog route at `/catalog/`
- Six trail dictionaries rendered through a Django template loop
- Automatic row numbering with `forloop.counter`
- Conditional `CLOSED`, `HARD`, and difficulty badges
- Distance formatting with the `floatformat:1` template filter
- A shared Catalog link across the homepage, search page, report page, confirmation page, and catalog
- Django tests for catalog content, formatting, badges, numbering, and shared navigation

The Week 11 catalog currently uses trail dictionaries supplied by the view. In Week 12, these temporary records will be replaced by Django model instances stored in the database.

## Website routes

- `/` displays the Waypoint homepage.
- `/catalog/` displays the temporary data-driven trail catalog.
- `/report/` displays and processes the trail-report form.
- `/search/` displays the trail search page.
- `/search/?q=Lake` searches for matching trail names.
- `/admin/` displays the Django administration login page.

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

Apply the Django migrations:

```powershell
python manage.py migrate
```

Check the Django configuration:

```powershell
python manage.py check
```

Run the complete test suite:

```powershell
python manage.py test
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

The current project contains 60 tests.

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

### A POST request returns `403 Forbidden`

Confirm that the form contains:

```django
{% csrf_token %}
```

Django rejects a POST request without a valid CSRF token to protect the application from cross-site request-forgery attacks.

## AI-assistance disclosure

I used substantial AI assistance for project planning, implementation guidance, code explanations, test design, documentation, and error troubleshooting. 
I personally ran and verified all commands and tests recorded as completed.