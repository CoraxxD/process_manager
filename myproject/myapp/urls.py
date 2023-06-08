from django.urls import path
from myapp.views import home, close_process, login_view, add_to_blacklist, remove_blacklisted_process, update_data, add_to_whitelist, remove_whitelisted_process

urlpatterns = [
    path('login/', login_view, name='login'),
    path('', home, name='home'),
    path('close_process/', close_process, name='close_process'),
    path('add_to_blacklist/', add_to_blacklist, name='add_to_blacklist'),
    path('add_to_whitelist/', add_to_whitelist, name='add_to_whitelist'),
    path('remove_blacklisted_process/<str:process_name>/', remove_blacklisted_process, name='remove_blacklisted_process'),
    path('remove_whitelisted_process/<str:process_name>/', remove_whitelisted_process, name='remove_whitelisted_process'),
    path('update_data/', update_data, name='update_data'),
#    path('metrics/', metrics, name='metrics'),
]
