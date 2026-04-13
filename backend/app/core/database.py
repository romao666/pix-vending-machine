import sqlite3
from pathlib import Path
import json

DB_PATH = Path(__file__).parent.parent / "data" / "cherry_bomb.db"
JSON_PATH = Path(__file__).parent.parent / "data" / "products.json"


def get_connection():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Cria tabela de produtos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL DEFAULT 0,
            image_url TEXT DEFAULT NULL
        )
    """)

    # Cria tabela de pagamentos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pagamentos (
            id TEXT PRIMARY KEY,
            status TEXT NOT NULL DEFAULT 'pending',
            itens TEXT NOT NULL,
            total REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Seed: importa products.json se a tabela estiver vazia
    cursor.execute("SELECT COUNT(*) FROM produtos")
    count = cursor.fetchone()[0]

    if count == 0 and JSON_PATH.exists():
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            produtos = json.load(f)
        cursor.executemany(
            "INSERT INTO produtos (id, name, price, stock) VALUES (?, ?, ?, ?)",
            [(p["id"], p["name"], p["price"], p["stock"]) for p in produtos]
        )
        print("✅ Seed: produtos importados do JSON para o SQLite")

    conn.commit()
    conn.close()