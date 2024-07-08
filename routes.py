from flask import Flask, request, jsonify, abort
from models import db, Admin, Company, Location, Sensor, SensorData
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

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

@app.route('/api/v1/sensor_data', methods=['POST'])
def add_sensor_data():
    data = request.get_json()
    sensor_api_key = data.get('api_key')
    sensor = Sensor.query.filter_by(sensor_api_key=sensor_api_key).first()
    if not sensor:
        return abort(400, 'Invalid sensor API key')
    
    sensor_data = data.get('json_data')
    for data_point in sensor_data:
        new_data = SensorData(sensor_id=sensor.id, json_data=data_point)
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
    app.run(debug=True)
