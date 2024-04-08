import asyncio

from aiosqlite import OperationalError

from db.base import BaseTable


async def run_schema(schema_path: str) -> None:
    with open(schema_path, 'r') as f:
        schema = f.read()
    statements = schema.split(';')
    async with BaseTable() as connection:
        for statement in statements:
            try:
                await connection.raw_query(statement)
            except OperationalError as e:
                split_lines = f"\n{'-' * 10}\n"
                print(f'ERROR WHILE EXECUTING:{split_lines} {statement}{split_lines} Error:{split_lines}{str(e)}')


async def main():
    import os
    for f_name in os.listdir('schemas/'):
        if f_name.endswith('.sql'):
            await run_schema(f'schemas/{f_name}')

if __name__ == "__main__":
    asyncio.run(main())
