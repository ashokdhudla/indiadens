# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

PROPERTY_TYPES = {10:'Apartments', 20:'Independent House', 25:' Villas', 30:'Pent House', 40: 'Farm House', 50:'Office Space', 100:'Residential Lands', 110:'Commercial Lands'}
PLANS = {0: 'Free', 1:'Silver', 2:'Gold', 3:'Platinum'}

class AuthGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=80L, unique=True)
    class Meta:
        db_table = 'auth_group'

class AuthGroupPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    group = models.ForeignKey(AuthGroup)
    permission = models.ForeignKey('AuthPermission')
    class Meta:
        db_table = 'auth_group_permissions'

class AuthPermission(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50L)
    content_type = models.ForeignKey('DjangoContentType')
    codename = models.CharField(max_length=100L)
    class Meta:
        db_table = 'auth_permission'

class AuthUser(models.Model):
    id = models.IntegerField(primary_key=True)
    password = models.CharField(max_length=128L)
    last_login = models.DateTimeField()
    is_superuser = models.IntegerField()
    username = models.CharField(max_length=30L, unique=True)
    first_name = models.CharField(max_length=30L)
    last_name = models.CharField(max_length=30L)
    email = models.CharField(max_length=75L)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()
    class Meta:
        db_table = 'auth_user'

class AuthUserGroups(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(AuthUser)
    group = models.ForeignKey(AuthGroup)
    class Meta:
        db_table = 'auth_user_groups'

class AuthUserUserPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(AuthUser)
    permission = models.ForeignKey(AuthPermission)
    class Meta:
        db_table = 'auth_user_user_permissions'

class Cities(models.Model):
    cityid = models.IntegerField(primary_key=True, db_column='CityID') # Field name made lowercase.
    name = models.CharField(max_length=50L, db_column='Name', blank=True) # Field name made lowercase.
    stateid = models.IntegerField(null=True, db_column='StateID', blank=True) # Field name made lowercase.
    isnew = models.IntegerField(null=True, db_column='IsNew', blank=True) # Field name made lowercase.

    @property
    def State(self):
      state = None
      states = States.objects.filter(stateid = self.stateid)
      if states:
         state = states[0]
      
      return state
      
    class Meta:
        db_table = 'cities'

class Customers(models.Model):
    customerid = models.IntegerField(primary_key=True, db_column='CustomerID') # Field name made lowercase.
    customertype = models.IntegerField(null=True, db_column='CustomerType', blank=True) # Field name made lowercase.
    parentid = models.IntegerField(null=True, db_column='ParentID', blank=True) # Field name made lowercase.
    title = models.CharField(max_length=255L, db_column='Title', blank=True) # Field name made lowercase.
    subtitle = models.CharField(max_length=100L, db_column='SubTitle', blank=True) # Field name made lowercase.
    firstname = models.CharField(max_length=100L, db_column='FirstName', blank=True) # Field name made lowercase.
    lastname = models.CharField(max_length=100L, db_column='LastName', blank=True) # Field name made lowercase.
    address = models.CharField(max_length=255L, db_column='Address', blank=True) # Field name made lowercase.
    cityid = models.IntegerField(null=True, db_column='CityID', blank=True) # Field name made lowercase.
    stateid = models.IntegerField(null=True, db_column='StateID', blank=True) # Field name made lowercase.
    countryid = models.IntegerField(null=True, db_column='CountryID', blank=True) # Field name made lowercase.
    phone = models.CharField(max_length=100L, db_column='Phone', blank=True) # Field name made lowercase.
    fax = models.CharField(max_length=100L, db_column='Fax', blank=True) # Field name made lowercase.
    email = models.CharField(max_length=100L, db_column='EMail', blank=True) # Field name made lowercase.
    loginpwd = models.CharField(max_length=25L, db_column='LoginPwd', blank=True) # Field name made lowercase.
    locationmap = models.CharField(max_length=255L, db_column='LocationMap', blank=True) # Field name made lowercase.
    website = models.CharField(max_length=255L, db_column='WebSite', blank=True) # Field name made lowercase.
    logo = models.CharField(max_length=255L, db_column='Logo', blank=True) # Field name made lowercase.
    profile = models.CharField(max_length=255L, db_column='Profile', blank=True) # Field name made lowercase.
    deals = models.CharField(max_length=255L, db_column='Deals', blank=True) # Field name made lowercase.
    dealinglocations = models.CharField(max_length=255L, db_column='DealingLocations', blank=True) # Field name made lowercase.
    description = models.CharField(max_length=255L, db_column='Description', blank=True) # Field name made lowercase.
    keywords = models.CharField(max_length=255L, db_column='KeyWords', blank=True) # Field name made lowercase.
    confirmcode = models.CharField(max_length=25L, db_column='ConfirmCode', blank=True) # Field name made lowercase.
    updatedby = models.IntegerField(null=True, db_column='UpdatedBy', blank=True) # Field name made lowercase.
    isconfirmed = models.IntegerField(null=True, db_column='IsConfirmed', blank=True) # Field name made lowercase.
    emailcode = models.CharField(max_length=50L, db_column='EMailCode', blank=True) # Field name made lowercase.
    isemailverified = models.IntegerField(null=True, db_column='IsEMailVerified', blank=True) # Field name made lowercase.
    ismobileverified = models.IntegerField(null=True, db_column='IsMobileVerified', blank=True) # Field name made lowercase.
    mobilecode = models.CharField(max_length=50L, db_column='MobileCode', blank=True) # Field name made lowercase.
    isdeleted = models.IntegerField(null=True, db_column='IsDeleted', blank=True) # Field name made lowercase.
    class Meta:
        db_table = 'customers'

    @property
    def State(self):
      state = States.objects.get(stateid = self.stateid)
      return state

    @property
    def City(self):
      city = Cities.objects.get(cityid = self.cityid)
      return city
    
    @property
    def Rentalcounter(self):
      counter = 0
      listing_count = Rentals.objects.filter(customerid = self.customerid)
      for i in listing_count:
        counter = counter+1
      return counter
    @property
    def Salecounter(self):
      counter = 0
      listing_count = Sales.objects.filter(customerid = self.customerid)
      for i in listing_count:
        counter = counter+1
      return counter


class DjangoContentType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100L)
    app_label = models.CharField(max_length=100L)
    model = models.CharField(max_length=100L)
    class Meta:
        db_table = 'django_content_type'

class DjangoSession(models.Model):
    session_key = models.CharField(max_length=40L, primary_key=True)
    session_data = models.TextField()
    expire_date = models.DateTimeField()
    class Meta:
        db_table = 'django_session'

class DjangoSite(models.Model):
    id = models.IntegerField(primary_key=True)
    domain = models.CharField(max_length=100L)
    name = models.CharField(max_length=50L)
    class Meta:
        db_table = 'django_site'

class Employees(models.Model):
    employeeid = models.IntegerField(primary_key=True, db_column='EmployeeID') # Field name made lowercase.
    firstname = models.CharField(max_length=50L, db_column='FirstName', blank=True) # Field name made lowercase.
    lastname = models.CharField(max_length=50L, db_column='LastName', blank=True) # Field name made lowercase.
    title = models.CharField(max_length=100L, db_column='Title', blank=True) # Field name made lowercase.
    branchid = models.IntegerField(null=True, db_column='BranchID', blank=True) # Field name made lowercase.
    designation = models.CharField(max_length=100L, db_column='Designation', blank=True) # Field name made lowercase.
    emailid = models.CharField(max_length=100L, db_column='EMailID', blank=True) # Field name made lowercase.
    loginpwd = models.CharField(max_length=25L, db_column='LoginPwd', blank=True) # Field name made lowercase.
    contactno = models.CharField(max_length=25L, db_column='ContactNo', blank=True) # Field name made lowercase.
    role = models.CharField(max_length=1L, db_column='Role', blank=True) # Field name made lowercase.
    businesscategory = models.IntegerField(null=True, db_column='BusinessCategory', blank=True) # Field name made lowercase.
    businessinfo = models.CharField(max_length=255L, db_column='BusinessInfo', blank=True) # Field name made lowercase.
    address = models.CharField(max_length=255L, db_column='Address', blank=True) # Field name made lowercase.
    city = models.CharField(max_length=100L, db_column='City', blank=True) # Field name made lowercase.
    stateid = models.IntegerField(null=True, db_column='StateID', blank=True) # Field name made lowercase.
    country = models.IntegerField(null=True, db_column='Country', blank=True) # Field name made lowercase.
    photo = models.CharField(max_length=255L, blank=True)
    confirmcode = models.CharField(max_length=25L, db_column='ConfirmCode', blank=True) # Field name made lowercase.
    isactive = models.TextField(db_column='IsActive', blank=True) # Field name made lowercase. This field type is a guess.
    class Meta:
        db_table = 'employees'
        
    @property
    def State(self):
      state = States.objects.get(stateid = self.stateid)
      return state
    @property
    def City(self):
      city = Cities.objects.get(cityid = self.cityid)
      return city

    @property
    def BusinessCategoryName(self):
      if self.businesscategory == 1:
          return 'Individual'
      elif self.businesscategory == 2:
          return 'Net Cafe'
      elif self.businesscategory == 3:
          return 'E-Seva Center'


class Iptable(models.Model):
    iptableid = models.BigIntegerField(primary_key=True, db_column='IPTableID') # Field name made lowercase.
    ip = models.CharField(max_length=50L, db_column='IP', blank=True) # Field name made lowercase.
    city = models.CharField(max_length=100L, db_column='City', blank=True) # Field name made lowercase.
    state = models.CharField(max_length=100L, db_column='State', blank=True) # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate') # Field name made lowercase.
    class Meta:
        db_table = 'iptable'

class Mobilemessages(models.Model):
    messageid = models.BigIntegerField(primary_key=True, db_column='MessageID') # Field name made lowercase.
    messagefrom = models.CharField(max_length=12L, db_column='MessageFrom', blank=True) # Field name made lowercase.
    messageto = models.CharField(max_length=12L, db_column='MessageTo', blank=True) # Field name made lowercase.
    sentdate = models.DateTimeField(null=True, db_column='SentDate', blank=True) # Field name made lowercase.
    message = models.CharField(max_length=512L, db_column='Message', blank=True) # Field name made lowercase.
    class Meta:
        db_table = 'mobilemessages'

class Newlistings(models.Model):
    newlistingid = models.BigIntegerField(primary_key=True, db_column='NewListingID') # Field name made lowercase.
    propertytype = models.IntegerField(null=True, db_column='PropertyType', blank=True) # Field name made lowercase.
    price = models.FloatField(null=True, db_column='Price', blank=True) # Field name made lowercase.
    priceinwords = models.IntegerField(null=True, db_column='PriceInWords', blank=True) # Field name made lowercase.
    area = models.IntegerField(null=True, db_column='Area', blank=True) # Field name made lowercase.
    areaunit = models.IntegerField(null=True, db_column='AreaUnit', blank=True) # Field name made lowercase.
    bedrooms = models.IntegerField(null=True, db_column='Bedrooms', blank=True) # Field name made lowercase.
    bathrooms = models.IntegerField(null=True, db_column='Bathrooms', blank=True) # Field name made lowercase.
    address = models.CharField(max_length=255L, db_column='Address', blank=True) # Field name made lowercase.
    city = models.CharField(max_length=255L, db_column='City', blank=True) # Field name made lowercase.
    stateid = models.IntegerField(null=True, db_column='StateID', blank=True) # Field name made lowercase.
    description = models.CharField(max_length=512L, db_column='Description', blank=True) # Field name made lowercase.
    imageurl = models.CharField(max_length=255L, db_column='ImageURL', blank=True) # Field name made lowercase.
    latitude = models.FloatField(null=True, db_column='Latitude', blank=True) # Field name made lowercase.
    longitude = models.FloatField(null=True, db_column='Longitude', blank=True) # Field name made lowercase.
    name = models.CharField(max_length=255L, db_column='Name', blank=True) # Field name made lowercase.
    email = models.CharField(max_length=255L, db_column='EMail', blank=True) # Field name made lowercase.
    phone = models.CharField(max_length=255L, db_column='Phone', blank=True) # Field name made lowercase.
    ownership = models.IntegerField(null=True, db_column='Ownership', blank=True) # Field name made lowercase.
    ipaddress = models.CharField(max_length=20L, db_column='IPAddress', blank=True) # Field name made lowercase.
    assignedto = models.IntegerField(null=True, db_column='AssignedTo', blank=True) # Field name made lowercase.
    status = models.IntegerField(null=True, db_column='Status', blank=True) # Field name made lowercase.
    confirmationcode = models.CharField(max_length=25L, db_column='ConfirmationCode', blank=True) # Field name made lowercase.
    isconfirmed = models.IntegerField(null=True, db_column='IsConfirmed', blank=True) # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate') # Field name made lowercase.
    listingtype = models.IntegerField(null=True, db_column='ListingType', blank=True) # Field name made lowercase.
    class Meta:
        db_table = 'newlistings'

class Rentalattributes(models.Model):
    attributeid = models.BigIntegerField(primary_key=True, db_column='AttributeID') # Field name made lowercase.
    listingid = models.BigIntegerField(null=True, db_column='ListingID', blank=True) # Field name made lowercase.
    valuetypeid = models.IntegerField(null=True, db_column='ValueTypeID', blank=True) # Field name made lowercase.
    name = models.CharField(max_length=50L, db_column='Name', blank=True) # Field name made lowercase.
    value = models.CharField(max_length=255L, db_column='Value', blank=True) # Field name made lowercase.
    class Meta:
        db_table = 'rentalattributes'

class Rentallistingimages(models.Model):
    listingimageid = models.BigIntegerField(primary_key=True, db_column='ListingImageID') # Field name made lowercase.
    listingid = models.BigIntegerField(db_column='ListingID') # Field name made lowercase.
    imagethumb = models.CharField(max_length=255L, db_column='ImageThumb', blank=True) # Field name made lowercase.
    largeimage = models.CharField(max_length=255L, db_column='LargeImage') # Field name made lowercase.
    description = models.CharField(max_length=255L, db_column='Description', blank=True) # Field name made lowercase.
    class Meta:
        db_table = 'rentallistingimages'

class Rentals(models.Model):
    listingid = models.IntegerField(primary_key=True, db_column='ListingID') # Field name made lowercase.
    parentid = models.IntegerField(null=True, db_column='ParentID', blank=True) # Field name made lowercase.
    customerid = models.IntegerField(null=True, db_column='CustomerID', blank=True) # Field name made lowercase.
    propertytypeid = models.IntegerField(null=True, db_column='PropertyTypeID', blank=True) # Field name made lowercase.
    ownership = models.IntegerField(null=True, db_column='Ownership', blank=True) # Field name made lowercase.
    title = models.CharField(max_length=255L, db_column='Title', blank=True) # Field name made lowercase.
    rent = models.IntegerField(null=True, db_column='Rent', blank=True) # Field name made lowercase.
    rentfreequency = models.IntegerField(null=True, db_column='RentFreequency', blank=True) # Field name made lowercase.
    advanceamount = models.IntegerField(null=True, db_column='AdvanceAmount', blank=True) # Field name made lowercase.
    advancefreequency = models.IntegerField(null=True, db_column='AdvanceFreequency', blank=True) # Field name made lowercase.
    maintenance = models.IntegerField(null=True, db_column='Maintenance', blank=True) # Field name made lowercase.
    allowed_family = models.IntegerField(null=True, db_column='Allowed-Family', blank=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    allowed_bachelors = models.IntegerField(null=True, db_column='Allowed-Bachelors', blank=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    bedrooms = models.IntegerField(null=True, db_column='Bedrooms', blank=True) # Field name made lowercase.
    bathrooms = models.IntegerField(null=True, db_column='Bathrooms', blank=True) # Field name made lowercase.
    area = models.IntegerField(null=True, db_column='Area', blank=True) # Field name made lowercase.
    areaunit = models.IntegerField(null=True, db_column='AreaUnit', blank=True) # Field name made lowercase.
    address = models.CharField(max_length=255L, db_column='Address', blank=True) # Field name made lowercase.
    landmark1 = models.CharField(max_length=255L, db_column='LandMark1', blank=True) # Field name made lowercase.
    landmark2 = models.CharField(max_length=255L, db_column='LandMark2', blank=True) # Field name made lowercase.
    landmark3 = models.CharField(max_length=255L, db_column='LandMark3', blank=True) # Field name made lowercase.
    landmark4 = models.CharField(max_length=255L, db_column='LandMark4', blank=True) # Field name made lowercase.
    cityid = models.IntegerField(null=True, db_column='CityID', blank=True) # Field name made lowercase.
    stateid = models.IntegerField(null=True, db_column='StateID', blank=True) # Field name made lowercase.
    postalcode = models.CharField(max_length=20L, db_column='PostalCode', blank=True) # Field name made lowercase.
    latitude = models.FloatField(null=True, db_column='Latitude', blank=True) # Field name made lowercase.
    longitude = models.FloatField(null=True, db_column='Longitude', blank=True) # Field name made lowercase.
    contactname = models.CharField(max_length=100L, db_column='ContactName', blank=True) # Field name made lowercase.
    phone = models.CharField(max_length=100L, db_column='Phone', blank=True) # Field name made lowercase.
    email = models.CharField(max_length=255L, db_column='EMail', blank=True) # Field name made lowercase.
    website = models.CharField(max_length=255L, db_column='WebSite', blank=True) # Field name made lowercase.
    virtualtour = models.CharField(max_length=255L, db_column='VirtualTour', blank=True) # Field name made lowercase.
    description = models.CharField(max_length=512L, db_column='Description', blank=True) # Field name made lowercase.
    lift = models.IntegerField(null=True, blank=True)
    gym = models.IntegerField(null=True, blank=True)
    swimmingpool = models.IntegerField(null=True, blank=True)
    gatedcommunity = models.IntegerField(null=True, blank=True)
    powerbackup = models.IntegerField(null=True, db_column='PowerBackup', blank=True) # Field name made lowercase.
    furnished = models.IntegerField(null=True, db_column='Furnished', blank=True) # Field name made lowercase.
    cupboards = models.IntegerField(null=True, blank=True)
    facing = models.IntegerField(null=True, db_column='Facing', blank=True) # Field name made lowercase.
    possession = models.CharField(max_length=25L, db_column='Possession', blank=True) # Field name made lowercase.
    constructiondate = models.CharField(max_length=25L, db_column='ConstructionDate', blank=True) # Field name made lowercase.
    propertystatus = models.CharField(max_length=30L, db_column='PropertyStatus', blank=True) # Field name made lowercase.
    imagethumb = models.CharField(max_length=255L, db_column='ImageThumb', blank=True) # Field name made lowercase.
    posteddate = models.DateTimeField(null=True, db_column='PostedDate', blank=True) # Field name made lowercase.
    expirydate = models.DateTimeField(null=True, db_column='ExpiryDate', blank=True) # Field name made lowercase.
    impressions = models.IntegerField(null=True, db_column='Impressions', blank=True) # Field name made lowercase.
    planid = models.IntegerField(null=True, db_column='PlanID', blank=True) # Field name made lowercase.
    sortorder = models.IntegerField(null=True, db_column='SortOrder', blank=True) # Field name made lowercase.
    rank = models.IntegerField(null=True, db_column='Rank', blank=True) # Field name made lowercase.
    duplicateid = models.IntegerField(null=True, db_column='DuplicateID', blank=True) # Field name made lowercase.
    isactive = models.IntegerField(null=True, db_column='IsActive', blank=True) # Field name made lowercase. This field type is a guess.
    ipaddress = models.CharField(max_length=20L, db_column='IPAddress', blank=True) # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate') # Field name made lowercase.
    propertyid = models.CharField(max_length=10L, db_column='PropertyID', blank=True) # Field name made lowercase.
    confirmcode = models.CharField(max_length=25L, db_column='ConfirmCOde', blank=True) # Field name made lowercase.
    isconfirmed = models.IntegerField(null=True, db_column='IsConfirmed', blank=True) # Field name made lowercase.
    approvalstatus = models.IntegerField(null=True, db_column='ApprovalStatus', blank=True) # Field name made lowercase.
    ismobileverified = models.IntegerField(null=True, db_column='IsMobileVerified', blank=True) # Field name made lowercase.
    mobilecode = models.CharField(max_length=50L, db_column='MobileCode', blank=True) # Field name made lowercase.
    isemailverified = models.IntegerField(null=True, db_column='IsEMailVerified', blank=True) # Field name made lowercase.
    class Meta:
        db_table = 'rentals'

    @property
    def State(self):
      state = States.objects.get(stateid = self.stateid)
      return state

    @property
    def City(self):
      city = Cities.objects.get(cityid = self.cityid)
      return city

    @property
    def PropertyType(self):
      return PROPERTY_TYPES[self.propertytypeid]

    @property
    def Plan(self):
      return PLANS[self.planid]


class Saleattributes(models.Model):
    attributeid = models.BigIntegerField(primary_key=True, db_column='AttributeID') # Field name made lowercase.
    listingid = models.BigIntegerField(null=True, db_column='ListingID', blank=True) # Field name made lowercase.
    valuetypeid = models.IntegerField(null=True, db_column='ValueTypeID', blank=True) # Field name made lowercase.
    name = models.CharField(max_length=50L, db_column='Name', blank=True) # Field name made lowercase.
    value = models.CharField(max_length=255L, db_column='Value', blank=True) # Field name made lowercase.
    class Meta:
        db_table = 'saleattributes'

class Salelistingimages(models.Model):
    listingimageid = models.BigIntegerField(primary_key=True, db_column='ListingImageID') # Field name made lowercase.
    listingid = models.BigIntegerField(db_column='ListingID') # Field name made lowercase.
    imagethumb = models.CharField(max_length=255L, db_column='ImageThumb', blank=True) # Field name made lowercase.
    largeimage = models.CharField(max_length=255L, db_column='LargeImage') # Field name made lowercase.
    description = models.CharField(max_length=255L, db_column='Description', blank=True) # Field name made lowercase.
    class Meta:
        db_table = 'salelistingimages'

class Sales(models.Model):
    listingid = models.IntegerField(primary_key=True, db_column='ListingID') # Field name made lowercase.
    parentid = models.IntegerField(null=True, db_column='ParentID', blank=True) # Field name made lowercase.
    customerid = models.IntegerField(null=True, db_column='CustomerID', blank=True) # Field name made lowercase.
    propertytypeid = models.IntegerField(null=True, db_column='PropertyTypeID', blank=True) # Field name made lowercase.
    title = models.CharField(max_length=255L, db_column='Title', blank=True) # Field name made lowercase.
    price = models.BigIntegerField(null=True, blank=True)
    bedrooms = models.IntegerField(null=True, db_column='Bedrooms', blank=True) # Field name made lowercase.
    bathrooms = models.IntegerField(null=True, db_column='Bathrooms', blank=True) # Field name made lowercase.
    area = models.IntegerField(null=True, db_column='Area', blank=True) # Field name made lowercase.
    areaunit = models.IntegerField(null=True, db_column='AreaUnit', blank=True) # Field name made lowercase.
    address = models.CharField(max_length=255L, db_column='Address', blank=True) # Field name made lowercase.
    landmark1 = models.CharField(max_length=255L, db_column='LandMark1', blank=True) # Field name made lowercase.
    landmark2 = models.CharField(max_length=255L, db_column='LandMark2', blank=True) # Field name made lowercase.
    landmark3 = models.CharField(max_length=255L, db_column='LandMark3', blank=True) # Field name made lowercase.
    landmark4 = models.CharField(max_length=255L, db_column='LandMark4', blank=True) # Field name made lowercase.
    cityid = models.IntegerField(null=True, db_column='CityID', blank=True) # Field name made lowercase.
    stateid = models.IntegerField(null=True, db_column='StateID', blank=True) # Field name made lowercase.
    postalcode = models.CharField(max_length=20L, db_column='PostalCode', blank=True) # Field name made lowercase.
    latitude = models.FloatField(null=True, db_column='Latitude', blank=True) # Field name made lowercase.
    longitude = models.FloatField(null=True, db_column='Longitude', blank=True) # Field name made lowercase.
    contactname = models.CharField(max_length=100L, db_column='ContactName', blank=True) # Field name made lowercase.
    phone = models.CharField(max_length=100L, db_column='Phone', blank=True) # Field name made lowercase.
    email = models.CharField(max_length=255L, db_column='EMail', blank=True) # Field name made lowercase.
    website = models.CharField(max_length=255L, db_column='WebSite', blank=True) # Field name made lowercase.
    virtualtour = models.CharField(max_length=255L, db_column='VirtualTour', blank=True) # Field name made lowercase.
    description = models.CharField(max_length=512L, db_column='Description', blank=True) # Field name made lowercase.
    lift = models.IntegerField(null=True, blank=True)
    gym = models.IntegerField(null=True, blank=True)
    swimmingpool = models.IntegerField(null=True, blank=True)
    gatedcommunity = models.IntegerField(null=True, blank=True)
    powerbackup = models.IntegerField(null=True, db_column='PowerBackup', blank=True) # Field name made lowercase.
    furnished = models.IntegerField(null=True, db_column='Furnished', blank=True) # Field name made lowercase.
    cupboards = models.IntegerField(null=True, blank=True)
    facing = models.IntegerField(null=True, db_column='Facing', blank=True) # Field name made lowercase.
    possession = models.CharField(max_length=25L, db_column='Possession', blank=True) # Field name made lowercase.
    constructiondate = models.CharField(max_length=25L, db_column='ConstructionDate', blank=True) # Field name made lowercase.
    propertystatus = models.CharField(max_length=20L, db_column='PropertyStatus', blank=True) # Field name made lowercase.
    posteddate = models.DateTimeField(null=True, db_column='PostedDate', blank=True) # Field name made lowercase.
    expirydate = models.DateTimeField(null=True, db_column='ExpiryDate', blank=True) # Field name made lowercase.
    impressions = models.IntegerField(null=True, db_column='Impressions', blank=True) # Field name made lowercase.
    planid = models.IntegerField(null=True, db_column='PlanID', blank=True) # Field name made lowercase.
    sortorder = models.IntegerField(null=True, db_column='SortOrder', blank=True) # Field name made lowercase.
    rank = models.IntegerField(null=True, db_column='Rank', blank=True) # Field name made lowercase.
    duplicateid = models.IntegerField(null=True, db_column='DuplicateID', blank=True) # Field name made lowercase.
    isactive = models.IntegerField(null=True, db_column='IsActive', blank=True) # Field name made lowercase. This field type is a guess.
    ipaddress = models.CharField(max_length=20L, db_column='IPAddress', blank=True) # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate') # Field name made lowercase.
    propertyid = models.CharField(max_length=10L, db_column='PropertyID', blank=True) # Field name made lowercase.
    ownership = models.IntegerField(null=True, db_column='Ownership', blank=True) # Field name made lowercase.
    imagethumb = models.CharField(max_length=255L, db_column='ImageThumb', blank=True) # Field name made lowercase.
    confirmcode = models.CharField(max_length=25L, db_column='ConfirmCOde', blank=True) # Field name made lowercase.
    isconfirmed = models.IntegerField(null=True, db_column='IsConfirmed', blank=True) # Field name made lowercase.
    approvalstatus = models.IntegerField(null=True, db_column='ApprovalStatus', blank=True) # Field name made lowercase.
    ismobileverified = models.IntegerField(null=True, db_column='IsMobileVerified', blank=True) # Field name made lowercase.
    mobilecode = models.CharField(max_length=50L, db_column='MobileCode', blank=True) # Field name made lowercase.
    isemailverified = models.IntegerField(null=True, db_column='IsEMailVerified', blank=True) # Field name made lowercase.
    @property
    def State(self):
      state = States.objects.get(stateid = self.stateid)
      return state

    @property
    def City(self):
      city = Cities.objects.get(cityid = self.cityid)
      return city

    @property
    def PropertyType(self):
      return PROPERTY_TYPES[self.propertytypeid]

    @property
    def Plan(self):
      return PLANS[self.planid]

    class Meta:
        db_table = 'sales'


class States(models.Model):
    stateid = models.IntegerField(primary_key=True, db_column='StateID') # Field name made lowercase.
    name = models.CharField(max_length=50L, db_column='Name', blank=True) # Field name made lowercase.
    class Meta:
        db_table = 'states'

class Callbackrequests(models.Model):
    callbackrequestid = models.BigIntegerField(primary_key=True, db_column='CallBackRequestID') # Field name made lowercase.
    requestdate = models.DateTimeField(null=True, db_column='RequestDate', blank=True) # Field name made lowercase.
    customerid = models.IntegerField(null=True, db_column='CustomerID', blank=True) # Field name made lowercase.
    listingid = models.IntegerField(null=True, db_column='ListingID', blank=True) # Field name made lowercase.
    listingtype = models.IntegerField(null=True, db_column='ListingType', blank=True) # Field name made lowercase.
    name = models.CharField(max_length=50L, db_column='Name', blank=True) # Field name made lowercase.
    email = models.CharField(max_length=50L, db_column='Email', blank=True) # Field name made lowercase.
    phone = models.CharField(max_length=50L, db_column='Phone', blank=True) # Field name made lowercase.
    preftime1 = models.CharField(max_length=20L, db_column='PrefTime1', blank=True) # Field name made lowercase.
    preftime2 = models.CharField(max_length=20L, db_column='PrefTime2', blank=True) # Field name made lowercase.
    preftime3 = models.CharField(max_length=20L, db_column='PrefTime3', blank=True) # Field name made lowercase.
    message = models.CharField(max_length=255L, db_column='Message', blank=True) # Field name made lowercase.
    confirmcode = models.CharField(max_length=10L, db_column='ConfirmCode', blank=True) # Field name made lowercase.
    isverified = models.IntegerField(null=True, db_column='IsVerified', blank=True) # Field name made lowercase.
    isattended = models.IntegerField(null=True, db_column='IsAttended', blank=True) # Field name made lowercase.
    comments = models.CharField(max_length=255L, db_column='Comments', blank=True) # Field name made lowercase.
    class Meta:
        db_table = 'callbackrequests'
    
    @property
    def Listing(self):
      if(self.listingtype==1):
       listing = Sales.objects.get(listingid = self.listingid)
      elif(self.listingtype==2):
       listing = Rentals.objects.get(listingid = self.listingid)
      return listing
    
class Visitorreviews(models.Model):
    visitorreviewid = models.BigIntegerField(primary_key=True, db_column='VisitorReviewID') # Field name made lowercase.
    customerid = models.IntegerField(null=True, db_column='CustomerID', blank=True) # Field name made lowercase.
    listingid = models.IntegerField(null=True, db_column='ListingID', blank=True) # Field name made lowercase.
    listingtype = models.IntegerField(null=True, db_column='ListingType', blank=True) # Field name made lowercase.
    name = models.CharField(max_length=100L, db_column='Name', blank=True) # Field name made lowercase.
    email = models.CharField(max_length=25L, db_column='EMail', blank=True) # Field name made lowercase.
    contactno = models.CharField(max_length=10L, db_column='ContactNo', blank=True) # Field name made lowercase.
    bestprice = models.IntegerField(null=True, db_column='BestPrice', blank=True) # Field name made lowercase.
    visitorcomments = models.CharField(max_length=255L, db_column='VisitorComments', blank=True) # Field name made lowercase.
    sellercomments = models.CharField(max_length=255L, db_column='SellerComments', blank=True) # Field name made lowercase.
    mobilecode = models.CharField(max_length=25L, db_column='MobileCode', blank=True) # Field name made lowercase.
    emailcode = models.CharField(max_length=25L, db_column='EMailCode', blank=True) # Field name made lowercase.
    isemailverified = models.IntegerField(null=True, db_column='IsEMailVerified', blank=True) # Field name made lowercase.
    ismobileverified = models.IntegerField(null=True, db_column='IsMobileVerified', blank=True) # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate') # Field name made lowercase.
    class Meta:
        db_table = 'visitorreviews'

    @property
    def Listing(self):
      if(self.listingtype==1):
       listing = Sales.objects.get(listingid = self.listingid)
      elif(self.listingtype==2):
       listing = Rentals.objects.get(listingid = self.listingid)
      return listing

class Visitors(models.Model):
    visitorid = models.BigIntegerField(primary_key=True, db_column='VisitorID') # Field name made lowercase.
    name = models.CharField(max_length=50L, db_column='Name', blank=True) # Field name made lowercase.
    email = models.CharField(max_length=50L, db_column='EMail', blank=True) # Field name made lowercase.
    mobileno = models.CharField(max_length=10L, db_column='MobileNo', blank=True) # Field name made lowercase.
    pinnumber = models.CharField(max_length=10L, db_column='PinNumber', blank=True) # Field name made lowercase.
    emailcode = models.CharField(max_length=50L, db_column='EMailCode', blank=True) # Field name made lowercase.
    ismobileverified = models.IntegerField(null=True, db_column='IsMobileVerified', blank=True) # Field name made lowercase.
    isemailverified = models.IntegerField(null=True, db_column='IsEMailVerified', blank=True) # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate') # Field name made lowercase.
    isacceptterms = models.IntegerField(null=True, db_column='isAcceptTerms', blank=True) # Field name made lowercase.
    class Meta:
        db_table = 'visitors'

    
    
    
