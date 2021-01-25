from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register(r'testsuites', views.TestsuitsViewSet)

urlpatterns = [

]
urlpatterns += router.urls
