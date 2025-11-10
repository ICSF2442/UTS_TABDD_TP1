from fastapi import APIRouter, HTTPException, Depends
from app.core.services.optimization_service import OptimizationService
from app.domain.schemas.route import RouteRequest, RouteResponse, RouteStopBase
from app.api.v1.auth import get_current_user

router = APIRouter(prefix="/routes", tags=["Route Optimization"])

@router.post("/optimal", response_model=RouteResponse, summary="Encontrar rota ótima")
def find_optimal_route(
    request: RouteRequest,
    #current_user = Depends(get_current_user)  # Requer autenticação
):
    """
    Encontra a melhor rota entre origem e destino
    """
    optimization_service = OptimizationService()
    
    try:
        route = optimization_service.find_optimal_route(request.origin, request.destination)
        
        # Converter para schema de resposta
        stops_response = [
            RouteStopBase(
                name=stop.name,
                type=stop.type,
                stop_id=stop.stop_id,
                latitude=stop.latitude,
                longitude=stop.longitude
            )
            for stop in route.stops
        ]
        
        segments_response = [
            {
                "from_stop": seg.from_stop,
                "to_stop": seg.to_stop,
                "transport": seg.transport,
                "line": seg.line,
                "time_min": seg.time_min,
                "distance_km": seg.distance_km
            }
            for seg in route.segments
        ]
        
        return RouteResponse(
            total_time_minutes=route.total_time_minutes,
            stops=stops_response,
            segments=segments_response,
            transfer_count=route.transfer_count,
            message=f"Melhor rota: {request.origin} → {request.destination}"
        )
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao calcular rota: {str(e)}")

@router.get("/stops", summary="Listar todas as paragens")
def get_all_stops(
    #current_user = Depends(get_current_user)  # Requer autenticação
):
    """
    Retorna todas as paragens disponíveis no sistema
    """
    optimization_service = OptimizationService()
    
    try:
        stops = optimization_service.get_all_stops()
        
        return {
            "stops": [
                {
                    "name": stop.name,
                    "type": stop.type,
                    "stop_id": stop.stop_id
                }
                for stop in stops
            ],
            "total": len(stops)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter paragens: {str(e)}")

@router.get("/stops/{stop_name}/validate", summary="Validar paragem")
def validate_stop(
    stop_name: str,
    #current_user = Depends(get_current_user)  # Requer autenticação
):
    """
    Valida se uma paragem existe no sistema
    """
    optimization_service = OptimizationService()
    
    try:
        exists = optimization_service.validate_stop_exists(stop_name)
        
        return {
            "stop_name": stop_name,
            "exists": exists
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao validar paragem: {str(e)}")