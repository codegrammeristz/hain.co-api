from database_operation import DatabaseOperator

pg_cloud = DatabaseOperator()
cursor = pg_cloud.get_cursor()

cursor.execute('SELECT version()')

db_version = cursor.fetchone()

print(f'The DB version is {db_version}')
