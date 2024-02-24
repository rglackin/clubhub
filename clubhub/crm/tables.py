import django_tables2 as tables
from .models import User, ClubUser
from django_tables2.utils import A
from django.utils.html import format_html

class UserTable(tables.Table):
    approve = tables.TemplateColumn(template_name="crm/approve_button.html", verbose_name="")
    deny = tables.TemplateColumn(template_name="crm/deny_button.html", verbose_name="")
    class Meta:
        model = User
        template_name = "django_tables2/bootstrap4.html"
        fields = ("username","phone_no","email","approved" )
        attrs = {
            "class":"table table-striped shadow table-hover sortable",
            "thead":{
                "class":"thead-dark text-white"
            }
            } 
    #render_foo method can change how column is rendered
    """def render_approve(self, record):
        if not record.approved:
            return format_html()
        #row_attrs = {'data-href': lambda record: record.get_absolute_url}"""

class ClubUserTable(tables.Table):
    class Meta:
        model = ClubUser
        template_name = "django_tables2/bootstrap4.html"
        #fields = ('__all__') 
        attrs = {
            "class":"table table-striped shadow table-hover sortable",
            "thead":{
                "class":"thead-dark text-white"
            }
            }    
        row_attrs = {'data-href': lambda record: record.get_absolute_url} 