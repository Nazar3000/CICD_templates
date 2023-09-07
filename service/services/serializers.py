from rest_framework import serializers
from services.models import Plan
from services.models import Subscription


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = "__all__"


class SubscriptionSerializer(serializers.ModelSerializer):
    plan = PlanSerializer()
    client_name = serializers.CharField(source="client.company_name")
    email = serializers.CharField(source="client.user.email")
    price = serializers.SerializerMethodField()

    def get_price(self, istance):
        return istance.price

    class Meta:
        model = Subscription
        fields = ("id", "plan_id", "client_name", "email", "plan", "price", "price2")
