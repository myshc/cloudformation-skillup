import os

os.environ['DB_HOST'] = 'localhost'
os.environ['DB_PORT'] = '3306'
os.environ['DB_USER'] = 'root'
os.environ['DB_PASSWORD'] = 'passw0rd'
os.environ['DB_NAME'] = 'books'


import booksapi

def test_add_book():
  for i in range(10):
    booksapi.lambda_handler(
      event={
        'httpMethod': 'POST',
        'resource': '/book',
        'body': {
          'name': 'book' + str(i)
        }
      },
      context=0
    )

def test_update_book():
  upd = {
    'id': 1,
    'name': 'bookname1'
  }
  print(booksapi.update_book(upd))


def test_get_books():
  return booksapi.lambda_handler(
    event={
        'httpMethod': 'GET',
        'resource': '/books'
    },
    context=0
  )

if __name__ == '__main__':
  #test_update_book()
  print(test_get_books())
