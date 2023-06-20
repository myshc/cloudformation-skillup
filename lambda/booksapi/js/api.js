const mysql = require('mysql2/promise');
const moment = require('moment-timezone');

process.env.DB_HOST = 'localhost'
process.env.DB_PORT = '3306'
process.env.DB_USER = 'root'
process.env.DB_PASSWORD = 'passw0rd'
process.env.DB_NAME = 'books'

const db_host     = process.env.DB_HOST;
const db_port     = process.env.DB_PORT;
const db_user     = process.env.DB_USER;
const db_password = process.env.DB_PASS;
const db_name     = process.env.DB_NAME;


const db_connection = mysql.createConnection({
  host: db_host,
  port: parseInt(db_port),
  user: db_user,
  password: db_password,
  database: db_name
});

const response = (status_code, body_message) => {
  return { 
    'statusCode': status_code, 
    'body': JSON.stringify(body_message)
  };
}


exports.lambda_handler = async (event, context) => {
  try {
    const http_method = event.httpMethod;
    const resource = event.resource;
    const request_body = http_method !== 'GET' ? JSON.parse(event.body) : null;
    
    if (http_method === 'GET' && resource === '/book') {
      return get_books();
    } else if (http_method === 'POST' && resource === '/book') {
      return add_book(request_body);
    } else if (http_method === 'PATCH' && resource === '/book') {
      return update_book(request_body);
    } else if (http_method === 'DELETE' && resource === '/book') {
      return delete_book(request_body);
    } else {
      return response(404, {'message': 'Not Found'});
    }
  } catch (err) {
    return response(500, {'error': err.toString()});
  }
};


const add_book = async (request_body) => {
  try {
    const book_name = request_body.name;

    const sql = "INSERT INTO books (book_name, end_time) VALUES (?, ?)";
    const current_time = moment().format('%Y-%m-%d %H-%M-%S');
    await db_connection.query(sql, [book_name, current_time]);

    return response(201, {'message': 'Book added successfully'});
  } catch (err) {
    return response(500, {'error': err.toString()});
  }
}


const get_books = async () => {
  try {
    const sql = "SELECT id, book_name, end_time FROM books";
    const [rows] = await db_connection.query(sql);

    const books = rows.map(row => {
      return {
        'id': row.id,
        'name': row.book_name,
        'end_time': row.end_time.toString()
      };
    });

    return response(200, books);
  } catch (err) {
    return response(500, {'error': err.toString()});
  }
}


const update_book = async (request_body) => {
  try {
    const book_id = request_body.id;
    const updated_name = request_body.name;

    const sql = "UPDATE books SET book_name = ? WHERE id = ?";
    const [rows_affected] = await db_connection.query(sql, [updated_name, book_id]);

    return response(200, {
      'message': 'Book updated successfully',
      'updated': rows_affected.affectedRows
    });
  } catch (err) {
    return response(500, {'error': err.toString()});
  }
}


const delete_book = async (request_body) => {
  try {
    const book_id = request_body.id;

    const sql = "DELETE FROM books WHERE id = ?";
    const [rows_affected] = await db_connection.query(sql, [book_id]);

    return response(200, {
      'message': 'Book deleted successfully',
      'deleted': rows_affected.affected
    });
  } catch (err) {
    return response(500, {'error': err.toString()});
  }
}
