from IndiaDens.Admin import *


class HomePage(TemplateView):

  def get(self, request, *args, **kwargs):  
    content = {}
    return render_to_response("Admin/Index.html")

