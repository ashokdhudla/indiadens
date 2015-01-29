from IndiaDens import *
from django.conf import settings
from django.core.paginator import *


class VisitorLogin(TemplateView):
  def post(self, request, *args, **kwargs):
    content = {}
    #type = request.session['proptype']
    mobileno = request.POST['VisitorMobile']
    pin  = request.POST['MobilePIN']
    visitorlist = Visitors.objects.filter(mobileno=mobileno , pinnumber=pin)
    if visitorlist:
      visitorobj = visitorlist[0]
      request.session['Visitor'] = visitorobj
      visitorobj.ismobileverified = 1
      visitorobj.save()
      return HttpResponse("success")
    else:  
      return HttpResponse("Login Failed")
    
   
class SearchResults(TemplateView):

  def get(self, request, *args, **kwargs):
    content = {}
    results = Sales.objects.all()
    content['ListingType'] = 1
    paginator = Paginator(results,3) 
    if 'page' in request.GET:
      results = Sales.objects.all()
      size = len(results)
      length = size/3
      lastpage = size%3
      if lastpage == 0:
        content['lastpage'] = length
      else:
        content['lastpage'] = length + 1
      page = int(request.GET['page'])
    else:
      page=1
    try:
        getresults = paginator.page(page)
    except PageNotAnInteger:
        getresults= paginator.page(1)
    except EmptyPage:
        getresults= paginator.page(paginator.num_pages)
    content['IMAGE_URL'] =settings.IMAGE_URL
    content['Listings'] = getresults
    return render_template(request, "SearchResults.html", content)
    

  def post(self, request, *args, **kwargs):
    
    content = {}
    propertytype = request.POST['PropertyType']
    city = request.POST['city']
    cityid = request.POST['cityid']
    bedrooms = request.POST['Bedrooms']
    minprice = request.POST['minprice']
    maxprice = request.POST['maxprice']
    minarea = request.POST['minarea']
    maxarea = request.POST['maxarea']
    area_unit = request.POST['AreaUnit']
    location = request.POST['location']
    adv_min = request.POST['advance_minprice']
    adv_max = request.POST['advance_maxprice']
    request.session['PType'] = propertytype
    request.session['CityId'] = cityid
    request.session['BedRooms'] = bedrooms
    request.session['Address'] = location
    if 'bacellors_alloed' in request.POST:
      bachelors_allowed = request.POST['bachelors_allowed']
    if 'families_alloed' in request.POST:
      families_allowed = request.POST['families_allowed']
    if 'lift' in request.POST:
      lift = request.POST['lift']
    if 'swimmingpool' in request.POST:
      swimmingpool = request.POST['swimmingpool']
    if 'gated_communtiy' in request.POST:
      gated_community = request.POST['gated_community']
    if 'power_backup' in request.POST:
      power_backup = request.POST['power_backup']
    if 'furnished' in request.POST:
      furnished = request.POST['furnished']
    if 'facing' in request.POST:
      facing = request.POST['facing']
    ptype = int(request.POST['type'])
    content['ListingType'] = ptype
    request.session['proptype'] = ptype
    ptype = 1
    if ptype == 1:
      results = Sales.objects.all()
      size = len(results)
      length = size/3
      lastpage = size%3
      if lastpage == 0:
        content['lastpage'] = length
      else:
        content['lastpage'] = length + 1
      ptype = int(request.POST['type'])
      content['ListingType'] = ptype
      paginator = Paginator(results,3) 
      page = 1
      try:
          getresults = paginator.page(page)
      except PageNotAnInteger:
          getresults= paginator.page(1)
      except EmptyPage:
          getresults= paginator.page(paginator.num_pages)
      content['IMAGE_URL'] = settings.IMAGE_URL
      content['Listings'] = getresults
      return render_template(request, "SearchResults.html", content)
    if ptype == 2:
      results = Rentals.objects.all()
      size = len(results)
      length = size/3
      lastpage = size%3
      if lastpage == 0:
        content['lastpage'] = length
      else:
        content['lastpage'] = length + 1
      paginator = Paginator(results,3) 
      page = request.POST.get('page')
      try:
          getresults = paginator.page(page)
      except PageNotAnInteger:
          getresults= paginator.page(1)
      except EmptyPage:
          getresults= paginator.page(paginator.num_pages)
      content['Listings'] = getresults
      content['IMAGE_URL'] = settings.IMAGE_URL
      return render_template(request, "SearchResults.html", content)
    for i in xrange(1):
        randomcode = random.randint(1000,10000)
        confirmcode=str(randomcode)
    request.session['VisitorConfirmCode'] = confirmcode
    content['IMAGE_URL'] = settings.IMAGE_URL
    content['confirmcode'] = confirmcode
    return render_template(request, "SearchResults.html", content) 

class TestSlide(TemplateView):
  def get(self, request, *args, **kwargs):
    content = {}
    return render_template(request, "image slider.html" ,content)

class ConfirmVisitors(TemplateView):
  def get(self, request, *args, **kwargs):
    content = {}
    content.update(csrf(request))
    return render_template(request, "SearchResults.html" ,content)
  def post(self, request, *args, **kwargs):
    content = {}
    #confirmcode = request.session['VisitorConfirmCode']
    name = request.POST['name']
    email = request.POST['email']
    phno = request.POST['phoneno']
    pswd = request.POST['password']
    accterms = request.POST['acceptterms']
    if accterms == 'true':
      act = 1
    visitorsobj = Visitors()
    visitorsobj.name = name
    visitorsobj.email = email
    visitorsobj.mobileno = phno
    visitorsobj.pinnumber = pswd
    visitorsobj.ismobileverified = False
    visitorsobj.isemailverified = False
    visitorsobj.isacceptterms = act
    visitorsobj.save()
    return HttpResponse("Saved Successfully")
        
      
     