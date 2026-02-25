"""
users: create table
"""

from yoyo import step

__depends__ = []

steps = [
    step(
        # SQL для применения миграции (UP)
        """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100) NOT NULL UNIQUE,
            email VARCHAR(255) NOT NULL UNIQUE,
            password_hash VARCHAR(255) NOT NULL,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Индексы для ускорения поиска
        CREATE INDEX idx_users_username ON users(username);
        CREATE INDEX idx_users_email ON users(email);
        
        -- Комментарии к таблице
        COMMENT ON TABLE users IS 'Таблица пользователей системы';
        COMMENT ON COLUMN users.id IS 'Уникальный идентификатор пользователя';
        COMMENT ON COLUMN users.username IS 'Имя пользователя для входа';
        COMMENT ON COLUMN users.email IS 'Email пользователя';
        """,
        
        # SQL для отката миграции (DOWN)
        """
        DROP INDEX IF EXISTS idx_users_email;
        DROP INDEX IF EXISTS idx_users_username;
        DROP TABLE IF EXISTS users CASCADE;
        """
    )
]
