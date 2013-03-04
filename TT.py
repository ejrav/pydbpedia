from SPARQLWrapper import SPARQLWrapper, JSON
import sys

class SparqlEndpoint(object):

    def __init__(self, endpoint, prefixes={}):
        self.sparql = SPARQLWrapper(endpoint)
        self.prefixes = {
            "dbpedia-owl": "http://dbpedia.org/ontology/",
            "owl": "http://www.w3.org/2002/07/owl#",
            "xsd": "http://www.w3.org/2001/XMLSchema#",
            "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
            "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
            "foaf": "http://xmlns.com/foaf/0.1/",
            "dc": "http://purl.org/dc/elements/1.1/",
            "dbpedia2": "http://dbpedia.org/property/",
            "dbpedia": "http://dbpedia.org/",
            "skos": "http://www.w3.org/2004/02/skos/core#",
            "foaf": "http://xmlns.com/foaf/0.1/",
            }
        self.prefixes.update(prefixes)
        self.sparql.setReturnFormat(JSON)

    def query(self, q):
        lines = ["PREFIX %s: <%s>" % (k, r) for k, r in self.prefixes.iteritems()]
        lines.extend(q.split("\n"))
        query = "\n".join(lines)
        print query
        self.sparql.setQuery(query)
        results = self.sparql.query().convert()
        return results["results"]["bindings"]


class DBpediaEndpoint(SparqlEndpoint):

    def __init__(self, prefixes = {}):
        endpoint = "http://it.dbpedia.org/sparql"
        super(DBpediaEndpoint, self).__init__(endpoint, prefixes)


def main ():
    s = DBpediaEndpoint()

    results = s.query("""
        SELECT * WHERE {
            ?movie a <http://dbpedia.org/ontology/Film> .
            ?movie <http://dbpedia.org/ontology/country> <http://it.dbpedia.org/resource/Italia> .
        }
    """)

    for d in results:
        print d



if __name__ == '__main__':
    try:
        main()
        sys.exit(0)
    except KeyboardInterrupt, e: # Ctrl-C
        raise e