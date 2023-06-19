import os
import json
import pymysql
import datetime


db_host     = os.environ['DB_HOST']
db_port     = os.environ['DB_PORT']
db_user     = os.environ['DB_USER']
db_password = os.environ['DB_PASSWORD']
db_name     = os.environ['DB_NAME']

db_connection = pymysql.connect(
  host=db_host,
  port=int(db_port),
  user=db_user,
  password=db_password,
  database=db_name
)


def response(status_code, body_message):
  return { 
    'statusCode': status_code, 
    'body': json.dumps(body_message)
  }


def lambda_handler(event, context):
  try:
    http_method = event['httpMethod']
    resource = event['resource']
    request_body = json.loads(event['body']) if http_method != 'GET' else None 
  except KeyError as err:
    return response(500, {'error': f'Bad key: {str(err)}'})
  except Exception as err:
    return response(500, {'error': str(err)})

  if http_method == 'GET' and resource == '/books':
    return get_books()
  elif http_method == 'POST' and resource == '/book':
    return add_book(request_body)
  elif http_method == 'PATCH' and resource == '/book':
    return update_book(request_body)
  elif http_method == 'DELETE' and resource == '/book':
    return delete_book(request_body)
  else:
    return response(404, {'message': 'Not Found'})


def add_book(request_body):
  try:
    book_name = request_body['name']

    with db_connection.cursor() as cursor:
      sql = "INSERT INTO books (book_name, end_time) VALUES (%s, %s)"
      current_time = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
      cursor.execute(sql, (book_name, current_time))

    db_connection.commit()

    return response(201, {'message': 'Book added successfully'})
  except Exception as err:
    return response(500, {'error': str(err)})


def get_books():
  try:
    with db_connection.cursor() as cursor:
      sql = "SELECT id, book_name, end_time FROM books"
      cursor.execute(sql)

    rows = cursor.fetchall()

    books = []
    for row in rows:
      books.append({
        'id': row[0],
        'name': row[1],
        'end_time': str(row[2]),
      })
  
    return response(200, books)
  except Exception as err:
    return response(500, {'error': str(err)})


def update_book(request_body):
  try:
    book_id = request_body['id']
    updated_name = request_body['name']

    with db_connection.cursor() as cursor:
      sql = "UPDATE books SET book_name = %s WHERE id = %s"
      rows_affected = cursor.execute(sql, (updated_name, book_id))

      db_connection.commit()
      return response(200, {
        'message': 'Book updated successfully',
        'updated': rows_affected
      })
  except Exception as err:
    return response(500, {'error': str(err)})


def delete_book(request_body):
  try:
    book_id = request_body['id']

    with db_connection.cursor() as cursor:
      sql = "DELETE FROM books WHERE id = %s"
      rows_affected = cursor.execute(sql, (book_id,))

    db_connection.commit()

    return response(200, {
      'message': 'Book deleted successfully',
      'deleted': rows_affected
    })
  except Exception as err:
    return response(500, {'error': str(err)})
