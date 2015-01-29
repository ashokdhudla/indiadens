from IndiaDens import *
from IndiaDens.lib import *
from django.conf import settings
from IndiaDens.models import *
from lib import *
import random
import os
import re
from datetime import *
from django.conf import settings
import urllib
from IndiaDens.lib import *

from django.conf import settings

class HomePage(TemplateView):

  def get(self, request, *args, **kwargs):
    content = {}
    if 'City' in request.session:
      city = request.session['City']
      content['City'] = city
      
    if 'State' in request.session:
      state = request.session['State']
      content['State'] = state
      
#     if 'Ip' in request.session:
#       ip = request.session['Ip']
#       content['IP'] = ip
#        
#     else:
#       ip = GetCllientIP(request)
#       request.session['Ip'] = ip
#       if(Iptable.objects.filter(ip = 'ip')):
#         ipobj = Iptable.objects.get(ip = 'ip')
#         city = ipobj.city
#         request.session['City'] = city
#         state = ipobj.state
#         request.session['State'] = state
#         content['IP'] = ip
#         content['City'] = city
#         content['State'] = state
#       else:
#         ipobj = Iptable();
#         ipobj.ip = ip
#         city,state = GetCityByIP(ip)
#         request.session['City'] = city
#         request.session['State'] = state
#         ipobj.city = city
#         ipobj.state = state
#         ipobj.isnew = True
#         ipobj.save()
#         content['IP'] = ip
#         content['City'] = city
#         content['State'] = state
                 
    content.update(csrf(request))
    return render_template(request, "Index.html", content)

class Logout(TemplateView):

  def get(self, request, *args, **kwargs):  
    content = {}
    login = ''

    
    if 'login' in request.GET:
      login = request.GET['login']

    for key in request.session.keys():
      del request.session[key]
      
    if 'next' in request.GET:
       return HttpResponseRedirect(request.GET['next'])
    
    if login == 'customer':
      return HttpResponseRedirect("/Customer/login")
    elif login == 'employee':
      return HttpResponseRedirect("/Staff/login")

    
    return render_to_response("Index.html")


class NewListing(TemplateView):
  def get(self, request, *args, **kwargs):
    content = {}
    data = {}
    content.update(csrf(request))
    Newlistings = None
    
    if 'type' in request.GET:
      pType = request.GET['type']
      data['listingType'] = pType
      SalesFormObj = SalesForm(initial = data)
      content['form'] = SalesFormObj
      content['Type'] = pType
      return render_template(request, "AddListing.html", content)
    
    return HttpResponse("Invalid request. You must provide Listing Type")
  
  def post(self, request, *args, **kwargs):
    content = {}
    data = {}
    cname = " "
    if 'ImageData' in request.FILES:
      f = request.FILES['ImageData']
      file_name = f.name
      flist = file_name.split(".")
      data = f.read()
      f.close()
      
    SalesFormObj = SalesForm(request.POST)
    submit = request.POST['Submit']
    if submit == 'Cancel':
        return HttpResponseRedirect('/')
    if SalesFormObj.is_valid():
      propertytype = SalesFormObj.cleaned_data['Property_Type']
      price  = SalesFormObj.cleaned_data['Price']
      area = SalesFormObj.cleaned_data['Area']
      areaunits = SalesFormObj.cleaned_data['AreainWords']
      bedrooms = SalesFormObj.cleaned_data['BedRooms']
      bathrooms = SalesFormObj.cleaned_data['BathRooms']
      propertylocation = SalesFormObj.cleaned_data['PropertyLocation']
      city = SalesFormObj.cleaned_data['City']
      state = SalesFormObj.cleaned_data['State']
      tellabturprpy = SalesFormObj.cleaned_data['TellabturProperty']
      name = SalesFormObj.cleaned_data['Name']
      emailid = SalesFormObj.cleaned_data['Email']
      contactno = SalesFormObj.cleaned_data['Contactno']
      ownertype = SalesFormObj.cleaned_data['ownershipType']
      listingType = SalesFormObj.cleaned_data['listingType']
      property_list = re.split('(,)|(\r\n)', propertylocation)
      if(propertytype == "10"):
        ptype = "Apartments"
      if(propertytype == "20"):
        ptype = "Independent House"
      if(propertytype == "25"):
        ptype = " Villas"
      if(propertytype == "30"):
        ptype = "Pent House"
      if(propertytype == "40"):
        ptype = "Farm House"
      if(propertytype == "50"):
        ptype = "Office Space"
      pricevalue = price.split(" ")
      plen = len(pricevalue)-1
      if(plen == 0):
        fprice = pricevalue[0].split(".")
        if(fprice[0]):
          plen1 = len(str(fprice[0]).strip())
          if(listingType == "1"):
            if(plen1 < 6):
              content['Type'] = listingType
              content['ErrMsg'] = "Invalid Format"
              content['form'] = SalesFormObj
              return render_template(request,"Addlisting.html",content)
            else:
              price = float(pricevalue[0])
          if(listingType == "2"):  
            if(plen1 < 4):
              content['Type'] = listingType
              content['ErrMsg'] = "Invalid Format"
              content['form'] = SalesFormObj
              return render_template(request,"Addlisting.html",content)
            else:
              price = float(pricevalue[0])
        else:
          pricelen = len(str.pricevalue[0].strip())
          if(listingType == "1"):
            if(pricelen < 6):
              content['Type'] = listingType
              content['ErrMsg'] = "Invalid Format"
              content['form'] = SalesFormObj
              return render_template(request,"Addlisting.html",content)
            else:
              price = float(pricevalue[0])
          if(listingType == "2"):  
            if(pricelen1 < 4):
              content['Type'] = listingType
              content['ErrMsg'] = "Invalid Format"
              content['form'] = SalesFormObj
              return render_template(request,"Addlisting.html",content)
            else:
              price = float(pricevalue[0])
          
      if(plen == 1):
        if(pricevalue[1] == 'Lacs' or pricevalue[1] == 'lacs'):
          price = float(pricevalue[0]) * 100000
        if(pricevalue[1] == 'Crores' or pricevalue[1] == 'crores'):
          price = float(pricevalue[0]) * 10000000
        if(pricevalue[1] == 'Thousands' or pricevalue[1] == 'thousands'):
          price = float(pricevalue[0]) * 1000
          
      if(bedrooms == "1"):
        property_title = ("Single Bedroom %3s at %3s") %(ptype,property_list[-1])
      if(bedrooms == "2"):
        property_title = ("Double Bedroom %3s at %3s" ) %(ptype,property_list[-1])
      if(bedrooms == "3"):
        property_title = ("Triple Bedroom %3s at %3s" ) %(ptype, property_list[-1])
      else:
        property_title = ("%s Bhk %s at %s") %(str(bedrooms), ptype, property_list[-1])
        
      city_list = Cities.objects.filter(name = city)
      if city_list:
        cityobj = city_list[0]
        
      else:
        cityobj = Cities();
        cityobj.name = city
        cityobj.stateid = state
        cityobj.isnew = True
        cityobj.save()
        cityobj = Cities.objects.latest('cityid')
          
      customerobj = Customers.objects.filter(email = emailid)
      if(customerobj):
        customer= customerobj[0]
        saleslistings = Sales.objects.filter(customerid = customer.customerid)
        rentalsistings = Rentals.objects.filter(customerid = customer.customerid)    
        if listingType == "2":
          RentalsObj = Rentals()
          custObj  = Customers.objects.get(customerid = customer.customerid)
          RentalsObj.planid = 0
          RentalsObj.customerid = custObj.customerid
          RentalsObj.propertytypeid = propertytype
          RentalsObj.rent = price
          RentalsObj.area = area
          RentalsObj.areaunit = areaunits
          RentalsObj.bedrooms = bedrooms
          RentalsObj.bathrooms = bathrooms
          RentalsObj.address = propertylocation
          RentalsObj.cityid = cityobj.cityid
          RentalsObj.stateid = state
          RentalsObj.description = tellabturprpy
          RentalsObj.contactname = name
          RentalsObj.email = custObj.email
          RentalsObj.phone = custObj.phone
          RentalsObj.ownership = ownertype
          RentalsObj.listingtype = listingType
          RentalsObj.approvalstatus = 0
          RentalsObj.posteddate = datetime.now()
          RentalsObj.expirydate = datetime.now() + timedelta(days = 15)
          RentalsObj.title = property_title
          for i in xrange(1):
            code = random.randint(1000,10000)
          code=str(code)
          request.session['confirmcode'] = code
          RentalsObj.save()
          if 'ImageData' in request.FILES:
            Rentallistingimageobj = Rentallistingimages()
            listIdObj = Rentals.objects.latest('listingid')
            filename = listIdObj.listingid
            imageUrl  = "Rentallisting-%s-1.%s" %(filename,flist[1])
            Rentallistingimageobj.listingid = listIdObj.listingid
            Rentallistingimageobj.largeimage = imageUrl
            Rentallistingimageobj.save()
            f = open(settings.IMAGE_ROOT + "\ListingImages\Rentallisting-%s-1.%s" %(filename,flist[1]), "wb")
            f.write(data)
            f.close()
            listIdObj.imagethumb = imageUrl
            listIdObj.save()
            listingidobj = Rentals.objects.latest('listingid')
            lid = str(listingidobj.listingid)
            listingidobj.propertyid = "IDR" + lid.zfill(8)
            listingidobj.save()

        if listingType == "1":
          cobj = Cities.objects.latest('name')
          SalesObj = Sales()
          custObj  = Customers.objects.get(customerid = customer.customerid)
          SalesObj.planid = 0
          SalesObj.customerid = custObj.customerid
          SalesObj.propertytypeid = propertytype
          SalesObj.price = price
          SalesObj.area = area
          SalesObj.areaunit = areaunits
          SalesObj.bedrooms = bedrooms
          SalesObj.bathrooms = bathrooms
          SalesObj.address = propertylocation
          SalesObj.cityid = cityobj.cityid
          SalesObj.stateid = state
          SalesObj.description = tellabturprpy
          SalesObj.contactname = name
          SalesObj.email = custObj.email
          SalesObj.phone = custObj.phone
          SalesObj.ownership = ownertype
          SalesObj.listingtype = listingType
          SalesObj.approvalstatus = 0
          SalesObj.posteddate = datetime.now()
          SalesObj.expirydate = datetime.now() + timedelta(days = 15)
          SalesObj.title = property_title
          for i in xrange(1):
              code = random.randint(1000,10000)
          code=  str(code)
          request.session['confirmcode'] = code
          SalesObj.confirmcode=code+str(custObj.customerid)
          SalesObj.save()
          if 'ImageData' in request.FILES:
            Salellistingimageobj = Salelistingimages()
            listIdObj = Sales.objects.latest('listingid')
            filename = listIdObj.listingid
            imageUrl  = "Saleslisting-%s-1.%s" %(filename,flist[1])
            listIdObj.imagethumb =  imageUrl
            Salellistingimageobj.listingid = listIdObj.listingid
            Salellistingimageobj.largeimage = imageUrl
            Salellistingimageobj.save()
            f = open(settings.IMAGE_ROOT + "\ListingImages\Saleslisting-%s-1.%s" %(filename,flist[1]), "wb")
            f.write(data)
            f.close()
            listIdObj.save()
            listingidobj = Sales.objects.latest('listingid')
            lid = str(listingidobj.listingid)
            listingidobj.propertyid = "IDS" + lid.zfill(8)
            listingidobj.save()   
        content['first_name'] = customer.firstname
        content['last_name'] = customer.lastname
        content['salelistings'] = saleslistings
        content['rentallistings'] = rentalsistings
        content['EMailID'] = customer.email
        content['login_link'] = "http://" + settings.CURRENT_DOMAIN + "/customer/login"
        html = render_email('EMail-ExistingCustomer.html', content)
        SendEMail("Please approve your listings", html, str(customer.email))
        return render_template(request,"ListingConfirmation.html",content)
      else:
        #cobj = Cities.objects.latest('cityid')
        cname = name.split(" ")
        custObj = Customers()
        clen = len(cname)-1
        if(clen == 0):
          custObj.firstname = cname[0]
        if(clen == 1):
          custObj.firstname = cname[0]
          custObj.lastname = cname[1]
        else:
          custObj.lastname = " "
        custObj.email = emailid
        for i in xrange(1):
            password = random.randint(100000,1000000)
        custObj.loginpwd = password
        custObj.phone = "91" + contactno
        custObj.cityid = cityobj.cityid
        custObj.stateid = state
        custObj.customertype = ownertype
        for i in xrange(1):
            code = random.randint(100,1000)
        code="10" + str(code)
        request.session['randomcode'] = code
        custObj.mobilecode = code
        
        if Customers.objects.count() > 0:
          customerobj = Customers.objects.latest('customerid')
          cid = str(customerobj.customerid)
        else:
          cid = '1'
          
        custObj.emailcode = cid + str(request.session._get_or_create_session_key())
        custObj.save()
        Cobj = Customers.objects.latest('customerid')
        content['first_name'] = Cobj.firstname
        content['last_name'] = Cobj.lastname
        content['ConfirmationCode'] = Cobj.mobilecode
        content['Customer_Emailid'] = Cobj.email
        content['Customer_Password'] = Cobj.loginpwd
        content['confirmation_link'] = "http://" + settings.CURRENT_DOMAIN + "/customer/confirm/" + Cobj.emailcode
        html = render_email('EMail-RegConfirmation.html', content)
        SendEMail("Welcome to IndiaDens.com", html, str(Cobj.email))
        
      if listingType == "2":
        RentalsObj = Rentals()
        custObj  = Customers.objects.latest('customerid')
        RentalsObj.planid = 0
        RentalsObj.customerid = custObj.customerid
        RentalsObj.propertytypeid = propertytype
        RentalsObj.rent = price
        RentalsObj.area = area
        RentalsObj.areaunit = areaunits
        RentalsObj.bedrooms = bedrooms
        RentalsObj.bathrooms = bathrooms
        RentalsObj.address = propertylocation
        RentalsObj.cityid = cityobj.cityid
        RentalsObj.stateid = state
        RentalsObj.description = tellabturprpy
        RentalsObj.contactname = name
        RentalsObj.email = custObj.email
        RentalsObj.phone = custObj.phone
        RentalsObj.ownership = ownertype
        RentalsObj.listingtype = listingType
        RentalsObj.approvalstatus = 1
        RentalsObj.posteddate = datetime.now()
        RentalsObj.expirydate = datetime.now() + timedelta(days = 15)
        RentalsObj.title = property_title
        for i in xrange(1):
          code = random.randint(1000,10000)
        code=str(code)
        request.session['confirmcode'] = code
        RentalsObj.save()
        if 'ImageData' in request.FILES:
          Rentallistingimageobj = Rentallistingimages()
          listIdObj = Rentals.objects.latest('listingid')
          filename = listIdObj.listingid
          imageUrl  = "Rentallisting-%s-1.%s" %(filename,flist[1])
          listIdObj.imagethumb =  imageUrl
          Rentallistingimageobj.listingid = listIdObj.listingid
          Rentallistingimageobj.largeimage = imageUrl
          Rentallistingimageobj.save()
          f = open(settings.IMAGE_ROOT + "\ListingImages\Rentallisting-%s-1.%s" %(filename,flist[1]), "wb")
          f.write(data)
          f.close()
          listIdObj.save()
          listingidobj = Rentals.objects.latest('listingid')
          lid = str(listingidobj.listingid)
          listingidobj.propertyid = "IDR" + lid.zfill(8)
          listingidobj.save()
        return HttpResponseRedirect('/reg-confirmation')

      if listingType == "1":
        cobj = Cities.objects.latest('name')
        SalesObj = Sales()
        custObj  = Customers.objects.latest('customerid')
        SalesObj.planid = 0
        SalesObj.customerid = custObj.customerid
        SalesObj.propertytypeid = propertytype
        SalesObj.price = price
        SalesObj.area = area
        SalesObj.areaunit = areaunits
        SalesObj.bedrooms = bedrooms
        SalesObj.bathrooms = bathrooms
        SalesObj.address = propertylocation
        SalesObj.cityid = cityobj.cityid
        SalesObj.stateid = state
        SalesObj.description = tellabturprpy
        SalesObj.contactname = name
        SalesObj.email = custObj.email
        SalesObj.phone = custObj.phone
        SalesObj.ownership = ownertype
        SalesObj.listingtype = listingType
        SalesObj.approvalstatus = 1
        SalesObj.posteddate = datetime.now()
        SalesObj.expirydate = datetime.now() + timedelta(days = 15)
        SalesObj.title = property_title
        for i in xrange(1):
            code = random.randint(1000,10000)
        code=  str(code)
        request.session['confirmcode'] = code
        SalesObj.confirmcode=code+str(custObj.customerid)
        SalesObj.save()
        if 'ImageData' in request.FILES:
          Salellistingimageobj = Salelistingimages()
          listIdObj = Sales.objects.latest('listingid')
          filename = listIdObj.listingid
          imageUrl  = "Saleslisting-%s-1.%s" %(filename,flist[1])
          listIdObj.imagethumb =  imageUrl
          Salellistingimageobj.listingid = listIdObj.listingid
          Salellistingimageobj.largeimage = imageurl
          Salellistingimageobj.save()
          f = open(settings.IMAGE_ROOT + "\ListingImages\Saleslisting-%s-1.%s" %(filename,flist[1]), "wb")
          f.write(data)
          f.close()
          listIdObj.save()
          listingidobj = Sales.objects.latest('listingid')
          lid = str(listingidobj.listingid)
          listingidobj.propertyid = "IDS" + lid.zfill(8)
          listingidobj.save()

        return HttpResponseRedirect('/reg-confirmation')
        
      else:
        return HttpResponse("Listing type is not found as hidden field")
      
    else:
      msg  = "Invalid Form"
      content['ErrorMessage'] =  msg
      content['form'] = SalesFormObj
      return render_template(request,"AddListing.html",content) 
      

class RegConfirmation(TemplateView):

  def get(self, request, *args, **kwargs):
    #confirm_code = request.session['']
    content = {}
    code = request.session['randomcode']
    confirm_code = code
    content['ConfirmationCode'] = confirm_code
    return render_template(request, "RegConfirmation.html", content)
     

class SaveMessage(TemplateView):
  def get(self, request, *args, **kwargs):
    content = {}
    msgfrom = request.GET['from']
    msgto = request.GET['to']
    msg = request.GET['msg']
    sntdate = request.GET['sentdate']
    sntdate = sntdate[0:-6]
    msgobj = Mobilemessages();
    msgobj.messagefrom = msgfrom
    msgobj.messageto = msgto
    msgobj.sentdate = sntdate
    #msgobj.sentdate = '2013-02-01 11:22:30'
    msgobj.message = msg
    msgobj.save()
    return HttpResponse("OK")
  
#class AutoDispalyCities(TemplateView):
 # def get(self, request, *args, **kwargs):
  #  content = {}
   # return HttpResponseRedirect(TestAjax.html)

class ListingInfo(TemplateView):
  def get(self, request, *args, **kwargs):
    content = {}
    data = {} 
    content.update(csrf(request))
    callbackform = CallbackRequestForm()
    typeid=int(request.GET['type'])
    content['type']=typeid
    if(typeid==1):
      lid = int(request.GET['lid'])
      Salesform=Sales.objects.get(listingid = lid)
      content['lid']=lid
      content['ownershipid'] = Salesform.ownership
      content['ptype']=Salesform.propertytypeid
      content['title'] = Salesform.title
      content['price'] = Salesform.price
      content['BedRooms']=Salesform.bedrooms
      content['contactname'] = Salesform.contactname
      content['email'] = Salesform.email
      content['phone'] = Salesform.phone
      content['constructionyear'] = Salesform.constructiondate
      content['possession'] =Salesform.possession 
      content['Longitude']=Salesform.longitude
      content['Latitude']=Salesform.latitude
      content['BathRooms']=Salesform.bathrooms
      content['area']=Salesform.area
      content['lift']=Salesform.lift
      content['gym']=Salesform.gym
      content['swimmingpool']=Salesform.swimmingpool
      content['gatedcommunity'] = Salesform.gatedcommunity
      content['areaunit'] = Salesform.areaunit
      content['powerbackup'] = Salesform.powerbackup
      content['furnished'] = Salesform.furnished
      content['pstatus']=Salesform.propertystatus
      content['facing'] = Salesform.facing
      data['Ownership']=Salesform.ownership
      content['PostedDate']=Salesform.posteddate
      content['address']=Salesform.address
      content['description']=Salesform.description
      content['landmark1'] = Salesform.landmark1
      content['landmark2'] = Salesform.landmark2
      content['landmark3'] = Salesform.landmark3
      content['landmark4'] = Salesform.landmark4
      content['IMAGE_URL'] = settings.IMAGE_URL
      cidobj = Sales.objects.get(listingid=lid)
      content['CustomerId'] = cidobj.customerid
      content['ListingId'] = lid
      content['ListingType'] = typeid
      callbackobj = CallbackRequestForm(initial=data)
      content['form'] = callbackobj
      limit = 5
      image_list = []
      imageobj_list = Salelistingimages.objects.filter(listingid=lid)
      i = 0
      if imageobj_list:
        for obj in imageobj_list:
            i += 1
            if i <= limit:
               image_list.append(obj)
            else:
              break
        content['image'] = image_list[0].largeimage
      else:
        content['image'] = 'http://webmaster.ypsa.org/wp-content/uploads/2012/08/no_thumb.jpg'     
      num_images = len(image_list)
      for i in range(0, limit - num_images):
        imgObj = Salelistingimages()
        imgObj.description = ""
        imgObj.listingimageid = 0
        imgObj.largeimage = 'http://webmaster.ypsa.org/wp-content/uploads/2012/08/no_thumb.jpg'
        image_list.append(imgObj)
      content['image_list'] = image_list
      attr_list = []
      attrobj_list = Saleattributes.objects.filter(listingid=lid)
      i = 0
      for obj in attrobj_list:
          i += 1
          if i <= limit:
             attr_list.append(obj)
          else:
            break
      content['image'] =image_list[0].largeimage
      num_attributes = len(attr_list)
      for i in range(0, limit - num_attributes):
          attrObj = Saleattributes()
          attrObj.value = ""
          attrObj.attributeid = 0
          attr_list.append(attrObj)
      content['Attr_List'] = attr_list
      return render_template(request, 'ListingInfo.html', content)
    if(typeid==2):
      lid = int(request.GET['lid'])
      Rentalsobj=Rentals.objects.get(listingid = lid)
      content['lid']=lid
      content['contactname'] = Rentalsobj.contactname
      content['email'] = Rentalsobj.email
      content['phone'] = Rentalsobj.phone
      content['ownershipid'] = Rentalsobj.ownership
      content['constructionyear'] = Rentalsobj.constructiondate
      content['landmark1'] = Rentalsobj.landmark1
      content['landmark2'] = Rentalsobj.landmark2
      content['landmark3'] = Rentalsobj.landmark3
      content['landmark4'] = Rentalsobj.landmark4
      content['Latitude'] = Rentalsobj.latitude
      content['Longitude'] = Rentalsobj.longitude
      content['possession'] =Rentalsobj.possession 
      content['lift'] = Rentalsobj.lift
      content['gym'] = Rentalsobj.gym
      content['swimmingpool'] = Rentalsobj.swimmingpool
      content['gatedcommunity'] = Rentalsobj.gatedcommunity
      content['facing'] = Rentalsobj.facing
      content['powerbackup'] = Rentalsobj.powerbackup
      content['furnished'] = Rentalsobj.furnished    
      content['ptype']=Rentalsobj.propertytypeid
      content['title'] = Rentalsobj.title
      content['price'] = Rentalsobj.rent
      content['BedRooms']=Rentalsobj.bedrooms
      content['BathRooms']=Rentalsobj.bathrooms
      content['area']=Rentalsobj.area
      content['areaunit'] = Rentalsobj.areaunit
      content['pstatus']=Rentalsobj.propertystatus
      data['Ownership']=Rentalsobj.ownership
      content['PostedDate']=Rentalsobj.posteddate
      content['address']=Rentalsobj.address
      content['description']=Rentalsobj.description
      cidobj = Rentals.objects.get(listingid=lid)
      content['CustomerId'] = cidobj.customerid
      content['ListingId'] = lid
      content['ListingType'] = typeid
      callbackobj = CallbackRequestForm(initial=data)
      content['form'] = callbackobj
      limit = 5 
      image_list = []
      imageobj_list = Rentallistingimages.objects.filter(listingid=lid)
      if imageobj_list:
        i = 0
        for obj in imageobj_list:
            i += 1
            if i <= limit:
               image_list.append(obj)
            else:
              break
        content['image'] =image_list[0].largeimage
      else:
        content['image'] = 'http://webmaster.ypsa.org/wp-content/uploads/2012/08/no_thumb.jpg'          
      num_images = len(image_list)
      for i in range(0, limit - num_images):
        imgObj = Salelistingimages()
        imgObj.description = ""
        imgObj.listingimageid = 0
        imgObj.largeimage = 'http://webmaster.ypsa.org/wp-content/uploads/2012/08/no_thumb.jpg'
        image_list.append(imgObj)
      content['image_list'] = image_list
      attr_list = []
      attrobj_list = Rentalattributes.objects.filter(listingid=lid)
      i = 0
      for obj in attrobj_list:
          i += 1
          if i <= limit:
             attr_list.append(obj)
          else:
            break
      num_attributes = len(attr_list)
      for i in range(0, limit - num_attributes):
          attrObj = Rentalattributes()
          attrObj.value = ""
          attrObj.attributeid = 0
          attr_list.append(attrObj)
      content['Attr_List'] = attr_list 
    return render_template(request, 'ListingInfo.html', content)
  
  def post(self,request, *args, **kwargs):
    content = {}
    requestformobj = CallbackRequestForm(request.POST)
    if requestformobj.is_valid():
      name = requestformobj.cleaned_data['name']
      email = requestformobj.cleaned_data['email']
      phone = requestformobj.cleaned_data['phone']
      time1 = requestformobj.cleaned_data['pftime1']
      time2 = requestformobj.cleaned_data['pftime2']
      time3 = requestformobj.cleaned_data['pftime3']
      message = requestformobj.cleaned_data['message']
      cid = requestformobj.cleaned_data['CustomerId']
      lid = requestformobj.cleaned_data['ListingId']
      type = requestformobj.cleaned_data['ListingType']
      callobj = Callbackrequests()
      callobj.customerid = int(cid)
      callobj.listingid = int(lid)
      callobj.listingtype = int(type)
      callobj.name = name
      callobj.email = email
      callobj.phone = phone
      callobj.preftime1 = time1
      callobj.preftime2 = time2
      callobj.preftime3 = time3
      callobj.message = message
      for i in xrange(1):
        randomcode = random.randint(100,1000)
        code=str(randomcode)
        callobj.confirmcode = '50' + code
        callobj.save()
      return HttpResponse("request taken")



class TestMail(TemplateView):
  def get(self, request, *args, **kwargs):  
    content = {}
    html =  render_email('EMail-RegConfirmation.html', content)
    #send_mail(subject = 'Test Subject', 
    #          message = html, 
    #          from_email = 'IndiaDens.com <services@indiadens.com>', 
    #          recipient_list =  ['flumensoft@yahoo.com' ], 
    #         html_message = "Registration Success",
    #         fail_silently=False)

    #msg = EmailMultiAlternatives('Html Mail Test' , html, 'IndiaDens.com <services@indiadens.com>', ['flumensoft@yahoo.com' ])
    #msg.attach_alternative(html, "text/html")
    #msg.send()
    if SendEMail("Welcome to IndiaDens.com", html, 'aravind@indiadens.com'):
      return HttpResponse("An email is successfully sent")
    else:
      return HttpResponse("An email is FAILED")

    return HttpResponse("No operation is done")
  
  
class VisitorReviews(TemplateView):
  def get(self, request, *args, **kwargs):
    content = {}
    data = {}
    lid = request.GET['lid']
    type = request.GET['type']
    type = int(type)
    lid = int(lid)
    visitorform = VForm()
    content.update(csrf(request))
    if(type==1):
      cidobj = Sales.objects.get(listingid=lid)
    if(type==2):
      cidobj = Rentals.objects.get(listingid=lid)
    data['CustomerId'] = cidobj.customerid
    data['ListingId'] = lid
    data['ListingType'] = type
    visitorobj = VForm(initial=data)
    content['form'] = visitorobj
    
    return render_template(request, "VisitorReviews.html", content)
  
  def post(self,request, *args, **kwargs):
    content = {}
    visitorformobj = VForm(request.POST)
    if visitorformobj.is_valid():
      name = visitorformobj.cleaned_data['Name']
      email = visitorformobj.cleaned_data['Email']
      phone = visitorformobj.cleaned_data['Contactno']
      price = visitorformobj.cleaned_data['Bestprice']
      comments = visitorformobj.cleaned_data['Visitorcomments']
      cid = visitorformobj.cleaned_data['CustomerId']
      lid = visitorformobj.cleaned_data['ListingId']
      type = visitorformobj.cleaned_data['ListingType']
      visitor = Visitorreviews()
      visitor.customerid = int(cid)
      visitor.listingid = int(lid)
      visitor.listingtype = int(type)
      visitor.name = name
      visitor.email = email
      visitor.contactno = phone
      visitor.bestprice = int(price)
      visitor.visitorcomments = comments
      for i in xrange(1):
        randomcode = random.randint(100,1000)
        code=str(randomcode)
        visitor.mobilecode = '40' + code
        visitor.save()
      return HttpResponse("review taken")
    else:
      content['form'] = VForm()
      return render_template(request,"VisitorReviews.html",content)
      
class TestAjax(TemplateView):

    def get(self, request, *args, **kwargs):
      content = {}
      return render_template(request, 'TestAjax.html', content)

class GetCityName(TemplateView):
  def get(self, request, *args, **kwargs):  
    content = {}
    stchar = request.GET['startch']
    #return HttpResponse(stchar)
    cities_json = {}
    #cities = Cities.objects.filter(name__istartswith=stchar)[:10]
    cities = Cities.objects.all()
    html = ""

    if cities:
       for city in cities:
         cities_json[str(city.cityid)] = city.name
         
         #name = city.name
         #state = city.State.name
         #html += "%s&nbsp;%s<br>" %(name, state)
    else:
      return HttpResponse("{}", 'application/json') 
    
    json_str = str(cities_json).replace(": u", ":")
    json_str = json_str.replace("'", '"')    
    return HttpResponse(json_str, 'application/json')
  
class CallBackRequest(TemplateView):
  def get(self, request, *args, **kwargs):
    content = {}
    data = {}
    lid = request.GET['lid']
    type = request.GET['type']
    type = int(type)
    lid = int(lid)
    callbackform = CallbackRequestForm()
    content.update(csrf(request))
    if(type==1):
      cidobj = Sales.objects.get(listingid=lid)
    if(type==2):
      cidobj = Rentals.objects.get(listingid=lid)
      
    content['CustomerId'] = cidobj.customerid
    content['ListingId'] = lid
    content['ListingType'] = type
    callbackobj = CallbackRequestForm(initial=data)
    content['form'] = callbackobj
    return render_template(request, "ListingInfo.html", content)
  
  def post(self,request, *args, **kwargs):
    content = {}
    name = request.POST['name']
    email = request.POST['email']
    phone = request.POST['phoneno']
    time1 = request.POST['pftime1']
    time2 = request.POST['pftime2']
    time3 = request.POST['pftime3']
    message = request.POST['message']
    cid = request.POST['customerid']
    lid = request.POST['listingid']
    type = request.POST['listingtype']
    callobj = Callbackrequests()
    callobj.customerid = int(cid)
    callobj.listingid = int(lid)
    callobj.listingtype = int(type)
    callobj.name = name
    callobj.email = email
    callobj.phone = phone
    callobj.preftime1 = time1
    callobj.preftime2 = time2
    callobj.preftime3 = time3
    callobj.message = message
    for i in xrange(1):
      randomcode = random.randint(100,1000)
      code=str(randomcode)
      callobj.confirmcode = '50' + code
      callobj.save()
    return HttpResponse("request taken")
    


class AjaxCustomerLogin(TemplateView):
  def get(self, request, *args, **kwargs):
    content = {}
    username = request.GET['username']
    pwd = request.GET['password'] 
    obj = Customers.objects.filter(email = username, loginpwd = pwd)
    if obj: 
      return HttpResponse("login success")
    else:
      return HttpResponse("Login Failed")   
    
    return HttpResponse('Done')
  
class AjaxConfirmMobile(TemplateView):

   def get(self, request, *args, **kwargs):
     mobile_no = request.GET['mobileno'].strip()
     mobile_no = mobile_no.replace('+','')
     
     #mobile_no = mobile_no[2:]
     #return HttpResponse(mobile_no)
     result = Customers.objects.filter(phone = mobile_no)
     c = 0

     if result:
       for obj in result:
         obj.ismobileverified = 1
         obj.save()
         c += 1
    
     result = Sales.objects.filter(phone = mobile_no)
     if result:
       for obj in result:
         obj.ismobileverified = 1
         obj.save()
         c += 1
       
     result = Rentals.objects.filter(phone = mobile_no)
     if result:
       for obj in result:
         obj.ismobileverified = 1
         obj.save()
         c += 1
       
     result = Visitors.objects.filter(mobileno = mobile_no)
     if result:
       for obj in result:
         obj.ismobileverified = 1
         obj.save()
         c += 1
       
     return HttpResponse('confirmed %d' %c) 

class MyIP(TemplateView):

   def get(self, request, *args, **kwargs):
     html = ''
     for key, value in request.META.items():
       html += '%s - %s<br>' %(key, value)

     return HttpResponse(html)
   

class TestModel(TemplateView):

  def get(self, request, *args, **kwargs):
    content = {}
    return render_template(request,"TestModel.html",content)

    
  
