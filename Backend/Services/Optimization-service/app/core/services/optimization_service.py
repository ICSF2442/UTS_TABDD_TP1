from typing import List, Optional
from app.infrastructure.repositories.route_repository import RouteRepository
from app.domain.models.route import OptimalRoute, RouteStop

class OptimizationService:
    def __init__(self):
        self.repo = RouteRepository()
    
    def find_optimal_route(self, origin: str, destination: str) -> OptimalRoute:
        """
        Encontra a rota ótima entre origem e destino
        """
        if not origin or not destination:
            raise ValueError("Origem e destino são obrigatórios")
        
        route = self.repo.find_optimal_route(origin, destination)
        
        if not route:
            raise ValueError(f"Nenhuma rota encontrada de {origin} para {destination}")
        
        return route
    
    def get_all_stops(self) -> List[RouteStop]:
        """
        Retorna todas as paragens disponíveis
        """
        return self.repo.get_all_stops()
    
    def validate_stop_exists(self, stop_name: str) -> bool:
        """
        Valida se uma paragem existe
        """
        stops = self.get_all_stops()
        return any(stop.name.lower() == stop_name.lower() for stop in stops)