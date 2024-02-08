# Импорт Blueprint'ов
from .main import main_bp
from .auth import auth_bp
from .admin import admin_bp
from .user import user_bp
from .catalog import catalog_bp

# Возвращает Blueprint'ы
def get_blueprints():
    return (main_bp, auth_bp, admin_bp, user_bp, catalog_bp)