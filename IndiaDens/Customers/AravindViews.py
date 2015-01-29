from IndiaDens.Customers import *
from IndiaDens.forms import *


class CustomerListDelete(LoginRequiredMixin, TemplateView):
  def get(self, request, *args, **kwargs):
    content = {}
    if 'listid' in request.GET: 
      lid = request.GET['listid']
      type = request.GET['type']
      if(type == "1"):
        salesDelObj = Sales.objects.get(listingid = lid)
        salesDelObj.delete()
        url = "/Customer/customer-listings?cid={{request.session.customerobj.customerid}}&type=1"
        return HttpResponseRedirect(url)
      if(type == "2"):
        RentalsDelObj = Rentals.objects.get(listingid = lid)
        RentalsDelObj.delete()
        url = "/Customer/customer-listings?cid={{request.session.customerobj.customerid}}&type=2"
        return HttpResponseRedirect(url)
      else:
        msg = "No type passed"
        return HttpResponse(msg)
    else:
      Errmsg = "There is no such listid to delete"
      content['Errmsg'] = Errmsg
      return render_template(request, 'Customers/CustomerListings.html', content)

class CustomerCallBackRequests(LoginRequiredMixin,TemplateView):
  def get(self,request,*args,**kwargs):
    content = {}
    custobj = request.session['Customer']
    content.update(csrf(request))
    callbackobj = CallbackRequestForm()
    cobj = Callbackrequests.objects.filter(customerid=custobj.customerid).order_by('isattended')
    if not cobj:
      msg = "There are no requests for your listings"
      content['errmsg'] = msg
    content['call_list'] = cobj
    content['form'] = CallbackRequestForm()
    return render_template(request,"Customers/Callbacklist.html",content)
  
  def post(self, request, *args, **kwargs):
    content = {}
    if 'callbackid' in request.POST:
      callbackid = request.POST['callbackid']
      callobj = Callbackrequests.objects.get(callbackrequestid=callbackid)
      call = request.POST['callattended']
      comments = request.POST['comments']
      callobj.comments = comments
      callobj.isattended = int(call)
      callobj.save()
      msg = "your request sumitted successfully"
      content['msg'] = msg
      return HttpResponseRedirect("callback-requests")
    else:
      content['form'] =  CallbackRequestForm()
      return render_template(request,"Customers/Callbacklist.html",content)
    
class VisitorReviewList(LoginRequiredMixin,TemplateView):
  def get(self,request,*args,**kwargs):
    content = {}
    custobj = request.session['Customer']
    content.update(csrf(request))
    visitorobj = VForm()
    vobj = Visitorreviews.objects.filter(customerid=custobj.customerid)
    if not vobj:
      msg = "There are no reviews for your listings"
      content['errmsg'] = msg
    content['review_list'] = vobj
    content['form'] = VForm()
    return render_template(request,"Customers/ReviewList.html",content)
  
  def post(self, request, *args, **kwargs):
    content = {}
    visitorobj = VForm(request.POST)
    reviewid = request.POST['reviewid']
    vobj = Visitorreviews.objects.get(visitorreviewid=reviewid)
    comments = request.POST['Sellercomments']
    vobj.sellercomments = comments
    vobj.save()
    return HttpResponseRedirect("visitor-reviews")
  
class CustomerRegistration(TemplateView):
  def get(self, request, *args, **kwargs):
    content = {}
    data = {}
    content.update(csrf(request))
    STATES = []
    state_list = States.objects.all()
    for state in state_list:
      STATES.append((state.stateid, state.name))
    CustomerFormObj = CustomerForm(states = STATES)
    if 'User' in request.session or 'Customer' in request.session:
      if 'cid' in request.GET:
        cid = request.GET['cid']
        cust_obj = Customers.objects.get(customerid=cid)
        data['customertype'] = cust_obj.customertype
        data['title'] = cust_obj.title
        data['subtitle'] = cust_obj.subtitle
        data['firstname'] = cust_obj.firstname
        data['lastname'] = cust_obj.lastname
        data['email'] = cust_obj.email
        data['loginpwd'] = cust_obj.loginpwd
        data['phone'] = cust_obj.phone
        data['City'] = cust_obj.City.name
        data['state'] = cust_obj.stateid
        data['address'] = cust_obj.address
        data['country'] = cust_obj.countryid
        data['fax'] = cust_obj.fax
        data['website'] = cust_obj.website
        data['profile'] = cust_obj.profile
        data['deals'] = cust_obj.deals
        data['dealinglocation'] = cust_obj.dealinglocations
        data['description'] = cust_obj.description
        rform = CustomerForm(initial=data, states = STATES)
        content['cid'] = cid
        content['form'] = rform
        return render_template(request, "Customers/CustomerRegistration.html", content)
      else:
        content['form'] = CustomerFormObj
        return render_template(request, "Customers/CustomerRegistration.html", content)
  
  def post(self, request, *args, **kwargs):
    content = {}
    data = {}
    STATES = []
    if 'cid' in request.POST:
      cid = request.POST['cid']
    state_list = States.objects.all()
    for state in state_list:
      STATES.append((state.stateid, state.name))
    if 'Imagefile' in request.FILES:
      f = request.FILES['Imagefile']
      #f = open(settings.IMAGE_ROOT,"ListingImages\\Customer-%s.%s" %(cid,flist[1]), "wb")
      file_name = f.name
      flist = file_name.split(".")
      data = f.read()
      f.close()
      f = open(settings.IMAGE_ROOT + "\ListingImages\-%s.%s" %(cid,flist[1]),"wb")
      f.write(data)
      f.close()
    CustomerFormObj = CustomerForm(request.POST, states = STATES)
    if CustomerFormObj.is_valid():
      if cid:
        customer = Customers.objects.get(customerid = cid)
        customer.customerid = int(cid)
      else:
        customer = Customers()
      c_type = CustomerFormObj.cleaned_data['customertype']
      title = CustomerFormObj.cleaned_data['title']
      subtitle = CustomerFormObj.cleaned_data['subtitle']
      firstname = CustomerFormObj.cleaned_data['firstname']
      lastname  = CustomerFormObj.cleaned_data['lastname']
      address = CustomerFormObj.cleaned_data['address']
      cityid = CustomerFormObj.cleaned_data['CityID']
      cityname = CustomerFormObj.cleaned_data['City']
      state = CustomerFormObj.cleaned_data['state']
      countryid = CustomerFormObj.cleaned_data['country']
      contactno = CustomerFormObj.cleaned_data['phone']
      fax = CustomerFormObj.cleaned_data['fax']
      website = CustomerFormObj.cleaned_data['website']
      profile = CustomerFormObj.cleaned_data['profile']
      deals = CustomerFormObj.cleaned_data['deals']
      d_location = CustomerFormObj.cleaned_data['dealinglocation']
      description = CustomerFormObj.cleaned_data['description']
      customer.customertype = c_type
      customer.title = title
      customer.subtitle = subtitle
      customer.firstname = firstname
      customer.lastname = lastname
      email_avail = Customers.objects.all()
      if not cid:
        for obj in email_avail:
          if(obj.email==emailid):
            notification = "This email was already in exist....Please try another"
            rform = CustomerForm(states = STATES)
            content['notification'] = notification
            content['form'] = rform
            return render_template(request, "Customers/CustomerRegistration.html",content)
      customer.phone = contactno
      customer.address = address
      customer.fax = fax
      customer.website = website
      customer.profile = profile
      customer.deals = deals
      customer.dealinglocations = d_location
      customer.description = description
      if not cityid:
        if(Cities.objects.filter(name = cityname)):
          cityobj = Cities.objects.get(name = cityname)
          customer.cityid = cityobj.cityid
        else:
          cityobj = Cities()
          cityobj.name = cityname
          cityobj.stateid = int(state)
          cityobj.isnew = True
          cityobj.save()
          city = Cities.objects.latest('cityid')
          customer.cityid =city.cityid
      else:
        customer.cityid = cityid
      customer.stateid = int(state)
      customer.countryid = countryid
      customer.save()
      if 'Imagefile' in request.FILES:
          imageUrl  = "Customer-%s.%s" %(customer.customerid,flist[1])
          customer.logo =  imageUrl
          customer.save()
      if 'User' in request.session:
        return HttpResponseRedirect("/Staff/customer-list")
      elif 'Customer' in request.session:
        return HttpResponseRedirect("/Customer")
      else:
        msg = "You are successfully registered with IndiaDens"
        content['successmsg'] = msg
        content['first_name'] = firstname
        content['last_name'] = lastname
        #content['ConfirmationCode'] = code
        content['form'] = CustomerForm()
        return render_template(request, "Customers/CustomerRegistration.html", content)
    else:
     content['form'] = CustomerForm()
     return render_template(request, "Customers/CustomerRegistration.html", content) 
class AjaxCallBackRequest(TemplateView):

  def get(self, request, *args, **kwargs):
    content = {}
    cbrid = request.GET['cbrid']
    content['cbrid'] = cbrid
    cbrobj = Callbackrequests.objects.get(callbackrequestid=cbrid)
    content['cbrobj'] = cbrobj
    phnum = cbrobj.phone
    listingsobj =Callbackrequests.objects.filter(phone=phnum)
    cbrlist = []
    for obj in listingsobj:
      ltype = obj.listingtype  
      if ltype==1:
        lid = int(obj.listingid)
        listobj = Sales.objects.get(listingid = lid)
        cbrlist.append(listobj)
        content['Listingtype'] = 1
      if ltype==2:
        lid = obj.listingid
        listobj = Rentals.objects.get(listingid = lid)
        cbrlist.append(listobj)
        content['ListingType'] = 2
    content['cbr'] = cbrlist
    content['Listingtype'] = 1
    return render_template(request, "Customers/Customercbr.html", content)
  def post(self, request, *args, **kwargs):
    content = {}
    data = {}
    callstatus = request.POST['ddlStatus']
    cbrid = request.POST['cbrid']
    cbrobj = Callbackrequests.objects.get(callbackrequestid=cbrid)
    cbrobj.isattended = callstatus
    cbrobj.save()
    return HttpResponse("your info succesfully updated") 
    
    
  
       


  