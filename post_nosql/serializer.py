import abc

from bson import ObjectId

from account.models import User
from account.serializers import UserSerializer
from .models import *


class BASESERIALIZER:
    def __init__(self,data , many=False) -> None:
        self.data = data
        self.many = many   
    
    def get_serialized_data(self):
        objs = list()
        if self.many  :        
            for obj in self.data:
                obj = self._retrieveNested_document(obj)
                objs.append(obj)
        else:
            self.data = self._retrieveNested_document(self.data)
            objs.append(self.data)
        
        return objs     
    
    @abc.abstractmethod
    def _retrieveNested_document(self , obj):
        pass


class PostRetrieveSerializer(BASESERIALIZER):   


    
    def _retrieveNested_document(self , obj):
        
        #rerieve attachments

        objects_attachments = Attatchment.read_query({'_id': {'$in': [ObjectId(id) for id in obj['attachments'] ] }})
        objects_comments  = Comment.read_query({'_id': {'$in': [ObjectId(id) for id in obj['comments'][:10] ] }})
 
        
        obj['attachments'] = objects_attachments 
        obj['comments'] = objects_comments 
        return obj
    
    
class PostCreateSerializer(BASESERIALIZER):
    pass
      
class CommentSerializer(BASESERIALIZER):

 
    
    def _retrieveNested_document(self , obj):

        return obj
    
class likeDetailSerilizer(BASESERIALIZER):
        
    def _retrieveNested_document(self , obj):
        
        user = User.objects.get(id=obj['created_by'])    
            
        obj['created_by'] = UserSerializer(user).data
        return obj