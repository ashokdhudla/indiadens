from django import forms
import time
#### Ashok Forms Begins here ##
class StaffLoginForm(forms.Form):
    Email = forms.CharField(forms.TextInput(attrs={'autocomplete':'ON', 'size':30, 'style':'width:10px'}), required=False)
    Password = forms.CharField(forms.PasswordInput(attrs={'autocomplete':'ON', 'size':30, 'style':'width:10px'}), required=False)

class SalesForm(forms.Form):
    ListingId = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'style':'width:60px'}), required=False)

    PropertyType =[('0','Select'),('10','Apartments'),
                   ('20','Individual Home'), ('25','villas'),('30','Pent House'),('40','Farm Hous0e'),('50','Office Space'),('100','Residential Land'),('110','Commercial Land')]
    PropertyType = forms.ChoiceField(choices = PropertyType,widget = forms.Select(attrs={'style':'width:150px'}), required=False)
    Ownership =[('0','Select'),('1','Owner'),
                   ('2','Agent'), ('3','Staff'),]
    Ownership = forms.ChoiceField(choices = Ownership,widget = forms.Select(attrs={'style':'width:100px'}), required=False)
    Title = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'style':'width:150px'}), required=False) 
    Price = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'style':'width:60px'}), required=False)
    BedRooms = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'style':'width:60px'}), required=False)
    BathRooms = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'style':'width:60px'}), required=False)
    Area = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'style':'width:60px'}), required=False)
    AreaUnit =[ ('1', "Sq.Ft"),
                ('2', "Sq.Mts"),
                ('3', "Sq.Yrds"),
                ]
    AreaUnit = forms.ChoiceField(choices = AreaUnit, widget = forms.Select(attrs={'style':'width:90px'}), required=False)
    Address = forms.CharField(widget=forms.Textarea(attrs={'rows':'4','autocomplete':'ON', 'style':'width:300px; height=50px;'}), required=False) 
    LandMark1 = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'style':'width:120px'}), required=False)
    LandMark2 = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'style':'width:120px'}), required=False)
    LandMark3 = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'style':'width:120px'}), required=False)
    LandMark4 = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'style':'width:120px'}), required=False)
    CityID = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'style':'width:8px'}), required=False)
    City = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'style':'width:120px'}), required=False)
    Latitude = forms.FloatField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'style':'width:150px', 'class':'gllpLatitude'}), required=False)
    Longitude = forms.FloatField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'style':'width:150px','class':'gllpLongitude' }), required=False)
    STATE = [('', "Select State"),
           ('1', "Andhra Pradesh"),
           ('2', "Chennai"),
           ('3', "Tamilnadu"),
           ('4', "Maharashtra"),
           ('5', "MadhyaPradesh"),
           ('6', "Delhi"),
          ]
    State = forms.ChoiceField(choices = STATE, widget = forms.Select(attrs={'style':'width:180px'}), required=False)
    PostalCode = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'style':'width:60px'}), required=False)
    ContactName = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'style':'width:100px'}), required=False)
    Phone = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'style':'width:100px'}), required=False)
    Email = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'style':'width:100px'}), required=False)
    Website = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'style':'width:100px'}), required=False)
    VirtualTour = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'style':'width:80px'}), required=False)
    Description = forms.CharField(widget=forms.Textarea(attrs={'autocomplete':'ON', 'style':'width:600px'}), required=False)
    Lift = forms.BooleanField(widget=forms.CheckboxInput(attrs={'autocomplete':'ON', 'style':'width:80px'}), required=False)
    Gym = forms.BooleanField(widget=forms.CheckboxInput(attrs={'autocomplete':'ON', 'style':'width:80px'}), required=False)
    SwimmingPool = forms.BooleanField(widget=forms.CheckboxInput(attrs={'autocomplete':'ON', 'style':'width:80px'}), required=False)
    GatedCommunity = forms.BooleanField(widget=forms.CheckboxInput(attrs={'autocomplete':'ON', 'style':'width:80px'}), required=False)
    PowerBackUp = [('0', "Select"),
           ('1', "no"),
           ('2', "semi"),
           ('3', "full"),
          ]
    PowerBackUp =forms.ChoiceField(choices = PowerBackUp, widget = forms.Select(attrs={'style':'width:80px'}), required=False)
    Furnished = [('0', "Select"),
           ('1', "no"),
           ('2', "semi"),
           ('3', "full"),
          ]
    Furnished =forms.ChoiceField(choices = Furnished, widget = forms.Select(attrs={'style':'width:80px'}), required=False)
    Cupboards = forms.BooleanField(widget=forms.CheckboxInput(attrs={'style':'width:40px'}), required=False)
    Facing = [('0', "Select"),
           ('1', "East"),
           ('2', "West"),
           ('3', "North"),
           ('4', "South"),
          ] 
    Facing = forms.ChoiceField(choices = Facing, widget = forms.Select(attrs={'style':'width:80px'}), required=False)
    Possession = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'style':'width:80px'}), required=False)
    Cyear =  [('0',"select"),
              ('2013',"2013"),
           ('2012',"2012"),
           ('2011',"2011"),
           ('2010',"2010"),
           ('2009',"2009"),
           ('2008',"2008"),
           ('2007',"2007"),
           ('2006',"2006"),
           ('2005',"2005"),
           ('2004',"2004"),
           ('2003',"2003"),
          ] 
    ConstructionDate = forms.ChoiceField(choices = Cyear,widget = forms.Select(attrs={'style':'width:80px'}), required=False)
    Pstatus =[('','Select'),('a','Under Construction'),
                   ('b','New Constrution'), ('c','Resale'),('d','New Project'),]
    PropertyStatus = forms.ChoiceField(choices = Pstatus,widget = forms.Select(attrs={'style':'width:160px'}), required=False)
    PostedDate = forms.DateField(widget=forms.DateInput(attrs={'autocomplete':'ON', 'style':'width:80px', 'readonly':'readonly' }), required=False)
    PropertyId = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'style':'width:80px'}), required=False) 
    Planid =[('0','Free'),]
    Planid = forms.ChoiceField(choices = Planid,widget = forms.Select(attrs={'style':'width:100px'}), required=False)
    Approved =[('0','Select '),('0','New'),('1','Pending Approved'),
                   ('2','DisApproved'), ('3','Approved'),]
    Approved = forms.ChoiceField(choices = Approved,widget = forms.Select(attrs={'style':'width:100px'}), required=False)

    def __init__(self, *args, **kwargs):
      states = []
      if 'states' in kwargs:
        states = kwargs.pop('states')
      super(SalesForm, self).__init__(*args,**kwargs)
      self.fields['State'].choices = states 
#       if 'Constructionyear' in kwargs:
#         Constructionyear = kwargs.pop('Constructionyear')
#       super(SalesForm, self).__init__(*args,**kwargs)
#       self.fields['Constructionyear'].choices = Constructionyear 



class RentalsForm(forms.Form):
    PType =[('0','Select'),('10','Apartments'),('20','Individual Home'), ('25','villas'),
                   ('30','Pent House'),('40','Farm House'),('50','Office Space'),('100','Residential Land'),('110','Commercial Land'),]
    PropertyType = forms.ChoiceField(choices = PType,widget = forms.Select(attrs={'style':'width:150px'}), required=False)
    Ownership =[('0','Select'),('1','Owner'),
                   ('2','Agent'), ('3','Staff'),]
    Ownership = forms.ChoiceField(choices = Ownership,widget = forms.Select(attrs={'style':'width:90px'}), required=False)
    Title = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'style':'width:150px'}), required=False) 
    Rent = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'style':'width:60px'}), required=False)
    RentFrequency = [
           ('1', "Monthly"),
           ('2', "Quarterly"),
           ('3', "Yearly"),
          ]
    RentFrequency = forms.ChoiceField(choices = RentFrequency, widget = forms.Select(attrs={'style':'width:110px'}), required=False)
    AdvanceAmount = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'style':'width:60px'}), required=False)
    Maintenance = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'style':'width:60px'}), required=False)
    AllowedFamily = forms.BooleanField(widget=forms.CheckboxInput(attrs={'autocomplete':'ON', 'style':'width:80px'}), required=False)
    AllowedBachelors = forms.BooleanField(widget=forms.CheckboxInput(attrs={'autocomplete':'ON', 'style':'width:80px'}), required=False)
    BedRooms = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'style':'width:60px'}), required=False)
    BathRooms = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'style':'width:60px'}), required=False)
    Area = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'style':'width:60px'}), required=False)
    AreaUnit =[('1', "Sq.Ft"),
                ('2', "Sq.Mts"),
                ('3', "Sq.Yrds"),
                ]
    AreaUnit = forms.ChoiceField(choices = AreaUnit, widget = forms.Select(attrs={'style':'width:90px'}), required=False)
    Address = forms.CharField(widget=forms.Textarea(attrs={'rows':'4','autocomplete':'ON', 'style':'width:300px; height=50px;'}), required=False) 
    LandMark1 = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'style':'width:120px'}), required=False)
    LandMark2 = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'style':'width:120px'}), required=False)
    LandMark3 = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'style':'width:120px'}), required=False)
    LandMark4 = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'style':'width:120px'}), required=False)
    CityID = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'style':'width:80px'}), required=False)
    City = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'style':'width:120px'}), required=False)
    Latitude = forms.FloatField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'style':'width:150px', 'class':'gllpLatitude'}), required=False)
    Longitude = forms.FloatField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'style':'width:150px','class':'gllpLongitude' }), required=False)
    STATE = [('0', "Select"),
           ('1', "Andhra Pradesh"),
           ('2', "Chennai"),
           ('3', "Tamilnadu"),
           ('4', "Maharashtra"),
           ('5', "MadhyaPradesh"),
           ('6', "Delhi"),
          ]
    State = forms.ChoiceField(choices = [], widget = forms.Select(attrs={'style':'width:180px'}), required=False)
    PostalCode = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'style':'width:60px'}), required=False)
    ContactName = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'style':'width:100px'}), required=False)
    Phone = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'style':'width:100px'}), required=False)
    Email = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'style':'width:100px'}), required=False)
    Website = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'style':'width:100px'}), required=False)
    VirtualTour = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'style':'width:80px'}), required=False)
    Description = forms.CharField(widget=forms.Textarea(attrs={'autocomplete':'ON', 'style':'width:600px'}), required=False)
    Lift = forms.BooleanField(widget=forms.CheckboxInput(attrs={'autocomplete':'ON', 'style':'width:80px'}), required=False)
    Gym = forms.BooleanField(widget=forms.CheckboxInput(attrs={'autocomplete':'ON', 'style':'width:80px'}), required=False)
    SwimmingPool = forms.BooleanField(widget=forms.CheckboxInput(attrs={'autocomplete':'ON', 'style':'width:80px'}), required=False)
    GatedCommunity = forms.BooleanField(widget=forms.CheckboxInput(attrs={'autocomplete':'ON', 'style':'width:80px'}), required=False)
    PowerBackUp = [('0', "Select"),
           ('1', "no"),
           ('2', "semi"),
           ('3', "full"),
          ]
    PowerBackUp =forms.ChoiceField(choices = PowerBackUp, widget = forms.Select(attrs={'style':'width:80px'}), required=False)
    Furnished = [('0', "Select"),
           ('1', "no"),
           ('2', "semi"),
           ('3', "full"),
          ]
    Furnished =forms.ChoiceField(choices = Furnished, widget = forms.Select(attrs={'style':'width:80px'}), required=False)
    Cupboards = forms.BooleanField(widget=forms.CheckboxInput(attrs={'style':'width:40px'}), required=False)
    Facing = [('0', "Select"),
           ('1', "East"),
           ('2', "West"),
           ('3', "North"),
           ('4', "South"),
          ] 
    Facing = forms.ChoiceField(choices = Facing, widget = forms.Select(attrs={'style':'width:80px'}), required=False)
    Possession = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'style':'width:80px'}), required=False)
    Cyear =  [('0',"select"),
              ('2013',"2013"),
           ('2012',"2012"),
           ('2011',"2011"),
           ('2010',"2010"),
           ('2009',"2009"),
           ('2009',"2009"),
           ('2008',"2008"),
           ('2007',"2007"),
           ('2006',"2006"),
           ('2005',"2005"),
           ('2004',"2004"),
           ('2003',"2003"),
          ] 
    ConstructionDate = forms.ChoiceField(choices = Cyear,widget = forms.Select(attrs={'style':'width:80px'}), required=False)
    Pstatus =[('x','Select'),('a','Occupied'),
                   ('b','Vacant'), ('c','Yet To Vacant')]
    PresentStatus = forms.ChoiceField(choices = Pstatus,widget = forms.Select(attrs={'style':'width:80px'}), required=False)
    PostedDate = forms.DateField(widget=forms.DateInput(attrs={'autocomplete':'ON', 'style':'width:80px','readonly':'readonly'}), required=False)
    PropertyId = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'style':'width:80px'}), required=False) 
    Planid =[('0','Free'),]
    Planid = forms.ChoiceField(choices = Planid,widget = forms.Select(attrs={'style':'width:80px'}), required=False)
    Approved =[('0','Select'),('0','New'),('1','Pending Approved'),
                   ('2','DisApproved'), ('3','Approved'),]
    Approved = forms.ChoiceField(choices = Approved,widget = forms.Select(attrs={'style':'width:150px'}), required=False)

    def __init__(self, *args, **kwargs):
      states = []
      if 'states' in kwargs:
        states = kwargs.pop('states')
      super(RentalsForm, self).__init__(*args,**kwargs)
      self.fields['State'].choices = states
      
      
class CustomerForm(forms.Form):
  CUSTOMER_TYPE = [('0', "Select Type"),
           ('1', "Owner"),
           ('2', "Dealer/Agent"),
           ('3', "Builder"),
          ]
  COUNTRY = [('1',"India")]
  customertype = forms.ChoiceField(choices = CUSTOMER_TYPE, widget = forms.Select(attrs={'style':'width:120px'}), required=True)
  title = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'style':'width:80px'}), required=False)
  subtitle= forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'style':'width:80px'}), required=False)
  firstname = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'style':'width:90px'}), required=True)
  lastname = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'style':'width:90px'}), required=True)
  address = forms.CharField(required=True, widget=forms.Textarea(attrs={'rows':4, 'style':'width:200px'}))
  CityID = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'style':'width:40px'}), required=False)
  City = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'style':'width:80px'}), required=True)
  state = forms.ChoiceField(choices = [], widget = forms.Select(attrs={'style':'width:100px'}), required=False)
  country = forms.ChoiceField(choices = COUNTRY, widget = forms.Select(attrs={'style':'width:100px'}), required=True)
  phone = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'style':'width:100px'}), required=True)
  fax = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'style':'width:80px'}), required=False)
  email = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'style':'width:100px'}), required=False)
  website = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'style':'width:80px'}), required=False)
  profile = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'style':'width:60px'}), required=False)
  deals = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows':4, 'style':'width:200px'}))
  dealinglocation = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows':4, 'style':'width:200px'}))
  description = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows':4, 'style':'width:200px'}))
  
  
  def __init__(self, *args, **kwargs):
      states = []
      if 'states' in kwargs:
        states = kwargs.pop('states')
      super(CustomerForm, self).__init__(*args,**kwargs)
      self.fields['state'].choices = states 
 
      
    





    
