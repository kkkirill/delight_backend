from django_elasticsearch_dsl_drf.constants import (
    LOOKUP_FILTER_RANGE,
    LOOKUP_QUERY_GT,
    LOOKUP_QUERY_GTE,
    LOOKUP_QUERY_IN,
    LOOKUP_QUERY_LT,
    LOOKUP_QUERY_LTE,
    SUGGESTER_COMPLETION,
)
from django_elasticsearch_dsl_drf.filter_backends import (
    DefaultOrderingFilterBackend,
    FacetedSearchFilterBackend,
    FilteringFilterBackend,
    SearchFilterBackend,
    SuggesterFilterBackend,
)
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet

#############################################################

# from rest_framework.views import APIView
#
#
# class SearchView(APIView):
#     authentication_classes = [authentication.TokenAuthentication]
#     permission_classes = [permissions.IsAdminUser]
#
#     def get(self, request, format=None):
#         """
#         Return a list of all users.
#         """
#         usernames = [user.username for user in User.objects.all()]
#         return Response(usernames)

#############################################################
from apps.search_old.documents import GlobalDocument
from apps.search_old.serializers import GlobalDocumentSerializer


class GlobalDocumentViewSet(DocumentViewSet):
    document = GlobalDocument
    serializer_class = GlobalDocumentSerializer
    ordering = ('id',)
    lookup_field = 'id'

    def get_serializer_class(self):
        return super().get_serializer_class()

    filter_backends = [
        DefaultOrderingFilterBackend,
        FilteringFilterBackend,
        SearchFilterBackend,
        SuggesterFilterBackend,
    ]

    search_fields = (
        'title',
        'stage_name'
    )

    filter_fields = {
        'id': {
            'field': 'id',
            'lookups': [
                LOOKUP_FILTER_RANGE,
                LOOKUP_QUERY_IN,
                LOOKUP_QUERY_GT,
                LOOKUP_QUERY_GTE,
                LOOKUP_QUERY_LT,
                LOOKUP_QUERY_LTE,
            ],
        },
        'title': 'title',
        'stage_name': 'stage_name',
    }

    suggester_fields = {
        'title_suggest': {
            'field': 'title.suggest',
            'suggesters': [
                SUGGESTER_COMPLETION,
            ],
        },
        'stage_name_suggest': {
            'field': 'stage_name.suggest',
            'suggesters': [
                SUGGESTER_COMPLETION,
            ],
        },
    }

    def list(self, request, *args, **kwargs):
        res = super().list(request, *args, **kwargs)
        return res

# from elasticsearch.client import Elasticsearch
# e = Elasticsearch(hosts=['elasticsearch:9200'])

# from elasticsearch_dsl import connections
# e = connections.create_connection(hosts=['elasticsearch:9200'])
# from elasticsearch_dsl import Search
# s = Search(using=e, index=['albums', 'artists', 'songs'], doc_type='_doc')
# s.aggs.bucket('byindex', 'terms', field='_index', size=100)
# l = s.execute()
# l.aggregations.byindex.buckets[0]

# s = GlobalDocument.search_old().query("match_all").extra(size=78)

#############################################################

# from elasticsearch_dsl import Search
#
#
# def global_search(request):
#     q = request.GET.get('q')
#     objects = ''
#
#     if q:
#         search_old = Search(index=['users', 'products'])
#         objects = search_old.query("multi_match", query=q,
#                                fields=['first_name', 'last_name', 'username', 'title', 'description', 'upc'])
#
#     return render(request, 'oscar/search_old/search_old.html', {'objects': objects})
