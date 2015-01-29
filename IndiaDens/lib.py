from django.core.mail import send_mail,  EmailMultiAlternatives
from django.conf import settings
import urllib
import json
import logging
import re


def SendEMail(subject, body, to):
    from_email = 'IndiaDens.com <services@indiadens.com>'

    if type(to) is str:
      to = [to]

    white_list = []
    for email in to:
      if email  in ['flumensoft@yahoo.com', 'murthy@indiadens.com', 'aravind@indiadens.com', 'venu@indiadens.com', 'ashok@indiadens.com', 'venugopalchnn@gmail.com', 'ashokdhudla@gmail.com', 'aravindgajelli1210@gmail.com']:
        white_list.append(email)

    if type(to) is not list:
      logging.info("Invalid To Address. To addresses should be in list")
      return False

    if settings.PRODUCTION:
      white_list = to
      
    try:      
      msg = EmailMultiAlternatives(subject, body, from_email, white_list)
      msg.attach_alternative(body, "text/html")
      if white_list:  msg.send()
    except Exception,  e:
      logging.info(str(e))
      return False
  
    return True

def GetCityByIP(ipaddress):
  ''''
  Sample Data Structure: 
  {u'city': u'Hyderabad', u'region_code': u'02', u'region_name': u'Andhra Pradesh', u'areacode': u'', u'ip': u'110.234.136.80', u'zipcode': u'', u'longitude': 78.4744, u'metro_code': u'', u'latitude': 17.3753, u'country_code': u'IN', u'country_name': u'India'}
  '''
  socket = urllib.urlopen('http://freegeoip.net/json/%s'  %ipaddress)
  json_str = socket.read()
  socket.close()
  json_data = json.loads(json_str)
  return (json_data['city'], json_data['region_name']) 

def GetCllientIP(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    if not ip:
      ip = ''

    if ip.__contains__('127.0.0.1'):
      ip = getPublicIp()
      
    return ip   
  
def getPublicIp():
  data = str(urllib.urlopen('http://checkip.dyndns.com/').read())
  # data = '<html><head><title>Current IP Check</title></head><body>Current IP Address: 65.96.168.198</body></html>\r\n'

  return re.compile(r'Address: (\d+\.\d+\.\d+\.\d+)').search(data).group(1)