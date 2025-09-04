from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html
from app.api import operating_systems, applications, vinci_divisions, environnements, networks, cloud_subscriptions, agents
from app.api import server_sources, server_roles, server_tiers
from app.api import servers

app = FastAPI(
    title="KPI HOSTING API",
    description="KPI HOSTING API",
    version="1.0.0",
    docs_url=None,
    redoc_url=None
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(operating_systems.router, prefix="/operatingsystems", tags=["Operating systems"])
app.include_router(applications.router, prefix="/applications", tags=["Applications"])
app.include_router(server_roles.router, prefix="/serverroles", tags=["Server roles"])
app.include_router(server_tiers.router, prefix="/servertiers", tags=["Server tiers"])
app.include_router(server_sources.router, prefix="/serversources", tags=["Server sources"])
app.include_router(vinci_divisions.router, prefix="/vincidivisions", tags=["Vinci divisions"])
app.include_router(environnements.router, prefix="/environnements", tags=["Environnements"])
app.include_router(networks.router, prefix="/networks", tags=["Networks"])
app.include_router(cloud_subscriptions.router, prefix="/cloudsubscriptions", tags=["Cloud subscriptions"])
app.include_router(agents.router, prefix="/agents", tags=["Agents"])
app.include_router(servers.router, prefix="/servers", tags=["Servers"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the KPI HOSTING API"}

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Documentation",
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
        swagger_favicon_url="/static/favicon-16x16.png",
    )