import os
import uuid
from pathlib import Path
from typing import Optional
from fastapi import UploadFile, HTTPException
import firebase_admin
from firebase_admin import credentials, storage
from firebase_admin.exceptions import FirebaseError
from app.core.config import settings

class FirebaseService:
    """
    Servicio para manejar Firebase Storage
    """
    
    def __init__(self):
        self.bucket = None
        self._initialized = False
    
    def _initialize_firebase(self):
        """
        Inicializa Firebase Admin SDK
        """
        try:
            # Verificar si ya está inicializado
            if not firebase_admin._apps:
                # Configuración de Firebase
                firebase_config = {
                    "type": settings.FIREBASE_TYPE,
                    "project_id": settings.FIREBASE_PROJECT_ID,
                    "private_key_id": settings.FIREBASE_PRIVATE_KEY_ID,
                    "private_key": settings.FIREBASE_PRIVATE_KEY.replace("\\n", "\n") if settings.FIREBASE_PRIVATE_KEY else "",
                    "client_email": settings.FIREBASE_CLIENT_EMAIL,
                    "client_id": settings.FIREBASE_CLIENT_ID,
                    "auth_uri": settings.FIREBASE_AUTH_URI,
                    "token_uri": settings.FIREBASE_TOKEN_URI,
                    "auth_provider_x509_cert_url": settings.FIREBASE_AUTH_PROVIDER_X509_CERT_URL,
                    "client_x509_cert_url": settings.FIREBASE_CLIENT_X509_CERT_URL
                }
                
                # Verificar que el project_id esté configurado
                if not firebase_config["project_id"]:
                    print("⚠️ FIREBASE_PROJECT_ID no está configurado. Firebase Storage no estará disponible.")
                    return
                
                # Inicializar Firebase Admin SDK
                cred = credentials.Certificate(firebase_config)
                
                # Configurar bucket de almacenamiento
                storage_bucket = settings.FIREBASE_STORAGE_BUCKET or f"{firebase_config['project_id']}.appspot.com"
                
                firebase_admin.initialize_app(cred, {
                    'storageBucket': storage_bucket
                })
                
                # Obtener bucket
                try:
                    self.bucket = storage.bucket()
                    self._initialized = True
                    print("✅ Firebase Storage inicializado correctamente")
                except Exception as bucket_error:
                    print(f"⚠️ Error accediendo al bucket de Firebase: {bucket_error}")
                    print("⚠️ Firebase Storage no estará disponible. Las imágenes se guardarán como URLs.")
                    
        except Exception as e:
            print(f"❌ Error inicializando Firebase: {str(e)}")
            print("⚠️ Firebase Storage no estará disponible. Las imágenes se guardarán como URLs.")
    
    async def upload_image(self, file: UploadFile) -> Optional[str]:
        """
        Sube una imagen a Firebase Storage
        
        Args:
            file (UploadFile): Archivo de imagen a subir
            
        Returns:
            str: URL de la imagen subida o None si falla
        """
        try:
            # Inicializar Firebase si no está inicializado
            if not self._initialized:
                self._initialize_firebase()
            
            # Si Firebase no está disponible, retornar URL de placeholder
            if not self.bucket:
                print("⚠️ Firebase Storage no está disponible. Usando URL de placeholder.")
                return "https://via.placeholder.com/400x300/cccccc/666666?text=Imagen+no+disponible"
            
            # Validar tipo de archivo
            if not file.content_type or not file.content_type.startswith('image/'):
                raise HTTPException(
                    status_code=400,
                    detail="El archivo debe ser una imagen válida"
                )
            
            # Generar nombre único para el archivo
            file_extension = Path(file.filename).suffix if file.filename else '.jpg'
            unique_filename = f"mascotas/{uuid.uuid4()}{file_extension}"
            
            # Crear blob en Firebase Storage
            blob = self.bucket.blob(unique_filename)
            
            # Leer contenido del archivo
            content = await file.read()
            
            # Subir archivo
            blob.upload_from_string(
                content,
                content_type=file.content_type
            )
            
            # Hacer el archivo público
            blob.make_public()
            
            # Retornar URL pública
            image_url = blob.public_url
            print(f"✅ Imagen subida exitosamente: {image_url}")
            return image_url
            
        except FirebaseError as e:
            print(f"Error de Firebase: {str(e)}")
            return None
        except Exception as e:
            print(f"❌ Error subiendo imagen: {str(e)}")
            return None
    
    async def delete_image(self, image_url: str) -> bool:
        """
        Elimina una imagen de Firebase Storage
        
        Args:
            image_url (str): URL de la imagen a eliminar
            
        Returns:
            bool: True si se eliminó correctamente, False en caso contrario
        """
        try:
            # Si Firebase no está disponible, retornar False
            if not self.bucket:
                print("⚠️ Firebase Storage no está configurado. No se puede eliminar imagen.")
                return False
            
            # Extraer nombre del archivo de la URL
            if "firebasestorage.googleapis.com" in image_url:
                # URL de Firebase Storage
                path_start = image_url.find("/o/") + 3
                path_end = image_url.find("?")
                if path_end == -1:
                    path_end = len(image_url)
                
                file_path = image_url[path_start:path_end]
                file_path = file_path.replace("%2F", "/")
                
                # Eliminar archivo
                blob = self.bucket.blob(file_path)
                blob.delete()
                
                print(f"✅ Imagen eliminada exitosamente: {file_path}")
                return True
            else:
                print(f"⚠️ URL no es de Firebase Storage: {image_url}")
                return False
                
        except Exception as e:
            print(f"❌ Error eliminando imagen: {str(e)}")
            return False

# Instancia global del servicio
firebase_service = FirebaseService() 