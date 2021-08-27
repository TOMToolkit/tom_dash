import json

from django import template

register = template.Library()


@register.inclusion_tag('tom_dash/partials/target_distribution.html', takes_context=True)
def dash_target_distribution(context, target_filter_queryset):
    """
    Loads the dash app to render the target distribution plot with Django Plotly Dash.

    :param context: Context object from the request
    :type context: dict

    :param target_filter_queryset: Queryset of targets to plot
    :type target_filter_queryset: Queryset
    """
    target_ids = [target.id for target in target_filter_queryset]

    # request is required for django-plotly-dash
    # dash_context is provided to initial_arguments in partial
    # values in dash_context correspond with input/state components in the dash app
    return {
        'request': context['request'],
        'dash_context': {
            'username': {'value': context['request'].user.username},
            'target-filter': {'data': target_ids}
        }
    }
