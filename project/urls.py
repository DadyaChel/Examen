from django.contrib import admin
from django.urls import path
from rest_framework import routers, permissions
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from rest_framework.authtoken import views as auth_views
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from account import views as acc_view
from news import views as news_view

acc_router = DefaultRouter()
acc_router.register('register', acc_view.AuthorViewSet)


router = routers.DefaultRouter()
router.register('news', news_view.NewsViewSet)
router.register('comment', news_view.CommentViewSet)
router.register('statuses', news_view.StatusViewSet)

schema_view = get_schema_view(
   openapi.Info(
      title="News API",
      default_version='v-0.01-alpha',
      description="API для взаимодействия с News API",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="NO licence"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/auth/', include('rest_framework.urls')),
    path('api/account/token/', auth_views.obtain_auth_token),

    path('api/account/', include(acc_router.urls)),
    path('api/', include(router.urls)),

    path('api/news/<int:news_id>/comment/', news_view.CommentListCreateAPIView.as_view()),

    # documentation URL
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger_doc'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc_doc'),
]
