from django.conf import settings
from IndiaDens.Customers import *
import urllib
import re
from datetime import*
import random
import datetime
from IndiaDens.lib import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
import time

class HomePage(LoginRequiredMixin, TemplateView):
  
  def get(self, request, *args, **kwargs):  
    content = {}
    Customerobj = request.session['Customer']
    if 'lid' in request.GET:
       listid = request.GET['lid']
       ptype = request.GET['type']
       if(ptype == '1'):
         salesobj = Sales.objects.filter(listingid = listid)
         if(salesobj):
           sobj = salesobj[0]
           sobj.delete()
         else:
           EMsg = "There is no list with this listing id"
           content['ErrMsg'] = EMsg
       if(ptype == '2'):
         rentalsobj = Rentals.objects.filter(listingid = listid)
         if(rentalsobj):
           robj = rentalsobj[0]
           robj.delete()
         else:
           EMsg = "There is no list with this listing id"
           content['ErrMsg'] = EMsg
    salesapprovallist = Sales.objects.filter(approvalstatus = 0, customerid = Customerobj.customerid)
    rentalapprovallist = Rentals.objects.filter(approvalstatus = 0, customerid = Customerobj.customerid)
    salesmobvercount = Sales.objects.filter(ismobileverified = 0, customerid = Customerobj.customerid).count()
    rentalsmobvercount = Rentals.objects.filter(ismobileverified = 0, customerid = Customerobj.customerid).count()
    mobilevercount = salesmobvercount + rentalsmobvercount
    
    salesapproval = Sales.objects.filter(approvalstatus = 0, customerid = Customerobj.customerid).count()
    rentalapproval = Rentals.objects.filter(approvalstatus = 0, customerid = Customerobj.customerid).count()
    approvalcount = salesapproval + rentalapproval
    
    salelist = Sales.objects.filter(customerid = Customerobj.customerid).count()
    rentlist = Rentals.objects.filter(customerid = Customerobj.customerid).count()
    listingcount = salelist + rentlist
    
    salesrejected = Sales.objects.filter(approvalstatus = -1, customerid = Customerobj.customerid).count()
    rentalsrejected = Rentals.objects.filter(approvalstatus = -1, customerid = Customerobj.customerid).count()
    rejectedcount = salesrejected + rentalsrejected
    
    salescount = 0
    salesexpirycount = Sales.objects.raw('select *from sales where DATEDIFF(expirydate, NOW()) BETWEEN 0 AND 3 AND customerid ='+ str(Customerobj.customerid))
    for sobj in salesexpirycount:
      salescount = salescount + 1
      
    callbackcount = Callbackrequests.objects.filter(isattended = 0, customerid = Customerobj.customerid).count()

    rentalscount  = 0
    rentalsexpirycount = Rentals.objects.raw('select *from rentals where DATEDIFF(expirydate, NOW()) BETWEEN 0 AND 3 AND customerid ='+ str(Customerobj.customerid))
    for robj in rentalsexpirycount:
      rentalscount = rentalscount + 1
    expirycount = salescount + rentalscount
    salescount = Sales.objects.filter(customerid = Customerobj.customerid).count()
    rentalcount = Rentals.objects.filter(customerid = Customerobj.customerid).count()
    count = salescount + rentalscount
    content['ismobileverified'] = Customerobj.ismobileverified
    content['listcount'] = approvalcount
    content['CountMobVerified'] = mobilevercount
    content['CountCusApproval'] = approvalcount
    content['CountRejected'] = rejectedcount
    content['CountCallBackReq'] = callbackcount
    content['CountExpiry'] = expirycount
    content['ConfirmationCode'] = Customerobj.mobilecode
    content['ismobverified'] = Customerobj.ismobileverified
    content['MobileNo'] = Customerobj.phone
    content['SaleList'] = salesapprovallist
    content['RentalList'] = rentalapprovallist
    content['CustomerType'] = Customerobj.customertype
    content['CountList'] = listingcount
    return render_template(request, "Customers/Index.html", content)

class Login(TemplateView):
  
  def get(self, request, *args, **kwargs):  
    content = {}
    content.update(csrf(request))
    if 'Customer' in request.session:
      return HttpResponseRedirect("/Customer/")
    return render_template(request, 'Customers/Login.html', content)

  def post(self, request, *args, **kwargs):  
    content = {}
    username = request.POST['username'].strip()
    password = request.POST['password'].strip()
    #mobile = request.POST['username2']
    customers = []
    if re.search('^\+?\d+$' , username, re.DOTALL):
      if len(username) == 10:
        username = username.replace("+", "")
        # If there is no ISD Code in the mobile prefix the number
        username = "91%s" %username
        
      customers = Customers.objects.filter(phone = username, loginpwd = password)
    else:
      customers = Customers.objects.filter(email = username, loginpwd = password)
    
    if customers:
      Customer = customers[0]
      request.session['Customer'] = Customer
      #return HttpResponseRedirect("/Customer/")
      return HttpResponse("Login Success")
    
    else:
      return HttpResponse("Login Failed")

# Commented by Murthy - To be removed.
#     if(Customers.objects.filter(email = username, loginpwd = password)):
#       Customer = Customers.objects.get(email = username, loginpwd = password)
#       request.session['Customer'] = Customer
#       return HttpResponseRedirect("/Customer/customer-menu")
# 
#     if(Customers.objects.filter(phone = mobile, loginpwd = password)):
#       Customer = Customers.objects.filter(phone = mobile, loginpwd = password)
#       request.session['Customer'] = Customer
#       return HttpResponseRedirect("/Customer/")
#     else:
#       errmsg = "Invalid username or password"
#       content['Errmsg'] = errmsg
#      return render_template(request, 'Customers/Login.html', content)

class CustomerListPage(TemplateView):
  def get(self, request, *args, **kwargs):  
    content = {}
    return render_template(request, 'Customers/CustomerListingsPage.html', content)
class CustomerListings(TemplateView):
  def get(self, request, *args, **kwargs):
    content = {}
    if 'cid' in request.GET:
        custid = int(request.GET['cid'])
        type = request.GET['type']
        if(type == "1"):
          if 'Customer' in request.session:
            Customer = request.session['Customer']
            if custid==Customer.customerid:
              CustomerSalesList = Sales.objects.filter(customerid = custid)
            else:
              Errmsg = "Access Denied"
              content['Errmsg'] = Errmsg
              return render_template(request, 'Customers/CustomerListings.html', content)
          elif 'User' in request.session:
            CustomerSalesList = Sales.objects.filter(customerid = custid)
          paginator = Paginator(CustomerSalesList,4)
          page = request.GET.get('page')
          try:
            getlistings = paginator.page(page)
          except PageNotAnInteger:
            getlistings= paginator.page(1)
          except EmptyPage:
            getlistings= paginator.page(paginator.num_pages)
          content['CustomersList'] = getlistings
          content['cid'] = custid
          content['type'] = type
          return render_template(request, 'Customers/CustomerListings.html', content)
        if(type == "2"):
          if 'Customer' in request.session:
            Customer = request.session['Customer']
            if custid==Customer.customerid:
              CustomerRentalList = Rentals.objects.filter(customerid = custid)
            else:
              Errmsg = "Access Denied"
              content['Errmsg'] = Errmsg
              return render_template(request, 'Customers/CustomerListings.html', content)
          elif 'User' in request.session:
            CustomerRentalList = Rentals.objects.filter(customerid = custid)
          paginator = Paginator(CustomerRentalList,4)
          page = request.GET.get('page')
          try:
            getrentallistings = paginator.page(page)
          except PageNotAnInteger:
            getrentallistings= paginator.page(1)
          except EmptyPage:
            getrentallistings= paginator.page(paginator.num_pages)
          content['CustomersList'] = getrentallistings
          content['type'] = type
          return render_template(request, 'Customers/CustomerListings.html', content)
    else:
        Errmsg = "You are not an authorized customer to view listing"
        content['Errmsg'] = Errmsg
        return render_template(request, 'Customers/CustomerListings.html', content)
  
  def post(self, request, *args, **kwargs):
    content = {}
    Listings = []
    type = request.POST['type']
    searchlisting = request.POST['keywords']
    customer = request.session['Customer']
    if(type == "1"):
      sale_list = Sales.objects.filter(customerid = customer.customerid)
      if len(searchlisting)!= 0:
        for salesobj in sale_list:
          if searchlisting in [salesobj.propertyid, salesobj.phone, 
                               salesobj.address, salesobj.City.name, 
                               salesobj.State.name]:
            Listings.append(salesobj)
          if salesobj.title.find(searchlisting.lower()):
            Listings.append(salesobj)
      else:
        Listings = Sales.objects.filter(customerid = customer.customerid)
      content['type'] = type
      content['CustomersList'] = Listings
      return render_template(request, 'Customers/CustomerListings.html', content)
    
    if(type == "2"):
      RentalsList = Rentals.objects.filter(customerid = customer.customerid)
      if len(searchlisting)!= 0:
        for rentalsobj in RentalsList:
          if searchlisting.lower() in [rentalsobj.propertyid, rentalsobj.phone, 
                                       rentalsobj.address, rentalsobj.City.name,
                                       rentalsobj.State.name]:
            Listings.append(rentalsobj)
          if rentalsobj.title.find(searchlisting.lower()):
            Listings.append(rentalsobj)
      else:
        Listings = Rentals.objects.filter(customerid = customer.customerid)
      content['type'] = type
      content['CustomersList'] = Listings
      return render_template(request, 'Customers/CustomerListings.html', content)
    
    else:
      return HttpResponse("Please Provide Type and Keyword to search")
       
    
class ListingDelete(TemplateView):
  def get(self, request, *args, **kwargs):
    content = {}
    custobj = request.session['Customer']
    type = request.GET['type']
    if 'lid' in request.GET:
      lid = request.GET['lid']
      if (type == "1"):
        salesDelObj = Sales.objects.get(listingid = lid)
        salesDelObj.delete()
        url = "/Customer/customer-listings?cid="+str(custobj.customerid)+"&type="+str(1)
        return HttpResponseRedirect(url)
      
      if(type == "2"):
        rentalsobj = Rentals.objects.get(listingid = lid)
        rentalsobj.delete()
        url ="/Customer/customer-listings?cid=" +str(custobj.customerid)+"&type=" +str(2)
        return HttpResponseRedirect(url)
#<<<<
    else:
      Errmsg = "There is no such listid to delete"
      content['Errmsg'] = Errmsg
      return render_template(request, 'Customers/CustomerListings.html', content)
  
class MobileConfirm(TemplateView):
  ''' Sample URL: http://localhost:8000/Customer/mobile-confirm?mobile=9440111843&pinno=4321'''
  def get(self, request, *args, **kwargs):
    content = {}
    mobile = request.GET['mobile']
    pinno = request.GET['pinno']
    code = pinno[0:2]
    if(code=='10'):    
      conf_list = Customers.objects.filter(phone=mobile,mobilecode=pinno)
    if(code=='22'):   
      conf_list = Sales.objects.filter(phone=mobile,mobilecode=pinno)
    if(code=='24'):    
      conf_list = Rentals.objects.filter(phone=mobile,mobilecode=pinno)
    if not conf_list:
      return HttpResponse("Not Matched")
    obj = conf_list[0]
    obj.ismobileverified = 1
    obj.save()
    return HttpResponse("Done")    
     
class ListingForm(LoginRequiredMixin, TemplateView):

  def get(self, request, *args, **kwargs):  
    content = {}
    data = {} 
    content.update(csrf(request))
    typeid=int(request.GET['type'])
    limit=5
    content['type']=typeid
    image_list = []
    STATES = []

   
    state_list = States.objects.all()
    for state in state_list:
      STATES.append((state.stateid, state.name))
    Cyear = []
    Cyear =  [x for x in range(1950, time.localtime().tm_year)]
    Cyear.reverse()

    # For Sales
    if(typeid==1):
      if 'cid' in request.GET:
        cid = int(request.GET['cid'])
        content['cid']=cid
        if 'Customer' in request.session:
          Cust = request.session['Customer']
          if cid==Cust.customerid:
            Customer = Customers.objects.get(customerid=Cust.customerid)
          elif 'User' in request.GET:
            Customer = Customers.objects.get(customerid=Cust.customerid)
          else:
            return HttpResponseRedirect("/Customer/")
          data['City'] = Customer.City.name
          data['State'] = Customer.stateid
          data['Phone']=Customer.phone
          data['Email']=Customer.email
          data['ContactName'] = Customer.firstname  +' '+  Customer.lastname
        imageobj_list = Salelistingimages.objects.filter(listingid= -1)
        i = 0
        for obj in imageobj_list:
            i += 1
            if i <= limit:
              image_list.append(obj)
            else:
              break
              
        num_images = len(image_list)
        i=0
        counter=limit-num_images
        for i in range(0, counter):
          imgObj = Salelistingimages()
          imgObj.description = ""
          if counter==5 and i==0:
            imgObj.imagethumb = 1
            i=i+1
          imgObj.listingimageid = 0
          imgObj.largeimage = 'http://webmaster.ypsa.org/wp-content/uploads/2012/08/no_thumb.jpg'
          image_list.append(imgObj)
        content['image_list'] = image_list
        attr_list = []
        attrobj_list = Saleattributes.objects.filter(listingid= -1)
        i = 0
        for obj in attrobj_list:
            i += 1
            if i <= limit:
               attr_list.append(obj)
            else:
              break
        num_attributes = len(attr_list)
        for i in range(0, limit - num_attributes):
            attrObj = Saleattributes()
            attrObj.value = ""
            attrObj.attributeid = 0
            attr_list.append(attrObj)
        content['attr_list'] = attr_list
        now = datetime.datetime.now()
        data['PostedDate'] = now
        data['BedRooms'] = 0
        data['BathRooms'] = 0
        content['form'] = SalesForm(initial=data, states = STATES)
        return render_template(request,"Customers/ListingForm.html",content)
 
      if 'lid' in request.GET:
        if 'Customer' in request.session:
          Cust = request.session['Customer']
          Customer = Customers.objects.get(customerid=Cust.customerid)
          data['Phone']=Customer.phone
          data['Email']=Customer.email
          data['ContactName'] = Customer.firstname  +' '+  Customer.lastname
          data['State'] = Customer.stateid
          data['City'] = Customer.City.name
          cid = Customer.customerid
          cobj = Sales.objects.filter(customerid = cid)
          lid = int(request.GET['lid'])
          l = []
          for i in cobj:
            l.append(i.listingid)
            if (i.listingid == lid):
              Salesform=Sales.objects.get(listingid = lid)
              content['lid'] = lid
          if lid not in l:
            return HttpResponse("invalid listing id")  
        if 'User' in request.session:
          lid = int(request.GET['lid'])
          Salesform=Sales.objects.get(listingid = lid)
          content['lid'] = lid
        data['PropertyType']=Salesform.propertytypeid
        propertytype= Salesform.propertytypeid
        content['PropertyType']=propertytype
        data['Ownership']=Salesform.ownership
        data['Title'] = Salesform.title
        data['Price']=Salesform.price
        data['BedRooms']=Salesform.bedrooms
        data['BathRooms']=Salesform.bathrooms
        data['Area']=Salesform.area
        data['AreaUnit']=Salesform.areaunit
        data['VirtualTour'] = Salesform.virtualtour
        data['LandMark1']=Salesform.landmark1
        data['LandMark2']=Salesform.landmark2
        data['LandMark3']=Salesform.landmark3
        data['LandMark4']=Salesform.landmark4
        data['PostalCode']=Salesform.postalcode
        #data['ContactName']=Salesform.contactname
        data['Phone']=Salesform.phone      
        data['Address']=Salesform.address
        data['Latitude'] = Salesform.latitude
        data['Longitude'] = Salesform.longitude
        data['Description']=Salesform.description
        cityid = Salesform.cityid
        content['cityid'] = cityid
        data['City']=Salesform.City.name
        data['State']=Salesform.stateid
        data['Email']=Salesform.email
        data['Website']=Salesform.website
        data['VirtualTour']=Salesform.virtualtour
        content['Approvalstatus'] = Salesform.approvalstatus
        #data['PropeetyId']=Salesform.propertyid
        x = Salesform.lift
        if (x==1):
          x=True
        elif(x==0):
          x = False
        data['Lift']= x
        y = Salesform.gym
        if (y==0):
          y= False
        else:
          y = True
        data['Gym']=y
        z = Salesform.swimmingpool
        if(z==1):
          z = True
        else:
          z = False
        data['SwimmingPool']= z
        a = Salesform.gatedcommunity
        if(a==1):
          a = True
        else:
          a = False
        data['GatedCommunity']= a
        data['PowerBackUp']=Salesform.powerbackup
        data['Furnished']=Salesform.furnished
        b = Salesform.cupboards
        if(b==1):
          b = True
        else:
          b = False
        data['Cupboards']= b
        data['Facing']=Salesform.facing
        data['Possession']=Salesform.possession
        data['ConstructionDate']=Salesform.constructiondate
        data['PropertyStatus']=Salesform.propertystatus
        now = datetime.datetime.now()
        data['PostedDate']=now
        data['PropertyId']=Salesform.propertyid
        data['Planid']=Salesform.planid
        saleform=SalesForm(initial=data, states = STATES)
        content['form']=saleform
        if 'message' in request.session:
          message = request.session['message']
          content['successmsg']=message
          del request.session['message']
 
        if 'User' in request.session:
          content['approved']=SalesForm()
          data['Approved']=Salesform.approvalstatus
          content['approved']=SalesForm(initial=data, states = STATES)
        
        imageobj_list = Salelistingimages.objects.filter(listingid=lid)
        i = 0
        for obj in imageobj_list:
          i += 1
          if i <= limit:
            image_list.append(obj)
          else:
            break
             
        num_images = len(image_list)
        count = limit-num_images
        i=0
        for i in range(0, count):
          imgObj = Salelistingimages()
          if count==5 and i==0:
            imgObj.imagethumb = 1
            i=i+1
          imgObj.description = ""
          imgObj.listingimageid = 0
          imgObj.largeimage = 'http://webmaster.ypsa.org/wp-content/uploads/2012/08/no_thumb.jpg'
          image_list.append(imgObj)
        content['IMAGE_URL'] = settings.IMAGE_URL
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
        num_attributes = len(attr_list)
        for i in range(0, limit - num_attributes):
            attrObj = Saleattributes()
            attrObj.value = ""
            attrObj.attributeid = 0
            attr_list.append(attrObj)
        content['attr_list'] = attr_list
 
        return render_template(request,"Customers/ListingForm.html",content)
      
    elif(typeid == 2):
      if 'cid' in request.GET:
        cid = int(request.GET['cid'])
        content['cid']=cid
        if 'Customer' in request.session:
          Cust = request.session['Customer']
          if cid==Cust.customerid:
            Customer = Customers.objects.get(customerid=Cust.customerid)
          elif 'User' in request.GET:
            Customer = Customers.objects.get(customerid=Cust.customerid)
          else:
            return HttpResponseRedirect("/Customer/")
          data['City'] = Customer.City.name
          data['State'] = Customer.stateid
          data['Phone']=Customer.phone
          data['Email']=Customer.email
          data['ContactName'] = Customer.firstname  +' '+  Customer.lastname
        imageobj_list = Rentallistingimages.objects.filter(listingid= -1)
        i = 0
        for obj in imageobj_list:
            i += 1
            if i <= limit:
               image_list.append(obj)
            else:
              break
               
        num_images = len(image_list)
        counter = limit-num_images
        i=0
        for i in range(0, counter):
          imgObj = Rentallistingimages()
          imgObj.description = ""
          if counter==5 and i==0:
            imgObj.imagethumb = 1
            i=i+1
          imgObj.listingimageid = 0
          imgObj.largeimage = 'http://webmaster.ypsa.org/wp-content/uploads/2012/08/no_thumb.jpg'
          image_list.append(imgObj)
        content['IMAGE_URL'] = settings.IMAGE_URL
        content['image_list'] = image_list
        attr_list = []
        attrobj_list = Rentalattributes.objects.filter(listingid= -1)
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
        content['attr_list'] = attr_list
        now = datetime.datetime.now()
        data['PostedDate'] = now
        data['BedRooms'] = 0
        data['BathRooms'] = 0
        content['form'] = RentalsForm(initial=data, states = STATES)
        return render_template(request,"Customers/ListingForm.html",content)
      if 'lid' in request.GET:
        if 'Customer' in request.session:
          Cust = request.session['Customer']
          Customer = Customers.objects.get(customerid=Cust.customerid)
          data['Phone']=Customer.phone
          data['Email']=Customer.email
          data['ContactName'] = Customer.firstname  +' '+  Customer.lastname
          data['State'] = Customer.stateid
          data['City'] = Customer.City.name
          cid = Customer.customerid
          cobj = Rentals.objects.filter(customerid = cid)
          lid = int(request.GET['lid'])
          l=[]
          for i in cobj:
            l.append(i.listingid)
            if (i.listingid == lid):
              Rentalsform=Rentals.objects.get(listingid = lid)
              content['lid'] = lid
          if lid not in l:
            return HttpResponse("invlaid listing id")
        if 'User' in request.session:
            lid = int(request.GET['lid'])
            Rentalsform=Rentals.objects.get(listingid = lid)
            content['lid'] = lid
        data['PropertyType'] = Rentalsform.propertytypeid
        propertytype = Rentalsform.propertytypeid
        content['PropertyType']=propertytype
        data['Ownership']=Rentalsform.ownership
        data['Title'] = Rentalsform.title
        data['Rent'] = Rentalsform.rent
        data['RentFrequency'] = Rentalsform.rentfreequency
        data['AdvanceAmount'] = Rentalsform.advanceamount
        data['AdvanceFrequency'] = Rentalsform.advancefreequency
        data['Maintenance']= Rentalsform.maintenance
        c = Rentalsform.allowed_family
        if (c==1):
          c = True
        else:
          c = False 
        data['AllowedFamily']= c
        d = Rentalsform.allowed_bachelors
        if(d==1):
          d = True
        else:
          d = False
        data['AllowedBachelors']= d
        data['BedRooms']=Rentalsform.bedrooms
        data['BathRooms']=Rentalsform.bathrooms
        data['Area']=Rentalsform.area
        data['AreaUnit']=Rentalsform.areaunit
        data['LandMark1']=Rentalsform.landmark1
        data['LandMark2']=Rentalsform.landmark2
        data['LandMark3']=Rentalsform.landmark3
        data['LandMark4']=Rentalsform.landmark4
        data['PostalCode']=Rentalsform.postalcode
        data['ContactName']=Rentalsform.contactname
        data['Longitude'] = Rentalsform.longitude
        data['Latitude'] = Rentalsform.longitude
        data['Description']=Rentalsform.description
        data['Phone']=Rentalsform.phone      
        data['Address']=Rentalsform.address
        data['Description']=Rentalsform.description
        data['City']=Rentalsform.City.name
        data['State']=Rentalsform.stateid
        data['Email']=Rentalsform.email
        data['Website']=Rentalsform.website
        data['VirtualTour']=Rentalsform.virtualtour
        content['Approvalstatus'] = Rentalsform.approvalstatus
        x = Rentalsform.lift
        if(x==1):
          x = True
        else:
          x = False 
        data['Lift']= x
        y = Rentalsform.gym
        if(y==1):
          y = True
        else:
          y = False
        data['Gym']=y
        z = Rentalsform.swimmingpool
        if(z==1):
          z = True
        else:
          z = False
        data['SwimmingPool']=z
        a = Rentalsform.gatedcommunity
        if(a==1):
          a = True
        else:
          a = False
        data['GatedCommunity']=a
        data['PowerBackUp']=Rentalsform.powerbackup
        data['Furnished']=Rentalsform.furnished
        b = Rentalsform.cupboards
        if(b==1):
          b=True
        else:
          b =False
        data['Cupboards']=b
        data['Facing']=Rentalsform.facing
        data['Possession']=Rentalsform.possession
        data['PresentStatus']=Rentalsform.propertystatus
        datenow = datetime.datetime.now()
        data['PostedDate']=datenow
        data['PropertyId']=Rentalsform.propertyid
        data['ConstructionDate'] = Rentalsform.constructiondate
        data['Planid']= Rentalsform.planid
        
        rform =RentalsForm(initial = data, states = STATES)
        content['form']=rform
        if 'message' in request.session:
          message = request.session['message']
          content['successmsg']=message
          del request.session['message']
        if 'User' in request.session:
          content['approved']=RentalsForm()
          data['Approved']=Rentalsform.approvalstatus
          content['approved']=RentalsForm(initial=data)
        imageobj_list = Rentallistingimages.objects.filter(listingid=lid)
        i = 0
        for obj in imageobj_list:
            i += 1
            if i <= limit:
               image_list.append(obj)
            else:
              break
             
        num_images = len(image_list)
        counter = limit-num_images
        i=0
        for i in range(0, counter):
          imgObj = Rentallistingimages()
          imgObj.description = ""
          if counter==5 and i==0:
            imgObj.imagethumb = 1
            i=i+1
          imgObj.listingimageid = 0
          imgObj.largeimage = 'http://webmaster.ypsa.org/wp-content/uploads/2012/08/no_thumb.jpg'
          image_list.append(imgObj)
        content['IMAGE_URL'] = settings.IMAGE_URL
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
        content['attr_list'] = attr_list
 
        return render_template(request,"Customers/ListingForm.html",content)
       
      else:
        return HttpResponse("Invalid ListingId")
       
    else:
      return HttpResponse("Invalid Typeid")

  def post(self, request, *args, **kwargs):
        content={}
        data = {}
        STATES = []
        state_list = States.objects.all()
        for state in state_list:
          STATES.append((state.stateid, state.name))        
        typeid = int(request.POST['Typeid'])
        if(typeid == 1):
          
          sform=SalesForm(request.POST,  states = STATES)           
          if sform.is_valid():
            cid = request.POST['cid']
            if cid:
              SaleObj = Sales()
              SaleObj.customerid = int(cid)
            lid = request.POST['lid']          
            if lid:
              lid = int(lid)
              SaleObj=Sales.objects.get(listingid = lid)
            else:
              cid = request.POST['cid']            
              SaleObj = Sales()
              SaleObj.customerid =cid 
            SaleObj.propertytypeid = int(sform.cleaned_data['PropertyType'])
            SaleObj.ownership = int(sform.cleaned_data['Ownership'])
            SaleObj.title = sform.cleaned_data['Title']
            SaleObj.price = int(sform.cleaned_data['Price'])
            bedrooms = sform.cleaned_data['BedRooms']
            if bedrooms:
              SaleObj.bedrooms = int(sform.cleaned_data['BedRooms'])
            else:
              SaleObj.bedrooms = 0
            bathrooms= sform.cleaned_data['BathRooms']
            if bathrooms:
              SaleObj.bathrooms = int(sform.cleaned_data['BathRooms'])
            else:
              SaleObj.bathrooms = 0
            area = sform.cleaned_data['Area']
            if area:
              SaleObj.area = int(sform.cleaned_data['Area'])
            else:
              SaleObj.area = 0
            SaleObj.areaunit = int(sform.cleaned_data['AreaUnit'])
            SaleObj.address = sform.cleaned_data['Address']
            SaleObj.landmark1 = sform.cleaned_data['LandMark1']
            SaleObj.landmark2 = sform.cleaned_data['LandMark2']
            SaleObj.landmark3 = sform.cleaned_data['LandMark3']
            SaleObj.landmark4 = sform.cleaned_data['LandMark4']
            SaleObj.latitude = sform.cleaned_data['Latitude']
            SaleObj.longitude = sform.cleaned_data['Longitude']
            CityID = sform.cleaned_data['CityID']
            state = sform.cleaned_data['State']
            cityname= sform.cleaned_data['City']
            Approvalstatus = request.POST['Approvalstatus']
            if (Approvalstatus=='0'):
              SaleObj.approvalstatus = 3
              SaleObj.save()
            if not CityID:
              if(Cities.objects.filter(name = cityname)):
                 cityobj = Cities.objects.get(name = cityname)
                 SaleObj.cityid = cityobj.cityid
              else:
                cityobj = Cities();
                cityobj.name = cityname
                cityobj.isnew = True
                cityobj.stateid = int(state)
                cityobj.save()
                city = Cities.objects.latest('cityid')
                SaleObj.cityid = city.cityid
            else:
              cityobj = Cities.objects.get(name = cityname)
              SaleObj.cityid = cityobj.cityid 
            SaleObj.stateid = int(sform.cleaned_data['State'])
            SaleObj.postalcode = sform.cleaned_data['PostalCode']
            SaleObj.contactname = sform.cleaned_data['ContactName']
            phone  = sform.cleaned_data['Phone']
            if phone:
              x= len(phone)
              if(x==10):
                SaleObj.phone='91'+phone
              else:
                SaleObj.phone = phone
            else:
              SaleObj.phone = ''
            SaleObj.email = sform.cleaned_data['Email']
            SaleObj.website = sform.cleaned_data['Website']
            SaleObj.description = sform.cleaned_data['Description']
            SaleObj.virtualtour = sform.cleaned_data['VirtualTour']
            SaleObj.lift = int(sform.cleaned_data['Lift'])
            SaleObj.gym = int(sform.cleaned_data['Gym'])
            SaleObj.swimmingpool = int(sform.cleaned_data['SwimmingPool'])
            SaleObj.gatedcommunity = int(sform.cleaned_data['GatedCommunity'])
            SaleObj.powerbackup = int(sform.cleaned_data['PowerBackUp'])
            SaleObj.furnished = int(sform.cleaned_data['Furnished'])
            SaleObj.cupboards = int(sform.cleaned_data['Cupboards'])
            SaleObj.facing = int(sform.cleaned_data['Facing'])
            SaleObj.possession = sform.cleaned_data['Possession']
            SaleObj.constructiondate = sform.cleaned_data['ConstructionDate']
            SaleObj.propertystatus = sform.cleaned_data['PropertyStatus']
            SaleObj.posteddate = sform.cleaned_data['PostedDate']
            SaleObj.planid =int(sform.cleaned_data['Planid'])
            if 'User' in request.session:
              SaleObj.approvalstatus=int(sform.cleaned_data['Approved'])
            SaleObj.save()
            if lid:
              message = "Your Info Has Been Successfully Updated"
              request.session['message']=message
            maxlimit=5
            html = ''
            for key in request.POST:
                if key.__contains__('ImgDelete-'):
                  index = key.split('-')[1]
                  imgdel = request.POST['ImgDelete-%s' %index]
                  imgobj = Salelistingimages.objects.get(listingimageid=imgdel)
                  imgobj.delete()             
            counter = 0  
            for key in request.FILES:
              index = key.split('-')[1]
              f = request.FILES[key]
              ext_name = f.name.split(".")[1]
              image_data = f.read()
              f.close()
              description = request.POST['Description-%s' %index]
              imagethumb = request.POST['ImageThumb-%s' %index]
              listing_image_id = int(request.POST['ListingImageID-%s' %index])
              file_name = "SaleListing-%s-%s.%s" %(lid, index, ext_name)
              SaleObj.imagethumb = file_name
              SaleObj.save()
              f = open(settings.IMAGE_ROOT + "\ListingImages\%s" %file_name,"wb")
              f.write(image_data)
              f.close()        
              if listing_image_id > 0:
                obj = Salelistingimages.objects.get(listingimageid=listing_image_id)
                if len(description.strip()) > 0:
                  obj.description = description
                  obj.save()
                if imagethumb:
                  obj.imagethumb = "%s" %file_name
                  obj.largeimage = "%s" %file_name
                else:
                  obj.largeimage = "%s" %file_name
                obj.save()
                return HttpResponseRedirect("listing-form?type=1&lid=%s" %lid)
              else:
                obj = Salelistingimages()
                if not lid:
                  l_obj = Sales.objects.latest('listingid')
                  obj.listingid = int(l_obj.listingid)
                else:
                  obj.listingid = int(lid)
                  obj.description = description
                if imagethumb: 
                  obj.imagethumb = "%s" %file_name
                  obj.largeimage = "%s" %file_name
                else:
                  obj.largeimage = "%s" %file_name
                obj.save()
     
            for key in request.POST:
                if not key.__contains__('-'): continue
                if not key.__contains__('AttributeID'): continue
                rowno = key.split("-")[1]
                name = request.POST['Name-%s' %rowno]
                value = request.POST['Value-%s' %rowno]
                attribute_id = int(request.POST['AttributeID-%s' %rowno])
                if attribute_id > 0:
                  obj = Saleattributes.objects.get(attributeid=attribute_id)
                  if (len(name.strip())>0 or len(value.strip())>0):
            
                    obj.name = name
                    obj.value = value
                    obj.save()   
                else:
                  obj = Saleattributes()
                  if not lid:
                    l_obj = Sales.objects.latest('listingid')
                    obj.listingid = int(l_obj.listingid)
                  else:
                    obj.listingid = int(lid)
                  if(len(name.strip())>0 and len(value.strip())>0):
                    obj.name = name
                    obj.value = value
                    obj.save()
            if cid:
              sobj=Sales.objects.latest('listingid')
              slid = str(sobj.listingid)
              sobj.propertyid = "IDS" + slid.zfill(8)
              sobj.approvalstatus = 2
              sobj.save()   
              lid = sobj.listingid
              return HttpResponseRedirect("listing-form?type=1&lid=%s" %lid)
            if lid:
              lid = request.POST['lid']
              return HttpResponseRedirect("listing-form?type=1&lid=%s" %lid)
         
        elif(typeid == 2):
            STATES = []
            state_list = States.objects.all()
            for state in state_list:
              STATES.append((state.stateid, state.name))
            rform = RentalsForm(request.POST,states=STATES)
            if rform.is_valid():
              cid = request.POST['cid']
              if cid:
                Rentalsobj = Rentals()
                Rentalsobj.customerid = int(cid)
              lid = request.POST['lid']  
              if lid:
                lid = int(request.POST['lid'])
                Rentalsobj=Rentals.objects.get(listingid = lid)
              else:
                Rentalsobj=Rentals()
                Rentalsobj.customerid = int(cid)
              Rentalsobj.propertytypeid = int(rform.cleaned_data['PropertyType'])              
              Rentalsobj.ownership = int(rform.cleaned_data['Ownership'])
              Rentalsobj.title = rform.cleaned_data['Title']
              Rentalsobj.rent = int(rform.cleaned_data['Rent'])
              Rentalsobj.rentfreequency = int(rform.cleaned_data['RentFrequency']) 
              AdvanceAmount = rform.cleaned_data['AdvanceAmount']
              if AdvanceAmount:
                Rentalsobj.advanceamount = int(rform.cleaned_data['AdvanceAmount'])
              else:
                Rentalsobj.advanceamount = 0
              Maintenance = rform.cleaned_data['Maintenance']
              if Maintenance:
                 Rentalsobj.maintenance = int(rform.cleaned_data['Maintenance'])
              else:
                Rentalsobj.maintenance = 0
              Rentalsobj.allowed_family = int(rform.cleaned_data['AllowedFamily'])
              Rentalsobj.allowed_bachelors = int(rform.cleaned_data['AllowedBachelors'])
              bedrooms = rform.cleaned_data['BedRooms']
              if bedrooms:
                Rentalsobj.bedrooms = int(rform.cleaned_data['BedRooms'])
              else:
                Rentalsobj.bedrooms = 0
              bathrooms= rform.cleaned_data['BathRooms']
              if bathrooms:
                Rentalsobj.bathrooms = int(rform.cleaned_data['BathRooms'])
              else:
                Rentalsobj.bathrooms = 0
              area = rform.cleaned_data['Area']
              if area:
                Rentalsobj.area = int(rform.cleaned_data['Area'])
              else:
                Rentalsobj.area = 0
              Rentalsobj.areaunit = int(rform.cleaned_data['AreaUnit'])
              Rentalsobj.landmark1 = rform.cleaned_data['LandMark1']
              Rentalsobj.landmark2 = rform.cleaned_data['LandMark2']
              Rentalsobj.landmark3 = rform.cleaned_data['LandMark3']
              Rentalsobj.landmark4 = rform.cleaned_data['LandMark4']
              Rentalsobj.postalcode = rform.cleaned_data['PostalCode']
              Rentalsobj.latitude = rform.cleaned_data['Latitude']
              Rentalsobj.longitude = rform.cleaned_data['Longitude']
              Rentalsobj.contactname = rform.cleaned_data['ContactName']
              phone  = rform.cleaned_data['Phone']
#               if 'Customer' in request.session:
#                 Customer = request.session['Customer']
#                 if(Customer.phone == phone):
#                   if(Customer.isconfirmed == 1):
#                     Rentalsobj.isconfirmed = 1
#                   else:
#                     Rentalsobj.isconfirmed = 0
#                 else:
#                   for i in xrange(1):
#                     randomcode = random.randint(1000,10000)
#                     code=str(randomcode)
#                     Rentalsobj.confirmcode = code
              if phone:
                x = len(phone)
                if(x==10):
                  Rentalsobj.phone='91'+phone
                else:
                  Rentalsobj.phone=phone
              else:
                Rentalsobj.phone = 0              
              Rentalsobj.address = rform.cleaned_data['Address']
              CityID = rform.cleaned_data['CityID']
              state = rform.cleaned_data['State']
              cityname = rform.cleaned_data['City']           
              if not CityID:
                if(Cities.objects.filter(name = cityname)):
                   cityobj = Cities.objects.get(name = cityname)
                   Rentalsobj.cityid = cityobj.cityid
                else:
                  cityobj = Cities();
                  cityobj.name = cityname
                  cityobj.isnew = True
                  cityobj.stateid = int(state)
                  cityobj.save()
                  city = Cities.objects.latest('cityid')
                  Rentalsobj.cityid = city.cityid 
              else:
                cityobj = Cities.objects.get(name = cityname)
                Rentalsobj.cityid = cityobj.cityid
              Rentalsobj.stateid = int(rform.cleaned_data['State'])
              Rentalsobj.email = rform.cleaned_data['Email']
              Rentalsobj.website = rform.cleaned_data['Website']
              Rentalsobj.virtualtour = rform.cleaned_data['VirtualTour']
              Rentalsobj.description = rform.cleaned_data['Description']
              Rentalsobj.lift =  int(rform.cleaned_data['Lift'])
              Rentalsobj.gym = int(rform.cleaned_data['Gym'])
              Rentalsobj.swimmingpool = int(rform.cleaned_data['SwimmingPool'])
              Rentalsobj.gatedcommunity = int(rform.cleaned_data['GatedCommunity'])
              Rentalsobj.powerbackup = int(rform.cleaned_data['PowerBackUp'])
              Rentalsobj.furnished = int(rform.cleaned_data['Furnished'])
              Rentalsobj.facing = int(rform.cleaned_data['Facing'])
              Rentalsobj.cupboards = int(rform.cleaned_data['Cupboards'])
              Rentalsobj.constructiondate = rform.cleaned_data['ConstructionDate']
              Rentalsobj.propertystatus = rform.cleaned_data['PresentStatus']
              Rentalsobj.possession = rform.cleaned_data['Possession']
              Approvalstatus = request.POST['Approvalstatus']
              if (Approvalstatus=='0'):
                Rentalsobj.approvalstatus = 3
                #Rentalsobj.save()
              #Rentalsobj.propertyid = rform.cleaned_data['PropertyId']
              if 'User' in request.session:
                Rentalsobj.approvalstatus=rform.cleaned_data['Approved']
              
              Rentalsobj.planid = int(rform.cleaned_data['Planid'])
 
              Rentalsobj.posteddate = rform.cleaned_data['PostedDate']
              Rentalsobj.save()
              if lid:
                message = "Your Info Has Been Successfully Updated"
                request.session['message']=message
              maxlimit=5
              html = '' 
              for key in request.POST:
                if key.__contains__('ImgDelete-'):
                  index = key.split('-')[1]
                  imgdel = request.POST['ImgDelete-%s' %index]
                  imgobj = Rentallistingimages.objects.get(listingimageid=imgdel)
                  imgobj.delete()             
              for key in request.FILES:
                index = key.split('-')[1]
                f = request.FILES[key]
                ext_name = f.name.split(".")[1]
                image_data = f.read()
                f.close()
                description = request.POST['Description-%s' %index]
                imagethumb = request.POST['ImageThumb-%s' %index]
                listing_image_id = int(request.POST['ListingImageID-%s' %index])
                file_name = "RentalListing-%s-%s.%s" %(lid, index, ext_name)
                Rentalsobj.imagethumb=file_name
                Rentalsobj.save()
                f = open(settings.IMAGE_ROOT + "\ListingImages\%s" %file_name,"wb")
                f.write(image_data)
                f.close()        
                if listing_image_id > 0:
                  obj = Rentallistingimages.objects.get(listingimageid=listing_image_id)
                  if len(description.strip()) > 0:
                    obj.description = description
                  if imagethumb:
                    obj.imagethumb="%s" %file_name
                    obj.largeimage = "%s" %file_name
                  else:
                    obj.largeimage = "%s" %file_name
                  obj.save()
                  return HttpResponseRedirect("listing-form?type=2&lid=%s" %lid)
                else:
                  obj = Rentallistingimages()
                  if not lid:
                    l_obj = Rentals.objects.latest('listingid')
                    obj.listingid = int(l_obj.listingid)
                  else:
                    obj.listingid = int(lid)
                  obj.description = description
                  if imagethumb: 
                    obj.imagethumb = "%s" %file_name
                    obj.largeimage = "%s"%file_name
                  else:
                    obj.largeimage = "%s" %file_name
                  obj.save()
            for key in request.POST:
                if not key.__contains__('-'): continue
                if not key.__contains__('AttributeID'): continue
                rowno = key.split("-")[1]
                name = request.POST['Name-%s' %rowno]
                value = request.POST['Value-%s' %rowno]
                attribute_id = int(request.POST['AttributeID-%s' %rowno])
                if attribute_id > 0:
                  obj = Rentalattributes.objects.get(attributeid=attribute_id)
                  if (len(name.strip())>0 or len(value.strip())>0):
                    obj.name = name
                    obj.value = value
                    obj.save()   
                else:
                  obj = Rentalattributes()
                  if not lid:
                    l_obj = Rentals.objects.latest('listingid')
                    obj.listingid = int(l_obj.listingid)
                  else:
                    obj.listingid = int(lid)
                  if(len(name.strip())>0 and len(value.strip())>0):
                    obj.name = name
                    obj.value = value
                    obj.save()
            if cid:
                robj=Rentals.objects.latest('listingid')
                rlid = str(robj.listingid)
                robj.propertyid = "IDR" + rlid.zfill(8)
                robj.approvalstatus = 2
                robj.save()   
                lid = robj.listingid
                return HttpResponseRedirect("listing-form?type=2&lid=%s" %lid)
            if lid:
                lid = request.POST['lid']
                return HttpResponseRedirect("listing-form?type=2&lid=%s" %lid)
   

class Confirm(TemplateView):

  def get(self, request, *args, **kwargs):
     content = {}
     code = self.args[0]
     if(Customers.objects.filter(emailcode = code)):
       Customerobj = Customers.objects.get(emailcode = code)
       Customerobj.isemailverified = True
       Customerobj.save()
     return render_template(request,"customers/CustomerConfirmed.html", content)


class ResetPassword(TemplateView):
  def get(self, request, *args, **kwargs):
    content = {}
    emailid = request.GET['emailid']
    if(Customers.objects.filter(email = emailid)):
      CustomerObj = Customers.objects.get(email = emailid)
      content['first_name'] = CustomerObj.firstname
      content['last_name'] = CustomerObj.lastname
      content['email'] = CustomerObj.email
      content['password'] = CustomerObj.loginpwd
      html = render_email('Customers/EMail-PasswordReset.html', content)
      SendEMail("Password Reset", html, str(CustomerObj.email.strip()))
      return HttpResponse('done')
    else:
      return HttpResponse("Email not found")

class CloseAccount(TemplateView):
  
  def get(self, request, *args, **kwargs):
    content = {}
    custid = request.GET['cid']
    return render_template(request, "Customers/CloseAccount.html", content)

  def post(self, request, *args, **kwargs):
    content={}
    custobj = request.session['Customer']
    cid = custobj.customerid 
    saleslist = Sales.objects.filter(customerid = cid)
    if(saleslist):
      for sobj in saleslist: 
        #sobj.isactive = False
        sobj.delete()
      
    rentalslist = Rentals.objects.filter(customerid = cid)
    if(rentalslist):
      for robj in rentalslist:
        #robj.isactive = False
        robj.delete()
        
    customer = Customers.objects.get(customerid = cid)
    if (customer):
      #customer.isdeleted = False
      customer.delete()
           
    return HttpResponseRedirect("/")
  
  
class ChangePassword(TemplateView):
  def get(self, request, *args, **kwargs):
    if 'Customer' in request.session:  
        content = {}
        content.update(csrf(request))
        return render_template(request, "Customers/ChangePassword.html", content)
    else:
        return HttpResponseRedirect("/Customer/login")

  def post(self, request, *args, **kwargs):
    content = {}
    cpwd = request.POST['currentpassword']
    npwd = request.POST['newpassword']
    cnfpwd = request.POST['confirmpassword']
    customer=request.session['Customer']
    cobj = Customers.objects.get(customerid=customer.customerid)
    if(cobj.loginpwd == cpwd):
        if(npwd == cnfpwd):
            cobj.loginpwd = cnfpwd
            cobj.save()
            msg = "Password has been changed successfully"
            content['msg'] = msg
            return HttpResponseRedirect("/Customer/")
        else:
            err = "password didn't match....try again"
            content['errmsg'] = err
            return render_template(request, "Customers/ChangePassword.html", content)
            
    else:
        err = "password didn't match....try again"
        content['errmsg'] = err
    return render_template(request, "Customers/ChangePassword.html", content) 

      
    