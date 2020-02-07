from flask import Flask, request, render_template
app = Flask(__name__)
file_path = "./sensors_data.csv"
my_port = 19237

#retrieve HTML to web browser
@app.route('/', methods=['GET'])
def get_html():
    try:
        f = open(file_path, 'r')
        for row in f:
            sensors = row
    except Exception as e:
        print(e)
        return e
    finally:
        f.close()
    data = sensors.split(',')
    return render_template('./index.html', data = data)

#receive & update sensor data
@app.route('/him', methods=['POST'])
def update_data():
    time = request.form["time"]
    pulse = request.form["pulse"]
    temperature = request.form["temperature"]
    condition = request.form["condition"]
    try:
        #write data to csv file
        f = open(file_path, 'w')
        f.write(time + "," + pulse + "," + temperature + "," + condition)
        #with open(file_path, 'w') as f:
        #    _writer = csv.writer(f)
        #    _writer = f.write(time + "," + sensors)
        return "success to write"
    except Exception as e:
        print(e)
        return "fail to write"
    finally:
        f.close()

#reading & retrieve sensor data to web browser
@app.route('/him', methods=['GET'])
def get_data():
    try:
        f = open(file_path, 'r')
        for row in f:
            sensors = row
        return sensors
    except Exception as e:
        print(e)
        return e
    finally:
        f.close()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=my_port)
