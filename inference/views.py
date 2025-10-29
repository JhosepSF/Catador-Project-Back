from typing import Any, Dict, cast
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import AssessmentSerializer
from .services import predict_eval_senso, get_model

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
        try:
            model = get_model()
            info = {
                'model_class': type(model).__name__,
                'expected_features': ['pH', 'tipo', '% cacao'],
            }
            return Response(info)
        except Exception as e:
            return Response({'error': 'No se pudo cargar el modelo', 'detail': str(e)}, status=500)

class PredictView(APIView):
    authentication_classes: list = []
    permission_classes: list = []

    def post(self, request):
        ser = AssessmentSerializer(data=request.data)
        ser.is_valid(raise_exception=True)  # <- garantiza validated_data

        data = cast(Dict[str, Any], ser.validated_data)  # <- Pylance feliz
        cacao_type: str = cast(str, data['cacaoType'])
        ph: float = cast(float, data['ph'])
        purity: float = cast(float, data['purity_f'])

        try:
            pred = predict_eval_senso(cacao_type, ph, purity)
        except Exception as e:
            return Response({'error': 'Error durante la inferencia', 'detail': str(e)}, status=500)

        return Response({
            'prediction': pred,
            'input': {'cacaoType': cacao_type, 'phLevel': ph, 'purity': purity}
        })