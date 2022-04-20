

# apt install libcurl4-openssl-dev
# pip3 --no-cache-dir install pycurl

import pycurl
import certifi
from io import BytesIO

curl_verbose = False
curl_followlocation = True

curl_url = 'https://google.com/'
curl_verify_ssl = False

curl_dns_doh = None
curl_dns_doh = "https://cloudflare-dns.com/dns-query"
#curl_dns_doh = "https://doh.mindlesstux.com/dns-query"
curl_doh_verifystatus = False

curl_dns_server = "1.1.1.2,1.0.0.2"

# 0 = both, 4 = ipv4, 6 = ipv6
curl_ipver = 8

curl_referer = None

curl_ssl_verifyhost = False

buffer = BytesIO()
c = pycurl.Curl()


# Verbose or not
c.setopt(c.VERBOSE, curl_verbose)
# Follow redirects
c.setopt(c.FOLLOWLOCATION, curl_followlocation)

# URL to go to
c.setopt(c.URL, curl_url)

c.setopt(c.SSL_VERIFYPEER, False)
c.setopt(c.SSL_VERIFYSTATUS, False)

# URL for a DoH server
if curl_dns_doh is not None:
    c.setopt(c.DOH_URL, curl_dns_doh)
#    c.setopt(c.DOH_SSL_VERIFYSTATUS, curl_doh_verifystatus)

# None or csv list of ips
#if curl_dns_server is not None:
#    c.setopt(c.DNS_SERVERS, curl_dns_server)

c.setopt(c.SSL_VERIFYHOST, curl_ssl_verifyhost)
c.setopt(pycurl.OPT_CERTINFO, False)
c.setopt(c.OPT_FILETIME, True)

if curl_ipver == 4:
    c.setopt(pycurl.IPRESOLVE, pycurl.IPRESOLVE_V4)
elif curl_ipver == 6:
    c.setopt(pycurl.IPRESOLVE, pycurl.IPRESOLVE_V6)
else:
    c.setopt(pycurl.IPRESOLVE, pycurl.IPRESOLVE_WHATEVER)
    a="Doh, how did we get here"


c.setopt(c.WRITEDATA, buffer)
c.setopt(c.CAINFO, certifi.where())
c.perform()


result = {}
# page response code, Ex. 200 or 404.
result['response_code'] =  c.getinfo(c.RESPONSE_CODE)

result['effective_url'] = c.getinfo(pycurl.EFFECTIVE_URL)
result['response_code2'] = c.getinfo(pycurl.RESPONSE_CODE)
result['info_filetime'] = c.getinfo(c.INFO_FILETIME)

result['time_total'] = c.getinfo(c.TOTAL_TIME)
result['time_nslookup'] = c.getinfo(c.NAMELOOKUP_TIME)
result['time_connect'] = c.getinfo(c.CONNECT_TIME)
result['time_appconnect'] = c.getinfo(c.APPCONNECT_TIME)
result['time_pretransfer'] = c.getinfo(c.PRETRANSFER_TIME)
result['time_starttransfer'] = c.getinfo(c.STARTTRANSFER_TIME)
result['time_redirect'] = c.getinfo(c.REDIRECT_TIME)
result['redirect_count'] = c.getinfo(c.REDIRECT_COUNT)
result['redirect_url'] = c.getinfo(c.REDIRECT_URL)

'''curl_easy_perform()
    |
    |--NAMELOOKUP
    |--|--CONNECT
    |--|--|--APPCONNECT
    |--|--|--|--PRETRANSFER
    |--|--|--|--|--STARTTRANSFER
    |--|--|--|--|--|--TOTAL
    |--|--|--|--|--|--REDIRECT
'''

result['os_errno'] = c.getinfo(c.OS_ERRNO)

result['local_ip'] = c.getinfo(c.LOCAL_IP)
result['local_port'] = c.getinfo(c.LOCAL_PORT)
result['remote_ip'] = c.getinfo(c.PRIMARY_IP)
result['remote_port'] = c.getinfo(c.PRIMARY_PORT)

result['info_certinfo'] = c.getinfo(c.INFO_CERTINFO)

print(result)

c.close()

body = buffer.getvalue()
# Body is a byte string.
# We have to know the encoding in order to print it to a text file
# such as standard output.
#print(body.decode('iso-8859-1'))