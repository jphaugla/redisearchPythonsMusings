#!/bin/python

# Dependencies:
# pip install flask
# pip install redis

from flask import Flask, jsonify
from flask import request
import redis
import time
import json
from flask import Response, stream_with_context

app = Flask(__name__)
app.debug = True
db = redis.StrictRedis('redis', charset="utf-8", decode_responses=True)  # connect to server


def isInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


@app.route('/', defaults={'path': ''}, methods=['PUT', 'GET', ])
@app.route('/<path:path>', methods=['PUT', 'GET', 'DELETE'])
def home(path):
    print("the request method is " + request.method + " path is " + path)
    if request.method == 'PUT':
        # if prod_idx is set it is a replace
        # if proc_idx is not set, is insert
        print('in PUT')
        event = request.json
        print('event is %s ' % event)
        if path == 'NEW':
            prod_idx = str(db.incr("prod_highest_idx"))
            path = "prod:" + str(prod_idx)
            print("insert-new index is " + path)
        else:
            db.delete(path)  # remove old keys
            print("prod_idx exists so is a replace")
        event['updated'] = int(time.time())
        event['prod_idx'] = path
        db.hmset(path, event)
        return_string = jsonify(event, 201)

    elif request.method == 'DELETE':
        return_status = db.delete(path)
        print("delete with path = " + path + " and status of " + str(return_status))
        return_string = jsonify(str(return_status), 201)

    elif request.method == 'GET':
        if path == 'search':
            search_str = request.args.get("search_string")
            print("search string is ", search_str)
            min_str = '[' + search_str
            max_str = min_str + "~"
            print("min is " + min_str + " max is " + max_str)
            product_list = db.zrangebylex("zProdModelName", min_str, max_str)
            product_results = []
            for prod in product_list:
                # print("prod is " + prod)
                product_idx = prod.split(':')
                product_id = product_idx[1]
                # print("product_idx is ")
                # print(product_idx)
                # print("product_id is " + product_id)
                product_record = db.hgetall("prod:"+product_id)
                product_results.append(product_record)
            return_string = jsonify(product_results, 200)

        # category passed in will be Category name, need to get the category index and pull products with category index
        elif path == 'category':
            get_category = request.args.get("show_category")
            print("reporting category is ", get_category)
            #  retrieve the category index using the passed in category name
            #  pull this from the zCategoryName sorted set holding category name and category id separated by colon
            min_str = "[" + get_category + ":"
            max_str = min_str + "~"
            print("min is " + min_str + " max is " + max_str)
            category_index = db.zrangebylex("zCategoryName", min_str, max_str)
            # print("category_idx is " + category_index)
            category_list = str(category_index[0]).split(':')
            category_name = str(category_list[0].strip("'"))
            category_id = category_list[1].strip("'")
            print("category_name is " + category_name)
            print("category_id is " + category_id)
            # a = {'name':'Sarah', 'age': 24, 'isEmployed': True }
            category_results = '{' + category_id + ':' + category_name + '}'
            # with the category_id, get the products in this category
            product_list = db.zrange("zCategProd:" + category_id, 0, -1)
            product_results = []
            # print("product list is\n")
            # print(product_list)
            for prod in product_list:
                # print("prod is " + prod)
                product_idx = prod.split(':')
                product_id = product_idx[1]
                # print("product_idx is ")
                # print(product_idx)
                # print("product_id is " + product_id)
                # product_on_market = db.hget(prod, "on_market")
                # print("product_on_market is " + product_on_market)
                # if product_on_market == "1":
                product_name = db.hget(prod, "model_name")
                if product_name:
                    # print("product name is " + product_name)
                    product_results.append('{' + product_id + ':' + product_name + '}')
            return_string = jsonify(category_results, product_results, 200)

        elif not db.exists(path):
            return_string = "Error: thing doesn't exist"

        else:
            event = db.hgetall(path)
            print("got event back" + str(event))
            # put path in as product index
            event["prod_idx"] = path
            # cast integers accordingly, nested arrays, dicts not supported for now  :(
            dict_with_ints = dict((k,int(v) if isInt(v) else v) for k, v in event.items())
            # return json.dumps(dict_with_ints), 200
            return_string = jsonify(dict_with_ints, 200)

    return return_string


if __name__ == "__main__":
    app.run(host='0.0.0.0')
