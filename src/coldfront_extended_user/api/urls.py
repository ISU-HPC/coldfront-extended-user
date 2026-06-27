from coldfront.api.routers import ColdFrontRouter

from . import views

router = ColdFrontRouter()
router.APIRootView = views.ExtendedUserRootView

# Projects
router.register("custom-user-fields", views.CustomUserFieldsViewSet)

app_name = "extended-user-api"
urlpatterns = router.urls