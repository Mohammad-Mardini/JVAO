from rest_framework import serializers
from .models import JinaBase

class JinabaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = JinaBase
        fields = ['x_value', 'y_value']
        
