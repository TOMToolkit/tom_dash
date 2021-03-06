import logging

from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as dhc
from django.contrib.auth.models import User
from django_plotly_dash import DjangoDash
from guardian.shortcuts import get_objects_for_user
from plotly.graph_objects import Figure
from tom_targets.models import Target


logger = logging.getLogger(__name__)

app = DjangoDash('TargetDistributionView', external_stylesheets=[dbc.themes.BOOTSTRAP], add_bootstrap_links=True)

layout = {
    'title': 'Target Distribution (sidereal)',
    'hovermode': 'closest',
    'showlegend': False,
    'geo': {
        'projection': {
            'type': 'mollweide',
        },
        'showcoastlines': False,
        'showland': False,
        'lonaxis': {
            'showgrid': True,
            'range': [0, 360],
        },
        'lataxis': {
            'showgrid': True,
            'range': [-90, 90],
        },
    }
}

# app.layout must come before the callback that depends on it
app.layout = dhc.Div([
    dcc.Graph(
        id='target-distribution',
        figure=Figure(data=[], layout=layout)
    ),
    dcc.Input(id='username', type='hidden', value=''),
    dcc.Store(id='target-filter', data={})
])

@app.callback(
    Output('target-distribution', 'figure'),
    [Input('username', 'value')],
    [State('target-filter', 'data')]
)
def get_target_distribution_plot(username, target_filter_data):
    """
    This callback returns the target distribution plot with only the targets with IDs matching those passed in.

    :param username: Username of the user requesting the plot
    :type username: str

    :param target_filter_data: IDs of targets to display
    :type target_filter_data: list of int

    :returns: Graph of target distribution for provided IDs
    :rtype: Plotly Figure
    """
    # This is unnecessary as the IDs from the view should already be filtered for the user, but is here just in case
    user = User.objects.get(username=username)
    targets = get_objects_for_user(user, 'tom_targets.view_target')

    locations = targets.filter(id__in=target_filter_data, type=Target.SIDEREAL).values_list('ra', 'dec', 'name')
    target_data = [
        dict(
            lon=[location[0] for location in locations],
            lat=[location[1] for location in locations],
            text=[location[2] for location in locations],
            hoverinfo='lon+lat+text',
            mode='markers',
            type='scattergeo'
        ),
        dict(
            lon=list(range(0, 360, 60))+[180]*4,
            lat=[0]*6+[-60, -30, 30, 60],
            text=list(range(0, 360, 60))+[-60, -30, 30, 60],
            hoverinfo='none',
            mode='text',
            type='scattergeo'
        )
    ]

    return Figure(data=target_data, layout=layout)
