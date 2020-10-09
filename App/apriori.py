import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from dbhelper import DBHelper
import simplejson as json
from json import dumps

from mlxtend.frequent_patterns import apriori

class Apriori:
  
  def predict(self, lid):
    helper = DBHelper()
    items = helper.getinvoiceitembyuserid(lid)
    te = TransactionEncoder()
    te_ary = te.fit(items).transform(items)
    df = pd.DataFrame(te_ary, columns=te.columns_)
    frequent_itemsets = apriori(df, min_support=0.05, use_colnames=True)
    frequent_itemsets['length'] = frequent_itemsets['itemsets'].apply(lambda x: len(x))
    data=frequent_itemsets.to_dict('records')
    j= json.dumps(data, iterable_as_array=True)
    #print(type(j))
    resObj = {
        'status':True,
        'data': j,
        'msg': 'Prediction Data'
      }
    return resObj
  
  def predictAll(self):
    helper = DBHelper()
    items = helper.getallinvoiceitem()
    te = TransactionEncoder()
    te_ary = te.fit(items).transform(items)
    df = pd.DataFrame(te_ary, columns=te.columns_)
    frequent_itemsets = apriori(df, min_support=0.05, use_colnames=True)
    frequent_itemsets['length'] = frequent_itemsets['itemsets'].apply(lambda x: len(x))
    data=frequent_itemsets.to_dict('records')
    j= json.dumps(data, iterable_as_array=True)
    #print(type(j))
    resObj = {
        'status':True,
        'data': j,
        'msg': 'Prediction Data'
      }
    return resObj
  