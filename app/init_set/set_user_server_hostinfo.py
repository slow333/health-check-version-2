import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app import create_app
from app.extensions import db
from app.models.servers import Servers
from app.models.users import Users
from app.models.hostinfos import HostInfos

def seed_data():
    """Seeds the database with initial data."""
    app = create_app()
    with app.app_context():
        # Check if data already exists to prevent duplicates
        if Users.query.first() is not None or Servers.query.first() is not None or HostInfos.query.first() is not None:
            print("Database already contains data. Skipping seeding.")
            return

        print("Seeding database...")
        s1 = Servers(server_name='R6', login_id='root', ip_address='192.168.219.206', port=22, password='1')
        s2 = Servers(server_name='R7', login_id='root', ip_address='192.168.219.7', port=22,password='1')
        s3 = Servers(server_name='R8', login_id='root', ip_address='192.168.219.111', port=22,password='1')
        s4 = Servers(server_name='R9', login_id='root', ip_address='192.168.219.209', port=22,password='1')
        s5 = Servers(server_name='R10', login_id='root', ip_address='192.168.219.210', port=22,password='1')

        admin = Users(username='admin', email='admin@demo.com', is_admin=True)
        admin.set_password('admin')

        op_kim = Users(username='op_kim', email='op_kim@demo.com')
        op_kim.set_password('1111')

        op_woo = Users(username='op_woo', email='op_woo@demo.com')
        op_woo.set_password('1111')

        test = Users(username='test', email='test@demo.com')
        test.set_password('1111')

        kalpa = Users(username='kalpa', email='kalpa@demo.com', is_admin=True)
        kalpa.set_password('1111')

        db.session.add_all([s1, s2, s3, s4,s5, admin, op_kim, op_woo, test, kalpa])

        admin.allowed_servers.extend([s1, s2, s3, s4, s5])
        kalpa.allowed_servers.extend([s1, s2, s3, s4])
        op_kim.allowed_servers.extend([s1, s3, s4, s5])
        op_woo.allowed_servers.append(s1)
        op_woo.allowed_servers.append(s5)
        test.allowed_servers.extend([s1,s4, s5])

        # h1 = HostInfos(hostname='server-r6', ip_address='192.168.219.206')
        # h2 = HostInfos(hostname='server-r7', ip_address='192.168.219.7')
        # h3 = HostInfos(hostname='server-r8', ip_address='192.168.219.111')
        # h4 = HostInfos(hostname='server-r9', ip_address='192.168.219.209')
        # h5 = HostInfos(hostname='server-r10', ip_address='192.168.219.210')

        # h1.access_info = s1
        # h2.access_info = s2
        # h3.access_info = s3
        # h4.access_info = s4
        # h5.access_info = s5
        # db.session.add_all([h1, h2, h3, h4, h5])

        db.session.commit()
        print("Database seeded successfully.")

if __name__ == '__main__':
    seed_data()
