from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

# trying the an experimental view
from .experimentalview import *

urlpatterns = [
    path('home/', home, name="home" ),
    path('monitor/<int:pk>', monitor, name="monitor"),
    path('location/', location, name="location"),
    path('', signin, name="signin"),
    path('logout/', logout_view, name='logout'),
    path('signup/', signup, name='signup'),
    path('about/', about, name='about'),
    path('map/', map, name='map'),

    path('video_feed/', video_feed, name='video_feed'), # for webcam view

    # experimental view url
    path('webcam/', webcam, name='webcam'),
]

# Add the following line to serve media files during development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
