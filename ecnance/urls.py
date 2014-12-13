#@PydevCodeAnalysisIgnore
from django.conf.urls import *
from ecnance.views import *

urlpatterns = patterns('',
                       (r'F1', myFirstView),
                       (r'home', DBcheck),
                       (r'Statements', Statements),
                       (r'getComp_Cache', GetCompanyCache),
)