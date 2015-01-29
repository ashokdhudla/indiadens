from django import forms

class SalesForm(forms.Form):
  PROPERTY_TYPE = [('', "Property Type"),
                   ('10', "Apartments"),
                   ('20', "Independent House"),
                   ('25', " Villas"),
                   ('30', "Pent House"),
                   ('40', "Farm House"),
                   ('50', "Office Space"),
                   ('100', "Residential Lands"),
                   ('110', "Commercial Lands"),
                  ]

  AREA_UNITS = [('', ""),
                ('1', "Sq.Ft"),
                ('2', "Sq.Mts"),
                ('3', "Sq.Yrds"),
                ]
  STATE = [('0', "Select State"),
           ('1', "Andaman Nicobar"),
           ('2', "Andhra Pradesh"),
           ('3', "Arunachal Pradesh"),
           ('4', "Assam"),
           ('5', "Bihar"),
           ('6', "Chattisghar"),
           ('7', "Daman and Diu"),
           ('8', "Goa"),
           ('9', "Gujarath"),
           ('10', "Haryana"),
           ('11', "Himachal Pradesh"),
           ('12', "Jammu and Kashmir"),
           ('13', "Jharkandh"),
           ('14', "Karnataka"),
           ('15', "Kerala"),
           ('16', "MadhyaPradesh"),
           ('17', "Maharashtra"),
           ('18', "Manipur"),
           ('19', "Meghalaya"),
           ('20', "Mizoram"),
           ('21', "Nagaland"),
           ('22', "New Delhi"),
           ('23', "Orissa"),
           ('24', "Puducherry"),
           ('25', "Panjab"),
           ('26', "Rajastan"),
           ('27', "Sikkim"), 
           ('28', "Tamilnadu"),
           ('29', "Tripura"),
           ('30', "UttarPradesh"),
           ('31', "Uttarakandh"),
           ('32', "West Bengal"),
          ]
  OWNERSHIP_TYPE = [('', "Select"),
                    ('1', "Owner"),
                    ('2', "Agent"),
                    ('3', "Builder"),
                   ]
  Property_Type = forms.ChoiceField(choices = PROPERTY_TYPE,  widget = forms.Select(attrs={'style':'width:200px'}), required=True)
  Price = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'style':'width:60px'}), required=True)
  Area = forms.CharField(widget = forms.TextInput(attrs={'autocomplete':'ON',  'style':'width:60px'}),  required=True)
  AreainWords = forms.ChoiceField(choices = AREA_UNITS, widget = forms.Select(attrs={'style':'width:100px'}), required=True, initial='1')
  BedRooms = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'style':'width:60px'}), required=False)
  BathRooms = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'style':'width:60px'}), required=False)
  PropertyLocation = forms.CharField(widget=forms.Textarea(attrs={'rows':3,'style':'width:300px; height=50px'}),  required=True)
  City = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'style':'width:100px'}), required=True)
  CityID = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'style':'width:80px'}), required=True)
  State = forms.ChoiceField(choices = STATE, widget = forms.Select(attrs={'style':'width:200px'}), required=True)
  TellabturProperty = forms.CharField(widget=forms.Textarea(attrs={'style':'width:300px'}), required=True)
  Name = forms.CharField(forms.TextInput(attrs={'autocomplete':'ON', 'size':30, 'style':'width:60px'}),  required=True)
  Email = forms.CharField(forms.TextInput(attrs={'autocomplete':'ON', 'size':30, 'style':'width:60px'}), required=True)
  Contactno = forms.CharField(forms.TextInput(attrs={'autocomplete':'ON', 'size':10, 'style':'width:60px'}), required=True)
  ownershipType = forms.ChoiceField(choices = OWNERSHIP_TYPE, required=True)
  listingType = forms.CharField(max_length = 50L, required=True)
  
  
  
class VForm(forms.Form):
  Name = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON','size':30, 'style':'width:80px'}), required=True)
  Email = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'size':30, 'style':'width:80px'}), required=True)
  Contactno = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON','size':30, 'style':'width:80px'}), required=True)
  Bestprice = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'style':'width:40px'}), required=True)
  Visitorcomments = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows':4, 'style':'width:200px'}))
  Sellercomments =  forms.CharField(required=False, widget=forms.Textarea(attrs={'rows':4, 'style':'width:200px'}))
  CustomerId = forms.CharField(widget=forms.HiddenInput(), required=True)
  ListingId = forms.CharField(widget=forms.HiddenInput(), required=True)
  ListingType = forms.CharField(widget=forms.HiddenInput(), required=True) 
  
  
class CallbackRequestForm(forms.Form):
  CALL = [('1',"Yes"),
          ('0','No'),
          ]

  name = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'style':'width:80px'}), required=True)
  email = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'style':'width:80px'}), required=True)
  phone = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'style':'width:80px'}), required=True)
  message = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows':4, 'style':'width:200px'}))
  pftime1 = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'style':'width:80px'}), required=True)
  pftime2 = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'style':'width:80px'}), required=False)
  pftime3 = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'style':'width:80px'}), required=False)
  callattended = forms.ChoiceField(choices = CALL, widget = forms.Select(attrs={'style':'width:200px'}), required=False)
  comments = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows':4, 'style':'width:200px'}))
  CustomerId = forms.CharField(widget=forms.HiddenInput(), required=True)
  ListingId = forms.CharField(widget=forms.HiddenInput(), required=True)
  ListingType = forms.CharField(widget=forms.HiddenInput(), required=True)
   
    
    




    
