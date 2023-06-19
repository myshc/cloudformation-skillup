const api = require('./api')

const test_get_books = async () => {
  const res = await api.lambda_handler({
        'httpMethod': 'GET',
        'resource': '/books'
  },
  0);

  console.log(res);
}

test_get_books();
