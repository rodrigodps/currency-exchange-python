import logging

import routes

logging.basicConfig(level=logging.DEBUG, filename='app.log')
logging.info('Starting App...')
routes.app.run()
logging.info('Finalize App...')
