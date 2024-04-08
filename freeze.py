# creating a static version of my app with Frozen-Flask so it can be uploaded to github pages and displayed
# because no data is stored, this works fine and doesn't mess with any functionality

from flask_frozen import Freezer
from flask_project.app import app

freezer = Freezer(app)

if __name__ == '__main__':
    freezer.freeze()
