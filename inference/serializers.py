from rest_framework import serializers

class AssessmentSerializer(serializers.Serializer):
    phLevel = serializers.CharField()

    def validate(self, attrs):
        def to_float(val, field_name):
            s = str(val).strip().replace(',', '.')
            try:
                return float(s)
            except ValueError:
                raise serializers.ValidationError({field_name: 'Debe ser numérico.'})

        attrs['ph'] = to_float(attrs['phLevel'], 'phLevel')
        
        # Validar rango de pH (típicamente 3.0 - 7.0 para cacao)
        if not (3.0 <= attrs['ph'] <= 7.0):
            raise serializers.ValidationError({
                'phLevel': 'El pH debe estar entre 3.0 y 7.0'
            })
        
        return attrs