from flask import Flask, request, render_template
app = Flask(__name__)
file_path = "./sensors_data.csv"
my_port = 19237
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

#To monitor temperature data
#def temperature_monitoring(time, temperature):
#    if temperature > 37.2 & temperature <= 39.9:
#        highTemp = [38, 39]
#        Htemp = temperature.count(highTemp)
#        if Htemp >= 30:
#            return "熱"
#    elif temperature >= 40:
#        feverTemp = 40
 #       Ftemp = temperature.count(feverTemp)
  #      if Ftemp >= 30:
   #         return "High 熱"
    #elif temperature < 31:
     #   lowTemp = 30
      #  Ltemp = temperature.count(lowTemp)
       # if Ltemp >= 30:
        #    return "Low body temperature is occured" 

#fuzzy set 
#pulse = ctrl.Antecedent(np.arange(0, 160, 80), 'pulse')
#temperature = ctrl.Antecedent(np.arange(0, 40, 30), 'temperature')
#arrhythmia = ctrl.Consequent(np.arrange(0, 100, 60), 'arrhythmia')


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
