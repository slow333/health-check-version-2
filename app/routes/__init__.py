from . import (
  commands_routes, contents_routes, auth, hostinfos_routes, servers_routes, 
  sar_traffic_routes, image_routes)

def init_app(app):
  app.register_blueprint(auth.bp)
  app.register_blueprint(servers_routes.bp)
  app.register_blueprint(hostinfos_routes.bp)
  app.register_blueprint(commands_routes.bp)
  app.register_blueprint(sar_traffic_routes.bp)
  app.register_blueprint(image_routes.bp)

  app.register_blueprint(contents_routes.bp)
