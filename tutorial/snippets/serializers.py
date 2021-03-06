from django.forms import widgets
from django.contrib.auth.models import User
from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES

class SnippetSerializer(serializers.HyperlinkedModelSerializer):
  owner = serializers.Field(source='owner.username')
  highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')
  pk = serializers.Field()
  title = serializers.CharField(required=False, max_length=100)
  code = serializers.CharField(widget=widgets.Textarea, max_length=100000)
  linenos = serializers.BooleanField(required=False)
  language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
  style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')
  owner = serializers.Field(source='owner.username')

  class Meta:
    model = Snippet
    fields = ('url', 'highlight', 'owner', 'title', 'code', 'linenos', 'language', 'style')

  def restore_object(self, attrs, instance=None):
    """
    Create or update a new snippet instance, given a dictionary
    of deserialized field values

    Note that if we don't define this method, then deserializing
    data will simply return a dictionary of items.
    """
    if instance:
      instance.title = attrs.get('title', instance.title)
      instance.code = attrs.get('code', instance.code)
      instance.linenos = attrs.get('linenos', instance.linenos)
      instance.language = attrs.get('language', instance.language)
      instance.style = attrs.get('style', instance.style)
      return instance

    return Snippet(**attrs)

class UserSerializer(serializers.HyperlinkedModelSerializer):
  snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail')

  class Meta:
    model = User
    fields = ('url', 'username', 'snippets')