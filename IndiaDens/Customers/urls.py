from django.conf.urls  import *
from views import *
from AravindViews import *

customer_urls = patterns('Customer.views',
    url(r'^$', HomePage.as_view()),
    url(r'^login', Login.as_view()),
    url(r'^listing-form', ListingForm.as_view()),
    url(r'^customer-menu', CustomerListPage.as_view()),
    url(r'^customer-listings', CustomerListings.as_view()),
    url(r'^confirm/([A-Za-z0-9]+)$', Confirm.as_view()),
    url(r'^mobile-confirm', MobileConfirm.as_view()),
    url(r'^reset-password', ResetPassword.as_view()),
    url(r'^close-account', CloseAccount.as_view()),
    url(r'^ListDelele', CustomerListDelete.as_view()),
    url(r'^callback-requests', CustomerCallBackRequests.as_view()),
    url(r'^ajaxcallback-request', AjaxCallBackRequest.as_view()),
    url(r'^visitor-reviews', VisitorReviewList.as_view()),
    url(r'^list-delete', ListingDelete.as_view()),
    url(r'^change-password', ChangePassword.as_view()),
    url(r'^customer-form', CustomerRegistration.as_view()),
)
