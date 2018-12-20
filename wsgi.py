from app import application
from werkzeug.debug import DebuggedApplication

if __name__ == "__main__":
    application.run(DEBUG=True)
    application.wsgi_application = DebuggedApplication(application.wsgi_application, True)
