import os
import random
import httpx
from fastapi import FastAPI, Request, Response

app = FastAPI()

# Загрузка конфигурации из переменных окружения
MONOLITH_URL = os.getenv("MONOLITH_URL", "http://monolith:8080")
MOVIES_SERVICE_URL = os.getenv("MOVIES_SERVICE_URL", "http://movies-service:8081")
EVENTS_SERVICE_URL = os.getenv("EVENTS_SERVICE_URL", "http://events-service:8082")
GRADUAL_MIGRATION = os.getenv("GRADUAL_MIGRATION", "true").lower() == "true"
MIGRATION_PERCENT = int(os.getenv("MOVIES_MIGRATION_PERCENT", "50"))

@app.get("/health")
async def health_check():
    return "Strangler Fig Proxy is healthy"

# Универсальный обработчик для всех запросов
@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_handler(request: Request, path: str):
    url_path = request.url.path
    
    # Определение целевого сервиса
    target_url = MONOLITH_URL
    
    # Логика Strangler Fig для фильмов
    if url_path.startswith("/api/movies"):
        if GRADUAL_MIGRATION and random.randint(1, 100) <= MIGRATION_PERCENT:
            target_url = MOVIES_SERVICE_URL
            print(f"[Proxy] Routing to MOVIES-SERVICE (Migration Active)")
        else:
            print(f"[Proxy] Routing to MONOLITH")
            
    # Перенаправление на сервис событий
    elif url_path.startswith("/api/events"):
        target_url = EVENTS_SERVICE_URL

    # Проксирование запроса
    async with httpx.AsyncClient() as client:
        content = await request.body()
        headers = dict(request.headers)
        # Удаляем host, чтобы не было конфликтов при пересылке
        headers.pop("host", None)
        
        try:
            response = await client.request(
                method=request.method,
                url=f"{target_url}{url_path}?{request.query_params}",
                content=content,
                headers=headers,
                timeout=10.0
            )
            return Response(
                content=response.content,
                status_code=response.status_code,
                headers=dict(response.headers)
            )
        except Exception as e:
            return Response(content=f"Proxy Error: {str(e)}", status_code=502)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
