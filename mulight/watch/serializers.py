from rest_framework import serializers
from watch.models import Watch



class WatchSerializer(serializers.ModelSerializer):
    # Not used in this case, but good to keep the architecture complete.

    class Meta:
        model = Watch
        fields = "__all__"
