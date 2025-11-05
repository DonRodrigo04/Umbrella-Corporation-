import logging
from typing import Dict, Any

# Configurar logger
logger = logging.getLogger("Normalizer")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(name)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

def normalize_data(raw_data: Dict[str, Any], data_type: str) -> Dict[str, Any]:
    """
    Normaliza datos crudos según el tipo de flujo (genético, bioquímico, físico).
    Valida rangos y registra errores si los datos son inconsistentes.
    """
    normalized = {"sample_id": raw_data.get("sample_id", "UNKNOWN")}

    try:
        if data_type == "genetico":
            sequence = raw_data.get("sequence", "").upper()
            quality = float(raw_data.get("quality", 0.0))

            # Validación de calidad
            if not (0.0 <= quality <= 1.0):
                logger.error(f"Calidad fuera de rango: {quality} (sample_id={normalized['sample_id']})")

            normalized.update({"sequence": sequence, "quality": quality})

        elif data_type == "bioquimico":
            ph = float(raw_data.get("ph", 7.0))
            enzyme_activity = float(raw_data.get("enzyme_activity", 0.0))

            # Validación de pH (rango fisiológico aproximado)
            if not (6.5 <= ph <= 8.0):
                logger.warning(f"pH fuera de rango: {ph} (sample_id={normalized['sample_id']})")

            normalized.update({"ph": ph, "enzyme_activity": enzyme_activity})

        elif data_type == "fisico":
            temperature = float(raw_data.get("temperature", 0.0))
            pressure = float(raw_data.get("pressure", 0.0))

            # Validación de temperatura y presión (rangos típicos)
            if not (30.0 <= temperature <= 40.0):
                logger.warning(f"Temperatura fuera de rango: {temperature} (sample_id={normalized['sample_id']})")
            if not (90.0 <= pressure <= 110.0):
                logger.warning(f"Presión fuera de rango: {pressure} (sample_id={normalized['sample_id']})")

            normalized.update({"temperature": temperature, "pressure": pressure})

        else:
            raise ValueError(f"Tipo de dato no soportado: {data_type}")

    except (ValueError, TypeError) as e:
        logger.error(f"Error al normalizar datos: {e} (raw_data={raw_data})")

    return normalized