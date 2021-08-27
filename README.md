# tom_dash

This module supplements the TOM Toolkit module with [Plotly Dash](https://plotly.com/dash/) support for more responsive plotting.

Please note that this module is a proof-of-concept and should be considered to be in alpha.

## Installation

Install the module into your TOM environment:

    pip install git+https://github.com/TOMToolkit/tom_dash

Add `tom_dash` and `django_plotly_dash.apps.DjangoPlotlyDashConfig` to the `INSTALLED_APPS` in your TOM's `settings.py`:

```python
    INSTALLED_APPS = [
        'django.contrib.admin',
        ...
        'tom_dataproducts',
        'tom_dash',
        'django_plotly_dash.apps.DjangoPlotlyDashConfig'
    ]
```

Add `STATIC_ROOT = os.path.join(BASE_DIR, '_static')` and the following `STATICFILES_FINDERS` configuration to your `settings.py`, ideally in the `Static files (CSS, JavaScript, Images)` section:

```python
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, '_static')
    MEDIA_ROOT = os.path.join(BASE_DIR, 'data')
    MEDIA_URL = '/data/'

    STATICFILES_FINDERS = [

        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',

        'django_plotly_dash.finders.DashAssetFinder',
        'django_plotly_dash.finders.DashComponentFinder',
        'django_plotly_dash.finders.DashAppDirectoryFinder',
    ]
```

Add `django_plotly_dash.middleware.BaseMiddleware` to `MIDDLEWARE` in your `settings.py`:

```python
    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        ...
        'django_plotly_dash.middleware.BaseMiddleware',
        'tom_common.middleware.Raise403Middleware',
        ...
    ]
```

Add the following Django Plotly Dash configuration to your `settings.py`:

```python
# django-plotly-dash configuration

X_FRAME_OPTIONS = 'SAMEORIGIN'

PLOTLY_COMPONENTS = [
    # Common components
    'dash_core_components',
    'dash_html_components',
    'dash_renderer',

    # django-plotly-dash components
    'dpd_components',
    # static support if serving local assets
    # 'dpd_static_support',

    # Other components, as needed
    'dash_bootstrap_components',
    'dash_table'
]
```

Add the `django_plotly_dash.urls` paths to your base `urls.py`:

```python
    url_patterns = [
        path('', include('tom_common.urls')),
        path('django_plotly_dash/', include('django_plotly_dash.urls')),
    ]
```

Finally, run the following to run the `django-plotly-dash` migrations:

```
    ./manage.py migrate
```

## Including a plot in your TOM

As of 8/27/2021, the sole plot offered by this library is the `target_distribution` plot, which is a good example for integration.

In order to integrate the `target_distribution` plot, first override the `target_list.html` template by copying [target_list.html]() from the base TOM Toolkit and placing it in `<project>/templates/tom_targets/target_list.html`.

Add `dash_extras` to the `{% load bootstrap4 target_extras ... %}` templatetag near the top of the file.

Replace `{% target_distribution filter.qs %}` with `{% dash_target_distribution filter.qs %}`

# Writing a dash component

With the setup followed above, a dash component can be written with no further setup, but requires a bit of knowhow.

The three files needed for a dash component are as follows:

- Templatetag module to write the templatetag
- `templates/<app_name>/partials/<file_name.html>`
- Module for the dash app

The partial is very simple, consisting of a minimum of the following:

```
{% load plotly_dash dash_extras static bootstrap4 %}
{% plotly_app name="TargetDistributionView" ratio=0.2 initial_arguments=dash_context %}
```

The templatetag should use partial that was created, and use the `takes_context=True` kwarg, as well as any additional values necessary. It should return, at minimum, the `request` from the `context`. In order to provide any additional context to the dash app itself, the return dictionary should include a `dash_context` key with a `dict` as the value. Each key/value pair in `dash_context` will need to correspond with a component in the dash app module.

```python
@register.inclusion_tag('tom_dash/partials/target_distribution.html', takes_context=True)
def dash_target_distribution(context):
    return {
        'request': context['request'],
        'dash_context': {
            'username': {'value': context['request'].user.username},
            'target-filter': {'data': target_ids}
        }
    }
```

The last piece is the dash app itself. The `target_distribution` example can be found [here]()