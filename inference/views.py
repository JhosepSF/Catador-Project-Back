from typing import Any, Dict, cast
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import AssessmentSerializer
from .services import analyze_cacao_quality

class HealthView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        return Response({'status': 'ok'})

# inference/views.py
class ModelInfoView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        info = {
            'method': 'Fórmula fisicoquímica',
            'description': 'Cálculo de acidez basado en pH usando equilibrio ácido-base del ácido acético',
            'expected_features': ['pH'],
            'formula': 'C = [H+]²/Ka + [H+], donde Ka = 1.76×10⁻⁵',
            'ranges': {
                'defecto': 'pH < 4.4',
                'manteca': 'pH 4.4-5.2',
                'chocolate': 'pH 5.3-5.8',
                'subóptima': 'pH > 5.8'
            }
        }
        return Response(info)

class PredictView(APIView):
    authentication_classes: list = []
    permission_classes: list = []

    def post(self, request):
        ser = AssessmentSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        data = cast(Dict[str, Any], ser.validated_data)
        ph: float = cast(float, data['ph'])

        try:
            result = analyze_cacao_quality(ph)
        except Exception as e:
            return Response({
                'error': 'Error durante el análisis',
                'detail': str(e)
            }, status=500)

        return Response({
            'success': True,
            'input': {'phLevel': ph},
            'results': result
        })