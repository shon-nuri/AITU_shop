# In your main urls.py (the one that includes your apps and static files)
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),  # Keep this, it includes your accounts-related URLs
    path('social-auth/', include('social_django.urls')),  # Keep only this in your root URLs
    path('', include('store.urls'))  # Your store URLs
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
