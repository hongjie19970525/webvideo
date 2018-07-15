from django.conf.urls import include, url
from django.contrib import admin
from videoplay.views import index, play, regist, login,check,checkhtml
from videoplay import views
from rest_framework import renderers, response, schemas
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.routers import DefaultRouter
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer

@api_view()
@renderer_classes([SwaggerUIRenderer, OpenAPIRenderer, renderers.CoreJSONRenderer])
def schema_view(request):
    generator = schemas.SchemaGenerator(title='Data API')
    return response.Response(generator.get_schema(request=request))

router = DefaultRouter()
router.register(r'movie', views.SnippetViewSet)

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^regist/$', regist),
    url(r'^$', login),
    url(r'^movie/$', index),
    url(r'^movie/video_(?P<id>\d{1,2}).html$', play),
    url(r'^swagger$', schema_view),
    url(r'^', include(router.urls)),
    url(r'^check/$',check),
    url(r'^face_camera/$',checkhtml),
    
]