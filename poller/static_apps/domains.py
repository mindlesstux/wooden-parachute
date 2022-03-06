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
db_connection = database.connect(user=mariadb_username, password=mariadb_password, host=mariadb_hostname, database=mariadb_database)
cursor = db_connection.cursor()

# Select only the domains that have not been updated in the past 3hr
statement = "SELECT * FROM staticapp_domains WHERE last_check <= (NOW() - INTERVAL 3 HOUR)"
logging.debug(statement)
cursor.execute(statement)

for (domain_id, content_id, domain_name, registrar, date_created, date_updated, date_expire, nameservers, status, dnssec, last_check, last_update) in cursor:
   whodata = whois.whois('mindlesstux.com')
   to_update = {}
   print(whodata)

   # Registrar check
   polled_registrar = whodata['registrar']
   if registrar is not polled_registrar:
      to_update['registrar'] = polled_registrar

   # TODO: Date Created
   # TODO: Date Updated
   # TODO: Date Expire

   # TODO: Nameservers

   # TODO: Status

   # TODO: DNSSEC



# Close down connections
cursor.close()
db_connection.close()

