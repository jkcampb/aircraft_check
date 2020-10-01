# [WIP] Aircraft Monitoring
## Plan:
Copy what skycircl.es is doing 

Use ADS-Bx (https://www.adsbexchange.com/) data to check for circling aircraft, starting with Denver.

Query API and write positions to database

Read database and check for circling craft (bearing changes > 720(?) deg)

Notify presense of circling craft via twitter
