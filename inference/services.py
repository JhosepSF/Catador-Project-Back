from pathlib import Path
from django.conf import settings
import threading
import joblib
import pandas as pd

_model = None
_lock = threading.Lock()

def _model_path() -> Path:
    return Path(settings.MODEL_PATH)

def get_model():
    global _model
    if _model is None:
        with _lock:
            if _model is None:
                mdl_path = _model_path()
                if not mdl_path.exists():
                    raise FileNotFoundError(f"No se encontró el modelo en: {mdl_path}")
            _model = joblib.load(mdl_path)
    return _model

def predict_eval_senso(cacao_type: str, ph: float, purity: float) -> float:
    """
    El pipeline fue entrenado con columnas: ['pH', 'tipo', '% cacao']
    """
    df = pd.DataFrame([
    {'pH': ph, 'tipo': cacao_type, '% cacao': purity}
    ])
    model = get_model()
    y_pred = model.predict(df)
    # asegurar float nativo para JSON
    return float(y_pred[0])