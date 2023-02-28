"""Script to seed database."""

import os
import json

import model
import server


os.system("createdb project")

model.connect_to_db(server.app)
model.db.create_all()

