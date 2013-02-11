from flask import Flask
from flask.ext import restful
from flask.ext.restful import abort

app = Flask(__name__)
api = restful.Api(app)


@app.route('/')
def index():
    return 'test'


class Search(restful.Resource):
    def get(self):
        abort(404, message='test')
        return {'hello': 'world'}

api.add_resource(Search, '/api/v1/search')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)
