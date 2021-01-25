from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register(r'envs', views.EnvsViewSet)

urlpatterns = [

]
urlpatterns += router.urls
