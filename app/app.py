import neo4j
from flask import Flask, send_from_directory, jsonify
from neo4j.v1 import GraphDatabase, basic_auth

from time import sleep
sleep(10)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Grovverg53s'

ENABLE_NEO4J=False

if ENABLE_NEO4J:
    connected = False
    while not connected:
        try:
            driver = GraphDatabase.driver("bolt://neo4j:7687", auth=basic_auth("neo4j", "coffy"))
            connected = True
        except neo4j.exceptions.ServiceUnavailable:
            sleep(5)

    session = driver.session()


@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('static', path)


@app.route('/')
def home(path='index.html'):
    return send_from_directory('static', path)


@app.route('/data.json')
def data():
    gods = session.run("MATCH(n) RETURN id(n) as id, n as god, labels(n) as labels")

    result = {
        'nodes': [],
        'links': [],
    }
    labels = []

    for record in gods:
        node = {
            'id': record['id'],
            'name': record['god']['name'],
            'label': record['labels']
        }
        if record['labels'][0] not in labels:
            labels.append(record['labels'][0])
        node['group'] = labels.index(record['labels'][0])
        result['nodes'].append(node)

    links = session.run("MATCH(n)<-[:KIND_VON]-(m) RETURN id(m) as source, n, id(n) as target")

    for link in links:
        result['links'].append({
            'source': link['source'],
            'target': link['target']
        })

    return jsonify(result)


if __name__ == '__main__':
    if ENABLE_NEO4J:
        # Clean the database
        session.run("MATCH(n) DETACH DELETE n")

        # Populate the database
        with open("goetter_DE.cyp") as f:
            session.run(f.read())

    app.debug = False
    app.run(host='0.0.0.0', port=9090)
