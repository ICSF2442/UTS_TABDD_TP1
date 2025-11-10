# test_neo4j_connection.py
from neo4j import GraphDatabase
from app.core.config import settings

def test_connection():
    try:
        print(f"A tentar ligar a: {settings.NEO4J_URI}")
        print(f"User: {settings.NEO4J_USER}")
        
        driver = GraphDatabase.driver(
            settings.NEO4J_URI,
            auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
        )
        
        # Testar conexão básica
        with driver.session() as session:
            result = session.run("RETURN 'Conexão Neo4j OK!' AS message")
            print("SUCESSO:", result.single()["message"])
            
        # Testar se os dados foram criados
        with driver.session() as session:
            result = session.run("MATCH (s:Stop) RETURN count(s) AS total_stops")
            count = result.single()["total_stops"]
            print(f"Paragens na BD: {count}")
            
        driver.close()
        
    except Exception as e:
        print(f"ERRO na conexão Neo4j: {e}")
        print("Verifica:")
        print("   - URL está correta?")
        print("   - Password está correta?") 
        print("   - Servidor Neo4j está a correr?")
        print("   - Porta está aberta?")

if __name__ == "__main__":
    test_connection()