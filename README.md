# Waypoint

Waypoint is my individual term project for CCGC-5003 Application Programming.

I began the project as a pure-Python object-oriented domain engine and am developing it into a Django trail-finder website.

## Current development stage

Week 13 Park-to-Trail relationships, ForeignKey migrations, protected deletion, and relationship-based catalog filtering.

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
- A database-backed `Park` model
- A database-backed `Trail` model
- A required Park-to-Trail ForeignKey
- Three committed Trail-app migrations
- Django admin configuration for Parks and Trails

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
- A readable Trail `__str__()` representation
- A committed initial migration
- Django admin registration
- Admin list columns
- Trail-name searching in Django admin
- Difficulty and availability filters
- Alphabetical admin ordering
- App-level URLs mounted under `/trails/`
- An ORM query that returns only open Trails
- Database records ordered by distance
- Reuse of the shared catalog template with Django model instances
- Automated model, routing, query, formatting, catalog, and navigation tests

The public catalog begins with this ORM query:

```python
Trail.objects.filter(is_open=True).order_by("distance_km")
```

Closed Trails remain manageable through Django admin but are excluded from the public catalog.

## Week 13 relationship and ForeignKey features

I added a database-backed `Park` model and connected every `Trail` to a Park through a required Django `ForeignKey`.

The Week 13 work includes:

- A `Park` model with `name` and `region` fields
- Alphabetical Park ordering
- A readable Park `__str__()` representation
- A required `ForeignKey` from `Trail` to `Park`
- A reverse relationship through `park.trails`
- Protected Park deletion through `on_delete=models.PROTECT`
- Park administration with list columns and search
- Park information in the Trail administration list
- Trail searching through related Park fields
- Park, difficulty, and availability filters in Django admin
- Three Park records assigned across all six local Trail records
- Park names and regions displayed in the public catalog
- A public Park-selection dropdown
- Cross-relation filtering of open Trails by Park
- Safe handling of invalid Park query-string values
- Automated Park model, reverse-relationship, protected-deletion, required-relationship, display, and filtering tests

The relationship is defined with:

```python
park = models.ForeignKey(
    Park,
    on_delete=models.PROTECT,
    related_name="trails",
)
```

The reverse relationship allows a Park to retrieve its Trails with:

```python
park.trails.all()
```

The catalog retrieves each Trail and its related Park efficiently with:

```python
Trail.objects.filter(is_open=True).select_related("park")
```

When a Park is selected, the catalog applies:

```python
trails.filter(park=selected_park)
```

### Existing-row migration strategy

I introduced the relationship in two database migrations so that the six existing Trail records were preserved.

First, migration `0002_park_trail_park.py`:

- Created the `Park` table
- Added a temporarily nullable `park` field to `Trail`
- Preserved all six existing Trail records

I then:

- Created three real Park records
- Assigned a Park to every existing Trail
- Verified that zero Trails had a missing Park

Finally, migration `0003_alter_trail_park.py` removed the temporary nullable setting and made the relationship mandatory.

I did not provide a fake default Park because every existing Trail was deliberately assigned to a real Park before the required database constraint was applied.

### Protected deletion policy

I use:

```python
on_delete=models.PROTECT
```

This prevents an administrator from deleting a Park while Trail records still reference it.

The related Trails must first be reassigned or removed. This protects the relationship and prevents Trails from pointing to a Park that no longer exists.

## Website routes

- `/` displays the Waypoint homepage.
- `/trails/` displays all open database Trails ordered by distance.
- `/trails/?park=<park-id>` displays open Trails belonging to the selected Park.
- `/report/` displays and processes the trail-report form.
- `/search/` displays the trail search page.
- `/search/?q=Lake` searches the temporary trail-name data.
- `/admin/` displays the Django administration login page.
- `/admin/trails/park/` allows an administrator to manage Park records.
- `/admin/trails/trail/` allows an administrator to manage Trail records and assign Parks.

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
│   │   ├── 0001_initial.py
│   │   ├── 0002_park_trail_park.py
│   │   └── 0003_alter_trail_park.py
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

The local `env/`, `db.sqlite3`, `__pycache__/`, compiled Python files, administrator accounts, and locally created Park and Trail records are intentionally excluded from Git.

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

Confirm the Trail-app migrations:

```powershell
python manage.py showmigrations trails
```

Expected migration status:

```text
trails
 [X] 0001_initial
 [X] 0002_park_trail_park
 [X] 0003_alter_trail_park
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

A fresh clone contains the recreated database structure after migrations, but it does not contain the administrator account, Parks, or Trails created in another local database.

The empty public catalog is therefore expected after a fresh clone.

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

The superuser is stored only in the local `db.sqlite3` database.

## Add local Park and Trail records

Because every Trail requires a Park, create Park records before creating Trail records.

Open:

```text
http://127.0.0.1:8000/admin/trails/park/
```

Create the required Parks.

Then open:

```text
http://127.0.0.1:8000/admin/trails/trail/
```

Create Trail records and assign one Park to every Trail.

Local Park and Trail data is stored inside `db.sqlite3`, which is excluded from Git.

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

The current project contains 70 tests.

Django creates a temporary test database while running the Django tests and destroys it when the tests finish.

## Trail catalog behaviour

The public trail catalog:

- Uses Trail records stored in the database
- Displays only Trails where `is_open=True`
- Orders visible Trails from shortest to longest
- Retrieves related Park information with `select_related("park")`
- Displays each Trail’s Park name and region
- Allows the user to filter open Trails by Park
- Safely ignores invalid Park query-string values
- Formats distance values to one decimal place
- Displays `HARD` for open expert Trails
- Uses the shared catalog template
- Updates automatically when Trail or Park relationships are changed in Django admin

Closed Trails do not appear in the public catalog.

Filtering by Greenwood Forest Park displays:

- Forest Ridge
- Pine Valley Route

## Park and Trail relationship behaviour

Each Trail must reference one Park.

A Park may contain multiple Trails through:

```python
park.trails.all()
```

Django admin allows an administrator to:

- Create Parks
- Search Parks by name or region
- Assign a Park to each Trail
- Search Trails by Trail name, Park name, or Park region
- Filter Trails by Park, difficulty, or availability

Django prevents deletion of a Park while Trails still reference it.

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

The itinerary follows the same principle by converting every Trail into the requested total-distance unit before adding the magnitudes.

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

Create Park records through:

```text
http://127.0.0.1:8000/admin/trails/park/
```

Then create Trail records and assign their Parks through:

```text
http://127.0.0.1:8000/admin/trails/trail/
```

### A Trail cannot be created without a Park

This is expected because the Park relationship is required.

Create at least one Park first and select it when creating the Trail.

### A Park cannot be deleted

Django prevents a Park from being deleted when one or more Trails reference it.

Reassign or delete the related Trails before attempting to delete the Park.

### A POST request returns `403 Forbidden`

Confirm that the form contains:

```django
{% csrf_token %}
```

Django rejects a POST request without a valid CSRF token to protect the application from cross-site request-forgery attacks.

## AI-assistance disclosure

I used substantial AI assistance for project planning, implementation guidance, code explanations, test design, documentation, and error troubleshooting.
I personally ran and verified all commands and tests recorded as completed.