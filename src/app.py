from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View
from redisearch import AutoCompleter, Suggestion, Client, Query, TextField, NumericField, aggregation, reducers

from os import environ

import json
import csv
import string

app = Flask(__name__)
bootstrap = Bootstrap()

if environ.get('REDIS_SERVER') is not None:
    redis_server = environ.get('REDIS_SERVER')
    print("passed in redis server is " + redis_server)
else:
    redis_server = 'redis'
    print("no passed in redis server variable ")

if environ.get('REDIS_PORT') is not None:
    redis_port = int(environ.get('REDIS_PORT'))
    print("passed in redis port is " + str(redis_port))
else:
    redis_port = 6379
    print("no passed in redis port variable ")


if environ.get('REDIS_PASSWORD') is not None:
    redis_password = environ.get('REDIS_PASSWORD')
else:
    redis_password = ''

client = Client(
    'product',
    host=redis_server,
    password=redis_password,
    port=redis_port
)
ac = AutoCompleter(
    'ac',
    conn=client.redis
)

nav = Nav()
topbar = Navbar('',
                View('Home', 'index'),
                View('Aggregations', 'show_agg'),
                )
nav.register_element('top', topbar)


def agg_by(field):
    print("in agg_by with field=" + field)
    ar = aggregation.AggregateRequest().group_by(field, reducers.count().alias('my_count')).sort_by(
        aggregation.Desc('@my_count'))
    return (client.aggregate(ar).rows)


def search_data(modelName):
    print("in search_data with modelName=" + modelName)
    j = client.search(Query(modelName).limit_fields('model_name').verbatim()).docs[0].__dict__
    del j['id']
    del j['payload']
    # jpgfile="url_for('high_pic',file_name=" + j['high_pic'] + ")"
    #  this doesn't seem correct-I think change must be in template
    # j['high_pic'] = jpgfile.replace('"','')
    return (j)


@app.route('/')
def index():
    return render_template('search.html')


@app.route('/display', methods=['POST'])
def display():
    print("in get display")
    display = request.form
    # print("after request form display=" + display)
    info = search_data(display['model_name'])
    return render_template('results.html', result=info)


@app.route('/aggregate')
def show_agg():
    return render_template("aggregate.html")


@app.route('/showagg', methods=['POST'])
def agg_show():
    a = request.form.to_dict()
    print("in agg_show with agg on " + a['agg'])
    rows = agg_by(a['agg'])
    # Filter and Capitalize the strings
    rows = [(lambda x: [string.capwords(x[1].decode()), x[3].decode()])(x) for x in rows]
    return render_template('aggresults.html', rows=rows, field=a['agg'].replace("@", '').capitalize())


@app.route('/autocomplete')
def auto_complete():
    name = request.args.get('term')
    print("in autocomplete with name=" + name)
    suggest = ac.get_suggestions(name, fuzzy=True)
    return (json.dumps(
        [{'value': item.string, 'label': item.string, 'id': item.string, 'score': item.score} for item in suggest]))


if __name__ == '__main__':
    bootstrap.init_app(app)
    nav.init_app(app)
    app.debug = True
    app.run(port=5000, host="0.0.0.0")
