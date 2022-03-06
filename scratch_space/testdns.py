
# https://dnspython.readthedocs.io/en/latest/resolver-class.html

import dns.resolver

domain = 'mindlesstux.com'
result = dns.resolver.query(domain)
print(result.rrset)

print()
print()
print("================================================")
print()
print()

domain = 'some-none-existant-fat-cat-domain.com'
result = dns.resolver.query(domain)
print(result.rrset)
