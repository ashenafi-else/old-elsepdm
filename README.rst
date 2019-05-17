======
Common
======

Common is a simple Django test app.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "common" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'common',
    ]

2. Include the common URLconf in your project urls.py like this::

    path('common/', include('common.urls')),

3. Run `python manage.py migrate` to create the common models.

4. Visit http://127.0.0.1:8000/common to participate in the common.
