from rest_framework import routers

from interfaces import views

router = routers.SimpleRouter()

router.register(r'interfaces', views.InterfacesViewSet)

urlpatterns = [

]
urlpatterns += router.urls
