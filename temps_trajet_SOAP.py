from spyne import Application, rpc, ServiceBase, Iterable, Unicode, Integer, Float
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

class CORSMiddleware:
    """Pour gérer la politique CORS"""
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        def custom_start_response(status, headers, exc_info=None):
            headers.append(('Access-Control-Allow-Origin', '*'))
            headers.append(('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, DELETE, PUT'))
            return start_response(status, headers, exc_info)

        return self.app(environ, custom_start_response)


class TrajetService(ServiceBase):
    @rpc(Float, Integer, Float, Float, _returns=Float)
    def calcul_trajet(ctx, distance, autonomie, vitesse_moyenne, tps_chargement):
        """Calcul le temps de trajet en fonction de la 
            distance et de l’autonomie des véhicules et en tenant compte du temps de 
            chargement et de la vitesse du véhicule"""
        if distance < autonomie:
            return distance / vitesse_moyenne
        else:
            nb_chargements = distance / autonomie
            return (nb_chargements * tps_chargement) + (distance / vitesse_moyenne)

application = Application([TrajetService],
    tns='spyne.examples.trajet',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

wsgi_app = WsgiApplication(application)
app = CORSMiddleware(wsgi_app)

# if __name__ == '__main__':
#     from wsgiref.simple_server import make_server
#     wsgi_app = WsgiApplication(application)
#     wsgi_app_with_cors = CORSMiddleware(wsgi_app)
#     server = make_server('127.0.0.1', 8000, wsgi_app_with_cors)
#     # http://localhost:8000/?wsdl
#     server.serve_forever()