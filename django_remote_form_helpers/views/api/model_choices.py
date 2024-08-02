from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.cache import cache


class ModelChoicesAPIView(APIView):
    model = None
    value_field = 'pk' 
    text_field = 'name'
    allowed_filters = '__all__' 

    def get_value_field(self):
        return self.value_field
    
    def get_text_field(self):
        return self.text_field
    
    def get_model(self):
        return self.model
    
    def get_allowed_filters(self):
        if self.allowed_filters == '__all__':
            return [field.name for field in self.model._meta.fields]
        return self.allowed_filters

    def get_queryset(self):
        model = self.get_model()
        return model.objects.all()

    def get_data(self, query_params):
        filters = {key: value for key, value in query_params.items() if key in self.get_allowed_filters()}
        queryset = self.get_queryset()
        value_field = self.get_value_field()
        text_field = self.get_text_field()
        return queryset.filter(**filters).values_list(value_field, text_field)

    def get(self, request, *args, **kwargs):
        cache_key = f"{self.model.__name__}_choices_{hash(frozenset(request.query_params.items()))}"
        cached_response = cache.get(cache_key)

        if cached_response:
            return Response(cached_response)

        data = self.get_data(request.query_params)
        cache.set(cache_key, data, timeout=60*15)

        return Response(data)
    