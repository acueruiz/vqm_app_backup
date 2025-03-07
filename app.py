from backend import create_app
from frontend.routes import frontend_bp

# Crear la aplicación usando create_app()
app = create_app()

# Asegurar que Flask busque los templates en frontend/templates
app.template_folder = "frontend/templates"
app.static_folder = "frontend/static"

# Registrar el Blueprint del frontend
app.register_blueprint(frontend_bp)

if __name__ == '__main__':
    app.run(debug=True)
