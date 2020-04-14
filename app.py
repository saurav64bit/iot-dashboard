import dash
import dash_auth
import dash_daq as daq
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import plotly
import plotly.graph_objs as go
from collections import deque
import random
import pandas
from boltiot import Bolt
import json
api_key = "f18c7b40-fcaf-43e8-8c13-024cbdced678"    
device_id  = "BOLT3852787"  
mybolt = Bolt(api_key, device_id)

external_stylesheets = ["https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                        "https://fonts.googleapis.com/css?family=Raleway:400,400i,700,700i",
                        "https://fonts.googleapis.com/css?family=Product+Sans:400,400i,700,700i"]



app = dash.Dash('IoT Dashboard', external_stylesheets=external_stylesheets)
server = app.server
app.title = "IoT Dashboard"

VALID_USERNAME_PASSWORD_PAIRS = {
    'test': 'test@123'
}

auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)


X = deque(maxlen=20)
X.append(1)
Y = deque(maxlen=20)
Y.append(1)


app.layout = html.Div([
    html.Div([
    # Header 
    html.Div([
        html.H2("IoT Dashboard"),
        html.Img(src="https://s3-us-west-1.amazonaws.com/plotly-tutorials/logo/new-branding/dash-logo-by-plotly-stripe-inverted.png"),
    ], className='banner'),
    # Dashboard Content
    html.Div([
        # Live Temperature Graph
        html.Div([
            html.Div([
                html.H3("Temperature (Celsius)")
            ], className='Title'),
            # Graph
            html.Div([
                dcc.Graph(id='temperature-graph', animate=True),
            ], className='twelve columns graph'),
            dcc.Interval(
                id='temperature-graph-update', 
                interval=5*1000, 
            ),
        ], className='seven columns dashboard-container-graph'),

        # GPIO Controls
        html.Div([
            html.Div([
                html.H3("GPIO Controls")
            ], className='Title'),
            
            html.Div([
                # GPIO 0
                html.Div([
                    daq.BooleanSwitch(
                        id='toggle-switch-gpio-0',
                        on=False,
                        color="#9B51E0",
                        label="GPIO 0",
                        labelPosition="top"
                    ),
                    html.Div(id='toggle-switch-gpio-0-output', className='gpio-message')
                ], className='container-gpio'),
                # GPIO 1
                html.Div([
                    daq.BooleanSwitch(
                        id='toggle-switch-gpio-1',
                        on=False,
                        color="#9B51E0",
                        label="GPIO 1",
                        labelPosition="top"
                    ),
                    html.Div(id='toggle-switch-gpio-1-output', className='gpio-message')
                ], className='container-gpio'),
                 # GPIO 2
                html.Div([
                    daq.BooleanSwitch(
                        id='toggle-switch-gpio-2',
                        on=False,
                        color="#9B51E0",
                        label="GPIO 2",
                        labelPosition="top"
                    ),
                    html.Div(id='toggle-switch-gpio-2-output', className='gpio-message')
                ], className='container-gpio'),
                 # GPIO 3
                html.Div([
                    daq.BooleanSwitch(
                        id='toggle-switch-gpio-3',
                        on=False,
                        color="#9B51E0",
                        label="GPIO 3",
                        labelPosition="top"
                    ),
                    html.Div(id='toggle-switch-gpio-3-output', className='gpio-message')
                ], className='container-gpio'),
                 # GPIO 4
                html.Div([
                    daq.BooleanSwitch(
                        id='toggle-switch-gpio-4',
                        on=False,
                        color="#9B51E0",
                        label="GPIO 4",
                        labelPosition="top"
                    ),
                    html.Div(id='toggle-switch-gpio-4-output', className='gpio-message')
                ], className='container-gpio'),

            ],className='twelve')

        ], className='five columns dashboard-container-gpio')


    ], className='row dashboard-container')

    ], style={'padding': '0px 10px 10px 10px',
          'marginLeft': 'auto', 'marginRight': 'auto', "width": "1000px",
          'boxShadow': '0px 0px 5px 5px rgba(204,204,204,0.4)'}
    ),
    # Footer
    html.Div([
        "Made with ",html.Span('❤', style={'color': 'red'})," by Saurav"
    ], className='footer')
])

# Callback for Temperature Graph
@app.callback(Output('temperature-graph', 'figure'),
              [Input('temperature-graph-update', 'n_intervals')])
def update_graph_scatter(input_data):
    X.append(X[-1]+1)
    Y.append(100*int(json.loads(mybolt.analogRead("A0"))['value'])/1024)

    data = plotly.graph_objs.Scatter(
            x=list(X),
            y=list(Y),
            name='Scatter',
            mode= 'lines+markers'
            )
    layout = go.Layout(
                xaxis=dict(
                    range=[min(X),max(X)],
                    title='Timestamp'
                ),
                yaxis=dict(
                    range=[min(Y),max(Y)],
                    title='Temperature (Celsius)'
                )
            )

    return {'data': [data],'layout' : layout }

# Callback for GPIO 0
@app.callback(
    Output('toggle-switch-gpio-0-output', 'children'),
    [Input('toggle-switch-gpio-0', 'on')])
def update_output(on):
    if(on == True):
        mybolt.digitalWrite('0','HIGH')
        return 'The switch is {}.'.format("On")
    else:
        mybolt.digitalWrite('0','LOW')
        return 'The switch is {}.'.format("Off")

# Callback for GPIO 1
@app.callback(
    Output('toggle-switch-gpio-1-output', 'children'),
    [Input('toggle-switch-gpio-1', 'on')])
def update_output(on):
    if(on == True):
        mybolt.digitalWrite('1','HIGH')
        return 'The switch is {}.'.format("On")
    else:
        mybolt.digitalWrite('1','LOW')
        return 'The switch is {}.'.format("Off")

# Callback for GPIO 2
@app.callback(
    Output('toggle-switch-gpio-2-output', 'children'),
    [Input('toggle-switch-gpio-2', 'on')])
def update_output(on):
    if(on == True):
        mybolt.digitalWrite('2','HIGH')
        return 'The switch is {}.'.format("On")
    else:
        mybolt.digitalWrite('2','LOW')
        return 'The switch is {}.'.format("Off")

# Callback for GPIO 3
@app.callback(
    Output('toggle-switch-gpio-3-output', 'children'),
    [Input('toggle-switch-gpio-3', 'on')])
def update_output(on):
    if(on == True):
        mybolt.digitalWrite('3','HIGH')
        return 'The switch is {}.'.format("on")
    else:
        mybolt.digitalWrite('3','LOW')
        return 'The switch is {}.'.format("Off")

# Callback for GPIO 4
@app.callback(
    Output('toggle-switch-gpio-4-output', 'children'),
    [Input('toggle-switch-gpio-4', 'on')])
def update_output(on):
    if(on == True):
        mybolt.digitalWrite('4','HIGH')
        return 'The switch is {}.'.format("On")
    else:
        mybolt.digitalWrite('4','LOW')
        return 'The switch is {}.'.format("Off")

################ Run Server ################
if __name__ == '__main__':
    app.run_server()