from sqlite3 import Cursor
import psycopg2
import pandas as pd
import numpy as np
import pandas.io.sql
import pyodbc
import xlrd


#reading the data from excel file
with  pd.ExcelFile('/Users/kumkum/tienda/Expiry-Upload.xlsx' ) as xlsx :
  df1 = pd.read_excel(xlsx, 'Sheet1' ,engine='openpyxl')
  #print ( df1 )

   
sql_d = "CREATE TABLE IF NOT EXISTS public.expiry_upload ( cproduct_id  bigint not null,sproduct_id bigint not null,expiry_days_for_sale integer not null,expiry_days_for_supplier integer not null ,expiry_handling integer not null)"
sql_s ="select s.supplier_number as supplier_number,sp.product_number as supplier_product_number,pp.id as customer_product_number, sp.promised_expiration_days as supplier_expiration_days,sp.expected_expiration_days as supplier_expected_expiration_day,bp.minimum_expiry_days_for_sale as backened_expiry_days_for_Sale ,bp.minimum_expiry_days_from_supplier as backened_expiry_days_for_supplier,bp.expiry_handling as backend_expiry_handling,ps.expiration_handling as supplier_expiry_handling,ps.promised_expiration_days_for_sale as supplier_expiry_days_for_sale from public.suppliers_supplier as s join public.suppliers_supplierproduct as sp on  s.id=sp.supplier_id join public.backend_products_backendproduct bp on sp.id=bp.frontend_product_id join public.products_product pp on bp.frontend_product_id = pp.id join product_selection_productregionstatus ps on pp.id = ps.product_id"
sql_in = "insert into public.expiry_upload (cproduct_id,sproduct_id,expiry_days_for_sale,expiry_days_for_supplier,expiry_handling) values (%s,%s,%s,%s,%s)"

book = xlrd.open_workbook('/Users/kumkum/tienda/Expiry-Upload.xlsx')
sheet = book.sheet_by_name('Sheet1')
for r in range(1, sheet.nrows):
  cproduct_id=sheet.cell(r,0).value
  sproduct_id=sheet.cell(r,1).value
  expiry_days_for_sale=sheet.cell(r,2).value
  expiry_days_for_supplier=sheet.cell(r,3).value
  expiry_handling=sheet.cell(r,4).value
values =(cproduct_id,sproduct_id,expiry_days_for_sale,expiry_days_for_supplier,expiry_handling)

#establishing the connection
conn = psycopg2.connect(
database="tienda", user='', password='', host='localhost', port= '5432')
  
#Creating a cursor object using the cursor() method
cursor = conn.cursor()

#Executing an MYSQL function using the execute() method
cursor.execute("select version()")

# Fetch a single row using fetchone() method.
data = cursor.fetchone()
print("Connection established to: ",data)

cursor.execute (sql_d)
cursor.execute ("commit")
cursor.execute ("select * from public.expiry_upload")
data=cursor.rowcount
print ("table created:", data )

cursor.execute (sql_in,values)
cursor.execute ("select * from public.expiry_upload")
data=cursor.rowcount
print ("upload table:",data)

cursor.execute ( sql_s)
data = cursor.fetchall ()
#print ( "current data:",data)



cursor.close ()
conn.close()
