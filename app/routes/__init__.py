from . import (
  contents_routes, auth, hostinfos_routes, servers_routes, 
  commands_bp, sar_traffic_routes, svinfos_routes)

def init_app(app):
  app.register_blueprint(auth.bp)
  app.register_blueprint(servers_routes.bp)
  app.register_blueprint(hostinfos_routes.bp)
  app.register_blueprint(commands_bp.bp)
  app.register_blueprint(sar_traffic_routes.bp)
  app.register_blueprint(svinfos_routes.bp)

  app.register_blueprint(contents_routes.bp)
