from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Body, Request
from app.schemas.solicitud import SolicitudUpdate, SolicitudEstadoUpdate, Solicitud
from app.models.solicitud_mongo import SolicitudMongoModel
from app.services.firebase_service import firebase_service
from app.constants.solicitudes import ESTADOS_PERMITIDOS
from typing import Optional, Union
import json

router = APIRouter()

@router.patch(
    "/{solicitud_id}",
    response_model=Solicitud,
    summary="Actualizar solicitud (JSON o Formulario)",
    description="Actualiza los datos de una solicitud existente. Acepta tanto JSON como datos de formulario. Solo se actualizan los campos enviados. Endpoint exclusivo para veterinarias.",
    responses={
        200: {
            "description": "Solicitud actualizada exitosamente",
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
                        "foto_mascota": "https://firebasestorage.googleapis.com/v0/b/project-id.appspot.com/o/mascotas%2Fnew-image.jpg"
                    }
                }
            }
        },
        400: {
            "description": "Datos inválidos o error en imagen",
            "content": {
                "application/json": {
                    "example": {"detail": "Datos de la solicitud inválidos o error en el archivo de imagen"}
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
async def update_solicitud(
    request: Request,
    solicitud_id: str,
    especie: Optional[str] = Form(None, description="Nueva especie de la mascota"),
    tipo_sangre: Optional[str] = Form(None, description="Nuevo tipo de sangre requerido"),
    urgencia: Optional[str] = Form(None, description="Nuevo nivel de urgencia"),
    peso_minimo: Optional[Union[float, str]] = Form(None, description="Nuevo peso mínimo requerido (en kg)"),
    descripcion_solicitud: Optional[str] = Form(None, description="Nueva descripción de la solicitud"),
    direccion: Optional[str] = Form(None, description="Nueva dirección de la veterinaria"),
    estado: Optional[str] = Form(None, description="Nuevo estado de la solicitud"),
    foto_mascota: Optional[UploadFile] = File(None, description="Nueva imagen de la mascota (opcional)")
):
    """
    Actualiza los datos de una solicitud existente.
    Acepta tanto JSON como datos de formulario.
    Solo se actualizan los campos enviados.
    Los campos vacíos o nulos son ignorados.
    Endpoint exclusivo para veterinarias.
    
    Args:
        solicitud_id (str): ID de la solicitud a actualizar
        especie (Optional[str]): Nueva especie de la mascota
        tipo_sangre (Optional[str]): Nuevo tipo de sangre requerido
        urgencia (Optional[str]): Nuevo nivel de urgencia
        peso_minimo (Optional[Union[float, str]]): Nuevo peso mínimo requerido
        descripcion_solicitud (Optional[str]): Nueva descripción de la solicitud
        direccion (Optional[str]): Nueva dirección
        estado (Optional[str]): Nuevo estado de la solicitud
        foto_mascota (Optional[UploadFile]): Nueva imagen de la mascota (opcional)
    
    Returns:
        Solicitud: Solicitud actualizada
        
    Raises:
        HTTPException: Si ocurre un error al procesar la solicitud
    """
    try:
        # Obtener la solicitud actual para manejar la imagen anterior
        solicitud_actual = await SolicitudMongoModel.get_solicitud_by_id(solicitud_id)
        if not solicitud_actual:
            raise HTTPException(
                status_code=404,
                detail="Solicitud no encontrada"
            )
        
        # Preparar datos de actualización
        update_data = {}
        
        # Manejar campos de formulario
        if especie is not None and especie != "":
            update_data["especie"] = especie
        if tipo_sangre is not None and tipo_sangre != "":
            update_data["tipo_sangre"] = tipo_sangre
        if urgencia is not None and urgencia != "":
            update_data["urgencia"] = urgencia
        if peso_minimo is not None and peso_minimo != "":
            # Convertir string a float si es necesario
            if isinstance(peso_minimo, str):
                try:
                    peso_minimo = float(peso_minimo)
                except ValueError:
                    raise HTTPException(
                        status_code=400,
                        detail="peso_minimo debe ser un número válido"
                    )
            update_data["peso_minimo"] = peso_minimo
        if descripcion_solicitud is not None and descripcion_solicitud != "":
            update_data["descripcion_solicitud"] = descripcion_solicitud
        if direccion is not None and direccion != "":
            update_data["direccion"] = direccion
        if estado is not None and estado != "":
            update_data["estado"] = estado
        
        # Manejar nueva imagen si se proporcionó
        if foto_mascota:
            # Eliminar imagen anterior si existe
            if solicitud_actual.foto_mascota:
                await firebase_service.delete_image(solicitud_actual.foto_mascota)
            
            # Subir nueva imagen
            nueva_foto_url = await firebase_service.upload_image(foto_mascota)
            if nueva_foto_url:
                update_data["foto_mascota"] = nueva_foto_url
        
        # Si no hay datos para actualizar, retornar la solicitud actual
        if not update_data:
            return solicitud_actual
        
        # Crear objeto de actualización
        solicitud_update = SolicitudUpdate(**update_data)
        
        # Actualizar la solicitud
        solicitud_actualizada = await SolicitudMongoModel.update_solicitud_datos(solicitud_id, solicitud_update)
        if not solicitud_actualizada:
            raise HTTPException(
                status_code=404,
                detail="Solicitud no encontrada"
            )
        
        return solicitud_actualizada
        
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Error interno del servidor al procesar la solicitud"
        )



@router.patch(
    "/{solicitud_id}/estado",
    response_model=Solicitud,
    summary="Actualizar estado de solicitud",
    description="Actualiza el estado de una solicitud existente. Endpoint exclusivo para veterinarias.",
    responses={
        200: {
            "description": "Estado de la solicitud actualizado exitosamente",
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
                        "estado": "Revision",
                        "foto_mascota": "https://ejemplo.com/foto-rocky.jpg"
                    }
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
async def update_solicitud_estado(solicitud_id: str, estado_update: SolicitudEstadoUpdate):
    """
    Actualiza el estado de una solicitud existente.
    Endpoint exclusivo para veterinarias.
    
    Args:
        solicitud_id (str): ID de la solicitud a actualizar
        estado_update (SolicitudEstadoUpdate): Nuevo estado de la solicitud
    
    Returns:
        Solicitud: Solicitud con estado actualizado
        
    Raises:
        HTTPException: Si ocurre un error al procesar la solicitud, si el estado es inválido o si la solicitud no existe
    """
    try:
        # Validar que el estado sea válido
        if estado_update.estado not in ESTADOS_PERMITIDOS:
            raise HTTPException(
                status_code=400,
                detail=f"Estado inválido. Los estados válidos son: {', '.join(ESTADOS_PERMITIDOS)}"
            )
        
        solicitud_actualizada = await SolicitudMongoModel.update_solicitud_estado(solicitud_id, estado_update.estado)
        if not solicitud_actualizada:
            raise HTTPException(
                status_code=404,
                detail="Solicitud no encontrada"
            )
        return solicitud_actualizada
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Error interno del servidor al procesar la solicitud"
        ) 