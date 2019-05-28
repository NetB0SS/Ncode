from backend.apps.vone import *



def register_views(app):
    api = Api(app)

    api.add_resource(Searchlicence, '/food/search/info')
    api.add_resource(Hello, '/hello', endpoint="hello")
    api.add_resource(Takekey, '/food/search/keylist')