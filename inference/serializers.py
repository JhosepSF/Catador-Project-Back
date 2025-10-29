from rest_framework import serializers

class AssessmentSerializer(serializers.Serializer):
    cacaoType = serializers.CharField()
    phLevel = serializers.CharField()
    purity = serializers.CharField()

    def validate(self, attrs):
        def to_float(val, field_name):
            s = str(val).strip().replace(',', '.')
            try:
                return float(s)
            except ValueError:
                raise serializers.ValidationError({field_name: 'Debe ser numérico.'})

        attrs['ph'] = to_float(attrs['phLevel'], 'phLevel')
        attrs['purity_f'] = to_float(attrs['purity'], 'purity')
        attrs['cacaoType'] = attrs['cacaoType'].strip()
        return attrs