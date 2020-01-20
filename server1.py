from flask import Flask, request, render_template
app = Flask(__name__)
file_path = "./sensors_data.csv"
my_port = 19237
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import csv

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
    fuzzy_process()
    try:
        #write data to csv file
        f = open(file_path, 'w')
        f.write(time + "," + pulse + "," + temperature)
        #with open(file_path, 'w') as f:
        #    _writer = csv.writer(f)
        #    _writer = f.write(time + "," + sensors)
        return "success to write"
    except Exception as e:
        print(e)
        return "fail to write"
    finally:
        f.close()

#fuzzy Logic 
def fuzzy_process():
    pulse = request.form["pulse"]
    temperature = request.form["temperature"]

    pulse = ctrl.Antecedent(np.arange(0, 160, 80), 'pulse')
    temperature = ctrl.Antecedent(np.arange(0, 40, 30), 'temperature')
    arrhythmia = ctrl.Consequent(np.arrange(0, 100, 60), 'arrhythmia')

    pulse.automf(3)
    temperature.automf(3)
    
    #Pythonic API
    arrhythmia['low'] = fuzz.trimf(arrhythmia.universe, [0,0,60])
    arrhythmia['non'] = fuzz.trimf(arrhythmia.universe, [60, 80, 100])
    arrhythmia['high'] = fuzz.trimf(arrhythmia.universe, [100,120,120])
    
    #fuzzy rule
    rule1 = ctrl.Rule(pulse['low'] & temperature['high'], arrhythmia['low'])
    rule2 = ctrl.Rule(pulse['normal'] & temperature['normal'], arrhythmia['non'])
    rule3 = ctrl.Rule(pulse['high'] & temperature['high'], temperature['high'])
    #control rule
    arrhythmia_control = ctrl.ControlSystem([rule1, rule2, rule3])
    arrhythmia = ctrl.ControlSystemSimulation(arrhythmia_control)
    
    arrhythmia.input['pulse'] = pulse
    arrhythmia.input['temperature'] = temperature
    arrhythmia.compute()
    print(arrhythmia.output['arrhythmia'])

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
