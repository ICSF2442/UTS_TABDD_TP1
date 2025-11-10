from neo4j import GraphDatabase
from app.core.config import settings

class Neo4jConnection:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            settings.NEO4J_URI,
            auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
        )
    
    def get_session(self):
        return self.driver.session()
    
    def close(self):
        self.driver.close()

# Singleton
neo4j_conn = Neo4jConnection()

def get_neo4j_session():
    return neo4j_conn.get_session()