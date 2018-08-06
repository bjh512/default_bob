from gmail import Gmail
import base64

with open('account.txt','r') as f:
	account = f.readline()
	id = account.split()[0]
	pw = account.split()[1]

#login
g = Gmail()
g.login(id,pw)
print(g.logged_in)
print("\n")

#read mails
mails = g.inbox().mail(sender="bjh512512@naver.com")
mail_bodies = list()

for amail in mails:
	amail.fetch()
	body = amail.body
	print(type(body))
	mail_bodies.append(body)

#logout
g.logout()
print(g.logged_in)