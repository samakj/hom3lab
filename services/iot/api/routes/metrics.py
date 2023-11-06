from fastapi import HTTPException

from shared.python.speedyapi import APIRouter
from shared.python.models.metric import CreateMetric, Metric
from shared.python.helpers.load_json_file import load_json_file

METRICS_V0_ROUTER = APIRouter(prefix="/v0/metrics", tags=["metrics"])

@METRICS_V0_ROUTER.get("/{id:int}", response_model=Metric)
def get_metric(id: int) -> Metric:
    for metric in load_json_file("test-data/metrics.json"):
        if metric["id"] == id:
            return Metric.parse_obj(metric)
    
    raise HTTPException(status=404)

@METRICS_V0_ROUTER.get("/", response_model=list[Metric])
def get_metrics() -> Metric:
    return [
        Metric.parse_obj(metric)
        for metric in load_json_file("test-data/metrics.json")
    ]

@METRICS_V0_ROUTER.post("/", response_model=Metric)
def create_metric(metric: CreateMetric) -> Metric:
    return Metric.parse_obj(load_json_file("test-data/metrics.json")[0])

@METRICS_V0_ROUTER.patch("/{id:int}", response_model=Metric)
def create_metric(id:int, metric: CreateMetric) -> Metric:
    return get_metric(id)
