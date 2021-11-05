"""mapiacompany URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib          import admin
from django.urls             import path, re_path, include
from drf_yasg                import openapi
from drf_yasg.views          import get_schema_view
from strawberry.django.views import GraphQLView

from music_streaming.schema  import schema


schema_view = get_schema_view(
    openapi.Info( 
        title            = "Mafiacompany",
        default_version  = "v1",
        description      = "Mafiacompany 과제 API",
        terms_of_service = "https://www.google.com/policies/terms/",
        contact          = openapi.Contact(name="test", email="test@test.com"),
        license          = openapi.License(name="Test License"),
    ), 
    public = True, 
)

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name="schema-json"),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('', include('music_streaming.urls')),
    path('graphql', GraphQLView.as_view(schema=schema)),
]