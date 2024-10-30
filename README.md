# superset-python-client

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![PyPI version](https://badge.fury.io/py/superset-api-client.svg)](https://badge.fury.io/py/superset-api-client)
[![Coverage Status](https://coveralls.io/repos/github/opus-42/superset-api-client/badge.svg?branch=develop)](https://coveralls.io/github/opus-42/superset-api-client?branch=develop)

A Python Client for Apache Superset REST API.

This is a Alpha version. Stability is not guaranteed.

## Usage

Setup a superset client:

```python3
from supersetapiclient.client import SupersetClient

client = SupersetClient(
    host="http://localhost:8080",
    username="admin",
    password="admin",
)
```

When developping in local (only), you may need to accept insecure transport (i.e. http).
This is NOT recommanded outside of local development environement, that is requesting `localhost`.

```python3
import os

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
```

### Quickstart

Get all dashboards or find one by name:

```python3
# Get all dashboards
dashboards = client.dashboards.find()

# Get a dashboard by name
dashboard = client.dashboards.find(dashboard_title="Example")[0]
```

To delete a dashboard:

```python3
dashboard.delete()
```

Update dashboard colors, some properties and save changes to server:

```python3
# Update label_colors mapping
print(dashboard.colors)
dashboard.update_colors({
    "label": "#fcba03"
})
print(dashboard.colors)

# Change dashboard title
dashboard.dashboard_title = "New title"

# Save all changes
dashboard.save()
```

Get the embed configuration for a dashboard:

```python3
embed = dashboard.get_embed()
```

Create the embed configuration for a dashboard:

```python3
embed = dashboard.create_embed(allowed_domains=[])
```

Copy a dashboard:

```python3
dashboard_copy = dashboard.copy_dashboard(dashboard_payload={
    "css": "",
    "dashboard_title": "your-new-dashboard-title",
    "duplicate_slices": False,
    "json_metadata": "{}",
})
```

### Export one ore more dashboard

You may export one or more dashboard user `client.dashboards` or directly on a `dashboard` object

```python3
# Export many dashboards
client.dashboards.export(
    # Set dashboard ids you would like to export
    [
        1,
        2
    ],
    "./dashboards.json" # A string or a path-like object where export will be saved
)

# Export one dashboard
dashboard.export(
    "./dashboard.json"
)
```

This functionality is also available in the same manner for datasets

### CSS Templates

```python3
# Get all CSS Templates
css_templates = client.css_templates.find()

# Get a CSS Template by name
css_template = client.css_templates.find(template_name="Flat")[0]

# Retrieve the CSS of a CSS Template
css = css_template.css
```

### Retrieve a Guest Token

You can retrieve a guest token using the `guest_token` method. This method requires the UUID of the resource (e.g., dashboard) and uses the user's first name, last name, and username from the client instance.

```python3
# Retrieve a guest token
guest_token = client.guest_token(uuid="your-example-uuid")
```

# Contributing

Before committing to this repository, you must have [pre-commit](https://pre-commit.com) installed, and install
the following pre-commit hooks:

```sh
pre-commit install --install-hooks -t pre-commit -t pre-push
```

## Setting up a development envi

You will need Docker and docker-compose in order to run development environment.
To start development environment run:

```bash
    docker-compose up -d
```
