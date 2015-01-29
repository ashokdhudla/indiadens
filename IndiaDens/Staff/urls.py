from django.conf.urls  import *
from views import *

staff_urls = patterns('Staff.views',
    url(r'^$', HomePage.as_view()),
    url(r'^login', Login.as_view()),
    url(r'^logout', Logout.as_view()),
    url(r'^new-listings', NewListings.as_view()),
    url(r'^change-password', ChangePassword.as_view()),
    url(r'^executive-registration', ExecutiveRegistration.as_view()),
    url(r'^employee-form', Employee.as_view()),
    url(r'^listings', Listings.as_view()),
    url(r'^listingimages', ListingImages.as_view()),
    url(r'^listing-attributes', ListingAttributes.as_view()),
    url(r'^customer-list', CustomerList.as_view()),
    url(r'^customer-delete', CustomerDelete.as_view()),
    url(r'^customer-sale-listings', CustomerSaleListings.as_view()),
    url(r'^customer-rental-listings', CustomerRentalListings.as_view()),
    url(r'^cities', Location.as_view()),
    url(r'^mobilemessages', ListMessages.as_view()),
    url(r'^delete-messages', DeleteMessages.as_view()),
    url(r'^employee-list', ExecutivesList.as_view()),
    url(r'^zap-db', ZapDb.as_view()),
    
)
