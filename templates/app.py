from flask import Flask , render_template, jsonify, request, redirect, url_for, jsonify,make_response
from flask_sqlalchemy import SQLAlchemy
import joblib,json
model = joblib.load("model.sav")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new.db' 
app.config['SQLALCHEMY_TRACK_MODIFICaTIONS']=False
db = SQLAlchemy(app)

class VALUES(db.Model):
    place = db.Column(db.String(80), primary_key=True)
    state = db.Column(db.String(80), primary_key=True)
    lat = db.Column(db.Float, unique=False, nullable=False)
    lon  = db.Column(db.Float, unique=False, nullable=False)
    power = db.Column(db.Float, unique=False, nullable=False)
    ws  =  db.Column(db.Float, unique=False, nullable=False)
    wd = db.Column(db.Float, unique=False, nullable=False)

class MAPFETCH(db.Model):
    place = db.Column(db.String(80), primary_key=True)
    state = db.Column(db.String(80), primary_key=True)
    lat = db.Column(db.Float, unique=False, nullable=False)
    lon  = db.Column(db.Float, unique=False, nullable=False)
    power = db.Column(db.Float, unique=False, nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_map_data', methods=['GET'])
def get_map_data():
    try:
        # Fetch all rows from MAPFETCH
        map_data = MAPFETCH.query.all()
        data_list = [{'place': row.place, 'state': row.state, 'lat': row.lat, 'lon': row.lon, 'power': row.power} for row in map_data]
        return jsonify({'success': True, 'data': data_list})
    except Exception as e:
        print(f'Error fetching map data: {str(e)}')
        return jsonify({'success': False, 'message': 'Error fetching map data'})



@app.route('/insights')
def insights():
    states = db.session.query(VALUES.state).distinct().all()
    j_array = request.cookies.get('A_c')
    my_array = []
    if j_array:
        my_array = json.loads(j_array)

    return render_template('insights.html', l=my_array, states=states)
    

@app.route('/clear_map_data', methods=['POST'])
def clear_map_data():
        # Delete all rows in MAPFETCH
    MAPFETCH.query.delete()
    db.session.commit()

@app.route('/predict', methods=['POST'])
def predict():
    # Extract input features from the request
    feature1 = float(request.form['wd'])
    feature2 = float(request.form['ws'])

    # Preprocess the input features
    # Make predictions using the loaded model
    prediction = model.predict([[feature1, feature2]])

    return render_template('index.html', prediction=round(prediction[0],3))

@app.route('/get_places/<selected_state>', methods=['GET'])
def get_places(selected_state):
    places = db.session.query(VALUES.place).filter_by(state=selected_state).distinct().all()
    return jsonify({'places': [place[0] for place in places]})





@app.route('/get_coordinates', methods=['POST'])
def get_coordinates():
    place = request.form.get('place')
    state = request.form.get('state')

    # Fetch coordinates for the specified place and state
    coordinates = VALUES.query.filter_by(place=place, state=state).first()

    if coordinates:
        new_map_data = MAPFETCH(
            place=coordinates.place,
            state=coordinates.state,
            lat=coordinates.lat,
            lon=coordinates.lon,
            power=coordinates.power
        )
        db.session.add(new_map_data)
        db.session.commit()

        return jsonify({'lat': coordinates.lat, 'lon': coordinates.lon, 'power': coordinates.power})

    else:
        print('Coordinates not found')
        return jsonify({'error': 'Coordinates not found'})


if __name__ == '__main__':
    app.run(debug=True)