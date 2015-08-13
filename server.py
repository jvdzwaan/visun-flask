from flask import Flask
from SPARQLWrapper import SPARQLWrapper, JSON, Wrapper
from flask import request, jsonify
from flask.ext.cors import CORS

import base64

import logging
from logging import StreamHandler

app = Flask(__name__)
CORS(app)

file_handler = StreamHandler()
app.logger.setLevel(logging.DEBUG)
app.logger.addHandler(file_handler)


@app.route('/')
def hello_world():
    return 'hello world'


@app.route('/do_sparql')
def do_sparql():
    auth = request.authorization
    query = request.args.get('query')
    dataset = request.args.get('dataset')

    #app.logger.debug(auth)
    #app.logger.debug(query)

    if not auth is None and not query is None:
        url = 'https://knowledgestore2.fbk.eu/nwr/{}/sparql'.format(dataset)
        sparql = SPARQLWrapper(url)
        sparql.setQuery(query)
        sparql.setCredentials(auth.username, auth.password)
        sparql.setReturnFormat(JSON)

        # Dirty hack!
        r = sparql._createRequest()
        encoded = base64.b64encode(':'.join([auth.username, auth.password]))
        app.logger.debug(encoded)
        r.add_header('Authorization', 'Basic {}'.format(encoded))
        app.logger.debug(r.headers)

        from urllib2 import urlopen
        response = urlopen(r)
        res = Wrapper.QueryResult((response, sparql.returnFormat))
        results = res.convert()

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

#if __name__ == '__main__':
#    app.run()
