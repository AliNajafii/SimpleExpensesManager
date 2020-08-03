from rest_framework import serializers
from django.utils.translation import gettext as _
class FilterSerializer(serializers.Serializer):

    all = serializers.BooleanField()
    tags = serializers.BooleanField()
    categories = serializers.BooleanField()
    transactions = serializers.BooleanField()

    class Meta:
        fields = ['all','tags','transactions','categories']

    def validate(self,attrs):
        all = attrs.get('all')
        tags = attrs.get('tags')
        cats = attrs.get('categories')
        trans = attrs.get('transactions')

        check_items = [int(i) for i in attrs.values()]

        if sum(check_items) != 1 :
            raise serializers.ValidationError(
            detail= _('One filter item should be selected.')
            )

        return attrs

class SearchSerializer(serializers.Serializer):

    keyword = serializers.CharField(max_length=1000)
    filter = FilterSerializer()

    class Meta:
        fields = ['filter','keyword']
