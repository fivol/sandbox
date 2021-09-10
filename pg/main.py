import psycopg2

PG_URL = 'postgresql://postgres:postgres@localhost:5432'

connection = psycopg2.connect(PG_URL)

with connection.cursor() as curr:
    curr.execute('SELECT 1, 2, 3; SELECT 1')
    print(curr.fetchall())


if __name__ == '__main__':
    pass
