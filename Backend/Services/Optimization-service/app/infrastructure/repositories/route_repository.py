from typing import List, Optional
from app.infrastructure.db.connection import get_neo4j_session
from app.domain.models.route import RouteStop, RouteSegment, OptimalRoute

class RouteRepository:
    def __init__(self):
        self.session = get_neo4j_session()
    
    def find_optimal_route(self, origin: str, destination: str) -> Optional[OptimalRoute]:
        query = """
        MATCH (start:Stop {name: $origin}), (end:Stop {name: $destination})
        MATCH path = shortestPath((start)-[:CONNECTS_TO|TRANSFER*]-(end))
        WITH path, 
             reduce(totalTime = 0, r IN relationships(path) | totalTime + r.time_min) AS total_time
        RETURN 
            total_time,
            [node IN nodes(path) | node {.name, .type, .stop_id}] AS route_stops,
            [rel IN relationships(path) | {
                from_stop: startNode(rel).name,
                to_stop: endNode(rel).name,
                transport: COALESCE(rel.transport, 'transfer'),
                line: COALESCE(rel.line, 'transfer'),
                time_min: rel.time_min,
                distance_km: COALESCE(rel.distance_km, 0)
            }] AS route_segments
        """
        
        try:
            result = self.session.run(query, origin=origin, destination=destination)
            record = result.single()
            
            if not record:
                return None
            
            # Converter para modelos de domínio
            stops = [
                RouteStop(
                    name=stop["name"],
                    type=stop["type"],
                    stop_id=stop["stop_id"]
                )
                for stop in record["route_stops"]
            ]
            
            segments = []
            for seg in record["route_segments"]:
                segments.append(RouteSegment(
                    from_stop=seg["from_stop"],
                    to_stop=seg["to_stop"],
                    transport=seg["transport"],
                    line=seg["line"],
                    time_min=seg["time_min"],
                    distance_km=seg["distance_km"]
                ))
            
            transfer_count = len([seg for seg in segments if seg.transport == "transfer"])
            
            return OptimalRoute(
                total_time_minutes=record["total_time"],
                stops=stops,
                segments=segments,
                transfer_count=transfer_count
            )
            
        except Exception as e:
            raise Exception(f"Erro ao calcular rota: {str(e)}")
    
    def get_all_stops(self) -> List[RouteStop]:
        query = "MATCH (s:Stop) RETURN s.name AS name, s.type AS type, s.stop_id AS stop_id ORDER BY s.name"
        
        try:
            result = self.session.run(query)
            stops = [
                RouteStop(
                    name=record["name"],
                    type=record["type"],
                    stop_id=record["stop_id"]
                )
                for record in result
            ]
            return stops
        except Exception as e:
            raise Exception(f"Erro ao obter paragens: {str(e)}")