"""Banco SQLite para controle de noticias processadas."""
import sqlite3
import logging
from datetime import datetime
from contextlib import contextmanager

from config.settings import DB_PATH

logger = logging.getLogger(__name__)


class Database:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._init_schema()

    @contextmanager
    def _conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def _init_schema(self):
        with self._conn() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS noticias (
                    hash_id TEXT PRIMARY KEY,
                    url TEXT UNIQUE NOT NULL,
                    portal TEXT NOT NULL,
                    titulo_original TEXT NOT NULL,
                    titulo_reescrito TEXT,
                    conteudo_original TEXT,
                    conteudo_reescrito TEXT,
                    status TEXT DEFAULT 'coletada',
                    wp_post_id INTEGER,
                    erro TEXT,
                    coletada_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    processada_em TIMESTAMP,
                    publicada_em TIMESTAMP
                )
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_status ON noticias(status)")

    def ja_processada(self, hash_id: str) -> bool:
        with self._conn() as conn:
            row = conn.execute(
                "SELECT 1 FROM noticias WHERE hash_id = ? AND status IN ('publicada', 'processando')",
                (hash_id,)
            ).fetchone()
            return row is not None

    def registrar_coleta(self, noticia) -> bool:
        try:
            with self._conn() as conn:
                conn.execute("""
                    INSERT INTO noticias (hash_id, url, portal, titulo_original, conteudo_original)
                    VALUES (?, ?, ?, ?, ?)
                """, (noticia.hash_id, noticia.url, noticia.portal,
                      noticia.titulo, noticia.conteudo))
            return True
        except sqlite3.IntegrityError:
            return False

    def atualizar_reescrita(self, hash_id, titulo_novo, conteudo_novo):
        with self._conn() as conn:
            conn.execute("""
                UPDATE noticias SET titulo_reescrito=?, conteudo_reescrito=?,
                       status='reescrita', processada_em=?
                WHERE hash_id=?
            """, (titulo_novo, conteudo_novo, datetime.now(), hash_id))

    def marcar_publicada(self, hash_id, wp_post_id):
        with self._conn() as conn:
            conn.execute("""
                UPDATE noticias SET status='publicada', wp_post_id=?, publicada_em=?
                WHERE hash_id=?
            """, (wp_post_id, datetime.now(), hash_id))

    def marcar_erro(self, hash_id, erro):
        with self._conn() as conn:
            conn.execute("UPDATE noticias SET status='erro', erro=? WHERE hash_id=?",
                         (erro[:500], hash_id))
