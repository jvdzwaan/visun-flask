from flask import Flask
from SPARQLWrapper import SPARQLWrapper, JSON
from flask import request, jsonify
from flask.ext.cors import CORS

import logging
from logging import StreamHandler

app = Flask(__name__)
CORS(app)

file_handler = StreamHandler()
app.logger.setLevel(logging.DEBUG)  # set the desired logging level here
app.logger.addHandler(file_handler)


@app.route('/')
def hello_world():
    return 'hello world'


@app.route('/sparql')
def do_sparql():
    app.logger.debug('called do_sparql')

    auth = request.authorization
    query = request.args.get('query')

    app.logger.debug(auth)
    app.logger.debug(query)

    if not auth is None and not query is None:
        app.logger.debug('preparing to query the knowledge store')
        sparql = SPARQLWrapper('https://knowledgestore2.fbk.eu/nwr/dutchhouse/sparql')
        sparql.setQuery(query)
        sparql.setCredentials(auth.username, auth.password)
        sparql.setReturnFormat(JSON)
        app.logger.debug('doing query')
        results = sparql.query().convert()
        app.logger.debug('done query')
        return jsonify(**results)
    else:
        app.logger.debug('found an error')
        msg = []
        if auth is None:
            msg.append('authorization error')
        if query is None:
            msg.append('no query')

        app.logger.debug('returning error: ' + ' '.join(msg))
        response = jsonify({'status': 404, 'statusText': ' '.join(msg)})
        response.status_code = 404
        return response

if __name__ == '__main__':
    app.run()
