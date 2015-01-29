from django.conf.urls import *
from Admin.urls import admin_urls
from Staff.urls import staff_urls
from Customers.urls import customer_urls
from views import *
from searchviews import *

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
    ('^_ah/warmup$', 'djangoappengine.views.warmup'),
    ('^$', HomePage.as_view()),
    ('^Admin/', include(admin_urls)),
    ('^Staff/', include(staff_urls)),
    ('^[Cc]ustomer/', include(customer_urls)),
    ('^new-listing', NewListing.as_view()),
    ('^reg-confirmation', RegConfirmation.as_view()),
    ('^logout', Logout.as_view()), 
    ('^getcities', GetCityName.as_view()),
    ('^listing-info', ListingInfo.as_view()),
    ('^mobile-message', SaveMessage.as_view()),
    ('^testmail', TestMail.as_view()),
    ('^visitor-reviewsform', VisitorReviews.as_view()),
    ('^callback-requestform', CallBackRequest.as_view()),
    ('^testajax', TestAjax.as_view()),
    ('^get-listings', SearchResults.as_view()),
    ('^visitor-login', VisitorLogin.as_view()),
    ('^confirm-code', ConfirmVisitors.as_view()),
    ('^test-slide', TestSlide.as_view()),
    ('^ajax-customerlogin', AjaxCustomerLogin.as_view()),
    ('^ajax-confirmmobile', AjaxConfirmMobile.as_view()),
    ('^whatismyip', MyIP.as_view()),
    #('^display-cities', AutoDispalyCities.as_view()),
    url(r'^testmodel', TestModel.as_view()),
)
