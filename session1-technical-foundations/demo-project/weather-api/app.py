from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import json
import os
import random
import hashlib
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Get configuration from app config
CACHE_DIR = app.config['CACHE_DIR']
CACHE_DURATION = timedelta(minutes=app.config['CACHE_DURATION_MINUTES'])

# Simulated weather conditions
WEATHER_CONDITIONS = ['sunny', 'cloudy', 'rainy', 'snowy', 'windy', 'foggy']
CITIES_DATA = {
    'taipei': {'lat': 25.0330, 'lon': 121.5654, 'country': 'TW'},
    'tokyo': {'lat': 35.6762, 'lon': 139.6503, 'country': 'JP'},
    'london': {'lat': 51.5074, 'lon': -0.1278, 'country': 'GB'},
    'newyork': {'lat': 40.7128, 'lon': -74.0060, 'country': 'US'},
    'paris': {'lat': 48.8566, 'lon': 2.3522, 'country': 'FR'},
    'sydney': {'lat': -33.8688, 'lon': 151.2093, 'country': 'AU'},
}

def ensure_cache_dir():
    """Ensure cache directory exists."""
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)

def get_cache_key(city):
    """Generate a cache key for a city."""
    return hashlib.md5(city.lower().encode()).hexdigest()

def get_cache_path(cache_key):
    """Get the full path for a cache file."""
    return os.path.join(CACHE_DIR, f'{cache_key}.json')

def read_cache(cache_key):
    """Read data from cache."""
    cache_path = get_cache_path(cache_key)

    if not os.path.exists(cache_path):
        return None

    try:
        with open(cache_path, 'r') as f:
            data = json.load(f)

        # Check if cache is expired
        cached_time = datetime.fromisoformat(data['cached_at'])
        if datetime.now() - cached_time > CACHE_DURATION:
            # Cache expired, delete file
            os.remove(cache_path)
            return None

        return data
    except (json.JSONDecodeError, KeyError, ValueError, OSError) as e:
        # Invalid cache file, delete it
        app.logger.warning(f'Could not read cache file {cache_path}: {e}')
        if os.path.exists(cache_path):
            try:
                os.remove(cache_path)
            except OSError:
                pass
        return None

def write_cache(cache_key, data):
    """Write data to cache."""
    ensure_cache_dir()
    cache_path = get_cache_path(cache_key)

    cache_data = {
        'data': data,
        'cached_at': datetime.now().isoformat()
    }

    try:
        with open(cache_path, 'w') as f:
            json.dump(cache_data, f, indent=2)
    except OSError as e:
        app.logger.error(f'Could not write cache file {cache_path}: {e}')

def generate_weather_data(city):
    """Generate simulated weather data for a city."""
    if city.lower() not in CITIES_DATA:
        return None

    city_info = CITIES_DATA[city.lower()]

    # Generate random but consistent-ish weather data
    random.seed(int(datetime.now().timestamp() / 3600) + hash(city))

    weather_data = {
        'city': city.title(),
        'country': city_info['country'],
        'coordinates': {
            'lat': city_info['lat'],
            'lon': city_info['lon']
        },
        'temperature': {
            'current': round(random.uniform(-5, 35), 1),
            'feels_like': round(random.uniform(-5, 35), 1),
            'min': round(random.uniform(-5, 25), 1),
            'max': round(random.uniform(15, 40), 1)
        },
        'condition': random.choice(WEATHER_CONDITIONS),
        'humidity': random.randint(30, 90),
        'pressure': random.randint(980, 1030),
        'wind_speed': round(random.uniform(0, 20), 1),
        'visibility': random.randint(1, 10),
        'timestamp': datetime.now().isoformat()
    }

    return weather_data

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'cache_dir': CACHE_DIR,
        'cache_duration_minutes': CACHE_DURATION.total_seconds() / 60,
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route('/weather/<city>', methods=['GET'])
def get_weather(city):
    """Get weather data for a specific city."""
    if city.lower() not in CITIES_DATA:
        return jsonify({
            'error': f'City not found: {city}',
            'available_cities': list(CITIES_DATA.keys())
        }), 404

    # Check cache first
    cache_key = get_cache_key(city)
    cached_data = read_cache(cache_key)

    if cached_data:
        response = cached_data['data']
        response['source'] = 'cache'
        response['cached_at'] = cached_data['cached_at']
        return jsonify(response), 200

    # Generate new weather data
    weather_data = generate_weather_data(city)
    weather_data['source'] = 'fresh'

    # Cache the data
    write_cache(cache_key, weather_data)

    return jsonify(weather_data), 200

@app.route('/weather', methods=['GET'])
def get_all_weather():
    """Get weather data for all cities."""
    cities = request.args.get('cities')

    if cities:
        city_list = [c.strip() for c in cities.split(',')]
    else:
        city_list = list(CITIES_DATA.keys())

    weather_list = []
    for city in city_list:
        if city.lower() not in CITIES_DATA:
            continue

        cache_key = get_cache_key(city)
        cached_data = read_cache(cache_key)

        if cached_data:
            data = cached_data['data']
            data['source'] = 'cache'
        else:
            data = generate_weather_data(city)
            data['source'] = 'fresh'
            write_cache(cache_key, data)

        weather_list.append(data)

    return jsonify({
        'count': len(weather_list),
        'cities': weather_list
    }), 200

@app.route('/weather/<city>/forecast', methods=['GET'])
def get_forecast(city):
    """Get 5-day forecast for a city."""
    if city.lower() not in CITIES_DATA:
        return jsonify({
            'error': f'City not found: {city}',
            'available_cities': list(CITIES_DATA.keys())
        }), 404

    try:
        days = int(request.args.get('days', 5))
    except ValueError:
        return jsonify({'error': 'Days must be a valid integer'}), 400

    if days < 1 or days > 10:
        return jsonify({'error': 'Days must be between 1 and 10'}), 400

    forecast = []
    for i in range(days):
        date = datetime.now() + timedelta(days=i)
        random.seed(int(date.timestamp() / 3600) + hash(city))

        forecast.append({
            'date': date.strftime('%Y-%m-%d'),
            'temperature': {
                'min': round(random.uniform(-5, 25), 1),
                'max': round(random.uniform(15, 40), 1)
            },
            'condition': random.choice(WEATHER_CONDITIONS),
            'humidity': random.randint(30, 90),
            'wind_speed': round(random.uniform(0, 20), 1)
        })

    return jsonify({
        'city': city.title(),
        'forecast': forecast
    }), 200

@app.route('/cache/info', methods=['GET'])
def cache_info():
    """Get information about the cache."""
    ensure_cache_dir()

    try:
        cache_files = [f for f in os.listdir(CACHE_DIR) if f.endswith('.json')]
        total_size = sum(os.path.getsize(os.path.join(CACHE_DIR, f)) for f in cache_files)
    except OSError as e:
        app.logger.error(f'Error accessing cache directory: {e}')
        return jsonify({'error': 'Could not access cache directory'}), 500

    cache_entries = []
    for cache_file in cache_files:
        try:
            with open(os.path.join(CACHE_DIR, cache_file), 'r') as f:
                data = json.load(f)
                cached_at = datetime.fromisoformat(data['cached_at'])
                age = datetime.now() - cached_at
                cache_entries.append({
                    'city': data['data'].get('city', 'Unknown'),
                    'cached_at': data['cached_at'],
                    'age_minutes': round(age.total_seconds() / 60, 1),
                    'expired': age > CACHE_DURATION
                })
        except (json.JSONDecodeError, KeyError, OSError, ValueError) as e:
            app.logger.warning(f'Could not process cache file {cache_file}: {e}')
            continue

    return jsonify({
        'cache_dir': CACHE_DIR,
        'total_entries': len(cache_files),
        'total_size_bytes': total_size,
        'cache_duration_minutes': CACHE_DURATION.total_seconds() / 60,
        'entries': cache_entries
    }), 200

@app.route('/cache/clear', methods=['POST'])
def clear_cache():
    """Clear all cache files."""
    ensure_cache_dir()

    try:
        cache_files = [f for f in os.listdir(CACHE_DIR) if f.endswith('.json')]
    except OSError as e:
        app.logger.error(f'Error accessing cache directory: {e}')
        return jsonify({'error': 'Could not access cache directory'}), 500

    cleared = 0
    for cache_file in cache_files:
        try:
            os.remove(os.path.join(CACHE_DIR, cache_file))
            cleared += 1
        except OSError as e:
            app.logger.warning(f'Could not remove cache file {cache_file}: {e}')
            continue

    return jsonify({
        'message': f'Cleared {cleared} cache entries',
        'cleared': cleared
    }), 200

@app.route('/cache/<city>', methods=['DELETE'])
def delete_cache(city):
    """Delete cache for a specific city."""
    cache_key = get_cache_key(city)
    cache_path = get_cache_path(cache_key)

    if not os.path.exists(cache_path):
        return jsonify({'error': 'Cache not found for this city'}), 404

    try:
        os.remove(cache_path)
        return jsonify({
            'message': f'Cache cleared for {city}',
            'city': city
        }), 200
    except OSError as e:
        app.logger.error(f'Error deleting cache file: {e}')
        return jsonify({'error': 'Could not delete cache file'}), 500

@app.route('/cities', methods=['GET'])
def get_cities():
    """Get list of available cities."""
    cities = []
    for city, info in CITIES_DATA.items():
        cities.append({
            'name': city,
            'country': info['country'],
            'coordinates': {
                'lat': info['lat'],
                'lon': info['lon']
            }
        })

    return jsonify({
        'count': len(cities),
        'cities': cities
    }), 200

if __name__ == '__main__':
    # Ensure cache directory exists
    ensure_cache_dir()

    # Run the application
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )
