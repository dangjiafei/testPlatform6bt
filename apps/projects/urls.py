from rest_framework import routers

from projects import views

router = routers.SimpleRouter()

router.register(r'projects', views.ProjectViewSet)

urlpatterns = [

]
urlpatterns += router.urls
