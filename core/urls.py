from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/', include('authapi.urls')),
    path('api/', include('aiapi.urls')),
    path('api/', include('authentications.urls')),
    path('api/', include('accounts.urls')),
    path('api/', include('news.urls'))
]
