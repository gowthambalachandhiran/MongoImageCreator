from flask import Flask, request, jsonify
from flask_caching import Cache
from GetRandomDocument import RandomDocumentRetriever
from Authentication import ConnectingMongoServer
from FileCreator import AnimationCreator
import logging 
class ServeDrawing:
    def __init__(self):
        connection = ConnectingMongoServer('config.yaml')
        self.client = connection.establish_connection()
        self.app = Flask(__name__)
        self.cache = Cache(self.app, config={'CACHE_TYPE': 'simple'})

        @self.app.route('/convert', methods=['POST'])
        def upload_file():
            
            try:
                logging.info("Started....")
                input_json = request.get_json(force=True) 
                object_name = input_json['object']
                session_id = input_json['session_id']
                db_name = input_json['db_name']
            except KeyError as e:
                error_msg = f"Missing data: {str(e)}"
                logging.error(error_msg)
                return jsonify({'error': error_msg}), 400
            document = RandomDocumentRetriever(self.client, db_name, object_name)
            random_document = document.get_random_document()
            
           
            animation = AnimationCreator(random_document['drawing'])
            base_64 = animation.create_animation()
            
            return jsonify({'session_id': session_id, 'file': base_64})

    def run(self):
        # Use Gunicorn as the WSGI server with multiple worker processes
        self.app.run()

# Example usage:
if __name__ == "__main__":
    processor = ServeDrawing()
    processor.run()
