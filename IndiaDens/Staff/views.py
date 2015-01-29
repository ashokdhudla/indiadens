from IndiaDens.Staff import *
from IndiaDens.Staff.forms import *
import urllib
import os
from django.conf import settings
from django.core.paginator import *
from django.db import connection

class HomePage(LoginRequiredMixin, TemplateView):
  def get(self, request, *args, **kwargs):
        content = {}
        return render_template(request, "Staff/Index.html", content)

class Logout(TemplateView):
  def get(self, request, *args, **kwargs):  
    content = {}
    session_keys = request.session.keys()
    for key in session_keys:
        del request.session[key]
    content.update(csrf(request))
    return HttpResponseRedirect("/Staff/login")
    
class Login(TemplateView):
  def get(self, request, *args, **kwargs):      
    content = {} 
    content.update(csrf(request))
    if 'User' in request.session:
      return HttpResponseRedirect("/Staff/")
    return render_template(request, "Staff/Login.html", content)

  def post(self,request, *args, **kwargs):
    content = {}
    username = request.POST['username']
    password = request.POST['password']
    user_list = Employees.objects.filter(emailid=username,loginpwd=password)
    if(user_list):
        userobj= user_list[0]
        request.session['User'] = userobj
        content['User']=userobj
        return HttpResponse('Success')
    else:
      return HttpResponse('Login Failed')   
    return render_template(request, "Staff/Login.html", content)

class NewListings(TemplateView):
  def get(self, request, *args, **kwargs):  
    content = {}
    content.update(csrf(request))
    return render_template(request, "Staff/NewListings.html", content)

  def post(self, request, *args, **kwargs):
    content = {}
    return render_template(request, "Staff/NewListings.html", content)

class ChangePassword(LoginRequiredMixin,TemplateView):
  def get(self, request, *args, **kwargs):
    if 'User' in request.session:  
        content = {}
        content.update(csrf(request))
        return render_template(request, "Staff/ChangePassword.html", content)
    else:
        return HttpResponseRedirect("/Staff/login")

  def post(self, request, *args, **kwargs):
    content = {}
    cpwd = request.POST['currentpassword']
    npwd = request.POST['newpassword']
    cnfpwd = request.POST['confirmpassword']
    user=request.session['User']
    lst = Employees.objects.get(employeeid=user.employeeid)
    if(lst.loginpwd == cpwd):
        if(npwd == cnfpwd):
            lst.loginpwd = cnfpwd
            lst.save()
            msg = "Password has been changed successfully"
            content['msg'] = msg
            return HttpResponseRedirect("/Staff/")
        else:
            err = "password didn't match....try again"
            content['errmsg'] = err
            return render_template(request, "Staff/ChangePassword.html", content)
            
    else:
        err = "password didn't match....try again"
        content['errmsg'] = err
    return render_template(request, "Staff/ChangePassword.html", content) 


    
class ExecutiveRegistration(LoginRequiredMixin,TemplateView):

  def get(self, request, *args, **kwargs):  
      content = {}
      data = {}
      content.update(csrf(request))
      STATES = []
      state_list = States.objects.all()
      for state in state_list:
        STATES.append((state.stateid, state.name))
      ExecutiveRegFormObj = ExecutiveRegForm(states = STATES)
      if 'eid' in request.GET:
        eid = request.GET['eid']
        executiveobj=Employees.objects.get(employeeid = eid)
        data['firstname'] = executiveobj.firstname
        data['lastname'] = executiveobj.lastname
        data['emailid'] = executiveobj.emailid
        data['loginpwd'] = executiveobj.loginpwd
        data['contactno'] = executiveobj.contactno
        data['address'] = executiveobj.address
        data['City'] = executiveobj.city
        data['state'] = executiveobj.stateid
        rform = ExecutiveRegForm(initial=data, states = STATES)
        content['employeeid'] = eid
        content['form'] = rform
        return render_template(request, "Staff/ExecutiveRegistration.html", content)
        
      content['form'] = ExecutiveRegFormObj
      return render_template(request, "Staff/ExecutiveRegistration.html", content)
    
  def post(self, request, *args, **kwargs):
    content = {}
    data={}
    STATES = []
    state_list = States.objects.all()
    for state in state_list:
      STATES.append((state.stateid, state.name)) 
    if 'Imagedata' in request.FILES:
        f = request.FILES['Imagedata']
        file_name = f.name
        flist = file_name.split(".")
        data = f.read()
        f.close()
        f = open(os.path.join(settings.IMAGE_ROOT, "ListingImages\\%s" %file_name), "wb")
        f.write(data)
        f.close()
    ExecutiveRegFormObj = ExecutiveRegForm(request.POST,states=STATES)
    submit = request.POST['Submit']
    if 'eid' in request.POST:
      eid = request.POST['eid']
    if submit == 'Cancel':
        return HttpResponseRedirect('/')
    if ExecutiveRegFormObj.is_valid():
      if eid:
        ExecutiveObj = Employees.objects.get(employeeid = eid)
        ExecutiveObj.employeeid = int(eid)
      else:
        ExecutiveObj = Employees()
      firstname = ExecutiveRegFormObj.cleaned_data['firstname']
      lastname  = ExecutiveRegFormObj.cleaned_data['lastname']
      title = ExecutiveRegFormObj.cleaned_data['title']
      emailid = ExecutiveRegFormObj.cleaned_data['emailid']
      loginpwd = ExecutiveRegFormObj.cleaned_data['loginpwd']
      contactno = ExecutiveRegFormObj.cleaned_data['contactno']
      businesscategory = ExecutiveRegFormObj.cleaned_data['business_category']
      business_info = ExecutiveRegFormObj.cleaned_data['business_info']
      address = ExecutiveRegFormObj.cleaned_data['address']
      city = ExecutiveRegFormObj.cleaned_data['City']
      cityid = ExecutiveRegFormObj.cleaned_data['CityID']
      state = ExecutiveRegFormObj.cleaned_data['state']
      ExecutiveObj.firstname = firstname
      ExecutiveObj.lastname = lastname
      ExecutiveObj.title = title
      ExecutiveObj.emailid = emailid
      ExecutiveObj.loginpwd = loginpwd
      ExecutiveObj.contactno = contactno
      ExecutiveObj.role = 'E'
      ExecutiveObj.businesscategory = int(businesscategory)
      ExecutiveObj.businessinfo = business_info
      ExecutiveObj.address = address
      if not cityid:
        if(Cities.objects.filter(name = city)):
          cityobj = Cities.objects.get(name = city)
          ExecutiveObj.city = cityobj.name
        else:
          cityobj = Cities()
          cityobj.name = city
          cityobj.stateid = int(state)
          cityobj.isnew = True
          cityobj.save()
          city = Cities.objects.latest('cityid')
          ExecutiveObj.city =city.name
      else:
        ExecutiveObj.city = city
      ExecutiveObj.stateid = int(state)
      ExecutiveObj.save()
      if 'Imagedata' in request.FILES:
          listIdObj = Employees.objects.latest('employeeid')
          file_name = listIdObj.employeeid
          imageUrl  = "static/ListingImages/Executive-%s.%s" %(file_name,flist[1])
          listIdObj.photo =  imageUrl
          listIdObj.save()
      if eid:
        return HttpResponseRedirect("employee-list")
      else:
        return render_template(request,"Staff/ExecutiveMessage.html",content)
    else:
        ExecutiveRegFormObj = ExecutiveRegForm(initial = data)
        content['form'] = ExecutiveRegFormObj
        return render_template(request, "Staff/ExecutiveRegistration.html", content)
    
class ListingImages(LoginRequiredMixin,TemplateView):
    def get(self, request, *args, **kwargs):  
        content = {}
        lid=request.GET['lid']
        limit=int(request.GET['maxlimit'])
        type=int(request.GET['type'])
        request.session['type']=type
        image_list = []
        if type==1:
            imageobj_list = Salelistingimages.objects.filter(listingid=lid)
        elif type==2:
            imageobj_list = Rentallistingimages.objects.filter(listingid=lid)
        i = 0
        for obj in imageobj_list:
            i += 1
            if i <= limit:
               image_list.append(obj)
            else:
              break
            
        num_images = len(image_list)
        for i in range(0, limit - num_images):
          if type==1:
              imgObj = Salelistingimages()
          elif type==2:
              imgObj = Rentallistingimages()
          imgObj.description = ""
          imgObj.listingimageid = 0
          imgObj.largeimage = 'http://webmaster.ypsa.org/wp-content/uploads/2012/08/no_thumb.jpg'
          image_list.append(imgObj)
        
        content['lid'] = lid
        content['maxlimit']=limit
        content['image_list'] = image_list
        return render_template(request, "Staff/ListingImages.html", content)
    
    def post(selfself,request,*args,**kwargs):
        content = {}
        lid=request.POST['lid']
        maxlimit=request.POST['maxlimit']
        html = ''
        lid = int(lid)
        type=request.session['type']
        for key in request.FILES:
          index = key.split('-')[1]
          f = request.FILES[key]
          ext_name = f.name.split(".")[1]
          image_data = f.read()
          f.close()
          description = request.POST['Description-%s' %index]
          html+="%s"%(description)
          listing_image_id = int(request.POST['ListingImageID-%s' %index])
          if type==1:
              file_name = "SaleListing-%s-%s.%s" %(lid, index, ext_name)
          elif type==2:
              file_name = "RentalListing-%s-%s.%s" %(lid, index, ext_name)
          f = open("Z:\\IndiaDens\\static\\ListingImages\\%s" %file_name,"wb")
          f.write(image_data)
          f.close()        
          if listing_image_id > 0:
              if type==1:
                  obj = Salelistingimages.objects.get(listingimageid=listing_image_id)
              elif type==2:
                  obj = Rentallistingimages.objects.get(listingimageid=listing_image_id)
              if len(description.strip()) > 0:
                 obj.description = description
              obj.largeimage = "/static/ListingImages/%s" %file_name
              obj.save()
          else:
              if type==1:
                  obj = Salelistingimages()
              elif type==2:
                  obj = Rentallistingimages()
              obj.listingid = lid
              obj.description = description
              obj.largeimage = "/static/ListingImages/%s" %file_name
              obj.save()
          
          html += "%s - %s - %s - Saved.<br>" %(key, file_name, listing_image_id)
          #html += "%s\n" %key   
        return HttpResponse(html)
    
class ListingAttributes(LoginRequiredMixin,TemplateView):
    def get(self,request,*args,**kwargs):
        content={}
        type=int(request.GET['type'])
        request.session['type']=type
        lid=request.GET['lid']
        request.session['lid']=lid
        limit=int(request.GET['maxlimit'])
        request.session['limit']=limit
        attr_list = []
        if type==1:
            attrobj_list = Saleattributes.objects.filter(listingid=lid)
        elif type==2:
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
            if type==1:
                attrObj = Saleattributes()
            elif type==2:
                attrObj = Rentalattributes()
            attrObj.value = ""
            attrObj.attributeid = 0
            attr_list.append(attrObj)
          
        #content['lid'] = lid
        #content['maxlimit']=limit
        content['attr_list'] = attr_list
        return render_template(request, "Staff/ListingAttributes.html", content)
    
    def post(selfself,request,*args,**kwargs):
        content = {}
        lid=request.session['lid']
        limit=request.session['limit']
        type=request.session['type']
        lid = int(lid)
        type=int(type)
        html = ''
        for key in request.POST:
          if not key.__contains__('-'): continue
          if not key.__contains__('AttributeID'): continue
          rowno = key.split("-")[1]
          name = request.POST['Name-%s' %rowno]
          value = request.POST['Value-%s' %rowno]
          attribute_id = int(request.POST['AttributeID-%s' %rowno])        
          if attribute_id > 0:
              if type==1:
                  obj = Saleattributes.objects.get(attributeid=attribute_id) 
                  if (len(name.strip())>0 or len(value.strip())>0):
                      obj.name = name
                      obj.value = value
                      obj.save() 
              elif type==2:
                  obj = Rentalattributes.objects.get(attributeid=attribute_id)
                  if (len(name.strip())>0 or len(value.strip())>0):
                      obj.name = name
                      obj.value = value
                      obj.save()   
          else:
              if type==1:
                obj = Saleattributes()
              elif type==2:
                obj = Rentalattributes()
              obj.listingid = lid
              obj.name = name
              obj.value = value
              obj.save()
          html += "%d-%s- %s - %s<br>" %(lid,attribute_id,name,value)          
        
        return HttpResponse(html)
 
class Listings(LoginRequiredMixin, TemplateView):
    def get(self,request,*args,**kwargs):
      content={}
      clist = Customers.objects.all()
      type = int(request.GET['type'])
      rentals = Rentals.objects.all()
      sales = Sales.objects.all()
     # Show 5 customers per page
      page = request.GET.get('page')
      customer_list = []
      result = []
      try:
        for customerobj in clist:
          if(type==2):
            for obj in rentals:
              if customerobj.customerid == obj.customerid:
                customer_list.append(customerobj)
                for i in customer_list: 
                  if i not in result:
                    result.append(i)                  
          if(type==1):
            for obj in sales:
              if customerobj.customerid == obj.customerid:
                customer_list.append(customerobj)
                for i in customer_list:
                  if i not in result:
                    result.append(i)
        paginator = Paginator(result, 5)
        result = paginator.page(page)
      except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        result = paginator.page(1)
      except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        result = paginator.page(paginator.num_pages)
      content['type'] = type
      content['cust_list'] = result
      content.update(csrf(request))
      return render_template(request, 'Staff/Listings.html', content)
    
    def post(self,request, *args, **kwargs):
      content = {}
      scustomer = request.POST['SearchCustomer']
      type = int(request.POST['type'])
      customer_list = []
      rentals = Rentals.objects.all()
      sales = Sales.objects.all()
      clist = Customers.objects.all()
      result = []
      if len(scustomer.strip())!=0:
        for customerobj in clist:
          if(type==1):
            for obj in sales:
              if customerobj.customerid == obj.customerid:
                 if scustomer.lower() in [customerobj.firstname.lower(), customerobj.lastname.lower(), customerobj.phone.lower(), customerobj.email.lower(), customerobj.City.name.lower()]:
                    customer_list.append(customerobj)
                    for i in customer_list:
                      if i not in result:
                        result.append(i)
          elif(type==2):
            for obj in rentals:
              if customerobj.customerid == customerobj.customerid:
                 if scustomer.lower() in [customerobj.firstname.lower(), customerobj.lastname.lower(), customerobj.phone.lower(), customerobj.email.lower(), customerobj.City.name.lower()]:
                    customer_list.append(customerobj)
                    for i in customer_list:
                      if i not in result:
                        result.append(i)
           
                    
      else:
        for customerobj in clist:
          if(type==1):
            for obj in sales:
              if customerobj.customerid == obj.customerid:
                customer_list.append(customerobj)
                for i in customer_list:
                  if i not in result:
                    result.append(i)
          elif(type==2):
            for obj in rentals:
              if customerobj.customerid == obj.customerid:
                customer_list.append(customerobj)
                for i in customer_list:
                  if i not in result:
                    result.append(i)
      paginator = Paginator(result, 5) # Show 5 customers per page

      page = request.GET.get('page')
      try:
        result = paginator.page(page)
      except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        result = paginator.page(1)
      except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        result = paginator.page(paginator.num_pages)

      content['type'] = type
      content['cust_list'] = result
      return render_template(request, 'Staff/Listings.html', content)

      
class CustomerList(LoginRequiredMixin,TemplateView):
    def get(self,request,*args,**kwargs):
      content={}
      clist = Customers.objects.all()
      paginator = Paginator(clist, 5) # Show 5 customers per page

      page = request.GET.get('page')
      try:
        customer_list = paginator.page(page)
      except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        customer_list = paginator.page(1)
      except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        customer_list = paginator.page(paginator.num_pages)
      content['cust_list'] = customer_list
      content.update(csrf(request))
      return render_template(request, 'Staff/CustomersList.html', content)
    def post(self, request, *args, **kwargs):
      content = {}
      customer_list = []
      scustomer = request.POST['SearchCustomer']
      clist = Customers.objects.all()
      if len(scustomer.strip())!=0:
        for customerobj in clist:
          if scustomer.lower() in [customerobj.firstname.lower(), customerobj.lastname.lower(), customerobj.phone.lower(), customerobj.email.lower(), customerobj.City.name.lower()]:
            customer_list.append(customerobj)
      else:
        customer_list = Customers.objects.all()
      paginator = Paginator(customer_list, 5) # Show 5 customers per page

      page = request.GET.get('page')
      try:
        cust_list = paginator.page(page)
      except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        cust_list = paginator.page(1)
      except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        cust_list = paginator.page(paginator.num_pages)


      content['cust_list'] = cust_list
      return render_template(request, 'Staff/CustomersList.html', content)
       
        
class CustomerDelete(LoginRequiredMixin,TemplateView):
  def get(self, request, *args, **kwargs):
    content = {} 
    cid = request.GET['customerid']
    CustObj = Customers.objects.get(customerid = cid)
    CustObj.delete()
    url = "/Staff/customer-list"
    return HttpResponseRedirect(url)

class CustomerRentalListings(LoginRequiredMixin,TemplateView):
    def get(self, request, *args, **kwargs):
        content = {} 
        approved_customer_list = Customers.objects.filter(isconfirmed=1)
        listings = Rentals.objects.filter(approvalstatus=0)
        rental_listings = []
        for obj in listings:
            for obj1 in approved_customer_list:
                if obj.customerid==obj1.customerid:
                    rental_listings.append(obj)
        paginator = Paginator(rental_listings, 5)

        page = request.GET.get('page')
        try:
          rent_list = paginator.page(page)
        except PageNotAnInteger:
      # If page is not an integer, deliver first page.
          rent_list = paginator.page(1)
        except EmptyPage:
      # If page is out of range (e.g. 9999), deliver last page of results.
          rent_list = paginator.page(paginator.num_pages)

        if not rental_listings:
          msg = "There are no Rental Listings"
          content['msg'] = msg
        content['CustomersListings']=rent_list
        content['type']=2
        return render_template(request,"Staff/CustomerListings.html",content)

class CustomerSaleListings(LoginRequiredMixin,TemplateView):
    def get(self, request, *args, **kwargs):
        content = {} 
        approved_customer_list = Customers.objects.filter(isconfirmed=1)
        listings = Sales.objects.filter(approvalstatus=0)
        sale_listings = []
        for obj in listings:
            for obj1 in approved_customer_list:
                if obj.customerid==obj1.customerid:
                    sale_listings.append(obj)
        paginator = Paginator(sale_listings, 5)

        page = request.GET.get('page')
        try:
          sale_list = paginator.page(page)
        except PageNotAnInteger:
      # If page is not an integer, deliver first page.
          sale_list = paginator.page(1)
        except EmptyPage:
      # If page is out of range (e.g. 9999), deliver last page of results.
          sale_list = paginator.page(paginator.num_pages)

        if not sale_listings:
          msg = "There are no Sale Listings"
          content['msg'] = msg
        content['CustomersListings']=sale_list
        content['type']=1
        return render_template(request,"Staff/CustomerListings.html",content)

        
class Location(TemplateView):
    def get(self,request,*args,**kwargs):
        content = {}
        city_list = Cities.objects.filter(isnew=1)
        req_list=[]             
        content['cities'] = city_list
        return render_template(request,"Staff/Cities.html",content)
             
class ListMessages(LoginRequiredMixin,TemplateView):
  def get(self, request, *args, **kwargs):
    content = {}
    messageobj = Mobilemessages.objects.all()
    content['Messagelist'] = messageobj
    return render_template(request, "Staff/ShowMessages.html", content)

class DeleteMessages(LoginRequiredMixin,TemplateView):
  def get(self, request, *args, **kwargs):
    content = {}
    msgid = request.GET['msgid']
    if(Mobilemessages.objects.filter(messageid = msgid)):
       mobj = Mobilemessages.objects.get(messageid = msgid)
       mobj.delete();
       msgobj = Mobilemessages.objects.all()
       content['Messagelist'] = msgobj
       return render_template(request, "Staff/ShowMessages.html", content)

class ExecutivesList(LoginRequiredMixin,TemplateView):
  def get(self, request, *args, **kwargs):
    content = {}
    content.update(csrf(request))
    if 'role' in request.GET:
      role1 = request.GET['role']
      content['role1'] = role1
    user = request.session['User']
    role = user.role
    if (role=='E' or role=='S'):
      employee_list = Employees.objects.filter(role='E')
      length = len(employee_list)
    elif (role=='S' or role=="A"):
      employee_list = Employees.objects.filter(role='S')
      length = len(employee_list)
    if not employee_list:
      msg = "There are No Empoyees"
      content['msg'] = msg 
      return render_template(request, "Staff/Executives.html",content)
    paginator = Paginator(employee_list, 5)
    page = request.GET.get('page')
    try:
      emp_list = paginator.page(page)
    except PageNotAnInteger:
      # If page is not an integer, deliver first page.
      emp_list = paginator.page(1)
    except EmptyPage:
      # If page is out of range (e.g. 9999), deliver last page of results.
      emp_list = paginator.page(paginator.num_pages)
    content['role'] = role
    content['emp_list']=emp_list
    return render_template(request, "Staff/Executives.html", content)
  
  def post(self, request, *args, **kwargs):
    content = {}
    name=request.POST['keywords']
    role = request.POST['role']
    if 'role1' in request.POST:
      role1 = request.POST['role1']
    req_list = []
    if len(name.strip()) != 0:
      if (role=='E' or role=='S'):
        employee_list = Employees.objects.filter(role='E')
      elif (role=='S'):
        employee_list = Employees.objects.filter(role='S')
      for obj in employee_list:
        if name.lower() in [obj.firstname.lower(), obj.lastname.lower(), obj.contactno, obj.city.lower()]:
          req_list.append(obj)
      paginator = Paginator(req_list, 5)

      page = request.GET.get('page')
      try:
        emp_list = paginator.page(page)
      except PageNotAnInteger:
      # If page is not an integer, deliver first page.
        emp_list = paginator.page(1)
      except EmptyPage:
      # If page is out of range (e.g. 9999), deliver last page of results.
        emp_list = paginator.page(paginator.num_pages)
    else:
      if (role=='E' or role=='S'):
        employee_list = Employees.objects.filter(role='E')
      elif (role=='S'):
        employee_list = Employees.objects.filter(role='S')
      paginator = Paginator(employee_list, 5)
      page = request.GET.get('page')
      try:
        emp_list = paginator.page(page)
      except PageNotAnInteger:
      # If page is not an integer, deliver first page.
        emp_list = paginator.page(1)
      except EmptyPage:
      # If page is out of range (e.g. 9999), deliver last page of results.
        emp_list = paginator.page(paginator.num_pages)
    content['emp_list']=emp_list
    content['role'] = role
    return render_template(request,"Staff/Executives.html",content)
    
  
class Employee(LoginRequiredMixin,TemplateView):
  def get(self, request, *args, **kwargs):
      content = {}
      data = {}
      if 'role1' in request.GET:
        role1 = request.GET['role1']
        content['role1'] = role1
      content.update(csrf(request))
      STATES = []
      state_list = States.objects.all()
      for state in state_list:
        STATES.append((state.stateid, state.name))
      EmployeeRegFormObj = EmployeeRegForm(states=STATES)
      if 'eid' in request.GET:
        eid = request.GET['eid']
        executiveobj=Employees.objects.get(employeeid = eid)
        data['firstname'] = executiveobj.firstname
        data['lastname'] = executiveobj.lastname
        data['emailid'] = executiveobj.emailid
        data['loginpwd'] = executiveobj.loginpwd
        data['contactno'] = executiveobj.contactno
        data['address'] = executiveobj.address
        data['City'] = executiveobj.city
        data['state'] = executiveobj.stateid
        rform = EmployeeRegForm(initial=data,states=STATES)
        content['form'] = rform
        content['eid'] = eid
        return render_template(request, "Staff/EmployeeForm.html", content)
        
      
      content['form'] = EmployeeRegFormObj
      return render_template(request, "Staff/EmployeeForm.html", content)
    
  def post(self, request, *args, **kwargs):
    content = {}
    data={}
    STATES = []
    state_list = States.objects.all()
    for state in state_list:
      STATES.append((state.stateid, state.name)) 
    if 'Imagefile' in request.FILES:
        f = request.FILES['Imagefile']
        file_name = f.name
        flist = file_name.split(".")
        data = f.read()
        f.close()
        f = open(os.path.join(settings.IMAGE_ROOT, "ListingImages\\%s" %file_name), "wb")
        f.write(data)
        f.close()
    EmployeeRegFormObj = EmployeeRegForm(request.POST,states=STATES)
    if 'eid' in request.POST:
      eid = request.POST['eid']
    submit = request.POST['Submit']
    if submit == 'Cancel':
        return HttpResponseRedirect('/')
    if EmployeeRegFormObj.is_valid():
      if eid:
        EmployeeObj = Employees.objects.get(employeeid = eid)
        EmployeeObj.employeeid = int(eid)
      else:
        EmployeeObj = Employees()
      firstname = EmployeeRegFormObj.cleaned_data['firstname']
      lastname  = EmployeeRegFormObj.cleaned_data['lastname']
      emailid = EmployeeRegFormObj.cleaned_data['emailid']
      loginpwd = EmployeeRegFormObj.cleaned_data['loginpwd']
      contactno = EmployeeRegFormObj.cleaned_data['contactno']
      address = EmployeeRegFormObj.cleaned_data['address']
      city = EmployeeRegFormObj.cleaned_data['City']
      cityid = EmployeeRegFormObj.cleaned_data['CityID']
      state = EmployeeRegFormObj.cleaned_data['state']
      EmployeeObj.firstname = firstname
      EmployeeObj.lastname = lastname
      EmployeeObj.emailid = emailid
      EmployeeObj.loginpwd = loginpwd
      EmployeeObj.contactno = contactno
      EmployeeObj.role = 'S'
      EmployeeObj.address = address
      if not cityid:
        if(Cities.objects.filter(name = city)):
          cityobj = Cities.objects.get(name = city)
          EmployeeObj.cityid = cityobj.cityid
        else:
          cityobj = Cities()
          cityobj.name = city
          cityobj.stateid = int(state)
          cityobj.isnew = True
          cityobj.save()
          city = Cities.objects.latest('cityid')
          EmployeeObj.city =city.name
      else:
        EmployeeObj.city = city
      EmployeeObj.stateid = int(state)
      EmployeeObj.save()
      if eid:
        return HttpResponseRedirect("employee-list")
      if 'Imagefile' in request.FILES:
          listIdObj = Employees.objects.latest('employeeid')
          file_name = listIdObj.employeeid
          imageUrl  = "static/ListingImages/Employee-%s.%s" %(file_name,flist[1])
          listIdObj.photo =  imageUrl
          listIdObj.save()
      return HttpResponseRedirect("/Staff/")
    else:
        EmployeeRegFormObj = EmployeeRegForm(initial = data)
        content['form'] = EmployeeRegFormObj
        return render_template(request, "Staff/EmployeeForm.html", content)

class ZapDb(TemplateView):
  def get(self, request, *args, **kwargs):
    content = {}
    cursor = connection.cursor()
    cursor.execute("TRUNCATE TABLE `employees`")
    cursor.execute("TRUNCATE TABLE `newlistings`")
    cursor.execute("TRUNCATE TABLE `customers`")
    cursor.execute("TRUNCATE TABLE `django_session`")
    cursor.execute("TRUNCATE TABLE `mobilemessages`")
    cursor.execute("TRUNCATE TABLE `rentalattributes`")
    cursor.execute("TRUNCATE TABLE `rentallistingimages`")
    cursor.execute("TRUNCATE TABLE `rentals`")
    cursor.execute("TRUNCATE TABLE `saleattributes`")
    cursor.execute("TRUNCATE TABLE `salelistingimages`")
    cursor.execute("TRUNCATE TABLE `sales`")
    cursor.execute("TRUNCATE TABLE `callbackrequests`")
    cursor.execute("TRUNCATE TABLE `visitorreviews`")
    cursor.execute("TRUNCATE TABLE `visitors`")

    admin = Employees()
    admin.firstname = 'Admin'
    admin.lastname = 'Indiadens'
    admin.role = 'A'
    admin.emailid = 'admin@indiadens.com'
    admin.loginpwd = 'welcome'
    admin.contactname = '919440111843'
    admin.address = 'Madinaguda'
    admin.city = 'Hyderabad'
    admin.save()
    for key in request.session.keys():
      del request.session[key]
      
    return render_template(request, "Staff/ZapDb.html", content) 
    


     
 
