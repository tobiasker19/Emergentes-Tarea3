from flask import Flask, request, jsonify, abort
from config import Config
from models import db, Admin, Company, Location, Sensor, SensorData

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'API is running'}), 200

@app.route('/companies', methods=['POST'])
def create_company():
    data = request.get_json()
    new_company = Company(
        company_name=data['company_name'],
        company_api_key=data['company_api_key']
    )
    db.session.add(new_company)
    db.session.commit()
    return jsonify({'message': 'Company created successfully'}), 201

@app.route('/locations', methods=['POST'])
def create_location():
    data = request.get_json()
    new_location = Location(
        company_id=data['company_id'],
        location_name=data['location_name'],
        location_country=data['location_country'],
        location_city=data['location_city'],
        location_meta=data['location_meta']
    )
    db.session.add(new_location)
    db.session.commit()
    return jsonify({'message': 'Location created successfully'}), 201

@app.route('/locations/<int:id>', methods=['GET'])
def get_location(id):
    location = Location.query.get_or_404(id)
    return jsonify({
        'company_id': location.company_id,
        'location_name': location.location_name,
        'location_country': location.location_country,
        'location_city': location.location_city,
        'location_meta': location.location_meta
    })

@app.route('/locations', methods=['GET'])
def get_locations():
    locations = Location.query.all()
    return jsonify([{
        'company_id': location.company_id,
        'location_name': location.location_name,
        'location_country': location.location_country,
        'location_city': location.location_city,
        'location_meta': location.location_meta
    } for location in locations])

@app.route('/locations/<int:id>', methods=['PUT'])
def update_location(id):
    data = request.get_json()
    location = Location.query.get_or_404(id)
    location.location_name = data['location_name']
    location.location_country = data['location_country']
    location.location_city = data['location_city']
    location.location_meta = data['location_meta']
    db.session.commit()
    return jsonify({'message': 'Location updated successfully'})

@app.route('/locations/<int:id>', methods=['DELETE'])
def delete_location(id):
    location = Location.query.get_or_404(id)
    db.session.delete(location)
    db.session.commit()
    return jsonify({'message': 'Location deleted successfully'})

@app.route('/sensors', methods=['POST'])
def create_sensor():
    data = request.get_json()
    new_sensor = Sensor(
        location_id=data['location_id'],
        sensor_name=data['sensor_name'],
        sensor_category=data['sensor_category'],
        sensor_meta=data['sensor_meta'],
        sensor_api_key=data['sensor_api_key']
    )
    db.session.add(new_sensor)
    db.session.commit()
    return jsonify({'message': 'Sensor created successfully'}), 201

@app.route('/sensors/<int:id>', methods=['GET'])
def get_sensor(id):
    sensor = Sensor.query.get_or_404(id)
    return jsonify({
        'location_id': sensor.location_id,
        'sensor_name': sensor.sensor_name,
        'sensor_category': sensor.sensor_category,
        'sensor_meta': sensor.sensor_meta,
        'sensor_api_key': sensor.sensor_api_key
    })

@app.route('/sensors', methods=['GET'])
def get_sensors():
    sensors = Sensor.query.all()
    return jsonify([{
        'location_id': sensor.location_id,
        'sensor_name': sensor.sensor_name,
        'sensor_category': sensor.sensor_category,
        'sensor_meta': sensor.sensor_meta,
        'sensor_api_key': sensor.sensor_api_key
    } for sensor in sensors])

@app.route('/sensors/<int:id>', methods=['PUT'])
def update_sensor(id):
    data = request.get_json()
    sensor = Sensor.query.get_or_404(id)
    sensor.sensor_name = data['sensor_name']
    sensor.sensor_category = data['sensor_category']
    sensor.sensor_meta = data['sensor_meta']
    db.session.commit()
    return jsonify({'message': 'Sensor updated successfully'})

@app.route('/sensors/<int:id>', methods=['DELETE'])
def delete_sensor(id):
    sensor = Sensor.query.get_or_404(id)
    db.session.delete(sensor)
    db.session.commit()
    return jsonify({'message': 'Sensor deleted successfully'})

@app.route('/api/v1/sensor_data', methods=['POST'])
def add_sensor_data():
    data = request.get_json()
    sensor_api_key = data.get('api_key')
    sensor = Sensor.query.filter_by(sensor_api_key=sensor_api_key).first()
    if not sensor:
        return abort(400, 'Invalid sensor API key')

    sensor_data = data.get('json_data')
    for data_point in sensor_data:
        timestamp = data_point.get('timestamp')
        if timestamp is None:
            return abort(400, 'Missing timestamp in sensor data')
        new_data = SensorData(sensor_id=sensor.id, json_data=data_point, timestamp=timestamp)
        db.session.add(new_data)
    db.session.commit()
    return jsonify({'message': 'Data added successfully'}), 201

@app.route('/api/v1/sensor_data', methods=['GET'])
def get_sensor_data():
    company_api_key = request.args.get('company_api_key')
    from_epoch = request.args.get('from')
    to_epoch = request.args.get('to')
    sensor_ids = request.args.getlist('sensor_id')
    
    company = Company.query.filter_by(company_api_key=company_api_key).first()
    if not company:
        return abort(400, 'Invalid company API key')

    query = SensorData.query.filter(
        SensorData.sensor_id.in_(sensor_ids),
        SensorData.timestamp.between(from_epoch, to_epoch)
    )
    results = query.all()
    return jsonify([data.json_data for data in results])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
