from flask import Flask, request, jsonify, g
from datetime import datetime
import sqlite3
import os
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

def get_db():
    """Get database connection for current request."""
    if 'db' not in g:
        g.db = sqlite3.connect(app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(error):
    """Close database connection at the end of request."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    """Initialize the database with required tables."""
    conn = sqlite3.connect(app.config['DATABASE'])
    try:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                completed BOOLEAN NOT NULL DEFAULT 0,
                priority TEXT CHECK(priority IN ('low', 'medium', 'high')) DEFAULT 'medium',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS todo_tags (
                todo_id INTEGER,
                tag_id INTEGER,
                FOREIGN KEY (todo_id) REFERENCES todos (id) ON DELETE CASCADE,
                FOREIGN KEY (tag_id) REFERENCES tags (id) ON DELETE CASCADE,
                PRIMARY KEY (todo_id, tag_id)
            )
        ''')
        conn.commit()
    finally:
        conn.close()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route('/todos', methods=['GET'])
def get_todos():
    """Get all todos with optional filtering."""
    db = get_db()

    # Query parameters for filtering
    completed = request.args.get('completed')
    priority = request.args.get('priority')

    query = 'SELECT * FROM todos WHERE 1=1'
    params = []

    if completed is not None:
        query += ' AND completed = ?'
        params.append(1 if completed.lower() == 'true' else 0)

    if priority:
        query += ' AND priority = ?'
        params.append(priority)

    query += ' ORDER BY created_at DESC'

    todos = db.execute(query, params).fetchall()

    return jsonify([dict(todo) for todo in todos]), 200

@app.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    """Get a specific todo by ID."""
    db = get_db()

    todo = db.execute('SELECT * FROM todos WHERE id = ?', (todo_id,)).fetchone()

    if todo is None:
        return jsonify({'error': 'Todo not found'}), 404

    # Get associated tags
    tags = db.execute('''
        SELECT t.name FROM tags t
        JOIN todo_tags tt ON t.id = tt.tag_id
        WHERE tt.todo_id = ?
    ''', (todo_id,)).fetchall()

    todo_dict = dict(todo)
    todo_dict['tags'] = [tag['name'] for tag in tags]

    return jsonify(todo_dict), 200

@app.route('/todos', methods=['POST'])
def create_todo():
    """Create a new todo."""
    data = request.get_json()

    if not data or 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400

    title = data['title']
    description = data.get('description', '')
    priority = data.get('priority', 'medium')
    tags = data.get('tags', [])

    if priority not in ['low', 'medium', 'high']:
        return jsonify({'error': 'Priority must be low, medium, or high'}), 400

    db = get_db()

    try:
        cursor = db.execute(
            'INSERT INTO todos (title, description, priority) VALUES (?, ?, ?)',
            (title, description, priority)
        )
        todo_id = cursor.lastrowid

        # Add tags if provided
        for tag_name in tags:
            # Get or create tag
            tag = db.execute('SELECT id FROM tags WHERE name = ?', (tag_name,)).fetchone()
            if tag is None:
                cursor = db.execute('INSERT INTO tags (name) VALUES (?)', (tag_name,))
                tag_id = cursor.lastrowid
            else:
                tag_id = tag['id']

            # Link tag to todo
            db.execute('INSERT INTO todo_tags (todo_id, tag_id) VALUES (?, ?)', (todo_id, tag_id))

        db.commit()

        # Fetch the created todo
        todo = db.execute('SELECT * FROM todos WHERE id = ?', (todo_id,)).fetchone()

        todo_dict = dict(todo)
        todo_dict['tags'] = tags

        return jsonify(todo_dict), 201
    except Exception as e:
        app.logger.error(f'Error creating todo: {e}')
        db.rollback()
        return jsonify({'error': 'An internal server error occurred'}), 500

@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    """Update an existing todo."""
    db = get_db()

    todo = db.execute('SELECT * FROM todos WHERE id = ?', (todo_id,)).fetchone()

    if todo is None:
        return jsonify({'error': 'Todo not found'}), 404

    data = request.get_json()

    title = data.get('title', todo['title'])
    description = data.get('description', todo['description'])
    completed = data.get('completed', todo['completed'])
    priority = data.get('priority', todo['priority'])
    tags = data.get('tags')  # Optional tags update

    if priority not in ['low', 'medium', 'high']:
        return jsonify({'error': 'Priority must be low, medium, or high'}), 400

    try:
        db.execute(
            '''UPDATE todos
               SET title = ?, description = ?, completed = ?, priority = ?, updated_at = CURRENT_TIMESTAMP
               WHERE id = ?''',
            (title, description, completed, priority, todo_id)
        )

        # Update tags if provided
        if tags is not None:
            # Remove existing tags
            db.execute('DELETE FROM todo_tags WHERE todo_id = ?', (todo_id,))

            # Add new tags
            for tag_name in tags:
                # Get or create tag
                tag = db.execute('SELECT id FROM tags WHERE name = ?', (tag_name,)).fetchone()
                if tag is None:
                    cursor = db.execute('INSERT INTO tags (name) VALUES (?)', (tag_name,))
                    tag_id = cursor.lastrowid
                else:
                    tag_id = tag['id']

                # Link tag to todo
                db.execute('INSERT INTO todo_tags (todo_id, tag_id) VALUES (?, ?)', (todo_id, tag_id))

        db.commit()

        # Fetch updated todo with tags
        updated_todo = db.execute('SELECT * FROM todos WHERE id = ?', (todo_id,)).fetchone()
        todo_tags = db.execute('''
            SELECT t.name FROM tags t
            JOIN todo_tags tt ON t.id = tt.tag_id
            WHERE tt.todo_id = ?
        ''', (todo_id,)).fetchall()

        result = dict(updated_todo)
        result['tags'] = [tag['name'] for tag in todo_tags]

        return jsonify(result), 200
    except Exception as e:
        app.logger.error(f'Error updating todo: {e}')
        db.rollback()
        return jsonify({'error': 'An internal server error occurred'}), 500

@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    """Delete a todo."""
    db = get_db()

    todo = db.execute('SELECT * FROM todos WHERE id = ?', (todo_id,)).fetchone()

    if todo is None:
        return jsonify({'error': 'Todo not found'}), 404

    try:
        db.execute('DELETE FROM todos WHERE id = ?', (todo_id,))
        db.commit()
        return jsonify({'message': 'Todo deleted successfully'}), 200
    except Exception as e:
        app.logger.error(f'Error deleting todo: {e}')
        db.rollback()
        return jsonify({'error': 'An internal server error occurred'}), 500

@app.route('/todos/<int:todo_id>/complete', methods=['POST'])
def complete_todo(todo_id):
    """Mark a todo as completed."""
    db = get_db()

    todo = db.execute('SELECT * FROM todos WHERE id = ?', (todo_id,)).fetchone()

    if todo is None:
        return jsonify({'error': 'Todo not found'}), 404

    try:
        db.execute(
            'UPDATE todos SET completed = 1, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
            (todo_id,)
        )
        db.commit()

        updated_todo = db.execute('SELECT * FROM todos WHERE id = ?', (todo_id,)).fetchone()
        return jsonify(dict(updated_todo)), 200
    except Exception as e:
        app.logger.error(f'Error completing todo: {e}')
        db.rollback()
        return jsonify({'error': 'An internal server error occurred'}), 500

@app.route('/stats', methods=['GET'])
def get_stats():
    """Get statistics about todos."""
    db = get_db()

    try:
        total = db.execute('SELECT COUNT(*) as count FROM todos').fetchone()['count']
        completed = db.execute('SELECT COUNT(*) as count FROM todos WHERE completed = 1').fetchone()['count']
        by_priority = db.execute('''
            SELECT priority, COUNT(*) as count
            FROM todos
            GROUP BY priority
        ''').fetchall()

        return jsonify({
            'total': total,
            'completed': completed,
            'pending': total - completed,
            'by_priority': {row['priority']: row['count'] for row in by_priority}
        }), 200
    except Exception as e:
        app.logger.error(f'Error getting stats: {e}')
        return jsonify({'error': 'An internal server error occurred'}), 500

if __name__ == '__main__':
    # Initialize database on startup
    init_db()

    # Run the application
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )
