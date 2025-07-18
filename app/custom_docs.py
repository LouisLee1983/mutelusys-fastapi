from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

def get_swagger_ui_html(
    *,
    openapi_url: str,
    title: str,
    swagger_js_url: str = "/static/swagger-ui/swagger-ui-bundle.js",
    swagger_css_url: str = "/static/swagger-ui/swagger-ui.css",
) -> HTMLResponse:
    """
    Generate Swagger UI HTML with local resources
    """
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <link type="text/css" rel="stylesheet" href="{swagger_css_url}">
    <title>{title} - Swagger UI</title>
    </head>
    <body>
    <div id="swagger-ui">
    </div>
    <script src="{swagger_js_url}"></script>
    <script>
    const ui = SwaggerUIBundle({{
        url: '{openapi_url}',
        dom_id: '#swagger-ui',
        deepLinking: true,
        presets: [
            SwaggerUIBundle.presets.apis,
            SwaggerUIBundle.SwaggerUIStandalonePreset
        ],
        plugins: [
            SwaggerUIBundle.plugins.DownloadUrl
        ],
        layout: "StandaloneLayout"
    }})
    window.ui = ui
    </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html)


def setup_custom_docs(app: FastAPI):
    """
    Setup custom documentation with local Swagger UI
    """
    @app.get("/docs", include_in_schema=False)
    async def custom_swagger_ui_html():
        return get_swagger_ui_html(
            openapi_url=app.openapi_url,
            title=app.title
        )
    
    @app.get("/redoc", include_in_schema=False)
    async def redoc_html():
        return HTMLResponse("""
        <!DOCTYPE html>
        <html>
        <head>
        <title>ReDoc</title>
        <meta charset="utf-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" rel="stylesheet">
        <style>
            body { margin: 0; padding: 0; }
        </style>
        </head>
        <body>
        <redoc spec-url='/openapi.json'></redoc>
        <script src="/static/swagger-ui/redoc.standalone.js"></script>
        </body>
        </html>
        """)