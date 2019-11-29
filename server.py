from flask import Flask, request, render_template
app = Flask(__name__)
file_path = "./temp_data.csv"
my_port = 19237
import csv

#retrieve HTML to web browser
@app.route('/him', methods=['GET'])
def get_html():
    try:
        f = open(file_path, 'r')
        for row in f:
            temperature = row
        return temperature
    except Exception as e:
        print(e)
        return e
    finally:
        f.close()
    data = temperature.split(',')
    return render_template('./index.html', data = data)

#receive & update sensor data
@app.route('/him', methods=['POST'])
def update_data():
    time = request.form["time"]
    temperature = request.form["temperature"]
    try:
        #write data to csv file
        with open(file_path, 'w') as f:
            _writer = csv.writer(f)
            _writer = f.write(time + "," + temperature)
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
            temperature = row
        return temperature
    except Exception as e:
        print(e)
        return e
    finally:
        f.close()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=my_port)
