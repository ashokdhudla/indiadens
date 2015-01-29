from django import forms

class SaleListingImages(forms.Form):
    largeimage = forms.CharField(forms.TextInput(attrs={'autocomplete':'ON', 'size':30, 'style':'width:40px'}),  required=True)
    description = forms.CharField(required=True, widget=forms.Textarea)

class ExecutiveRegForm(forms.Form):
    BUSINESS_CATEGORY = [
                   ('0', "Individual"),
                   ('1', "NetCafe"),
                   ('2', "E-seva"),
                   ]
    
    firstname = forms.CharField(widget = forms.TextInput(attrs={'autocomplete':'ON',  'style':'width:80px'}),  required=True)
    lastname = forms.CharField(widget = forms.TextInput(attrs={'autocomplete':'ON', 'size':30, 'style':'width:80px'}),  required=True)
    title = forms.CharField(widget = forms.TextInput(attrs={'autocomplete':'ON', 'size':30, 'style':'width:80px'}),  required=False)
    emailid = forms.CharField(widget = forms.TextInput(attrs={'autocomplete':'ON', 'size':30, 'style':'width:80px'}),  required=True)
    loginpwd = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'class' : 'txt-box1', 'autocomplete':'ON',}))
    contactno=forms.CharField(widget = forms.TextInput(attrs={'autocomplete':'ON', 'size':10, 'style':'width:80px'}),  required=True)
    business_category=forms.ChoiceField(choices = BUSINESS_CATEGORY, widget = forms.Select(attrs={'style':'width:100px'}), required=True)
    business_info = forms.CharField(widget = forms.Textarea(attrs={'autocomplete':'ON', 'size':30, 'rows' :3, 'style':'width:200px'}),  required=False)
    address = forms.CharField(required=True, widget=forms.Textarea(attrs={'rows':4, 'style':'width:200px'}))
    City = forms.CharField(widget = forms.TextInput(attrs={'autocomplete':'ON', 'size':30, 'style':'width:80px'}),  required=True)
    CityID = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'style':'width:40px'}), required=False)
    state = forms.ChoiceField(choices = [], widget = forms.Select(attrs={'style':'width:100px'}), required=True) 
    
    def __init__(self, *args, **kwargs):
      states = []
      if 'states' in kwargs:
        states = kwargs.pop('states')
      super(ExecutiveRegForm, self).__init__(*args,**kwargs)
      self.fields['state'].choices = states 
    
class EmployeeRegForm(forms.Form):
    
    firstname = forms.CharField(widget = forms.TextInput(attrs={'autocomplete':'ON',  'style':'width:90px',}),  required=True)
    lastname = forms.CharField(widget = forms.TextInput(attrs={'autocomplete':'ON', 'size':30, 'style':'width:90px'}),  required=True)
    emailid = forms.CharField(widget = forms.TextInput(attrs={'autocomplete':'ON', 'size':30, 'style':'width:100px'}),  required=True)
    loginpwd = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'class' : 'txt-box1', 'autocomplete':'ON',}))
    contactno=forms.CharField(widget = forms.TextInput(attrs={'autocomplete':'ON', 'size':30, 'style':'width:100px'}),  required=True)
    address = forms.CharField(required=True, widget=forms.Textarea(attrs={'rows':4, 'style':'width:200px'}))
    City = forms.CharField(widget = forms.TextInput(attrs={'autocomplete':'ON', 'size':30, 'style':'width:80px'}),  required=True)
    CityID = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'style':'width:80px'}), required=False)
    state = forms.ChoiceField(choices = [], widget = forms.Select(attrs={'style':'width:100px'}), required=True)
    
    def __init__(self, *args, **kwargs):
      states = []
      if 'states' in kwargs:
        states = kwargs.pop('states')
      super(EmployeeRegForm, self).__init__(*args,**kwargs)
      self.fields['state'].choices = states  
            
  
  
  
  