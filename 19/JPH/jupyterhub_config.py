"""
JupyterHub Configuration File
"""

import os
from pathlib import Path

# ============================================================================
# Базовая конфигурация
# ============================================================================

# Bind IP и порт
c.JupyterHub.bind_url = 'http://0.0.0.0:8000'
c.JupyterHub.hub_ip = '0.0.0.0'
c.JupyterHub.hub_port = 8081

# База данных
# Используем PostgreSQL если переменные окружения заданы
postgres_host = os.getenv('POSTGRES_HOST', 'db')
postgres_port = os.getenv('POSTGRES_PORT', '5432')
postgres_db = os.getenv('POSTGRES_DB', 'jupyterhub')
postgres_user = os.getenv('POSTGRES_USER', 'jupyterhub')
postgres_password = os.getenv('POSTGRES_PASSWORD', 'changeme')

c.JupyterHub.db_url = (
    f'postgresql://{postgres_user}:{postgres_password}@'
    f'{postgres_host}:{postgres_port}/{postgres_db}'
)

# Альтернатива: SQLite база данных (если PostgreSQL не используется)
# c.JupyterHub.db_url = 'sqlite:///data/jupyterhub.sqlite'

# ============================================================================
# Безопасность
# ============================================================================

# Cookie secret для шифрования cookies
cookie_secret = os.getenv('JUPYTERHUB_COOKIE_SECRET')
if cookie_secret:
    c.JupyterHub.cookie_secret_file = '/srv/jupyterhub/data/jupyterhub_cookie_secret'
    # Записываем секрет в файл, если его еще нет
    cookie_secret_path = Path(c.JupyterHub.cookie_secret_file)
    if not cookie_secret_path.exists():
        cookie_secret_path.parent.mkdir(parents=True, exist_ok=True)
        cookie_secret_path.write_bytes(cookie_secret.encode())

# Crypt key для шифрования базы данных
crypt_key = os.getenv('JUPYTERHUB_CRYPT_KEY')
if crypt_key:
    c.CryptKeeper.keys = [crypt_key.encode()]

# Отключение SSL (для локального развертывания)
c.JupyterHub.ssl_key = ''
c.JupyterHub.ssl_cert = ''

# ============================================================================
# Аутентификация
# ============================================================================

# Используем PAM (Unix) аутентификацию по умолчанию
# c.JupyterHub.authenticator_class = 'jupyterhub.auth.PAMAuthenticator'

# Или используем Dummy аутентификатор для разработки (без пароля)
c.JupyterHub.authenticator_class = 'jupyterhub.auth.DummyAuthenticator'

# Администраторы
admin_users = os.getenv('JUPYTERHUB_ADMIN', 'admin')
c.Authenticator.admin_users = set(admin_users.split(','))

# Разрешить администраторам заходить в серверы других пользователей
c.JupyterHub.admin_access = True

# Разрешить пользователям создавать аккаунты
c.Authenticator.allowed_users = set()  # Пустое множество = все могут
c.JupyterHub.allow_named_servers = True

# Whitelist пользователей (опционально)
# c.Authenticator.allowed_users = {'admin', 'user1', 'user2'}

# ============================================================================
# Spawner конфигурация
# ============================================================================

# Используем LocalProcessSpawner для простоты
c.JupyterHub.spawner_class = 'jupyterhub.spawner.SimpleLocalProcessSpawner'

# Настройки Spawner
c.Spawner.default_url = '/lab'  # Открывать JupyterLab по умолчанию
c.Spawner.cmd = ['jupyter-labhub']

# Таймауты
c.Spawner.http_timeout = 120
c.Spawner.start_timeout = 120

# Окружение для запускаемых серверов
c.Spawner.environment = {
    'JUPYTER_ENABLE_LAB': 'yes',
}

# Лимиты ресурсов (опционально)
# c.Spawner.cpu_limit = 2
# c.Spawner.mem_limit = '2G'

# ============================================================================
# Прокси конфигурация
# ============================================================================

# Используем configurable-http-proxy
c.ConfigurableHTTPProxy.should_start = True
c.ConfigurableHTTPProxy.auth_token = os.getenv(
    'CONFIGPROXY_AUTH_TOKEN', 
    'default-proxy-token-change-me'
)

# ============================================================================
# Логирование
# ============================================================================

c.JupyterHub.log_level = 'INFO'
c.Application.log_level = 'INFO'

# Логи в файл
c.JupyterHub.extra_log_file = '/var/log/jupyterhub/jupyterhub.log'

# ============================================================================
# Сервисы
# ============================================================================

# Idle culler - автоматическое завершение неактивных серверов
c.JupyterHub.services = [
    {
        'name': 'idle-culler',
        'admin': True,
        'command': [
            'python3', '-m', 'jupyterhub_idle_culler',
            '--timeout=3600',  # 1 час неактивности
        ],
    },
]

# ============================================================================
# Дополнительные настройки
# ============================================================================

# Shutdown при выходе
c.JupyterHub.cleanup_servers = True
c.JupyterHub.cleanup_proxy = True

# Редирект на /hub при заходе на /
c.JupyterHub.redirect_to_server = False

# Показывать страницу спавнинга
c.JupyterHub.show_spawn_pending = True

# Разрешить несколько серверов на пользователя
c.JupyterHub.allow_named_servers = True

# Кастомный HTML шаблон (опционально)
# c.JupyterHub.template_paths = ['/srv/jupyterhub/templates']

print("=" * 80)
print("JupyterHub Configuration Loaded Successfully")
print(f"Database: {c.JupyterHub.db_url}")
print(f"Admin users: {c.Authenticator.admin_users}")
print(f"Spawner: {c.JupyterHub.spawner_class}")
print("=" * 80)
