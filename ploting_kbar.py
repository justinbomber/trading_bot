import dash                                # pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc    # pip install dash-bootstrap-components
import pandas as pd
from dash import Dash
import plotly.express as px
import plotly.graph_objects as go
from math import ceil
from function import DEMA, supertrend
from alpha_vantage.timeseries import TimeSeries # pip install alpha-vantage


app = Dash(__name__, external_stylesheets=[dbc.themes.LUMEN])
btc_cb_2hr = pd.read_csv("C:\\Users\\justin\\Desktop\\data\\coinbase_btc\\coinbase_BTC_df2hr.csv")
btc_cb_2hr['Time'] = pd.to_datetime(btc_cb_2hr['Time'])
btc_cb_2hr['DEMA123'] = DEMA(btc_cb_2hr, 123, 'close')
btc_cb_2hr['DEMA148'] = DEMA(btc_cb_2hr, 148, 'close')
btc_cb_2hr = supertrend(btc_cb_2hr)
btc_cb_2hr['lowerband'] = btc_cb_2hr[btc_cb_2hr['in_uptrend']== True ].lowerband
btc_cb_2hr['upperband'] = btc_cb_2hr[btc_cb_2hr['in_uptrend']== False ].upperband
btc_cb_2hr = btc_cb_2hr.iloc[2000:4000]


app.layout = dbc.Container([
    html.H1('Candlesticks btc coinbase 2hr', style={'textAlign': 'center'}),
    dbc.Row([
        dbc.Col([
            html.Label('Volume of btc over:'),
            dcc.Input(id='btc_volume', type='number', min=0, max=1000000, step=1, value=0)
        ], width=4),
    ]),
    dbc.Row([
        dbc.Col([html.Label('btc OHLC chart')], width=dict(size=30, offset=5))
    ]),
    dbc.Row([
        dbc.Col([dcc.Graph(id='Candle', figure={}, style={'height':'80vh'})], width=12)
    ])
    # html.Div([
    #     dcc.RangeSlider(btc_cb_2hr['Time'], value=[btc_cb_2hr.iloc[0,0], btc_cb_2hr.iloc[-1,0]], id='my-range-slider'),
    #     html.Div(id='output-container-range-slider')
# ])
], fluid=True)
@app.callback(
    Output(component_id='Candle', component_property='figure'),
    Input(component_id='btc_volume', component_property='value')
)
def build_graphs(chosen_volume):
    btc2h = btc_cb_2hr[btc_cb_2hr.volume > chosen_volume]
    fig_kbar = go.Figure(data=[go.Candlestick(x=btc2h['Time'],
                    open=btc2h['open'],
                    high=btc2h['high'],
                    low=btc2h['low'],
                    close=btc2h['close'],
                    text=btc2h['volume']),
                    go.Scatter(x=btc2h['Time'], y=btc2h['DEMA123'], line=dict(color='green', width=1), name='DEMA123'),
                    go.Scatter(x=btc2h['Time'], y=btc2h['DEMA148'], line=dict(color='purple', width=1), name='DEMA148'),
                    go.Scatter(x=btc2h['Time'],y=btc2h['upperband'], line=dict(color='red', width=3), name='upperband'),
                    go.Scatter(x=btc2h['Time'], y=btc2h['lowerband'], line=dict(color='green', width=3),name='lowerband')
                    ])

    fig_kbar.update_layout(margin=dict(t=30, b=30))
    return  fig_kbar

#region
# def transform_value(value):
#     return 10 ** value
#
# app.layout = html.Div([
#     dcc.RangeSlider(0, 3,
#         id='non-linear-range-slider',
#         marks={i: '{}'.format(10 ** i) for i in range(4)},
#         value=[0.1, 2],
#         dots=False,
#         step=0.01,
#         updatemode='drag'
#     ),
#     html.Div(id='output-container-range-slider-non-linear', style={'margin-top': 20})
# ])
# @app.callback(
#     Output('output-container-range-slider-non-linear', 'children'),
#     Input('non-linear-range-slider', 'value'))
# def update_output(value):
#     transformed_value = [transform_value(v) for v in value]
#     return 'Linear Value: {}, Log Value: [{:0.2f}, {:0.2f}]'.format(
#         str(value),
#         transformed_value[0],
#         transformed_value[1]
#     )
#endregion
if __name__ == '__main__':
    app.run_server()











