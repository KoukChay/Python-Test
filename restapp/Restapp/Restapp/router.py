from rest_framework import routers
from infoAPI.viewsets import DbViewset

router = routers.DefaultRouter()
router.register('db', DbViewset)
