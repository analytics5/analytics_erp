import dash

app = dash.Dash()
server = app.server
app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})    # то, что предлагают плотли
app.config.suppress_callback_exceptions = True
