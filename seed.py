"""Script to seed database."""

import model
import server


# os.system("createdb project")

# with server.app.app_context():
model.connect_to_db(server.app)
model.db.create_all()
