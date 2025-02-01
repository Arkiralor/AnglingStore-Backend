from rest_framework.serializers import ModelSerializer
from middleware_app.models import RequestLog
from user_app.serializers import ShowUserSerializer


class RequestLogInputSerializer(ModelSerializer):

    class Meta:
        model = RequestLog
        fields = "__all__"

    def create(self, validated_data, *args, **kwargs):
        body_text = validated_data.get("body", "").decode('utf8', 'strict')
        validated_data["body_text"] = body_text if body_text else ""


class RequestLogOuputSerializer(ModelSerializer):
    user = ShowUserSerializer()

    class Meta:
        model = RequestLog
        fields = "__all__"
