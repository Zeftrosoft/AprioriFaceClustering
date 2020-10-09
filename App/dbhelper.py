import sqlite3
from itertools import groupby
from operator import itemgetter


class DBHelper:
  
  def connect(self):
    # , check_same_thread= False
    self.conn = sqlite3.connect('./data/mydb.sqlite')
    self.cursor = self.conn.cursor()
    # print("Opened database successfully")
    return self.conn
   

  def getcursor(self):
    return self.cursor

  def close(self):
    self.conn.close()
    print('Connection closed')

  def insert_labelid_montage(self, lid, montage):
    # if lid == -1:
    #     query = "insert into user('montage_path') VALUES (0)"
    #     self.connect()
    #     self.cursor.execute(query)
    #     self.conn.commit()
    #     self.conn.close()
    # else:
    querry = "insert into user('lid','montage_path') VALUES (\'{0}\',\'{1}\')".format(
        lid, montage)
    self.connect()
    self.cursor.execute(querry)
    self.conn.commit()
    self.conn.close()

  def insert_labelid_image_path_invoiceno(self, labelID, image_path, image_name):
    querry = "insert into invoice('lid','image_path','inv_no') VALUES (\'{0}\',\'{1}\',\'{2}\')".format(
        labelID, image_path, image_name)
    self.connect()
    self.cursor.execute(querry)
    self.conn.commit()
    self.conn.close()

  def getuserid(self, lid):
    querry = "select uid from user where lid={0}".format(lid)
    self.connect()
    user_id = self.cursor.execute(querry)
    userid = list(user_id)
    self.conn.commit()
    self.conn.close()
    return userid

  def update_user(self, user_id, montage):
    querry = "update user set montage_path=\'{0}\' where uid={1}".format(
        montage, user_id)
    self.connect()
    self.cursor.execute(querry)
    self.conn.commit()
    self.conn.close()

  def getinvoiceid(self, lid, img_path, image_name):
    querry = "select inv_id from invoice where lid=\'{0}\' and image_path=\'{1}\' and inv_no=\'{2}\'".format(
        lid, img_path, image_name)
    # print(querry)
    self.connect()
    invoice_id = self.cursor.execute(querry)
    invoiceid = list(invoice_id)
    # print(invoiceid)
    self.conn.commit()
    self.conn.close()
    return invoiceid

  def getalluser(self):
    query = "select * from user"
    self.connect()
    labelid_list = self.cursor.execute(query)
    labelids_list = list(labelid_list)
    self.conn.commit()
    self.conn.close()
    return labelids_list

  def getinvoicesbyuserid(self, lid):
    query = """SELECT invoice.image_path,invoice.inv_no,invoice_item.item_name FROM invoice
            INNER JOIN invoice_item ON invoice.inv_no = invoice_item.inv_no 
            WHERE invoice.lid ="""+lid
    self.connect()
    invoice = self.cursor.execute(query)
    invoicee = list(invoice)
    if len(invoicee) <= 0 :
        invoicee = {
          'status':False,
          'data':[],
          'msg': 'Invoice Data Doesnot Exists'
        }
    else:
      invoicee = {
        'status':True,
        'data':invoicee,
        'msg': 'invoice Data Exists'
      }
    self.conn.commit()
    self.conn.close()
    return invoicee

  def getinvoiceitembyuserid(self, lid):
    query = """SELECT invoice_item.item_name, invoice.inv_no
                FROM invoice
                INNER JOIN invoice_item
                ON invoice.inv_no = invoice_item.inv_no 
                WHERE invoice.lid = {} """.format(lid)        
    self.connect()
    item = self.cursor.execute(query)
    items = list(item)
    sorter = sorted(items, key=itemgetter(1))
    grouper = groupby(sorter, key=itemgetter(1))
    res = {k: list(map(itemgetter(0), v)) for k, v in grouper}
    items_list = []
    for row in res.items():
        items_list.append(row[1])
    self.conn.commit()
    self.conn.close()
    return items_list

  def getallinvoiceitem(self):
    query = """SELECT invoice_item.item_name, invoice.inv_no
                FROM invoice
                INNER JOIN invoice_item
                ON invoice.inv_no = invoice_item.inv_no"""      
    self.connect()
    item = self.cursor.execute(query)
    items = list(item)
    sorter = sorted(items, key=itemgetter(1))
    grouper = groupby(sorter, key=itemgetter(1))
    res = {k: list(map(itemgetter(0), v)) for k, v in grouper}
    items_list = []
    for row in res.items():
        items_list.append(row[1])
    self.conn.commit()
    self.conn.close()
    return items_list
