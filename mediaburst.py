
import urllib,urllib2
import phonenumbers

class MediaBurstError(Exception):
    pass

class MediaBurst(object):

    def __init__(self,user,password):
        self.user = user
        self.password = password

    def credit(self):
        url = "https://api.mediaburst.co.uk/http/credit.aspx"
        params = { "user" : self.user.encode('utf-8'),
                   "password" : self.password.encode('utf-8') }
        query = url + "?" + urllib.urlencode(params)
        response = urllib2.urlopen(urllib2.Request(query)).read()
        if response.startswith("Error"):
            raise MediaBurstError(response.split(':',2)[1].strip())
        else:
            return int(response.split(':',2)[1].strip())

    def send(self,to,content,region="GB"):
        url = "https://api.mediaburst.co.uk/http/send.aspx"
        number = phonenumbers.parse(to,region)
        params = { "user" : self.user.encode('utf-8'),
                   "password" : self.password.encode('utf-8'),
                   "to" : "%s%s" % (number.country_code,number.national_number),
                   "content" : content.encode('utf-8') }
        if len(params['content']) > 160:
            params["long"] = 1
        query = url + "?" + urllib.urlencode(params)
        response = urllib2.urlopen(urllib2.Request(query)).read()
        return response

