from os import path

import aiosqlite
from models.db.base import DatabaseModel


class BaseTable:
    db_path: str
    conn: aiosqlite.Connection

    @property
    def table(self) -> str:
        return None

    @property
    def model(self) -> DatabaseModel:
        return None

    @property
    def primary_key(self) -> str:
        return None

    def __init__(self):
        self.db_path = path.join('main.db')

    async def __aenter__(self):
        self.conn = await aiosqlite.connect(self.db_path)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.conn.commit()
        await self.conn.close()

    async def raw_query(self, query):
        return await self.conn.execute_fetchall(query)

    async def get_by_key(self, value) -> DatabaseModel:
        key = self.primary_key
        query = await self.conn.execute(f"SELECT * FROM {self.table} WHERE {key} = $1", (value, ))
        result = await query.fetchone()
        return self.model.from_list(result) if result else None

    async def update_by_key(self, key_value: str, value_cl: str, value):
        key = self.primary_key
        query = f"UPDATE {self.table} SET {value_cl}=$1 WHERE {key}=$2"
        await self.conn.execute(query, (value, key_value,))
        await self.conn.commit()

    async def remove_by_key(self, key_value):
        key = self.primary_key
        return await self.conn.execute(f"DELETE FROM {self.table} WHERE {key}=$1", (key,))

    async def add_one(self, new_obj: DatabaseModel):
        if not isinstance(new_obj, self.model):
            raise TypeError(f'Object {new_obj} is not of type {self.model}')
        obj_attrs = new_obj.model_dump()
        print(obj_attrs)
        obj_keys, obj_values = obj_attrs.keys(), obj_attrs.values()
        print(obj_keys, obj_values)
        obj_plug = ','.join('?' for _ in obj_keys)
        result = await self.conn.execute(f"INSERT INTO {self.table}{tuple(obj_keys)} VALUES ({obj_plug}) RETURNING *",
                                         tuple(obj_values))
        return self.model.from_list(result)
