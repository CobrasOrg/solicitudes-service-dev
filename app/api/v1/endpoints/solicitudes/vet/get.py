from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.schemas.solicitud import Solicitud
from app.models.solicitud_mongo import SolicitudMongoModel
from app.constants.solicitudes import ESTADOS_PERMITIDOS

router = APIRouter()

@router.get(
    "/",
    response_model=List[Solicitud],
    summary="Obtener todas las solicitudes (Veterinaria)",
    description="Retorna todas las solicitudes independientemente de su estado. Endpoint exclusivo para veterinarias.",
    responses={
        200: {
            "description": "Lista de todas las solicitudes",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": "684a01e4c351aa9d49b145b8",
                            "nombre_veterinaria": "Veterinaria San Patricio",
                            "nombre_mascota": "Rocky",
                            "especie": "Perro",
                            "localidad": "Suba",
                            "descripcion_solicitud": "Rocky es un pastor alemán de 5 años que ha sido diagnosticado con anemia severa después de una complicación durante una cirugía de emergencia.",
                            "direccion": "Clínica VetCentral, Av. Principal 123",
                            "ubicacion": "Suba, Bogotá",
                            "contacto": "+57 300 123 4567",
                            "peso_minimo": 25,
                            "tipo_sangre": "DEA 1.1+",
                            "fecha_creacion": "2024-02-14T10:30:00",
                            "urgencia": "Alta",
                            "estado": "Activa",
                            "foto_mascota": "https://ejemplo.com/foto-rocky.jpg"
                        }
                    ]
                }
            }
        },
        500: {
            "description": "Error interno del servidor",
            "content": {
                "application/json": {
                    "example": {"detail": "Error interno del servidor al procesar la solicitud"}
                }
            }
        }
    }
)
async def get_all_solicitudes():
    """
    Obtiene todas las solicitudes independientemente de su estado.
    Endpoint exclusivo para veterinarias.
    
    Returns:
        List[Solicitud]: Lista de todas las solicitudes
        
    Raises:
        HTTPException: Si ocurre un error al procesar la solicitud
    """
    try:
        return await SolicitudMongoModel.get_all_solicitudes()
    except Exception as e:
        print(f"Error en get_all_solicitudes: {str(e)}")  # Para debugging
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener las solicitudes: {str(e)}"
        )

@router.get(
    "/filtrar",
    response_model=List[Solicitud],
    summary="Filtrar solicitudes por estado (Veterinaria)",
    description="Retorna las solicitudes filtradas por estado. Endpoint exclusivo para veterinarias.",
    responses={
        200: {
            "description": "Lista de solicitudes filtradas",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": "684a01e4c351aa9d49b145b8",
                            "nombre_veterinaria": "Veterinaria San Patricio",
                            "nombre_mascota": "Rocky",
                            "especie": "Perro",
                            "localidad": "Suba",
                            "descripcion_solicitud": "Rocky es un pastor alemán de 5 años que ha sido diagnosticado con anemia severa después de una complicación durante una cirugía de emergencia.",
                            "direccion": "Clínica VetCentral, Av. Principal 123",
                            "ubicacion": "Suba, Bogotá",
                            "contacto": "+57 300 123 4567",
                            "peso_minimo": 25,
                            "tipo_sangre": "DEA 1.1+",
                            "fecha_creacion": "2024-02-14T10:30:00",
                            "urgencia": "Alta",
                            "estado": "Activa",
                            "foto_mascota": "https://ejemplo.com/foto-rocky.jpg"
                        }
                    ]
                }
            }
        },
        400: {
            "description": "Estado inválido",
            "content": {
                "application/json": {
                    "example": {"detail": f"Estado inválido. Los estados válidos son: {', '.join(ESTADOS_PERMITIDOS)}"}
                }
            }
        },
        500: {
            "description": "Error interno del servidor",
            "content": {
                "application/json": {
                    "example": {"detail": "Error interno del servidor al procesar la solicitud"}
                }
            }
        }
    }
)
async def get_solicitudes_by_status(
    estado: Optional[str] = Query(
        default=None,
        description="Estado de las solicitudes a filtrar",
        examples=["Activa"],
        enum=ESTADOS_PERMITIDOS + [""]  # Permitir estado vacío
    ),
    especie: Optional[str] = Query(
        None,
        description="Filtrar por especie (ej: Perro, Gato). Múltiples valores separados por coma: Perro,Gato",
        examples={"value": "Perro", "multiple": "Perro,Gato"}
    ),
    tipo_sangre: Optional[str] = Query(
        None,
        description="Filtrar por tipo de sangre (ej: DEA 1.1+, A). Múltiples valores separados por coma: DEA 1.1+,A",
        examples={"value": "DEA 1.1+", "multiple": "DEA 1.1+,A"}
    ),
    urgencia: Optional[str] = Query(
        None,
        description="Filtrar por nivel de urgencia (Alta, Media). Múltiples valores separados por coma: Alta,Media",
        examples={"value": "Alta", "multiple": "Alta,Media"}
    ),
    localidad: Optional[str] = Query(
        None,
        description="Filtrar por localidad (ej: Suba, Chapinero). Múltiples valores separados por coma: Suba,Teusaquillo",
        examples={"value": "Suba", "multiple": "Suba,Teusaquillo"}
    )
):
    """
    Obtiene las solicitudes filtradas por estado y otros criterios.
    Endpoint exclusivo para veterinarias.
    
    Args:
        estado (Optional[str]): Estado de las solicitudes a filtrar (un solo valor)
        especie (Optional[str]): Especie a filtrar. Múltiples valores separados por coma: "Perro,Gato"
        tipo_sangre (Optional[str]): Tipo de sangre a filtrar. Múltiples valores separados por coma: "DEA 1.1+,A"
        urgencia (Optional[str]): Nivel de urgencia a filtrar. Múltiples valores separados por coma: "Alta,Media"
        localidad (Optional[str]): Localidad a filtrar. Múltiples valores separados por coma: "Suba,Teusaquillo"
    
    Returns:
        List[Solicitud]: Lista de solicitudes que coinciden con los filtros
        
    Raises:
        HTTPException: Si ocurre un error al procesar la solicitud o si el estado es inválido
        
    Examples:
        - Filtrar por estado y especie: ?estado=Activa&especie=Perro
        - Filtrar por múltiples localidades: ?estado=Activa&localidad=Suba,Teusaquillo
        - Filtrar por múltiples criterios: ?estado=Activa&especie=Perro,Gato&localidad=Suba,Chapinero&urgencia=Alta,Media
    """
    try:
        if estado and estado.strip():  # Verificar que el estado no esté vacío después de quitar espacios
            # Normalizar el estado: primera letra mayúscula, resto minúscula
            estado_normalizado = estado.title()
            
            if estado_normalizado not in ESTADOS_PERMITIDOS:
                raise HTTPException(
                    status_code=400,
                    detail=f"Estado inválido. Los estados válidos son: {', '.join(ESTADOS_PERMITIDOS)}"
                )
            estado = estado_normalizado
        else:
            estado = None  # Si el estado está vacío, establecerlo como None
        
        solicitudes = await SolicitudMongoModel.filter_solicitudes_by_status(
            estado=estado,
            especie=especie,
            tipo_sangre=tipo_sangre,
            urgencia=urgencia,
            localidad=localidad
        )
        return solicitudes
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Error interno del servidor al procesar la solicitud"
        )

@router.get(
    "/{solicitud_id}",
    response_model=Solicitud,
    summary="Obtener una solicitud específica (Veterinaria)",
    description="Retorna una solicitud específica por su ID. Endpoint exclusivo para veterinarias.",
    responses={
        200: {
            "description": "Solicitud encontrada",
            "content": {
                "application/json": {
                    "example": {
                        "id": "684a01e4c351aa9d49b145b8",
                        "nombre_veterinaria": "Veterinaria San Patricio",
                        "nombre_mascota": "Rocky",
                        "especie": "Perro",
                        "localidad": "Suba",
                        "descripcion_solicitud": "Rocky es un pastor alemán de 5 años que ha sido diagnosticado con anemia severa después de una complicación durante una cirugía de emergencia.",
                        "direccion": "Clínica VetCentral, Av. Principal 123",
                        "ubicacion": "Suba, Bogotá",
                        "contacto": "+57 300 123 4567",
                        "peso_minimo": 25,
                        "tipo_sangre": "DEA 1.1+",
                        "fecha_creacion": "2024-02-14T10:30:00",
                        "urgencia": "Alta",
                        "estado": "Activa",
                        "foto_mascota": "https://ejemplo.com/foto-rocky.jpg"
                    }
                }
            }
        },
        404: {
            "description": "Solicitud no encontrada",
            "content": {
                "application/json": {
                    "example": {"detail": "Solicitud no encontrada"}
                }
            }
        },
        500: {
            "description": "Error interno del servidor",
            "content": {
                "application/json": {
                    "example": {"detail": "Error interno del servidor al procesar la solicitud"}
                }
            }
        }
    }
)
async def get_solicitud_by_id(solicitud_id: str):
    """
    Obtiene una solicitud específica por su ID.
    Endpoint exclusivo para veterinarias.
    
    Args:
        solicitud_id (str): ID de la solicitud a obtener
    
    Returns:
        Solicitud: Solicitud encontrada
        
    Raises:
        HTTPException: Si la solicitud no existe o ocurre un error
    """
    try:
        solicitud = await SolicitudMongoModel.get_solicitud_by_id(solicitud_id)
        if not solicitud:
            raise HTTPException(
                status_code=404,
                detail="Solicitud no encontrada"
            )
        return solicitud
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Error interno del servidor al procesar la solicitud"
        ) 