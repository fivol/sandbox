from abc import abstractmethod, ABCMeta
from enum import Enum

from utils import jsonify_spec


class OASpec:
    """OpenAPI Specification base class"""

    def __init__(self, *args, **kwargs):
        """By default this object represented as self.data if self.key is None else self.key : self.data"""
        self.data = kwargs
        self.key = None

    def spec(self):
        """Return object responding openapi spec json"""
        return self.data

    def json(self):
        return jsonify_spec(self.spec())

    def with_data(self, replace_dict):
        return {
            **self.data,
            **replace_dict
        }


class EntityWithDescription(OASpec):
    def __init__(self, description='', *args, **kwargs):
        super(EntityWithDescription, self).__init__(*args, **kwargs)
        self.data.update({
            'description': description
        })


class Info(OASpec):
    pass


class Server(OASpec):
    pass


class Tag(OASpec):
    pass


class Description(OASpec):
    pass


class Response(EntityWithDescription):
    def __init__(self, code, **kwargs):
        super(Response, self).__init__(**kwargs)


class Path(OASpec):
    def __init__(self, path, requests, **kwargs):
        super(Path, self).__init__(**kwargs)
        self.path = path.strip('/')
        self.data.update({
            'path': self.path,
            'requests': requests
        })

    def spec(self):
        return {
            request.type: Request
            for request in self.data['requests']
        }


class Schema(EntityWithDescription):
    def __init__(self, enum=None, default=None, format=None, **kwargs):
        super(Schema, self).__init__(**kwargs)
        self.data.update({
            'enum': enum,
            'default': default,
            'format': format
        })


class Request(OASpec):
    GET = 'get'
    POST = 'post'
    PUT = 'put'
    DELETE = 'put'

    def __init__(self, request_type, *args, **kwargs):
        super(Request, self).__init__(*args, **kwargs)
        self.key = request_type


class Parameter(EntityWithDescription):
    HEADER = 'header'
    QUERY = 'query'
    PATH = 'path'
    COOKIE = 'cookie'

    def __init__(self, in_, name, required=True, *args, **kwargs):
        super(Parameter, self).__init__(*kwargs, **kwargs)
        self.data.update({
            'in': in_,
            'name': name,
            'required': required
        })


class PostRequest(Request):
    def __init__(self, *args, **kwargs):
        super(PostRequest, self).__init__(*args, **kwargs)
        self.type = Request.RequestType.post


class GetRequest(Request):
    def __init__(self, *args, **kwargs):
        super(GetRequest, self).__init__(*args, **kwargs)
        self.key = Request.RequestType.post.value


class PutRequest(Request):
    def __init__(self, *args, **kwargs):
        super(PutRequest, self).__init__(*args, **kwargs)
        self.type = Request.RequestType.put


class String(Schema):
    def __init__(self, value, **kwargs):
        assert isinstance(value, str)
        self.value = value
        super(String, self).__init__(**kwargs)

    def spec(self):
        return self.value


class Integer(Schema):
    def __init__(self, **kwargs):
        super(Integer, self).__init__(kwargs)


class Object(Schema):
    def __init__(self, properties, **kwargs):
        super(Object, self).__init__(**kwargs)
        self.data.update({
            'properties': properties
        })


class OpenAPI(OASpec):
    def __init__(self, info, servers, paths, **kwargs):
        super(OpenAPI, self).__init__(**kwargs)
        self.data = {
            'info': info,
            'severs': servers,
            'paths': paths
        }
