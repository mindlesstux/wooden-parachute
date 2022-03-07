from dateutil import parser
from dotenv import load_dotenv
import logging
import mysql.connector as database
import os
import whois

load_dotenv()

mariadb_username=os.environ.get("mariadb_user")
mariadb_password=os.environ.get("mariadb_pass")
mariadb_hostname=os.environ.get("mariadb_host")
mariadb_database=os.environ.get("mariadb_database")

logging.basicConfig(filename='staticapp_domains.log', level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S')

# Create connection to the database
try:
   db_connection = database.connect(user=mariadb_username, password=mariadb_password, host=mariadb_hostname, database=mariadb_database)
except Error as e:
   logging.error(e)

# Select only the domains that have not been updated in the past 3hr

statement = "SELECT * FROM staticapp_domains WHERE last_check <= (NOW() - INTERVAL 3 HOUR) LIMIT 3"
#statement = "SELECT * FROM staticapp_domains"
cursor = db_connection.cursor()
cursor.execute(statement)

update_sql = []
check_sql = []

for (domain_id, content_id, domain_name, registrar, date_created, date_updated, date_expire, nameservers, status, dnssec, last_check, last_update) in cursor:
   whodata = whois.whois(domain_name)
   to_update = {}
   print(whodata)

   # Registrar
   polled_registrar = whodata['registrar']
   if registrar != polled_registrar:
      to_update['registrar'] = "'%s'" % (polled_registrar)

   # ---------------------------------------------------------------------------------------------
   # Date Created
   if type(whodata['creation_date']) is list:
      tmp_date = sorted(list(set([str(x).lower() for x in whodata['creation_date']])))
      polled_date_create = tmp_date[0]
      del tmp_date
   else:
      polled_date_create = str(whodata['creation_date'])
   
   polled_date_create = parser.parse(polled_date_create)
   print(polled_date_create)
   if date_created != polled_date_create:
      to_update['date_created'] = "'%s'" % (polled_date_create)

   # ---------------------------------------------------------------------------------------------
   # Date Updated
   if type(whodata['updated_date']) is list:
      tmp_date = sorted(list(set([str(x).lower() for x in whodata['updated_date']])))
      polled_date_updated = tmp_date[0]
      del tmp_date
   else:
      polled_date_updated = str(whodata['updated_date'])
   
   polled_date_updated = parser.parse(polled_date_updated)
   print(polled_date_updated)
   if date_created != polled_date_updated:
      to_update['date_updated'] = "'%s'" % (polled_date_updated)

   # ---------------------------------------------------------------------------------------------
   # Date Expire
   if type(whodata['expiration_date']) is list:
      tmp_date = sorted(list(set([str(x).lower() for x in whodata['expiration_date']])))
      polled_date_expire = tmp_date[0]
      del tmp_date
   else:
      polled_date_expire = str(whodata['expiration_date'])
   
   polled_date_expire = parser.parse(polled_date_expire)
   print(polled_date_expire)
   if date_created != polled_date_expire:
      to_update['date_expire'] = "'%s'" % (polled_date_expire)

   # ---------------------------------------------------------------------------------------------
   # Nameservers
   if type(whodata['name_servers']) is list:
      polled_nameservers = sorted(list(set([x.lower() for x in whodata['name_servers']])))
      polled_nameservers = ', '.join(polled_nameservers)
      print(polled_nameservers)
   else:
      polled_nameservers = whodata['name_servers']

   if nameservers != polled_nameservers:
      to_update['nameservers'] = "'%s'" % (polled_nameservers)

   # ---------------------------------------------------------------------------------------------
   # Status
   if type(whodata['status']) is list:
      polled_status = sorted(list(set([x.lower() for x in whodata['status']])))
      tmpsplit = []
      for x in polled_status:
         tmp = x.split(' ')
         tmpsplit.append(tmp[0])
      polled_status = tmpsplit
      del tmpsplit
      polled_status = ', '.join(polled_status)
   else:
      polled_status = whodata['status']

   if status != polled_status:
      to_update['status'] = "'%s'" % (polled_status)

   # ---------------------------------------------------------------------------------------------
   # DNSSEC
   if type(whodata['dnssec']) is list:
      polled_dnssec = sorted(list(set([x.lower() for x in whodata['dnssec']])))
      polled_dnssec = ', '.join(polled_dnssec)
   else:
      polled_dnssec = whodata['dnssec']

   if dnssec != polled_dnssec:
      to_update['dnssec'] = "'%s'" % (polled_dnssec)

   # ---------------------------------------------------------------------------------------------
   # Generate the SQL to update the row with the new data
   if to_update:
      print(to_update)
      sql = "UPDATE staticapp_domains SET "
      for item in to_update.items():
         sql += "%s = %s, " % (item[0], item[1])
      sql += "last_update = NOW() "
      sql += "WHERE domain_id = %s" % (domain_id)
      print(sql)
      update_sql.append(sql)
   
   sql = "UPDATE staticapp_domains SET last_check = NOW() WHERE domain_id = %s" % (domain_id)
   check_sql.append(sql)

cursor.close()
del cursor

if update_sql is not []:
   for sql in update_sql:
      db_connection.cmd_query(sql)
      db_connection.commit()

if check_sql is not []:
   for sql in check_sql:
      db_connection.cmd_query(sql)
      db_connection.commit()


# Close down connection
db_connection.close()
