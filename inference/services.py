import math
from typing import Dict, Any

# Constante de disociación del ácido acético a 25°C
KA_ACETIC_ACID = 1.76e-5

# Peso molecular del ácido acético (g/mol)
MW_ACETIC_ACID = 60.0

def calculate_acidity_from_ph(ph: float) -> float:
    """
    Calcula la concentración de ácido acético (mol/L) a partir del pH.
    
    Fórmula: C = [H+]²/Ka + [H+]
    Donde:
    - [H+] = 10^(-pH)
    - Ka = 1.76 × 10^(-5) (constante de disociación del ácido acético)
    
    Args:
        ph: Valor de pH medido
        
    Returns:
        Concentración de ácido acético en mol/L
    """
    h_concentration = math.pow(10, -ph)
    concentration = (h_concentration ** 2) / KA_ACETIC_ACID + h_concentration
    return concentration

def acidity_to_percentage(concentration_mol_l: float) -> float:
    """
    Convierte la concentración de ácido acético de mol/L a porcentaje (% w/v).
    
    Fórmula: % = (C × 60) × 100
    Donde 60 es el peso molecular del ácido acético
    
    Se multiplica por factor adicional para reflejar concentración en muestra original
    ya que las mediciones de pH típicamente se hacen en suspensión diluida.
    
    Args:
        concentration_mol_l: Concentración en mol/L
        
    Returns:
        Porcentaje de ácido acético (% w/v)
    """
    # C (mol/L) × 60 (g/mol) = g/L
    # Multiplicado por factor para ajustar a muestra original (típicamente 20x dilución)
    percentage = (concentration_mol_l * MW_ACETIC_ACID) * 100 * 20
    return percentage

def classify_cacao_by_ph(ph: float, acidity_percentage: float) -> Dict[str, Any]:
    """
    Clasifica el cacao según el pH y determina su uso recomendado.
    
    Rangos:
    - pH < 4.4: Acidez muy alta - No recomendado (posible defecto)
    - pH 4.4-5.2: Alta acidez (>0.7-1.5%) - Recomendado para MANTECA DE CACAO
    - pH 5.3-5.8: Acidez moderada (0.5-0.7%) - Recomendado para CHOCOLATE
    - pH > 5.8: Acidez baja - Calidad subóptima (posible defecto de fermentación)
    
    Args:
        ph: Valor de pH
        acidity_percentage: Porcentaje de acidez
        
    Returns:
        Diccionario con clasificación, uso recomendado y descripción
    """
    if ph < 4.4:
        return {
            'classification': 'Acidez muy alta',
            'recommended_use': 'No recomendado',
            'quality': 'defecto',
            'description': 'pH muy bajo indica posible sobrefermentación o defecto en el proceso. No apto para productos de calidad.',
            'ph_range': '< 4.4',
            'acidity_range': f'> 1.5% (medido: {acidity_percentage:.2f}%)'
        }
    elif 4.4 <= ph <= 5.2:
        return {
            'classification': 'Alta acidez',
            'recommended_use': 'Manteca de cacao',
            'quality': 'aceptable',
            'description': 'Acidez elevada, ideal para prensado y extracción de manteca. La manteca es neutra en sabor.',
            'ph_range': '4.4 - 5.2',
            'acidity_range': f'0.7 - 1.5% (medido: {acidity_percentage:.2f}%)'
        }
    elif 5.3 <= ph <= 5.8:
        return {
            'classification': 'Acidez equilibrada',
            'recommended_use': 'Chocolate premium',
            'quality': 'excelente',
            'description': 'Perfil de sabor equilibrado, ideal para chocolate de alta calidad. Notas frutales y complejas.',
            'ph_range': '5.3 - 5.8',
            'acidity_range': f'0.5 - 0.7% (medido: {acidity_percentage:.2f}%)'
        }
    else:  # ph > 5.8
        return {
            'classification': 'Acidez baja',
            'recommended_use': 'Cacao alcalizado o mezclas industriales',
            'quality': 'subóptima',
            'description': 'pH alto indica subfermentación. Sabor plano sin notas complejas, mayor astringencia. Puede usarse para proceso alcalino (Dutch), coberturas industriales o mezclas de bajo costo.',
            'ph_range': '> 5.8',
            'acidity_range': f'< 0.5% (medido: {acidity_percentage:.2f}%)'
        }

def analyze_cacao_quality(ph: float) -> Dict[str, Any]:
    """
    Función principal que analiza la calidad del cacao basándose únicamente en el pH.
    
    Args:
        ph: Valor de pH del licor de cacao
        
    Returns:
        Diccionario con todos los resultados del análisis
    """
    # Calcular concentración de ácido acético
    acidity_mol_l = calculate_acidity_from_ph(ph)
    
    # Convertir a porcentaje
    acidity_percentage = acidity_to_percentage(acidity_mol_l)
    
    # Clasificar el cacao
    classification_result = classify_cacao_by_ph(ph, acidity_percentage)
    
    return {
        'ph': ph,
        'acidity_concentration_mol_l': round(acidity_mol_l, 6),
        'acidity_percentage': round(acidity_percentage, 3),
        **classification_result
    }