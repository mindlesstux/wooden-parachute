import ntplib
from time import ctime
c = ntplib.NTPClient()
try:
    response = c.request('172.16.0.52', version=3)
except ntplib.NTPException:
    response = False
print(response)

