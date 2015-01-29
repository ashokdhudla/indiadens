from IndiaDens.Admin import *
import urllib
import json

def GetCurrentLocation(request):
  try:
    client_id = request.META.get('REMOTE_ADDR')
    socket = urllib.urlopen('http://freegeoip.net/json/%s' %client_id)
    json_text = socket.read()
    socket.close()
    js_object = json.loads(json_text)
    city = js_object['city']
    state = js_object['region_name']
  except Exception, e:
    city = ''
    state = ''

  return city, state

class HomePage(TemplateView):


  def get(self, request, *args, **kwargs):  
    content = {}

    #client_id = '110.234.136.80'
    city, state = GetCurrentLocation(request)
    
    #return HttpResponse("%s, %s" %(city, state))
    return render_to_response("Admin/Index.html")

