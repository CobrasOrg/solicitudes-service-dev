from fastapi import APIRouter, HTTPException
from app.models.solicitud_mongo import SolicitudMongoModel
from app.services.firebase_service import firebase_service
from app.services.cloudinary_service import upload_image
import cloudinary.uploader

router = APIRouter()

@router.delete(
    "/{solicitud_id}",
    status_code=204,
    summary="Eliminar solicitud (Veterinaria)",
    description="Elimina una solicitud existente. Endpoint exclusivo para veterinarias.",
    responses={
        204: {
            "description": "Solicitud eliminada exitosamente"
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
async def delete_solicitud(solicitud_id: str):
    """
    Elimina una solicitud existente.
    Endpoint exclusivo para veterinarias.
    
    Args:
        solicitud_id (str): ID de la solicitud a eliminar
    
    Returns:
        None
        
    Raises:
        HTTPException: Si ocurre un error al procesar la solicitud o si la solicitud no existe
    """
    try:
        # Obtener la solicitud antes de eliminarla para acceder a la imagen
        solicitud = await SolicitudMongoModel.get_solicitud_by_id(solicitud_id)
        if not solicitud:
            raise HTTPException(
                status_code=404,
                detail="Solicitud no encontrada"
            )
        
        # Eliminar imagen de Cloudinary si existe
        if solicitud.foto_mascota:
            try:
                url = solicitud.foto_mascota
                public_id = url.split("/petmatch-solicitudes/")[-1].split(".")[0]
                cloudinary.uploader.destroy(f"petmatch-solicitudes/{public_id}")
            except Exception as e:
                print(f"Error eliminando imagen de Cloudinary: {str(e)}")
                # No fallar la eliminación de la solicitud si falla la eliminación de la imagen
        
        # Eliminar la solicitud
        if not await SolicitudMongoModel.delete_solicitud(solicitud_id):
            raise HTTPException(
                status_code=404,
                detail="Solicitud no encontrada"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Error interno del servidor al procesar la solicitud"
        ) 