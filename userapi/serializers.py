from rest_framework import serializers
from shortener.models import Campaign, PageURL, SimpleRedirection


class RedirectionRelatedField(serializers.RelatedField):
    """
    A custom field to use for the `tagged_object` generic relationship.
    """

    def to_representation(self, value):
        """
        Serialize tagged objects to a simple textual representation.
        """
        if isinstance(value, SimpleRedirection):
            # return 'Redirection: ' + value.long_url
            return value.long_url
        # raise Exception('Unexpected type of tagged object')


class PageURLSerializer(serializers.ModelSerializer):
    cannonical_url = RedirectionRelatedField(
        queryset=PageURL.objects.all(),
        source='content_object',
        required=False
    )
    campaign = serializers.StringRelatedField()

    class Meta:
        model = PageURL
        fields = ('url_id', 'created',
                  'hits', 'title', 'description', 'cannonical_url',
                  'campaign')

    def create(self, validated_data):
        long_url = validated_data.get('long_url')
        author = validated_data.get('author')
        campaign = validated_data.pop('campaign')
        s = SimpleRedirection.objects.create(long_url=long_url)
        c = Campaign.objects.get(name=campaign)
        obj = PageURL.objects.create(
            author=author,
            url_type=PageURL.SIMPLE,
            content_object=s,
            campaign=c
        )
        return obj


class PageURLCreateSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    campaign = serializers.StringRelatedField()

    class Meta:
        model = PageURL
        fields = ('author', 'long_url', 'campaign')


class CampaignSerializer(serializers.ModelSerializer):

    class Meta:
        model = Campaign
        fields = ('name', 'description', 'owner')
