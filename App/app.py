from flask import Flask, render_template, request, jsonify, redirect
from dbhelper import DBHelper
from apriori import Apriori
from cluster import Cluster
from encode_faces import Encode
import sys
app = Flask(__name__,
            static_url_path='', 
            static_folder='web/static',
            template_folder='web/templates')
helper = DBHelper()
result =  Apriori()
cluster = Cluster()
index = Encode()

@app.route('/')
@app.route("/dashboard", methods=['GET'])
def dashboard():
    init_res = {
        'status': False,
        'data' : [],
        'title': 'Dashboard', 
    }
    data = helper.getalluser()
    res = {}
    if len(data)>0:
        res['title'] = 'Dashboard'
        res['data'] = data
        return render_template('dashboard.html',data=res)
    else:
        return render_template('dashboard.html',data=init_res)

@app.route('/invoices/<lid>', methods=['GET'])
def invoices(lid):
    init_res = {
        'status': False,
        'data' : [],
        'title': 'Invoices'
    }
    res = helper.getinvoicesbyuserid(lid)
    if res['status']:
        res['title'] = 'Invoices'
        return jsonify(res)
    else:
        jsonify(init_res)

@app.route('/prediction/<lid>', methods=['GET'])
def apriori(lid):
    init_res = {
        'status': False,
        'data' : [],
        'title': 'Prediction'
    }
    res = result.predict(lid)
    # print(res)
    if len(res)>0:
        return res
    else:
       return init_res

@app.route('/prediction/all', methods=['GET'])
def aprioriAll():
    init_res = {
        'status': False,
        'data' : [],
        'title': 'All Prediction'
    }
    res = result.predictAll()
    # print(res)
    if len(res)>0:
        return res
    else:
       return init_res

@app.route('/startclustering', methods=['GET'])
def faceclust():
    init_res = {
        'status': True,
        'data' : [],
        'msg': 'Face clustering Started'
    }
    index.pickle(r'web\\static\\dist\\image\\dataset1',r'web\\static\\dist\\image\\encodings.pickle')
    cluster.montage(r'web\\static\\dist\\image\\encodings.pickle')
    # print(res)
    return init_res       
       
        
if __name__ == "__main__":
    app.run(debug=True)


