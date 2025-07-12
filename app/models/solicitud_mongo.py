from datetime import datetime
from typing import List, Optional, Dict
from bson import ObjectId
from app.schemas.solicitud import Solicitud, SolicitudCreate, SolicitudUpdate, SolicitudEstadoUpdate
from app.db.mongodb import mongodb
import json

class SolicitudMongoModel:
    collection_name = "solicitudes"
    
    @staticmethod
    def get_collection():
        """Obtiene la colección de solicitudes"""
        if mongodb.database is None:
            raise Exception("MongoDB no está conectado")
        return mongodb.database[SolicitudMongoModel.collection_name]
    
    @staticmethod
    def _convert_mongo_doc_to_schema(doc: Dict) -> Dict:
        """Convierte un documento de MongoDB al formato del esquema Pydantic"""
        if doc and "_id" in doc:
            doc["id"] = str(doc["_id"])
            del doc["_id"]
        return doc
    
    @staticmethod
    async def get_active_solicitudes() -> List[Solicitud]:
        """
        Get all active solicitations from MongoDB
        Returns:
            List[Solicitud]: List of active solicitations
        """
        collection = SolicitudMongoModel.get_collection()
        cursor = collection.find({"estado": "Activa"})
        solicitudes = await cursor.to_list(length=None)
        return [Solicitud(**SolicitudMongoModel._convert_mongo_doc_to_schema(solicitud)) for solicitud in solicitudes]

    @staticmethod
    async def get_all_solicitudes() -> List[Solicitud]:
        """
        Get all solicitations from MongoDB
        Returns:
            List[Solicitud]: List of all solicitations
        """
        collection = SolicitudMongoModel.get_collection()
        cursor = collection.find({})
        solicitudes = await cursor.to_list(length=None)
        return [Solicitud(**SolicitudMongoModel._convert_mongo_doc_to_schema(solicitud)) for solicitud in solicitudes]

    @staticmethod
    async def get_solicitudes_by_status(estado: Optional[str] = None) -> List[Solicitud]:
        """
        Get solicitations filtered by status from MongoDB
        Args:
            estado (Optional[str]): Status to filter by ('Activa', 'Completada', 'Cancelada', 'Revision')
        Returns:
            List[Solicitud]: List of solicitations matching the status
        """
        collection = SolicitudMongoModel.get_collection()
        if estado:
            cursor = collection.find({"estado": estado})
        else:
            cursor = collection.find({})
        solicitudes = await cursor.to_list(length=None)
        return [Solicitud(**SolicitudMongoModel._convert_mongo_doc_to_schema(solicitud)) for solicitud in solicitudes]

    @staticmethod
    async def filter_active_solicitudes(
        especie: Optional[str] = None,
        tipo_sangre: Optional[str] = None,
        urgencia: Optional[str] = None,
        localidad: Optional[str] = None
    ) -> List[Solicitud]:
        """
        Filter active solicitations by multiple parameters from MongoDB
        Args:
            especie (Optional[str]): Especie to filter by
            tipo_sangre (Optional[str]): Tipo de sangre to filter by
            urgencia (Optional[str]): Urgencia to filter by
            localidad (Optional[str]): Localidad to filter by
        Returns:
            List[Solicitud]: List of active solicitations matching all provided filters
        """
        collection = SolicitudMongoModel.get_collection()
        
        # Construir filtro
        filter_query = {"estado": "Activa"}
        
        if especie:
            filter_query["especie"] = {"$regex": especie, "$options": "i"}
        if tipo_sangre:
            filter_query["tipo_sangre"] = {"$regex": tipo_sangre, "$options": "i"}
        if urgencia:
            filter_query["urgencia"] = {"$regex": urgencia, "$options": "i"}
        if localidad:
            filter_query["localidad"] = {"$regex": localidad, "$options": "i"}
        
        cursor = collection.find(filter_query)
        solicitudes = await cursor.to_list(length=None)
        return [Solicitud(**SolicitudMongoModel._convert_mongo_doc_to_schema(solicitud)) for solicitud in solicitudes]

    @staticmethod
    async def create_solicitud(solicitud_data: Dict) -> Solicitud:
        """
        Create a new solicitation in MongoDB
        Args:
            solicitud_data (Dict): Solicitation data
        Returns:
            Solicitud: Created solicitation
        """
        collection = SolicitudMongoModel.get_collection()
        
        # Agregar campos por defecto si no están presentes
        from datetime import datetime
        
        # Crear una copia para no modificar el original
        data_to_insert = solicitud_data.copy()
        
        # Agregar estado por defecto si no está presente
        if "estado" not in data_to_insert:
            data_to_insert["estado"] = "Activa"
        
        # Agregar fecha de creación si no está presente
        if "fecha_creacion" not in data_to_insert:
            data_to_insert["fecha_creacion"] = datetime.now()
        
        # Convertir string ID a ObjectId si es necesario
        if "id" in data_to_insert and isinstance(data_to_insert["id"], str):
            data_to_insert["_id"] = ObjectId(data_to_insert["id"])
            del data_to_insert["id"]
        
        result = await collection.insert_one(data_to_insert)
        
        # Obtener el documento insertado
        inserted_doc = await collection.find_one({"_id": result.inserted_id})
        
        # Convertir ObjectId a string para el esquema
        converted_doc = SolicitudMongoModel._convert_mongo_doc_to_schema(inserted_doc)
        
        return Solicitud(**converted_doc)

    @staticmethod
    async def delete_solicitud(solicitud_id: str) -> bool:
        """
        Delete a solicitation by ID from MongoDB
        Args:
            solicitud_id (str): ID of the solicitation to delete
        Returns:
            bool: True if deleted, False if not found
        """
        collection = SolicitudMongoModel.get_collection()
        
        try:
            object_id = ObjectId(solicitud_id)
            result = await collection.delete_one({"_id": object_id})
            return result.deleted_count > 0
        except Exception:
            return False

    @staticmethod
    async def update_solicitud_estado(solicitud_id: str, estado: str) -> Optional[Solicitud]:
        """
        Update solicitation status in MongoDB
        Args:
            solicitud_id (str): ID of the solicitation
            estado (str): New status
        Returns:
            Optional[Solicitud]: Updated solicitation if found, None otherwise
        """
        collection = SolicitudMongoModel.get_collection()
        
        try:
            object_id = ObjectId(solicitud_id)
            result = await collection.update_one(
                {"_id": object_id},
                {"$set": {"estado": estado}}
            )
            
            if result.modified_count > 0:
                # Obtener el documento actualizado
                updated_doc = await collection.find_one({"_id": object_id})
                if updated_doc:
                    # Convertir ObjectId a string para el esquema
                    converted_doc = SolicitudMongoModel._convert_mongo_doc_to_schema(updated_doc)
                    return Solicitud(**converted_doc)
            
            return None
        except Exception:
            return None

    @staticmethod
    async def update_solicitud_datos(solicitud_id: str, solicitud_update: SolicitudUpdate) -> Optional[Solicitud]:
        """
        Update solicitation data in MongoDB
        Args:
            solicitud_id (str): ID of the solicitation
            solicitud_update (SolicitudUpdate): Updated solicitation data
        Returns:
            Optional[Solicitud]: Updated solicitation if found, None otherwise
        """
        collection = SolicitudMongoModel.get_collection()
        
        try:
            object_id = ObjectId(solicitud_id)
            update_data = solicitud_update.model_dump(exclude_unset=True)
            
            result = await collection.update_one(
                {"_id": object_id},
                {"$set": update_data}
            )
            
            if result.modified_count > 0:
                # Obtener el documento actualizado
                updated_doc = await collection.find_one({"_id": object_id})
                if updated_doc:
                    # Convertir ObjectId a string para el esquema
                    converted_doc = SolicitudMongoModel._convert_mongo_doc_to_schema(updated_doc)
                    return Solicitud(**converted_doc)
            
            return None
        except Exception:
            return None

    @staticmethod
    async def filter_solicitudes_by_status(
        estado: Optional[str] = None,
        especie: Optional[str] = None,
        tipo_sangre: Optional[str] = None,
        urgencia: Optional[str] = None,
        localidad: Optional[str] = None
    ) -> List[Solicitud]:
        """
        Filter solicitations by multiple parameters from MongoDB
        Args:
            estado (Optional[str]): Status to filter by
            especie (Optional[str]): Especie to filter by
            tipo_sangre (Optional[str]): Tipo de sangre to filter by
            urgencia (Optional[str]): Urgencia to filter by
            localidad (Optional[str]): Localidad to filter by
        Returns:
            List[Solicitud]: List of solicitations matching all provided filters
        """
        collection = SolicitudMongoModel.get_collection()
        
        # Construir filtro
        filter_query = {}
        
        if estado:
            filter_query["estado"] = {"$regex": estado, "$options": "i"}
        if especie:
            filter_query["especie"] = {"$regex": especie, "$options": "i"}
        if tipo_sangre:
            filter_query["tipo_sangre"] = {"$regex": tipo_sangre, "$options": "i"}
        if urgencia:
            filter_query["urgencia"] = {"$regex": urgencia, "$options": "i"}
        if localidad:
            filter_query["localidad"] = {"$regex": localidad, "$options": "i"}
        
        cursor = collection.find(filter_query)
        solicitudes = await cursor.to_list(length=None)
        return [Solicitud(**SolicitudMongoModel._convert_mongo_doc_to_schema(solicitud)) for solicitud in solicitudes]

    @staticmethod
    async def get_solicitud_by_id(solicitud_id: str) -> Optional[Solicitud]:
        """
        Get a solicitation by ID from MongoDB
        Args:
            solicitud_id (str): ID of the solicitation
        Returns:
            Optional[Solicitud]: Solicitation if found, None otherwise
        """
        collection = SolicitudMongoModel.get_collection()
        
        try:
            object_id = ObjectId(solicitud_id)
            solicitud = await collection.find_one({"_id": object_id})
            
            if solicitud:
                # Convertir ObjectId a string para el esquema
                converted_doc = SolicitudMongoModel._convert_mongo_doc_to_schema(solicitud)
                return Solicitud(**converted_doc)
            
            return None
        except Exception:
            return None

    @staticmethod
    async def migrate_from_mock_data():
        """
        Migrate data from mock_data.json to MongoDB
        """
        try:
            collection = SolicitudMongoModel.get_collection()
            
            # Verificar si ya hay datos
            count = await collection.count_documents({})
            if count > 0:
                print(f"⚠️ La base de datos ya contiene {count} registros. Saltando migración.")
                return
            
            # Leer datos del archivo JSON
            with open("app/data/mock_data.json", "r", encoding="utf-8") as file:
                data = json.load(file)
            
            solicitudes = data.get("solicitudes", [])
            
            if not solicitudes:
                print("⚠️ No se encontraron datos para migrar.")
                return
            
            # Convertir IDs string a ObjectId
            for solicitud in solicitudes:
                if "id" in solicitud and isinstance(solicitud["id"], str):
                    solicitud["_id"] = ObjectId(solicitud["id"])
                    del solicitud["id"]
            
            # Insertar datos
            result = await collection.insert_many(solicitudes)
            print(f"✅ Migrados {len(result.inserted_ids)} registros a MongoDB")
            
        except Exception as e:
            print(f"❌ Error durante la migración: {e}")
            # No lanzar excepción para evitar que falle el startup 