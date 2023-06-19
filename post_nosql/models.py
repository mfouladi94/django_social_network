import json
from django.db import models
from django_social_network import settings
from django_social_network.settings import MONGODB
from pymongo import *
from bson import ObjectId
from bson.json_util import dumps
from utils.mongodbManager import *
import datetime
from django.utils.timesince import timesince


class NosqlCollection:

    def __init__(self, collectionName):
        self.collection = get_collection(collectionName)

    def get(self):
        return self.collection


class NosqlCRUD:

    collectionName = None
    
    def __init__(self) -> None:
        self.collection = get_collection(self.collectionName)

    #########################
    # UPDATE
    #########################

    def update_query(self, query: dict):
        '''
        update object by query dictionary
        '''
        result = self.collection.update_one({"_id": ObjectId(self.id)}, query)
        return result.modified_count > 0

    def update_partial_set(self, values: dict):
        '''
        update object by specific values dictionary
        '''
        result = self.collection.update_one({"_id": ObjectId(self.id)},
                                            {"$set":  self._remove_IDS(values)})
        return result.modified_count > 0

    def update(self):

        if self.collection.count_documents({'_id': ObjectId(self.id)}):
            self.collection.update_one({"_id": ObjectId(self.id)},
                                       {"$set":  self._remove_IDS(self.dump_to_dic())})
        else:
            self.create()

    #########################
    # DELETE
    #########################

    def remove(self):

        
        self.collection.delete_one({"_id": ObjectId(self.id) })

    @classmethod
    def remove_query(cls, query):
        '''
        remove objs based on query 
        '''
        self = cls()
        self.collection.deleteMany(query)

    #########################
    # READ
    #########################

    @classmethod
    def read_query(cls, query={}):
        self = cls()
        objects = self.collection.find(query)
        return [self._convert_document(doc) for doc in objects]

    @classmethod
    def read_query_pagination(cls, query={}, offset=1, count=settings.DEFAULT_PER_PAGE):
        self = cls()

        objects = self.collection.find(query).sort(
            "_id", -1).skip((offset-1)*settings.DEFAULT_PER_PAGE).limit(count)

        return [self._convert_document(doc) for doc in objects]

    @classmethod
    def read_all(cls):
        self = cls()
        cursor = self.collection.find()
        return [self._convert_document(doc) for doc in cursor]

    @classmethod
    def read_all_pagination(cls, offset=0, count=settings.DEFAULT_PER_PAGE):
        self = cls()
        cursor = self.collection.find().sort("_id", -1).skip(offset).limit(count)
        return [self._convert_document(doc) for doc in cursor]

    @classmethod
    def read_one(cls, query: dict):
        self = cls()
        cursor = self.collection.find_one(query)
        return self._convert_document(cursor)

    #########################
    # CREATE
    #########################
    def create(self):

        data = self._remove_IDS(self.dump_to_dic())
        result = self.collection.insert_one(data)
        self.id = str(result.inserted_id)
        return self.id

    #########################
    # UTILS
    #########################

    def dump_to_dic(self):
        data = self.__dict__.copy()
        if 'collection' in data.keys():
            data.pop('collection')
        return data

    def _convert_document(self, doc):
        if doc is not None:
            doc["id"] = str(doc["_id"] )
        return doc

    def _remove_IDS(self, data):
        if 'id' in data.keys():
            del data['id']
        if '_id' in data.keys():
            del data['_id']

        return data

    def dumps_json(self):
        return dumps(self.dump_to_dic())


class Post(NosqlCRUD):

    collectionName = "post"
    

    @classmethod
    def construt(cls, body, is_private, created_by, likes_count=0, comments_count=0, attachments=list(), likes=list()):
        self = cls()
        self.body = body
        self.is_private = is_private
        self.created_by = created_by
        self.likes_count = likes_count
        self.comments_count = comments_count
        self.attachments = attachments
        self.likes = list()
        self.comments = list()
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        return self

    def load_bson(self, obj):
        self.id = str(obj.get('_id'))
        self.body = obj["body"]
        self.is_private = obj["is_private"]
        self.created_by = obj["created_by"]
        self.likes_count = obj["likes_count"]
        self.comments_count = obj["comments_count"]
        self.attachments = obj["attachments"]
        self.likes = obj["likes"]
        self.comments = obj["comments"]
        self.created_at = obj["created_at"]
        self.updated_at = obj["updated_at"]
        return self

    def add_attachment(self, id):
        self.attachments.append(id)

    def add_comment(self, id):
        self.comments_count += 1
        self.comments.append(id)


class Attatchment(NosqlCRUD):
    collectionName = "post_attachments"
    
    @classmethod
    def construt(cls, image, created_by):
        self = cls()
        self.image = image
        self.created_by = created_by
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        return self


class Like(NosqlCRUD):

    collectionName = "likes"


    @classmethod
    def construt(cls, postID, created_by):
        self = cls()
        self.created_by = created_by
        self.postID = postID
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        return self

    def load_bson(self, obj):
        self.id = str(obj.get('_id'))
        self.postID = obj["postID"]
        self.created_by = obj["created_by"]
        self.created_at: obj["created_at"]
        self.updated_at: obj["updated_at"]
        return self

class Comment(NosqlCRUD):

    collectionName = "comments"

    @classmethod
    def construct(cls, body, created_by, postID, replies_count=0, parentComment=None):
        self = cls()
        self.body = body
        self.created_by = created_by
        self.postID = postID
        self.parentComment = parentComment
        self.replies_count = replies_count
        self.replies = list()
        self.created_at = datetime.datetime.now()
        return self

    def load_bson(self, obj):
        self.id = obj['_id']
        self.body = obj["body"]
        self.postID = obj["postID"]
        self.parentComment = obj['parentComment']
        self.created_by = obj["created_by"]
        self.replies_count = obj["replies_count"]
        self.replies = obj["replies"]
        self.created_at: obj["created_at"]
        self.updated_at: obj["updated_at"]
