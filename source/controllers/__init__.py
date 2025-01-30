from .controller import controller
from .userContrroller import userController
from .courseController import courseController
from .studentController import studentController
from .courseStudentController import courseStudentController

class Controllers:
    def init_app(self, app):
        blueprints = [
            userController,
            courseController,
            studentController,
            courseStudentController,
            controller
        ]       
        for blueprint in blueprints:
            app.register_blueprint(blueprint)
controllers = Controllers()
