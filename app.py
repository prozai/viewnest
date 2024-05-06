from app import create_app

app = create_app()

import app.control.adminController as adminController
import app.control.mainController as mainController

if __name__ == '__main__':
    app.run(debug=True)
