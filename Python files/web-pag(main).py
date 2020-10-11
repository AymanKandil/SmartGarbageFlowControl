
from flask import Flask, render_template, request,jsonify,redirect
from datetime import datetime
from db_interface import DBInterface
#import RPi.GPIO as GPIO
import time

app = Flask(__name__)


#GPIO.setmode(GPIO.BOARD)
#ayman_pin=15
#kandari_pin = 11
#mohamed_pin = 13
#enezi_pin=37

#GPIO.setup(ayman_pin, GPIO.OUT)
#p=GPIO.PWM(ayman_pin,50)
#p.start(0)

#GPIO.setup(kandari_pin, GPIO.OUT)
#p=GPIO.PWM(kandari_pin,50)
#q.start(0)

#GPIO.setup(mohamed_pin, GPIO.OUT)
#p=GPIO.PWM(mohamed_pin,50)
#s.start(0)

#GPIO.setup(enezi_pin, GPIO.OUT)
#p=GPIO.PWM(enezi_pin,50)
#u.start(0)


@app.route('/home')
def hello():
    db = DBInterface("garbage.db")
    bins = db.getAllBins() 
    if not bins:
        bins = []

    print(bins)
    data = []
    for bin_ in bins:
        distances = db.selectDistance(bin_[0])
        data.append((bin_[0], bin_[1], bin_[2], distances[-1][2]))
    print(data)
    return render_template('home.html', data=data)

@app.route('/bin/<source_id>')
def bin(source_id):
    db = DBInterface("garbage.db")
    bin_data = db.selectBinBySource(source_id)
    distance_data = db.selectDistance(source_id)
    if not distance_data:
        distance_data = []
    if not bin_data:
        bin_data = [None, None]
    db.close()

    label = []
    data = []
    for i in distance_data:
        dt_object = datetime.fromtimestamp(i[1])
        label.append("{}-{}".format(dt_object.day, dt_object.month))
        data.append(i[2])
    print(label)
    print(data)
    return render_template('bin.html', name=bin_data[1], label=label, data=data)


#@app.route('/servo',methods= ["POST"])
#def servo():
#    Btn=request.form["button1"]
    
 #   p.ChangeDutyCycle(15)
  #  time.sleep(0.3)
   # p.ChangeDutyCycle(0)
    #time.sleep(0.3)
    #p.stop()
    #GPIO.cleanup()
    #return redirect(request.referrer)
#@app.route('/servo2',methods= ["POST"])
#def servo2():

 #   Btn2=request.form["button2"]
  #  q.ChangeDutyCycle(8)
  #  time.sleep(0.3)
  #  q.ChangeDutyCycle(0)
   # time.sleep(0.3)
    #q.stop()
    #GPIO.cleanup()
    #return redirect(request.referrer)
#@app.route('/servo3',methods= ["POST"])
#def servo3():
 #   Btn3=request.form["button3"]
  #  s.ChangeDutyCycle(15)
   # time.sleep(0.3)
    #s.ChangeDutyCycle(0)
    #time.sleep(0.3)
    #s.stop()
    #GPIO.cleanup()
    #return redirect(request.referrer)
#@app.route('/servo4',methods= ["POST"])
#def servo4():
 #   Btn4=request.form["button4"]
  #  u.ChangeDutyCycle(15)
   # time.sleep(0.3)
    #u.ChangeDutyCycle(0)
    #time.sleep(0.3)
    #u.stop()
    #GPIO.cleanup()
    #return redirect(request.referrer)


@app.route('/bins')
def bins():
    db = DBInterface("garbage.db")
    binss = db.getAllBins() 
    if not binss:
        binss = []
    names =[]
    labels = []
    datas = []
   
    for bin_ in binss:
        bin_data = db.selectBinBySource(bin_[0])
        distance_data = db.selectDistance(bin_[0])
        if not distance_data:
            distance_data = []
        if not bin_data:
            bin_data = [None, None]
        

        label = []
        data = []
        for i in distance_data:
            dt_object = datetime.fromtimestamp(i[1])
            label.append("{}-{}-time: {}".format(dt_object.day, dt_object.month, dt_object.hour))
            data.append(i[2])
        print(label)
        print(data)
        names.append(bin_data[1])
        labels.append(label)
        datas.append(data)
    db.close()
    return render_template('bins.html', name=names[0], label=labels[0], data=datas[0],name2=names[1], label2=labels[1], data2=datas[1],name3=names[2], label3=labels[2], data3=datas[2],name4=names[3], label4=labels[3], data4=datas[3])


@app.route('/jbins')
def jbins():
    db = DBInterface("garbage.db")
    binss = db.getAllBins() 
    if not binss:
        binss = []
    names =[]
    labels = []
    datas = []
   
    for bin_ in binss:
        bin_data = db.selectBinBySource(bin_[0])
        distance_data = db.selectDistance(bin_[0])
        if not distance_data:
            distance_data = []
        if not bin_data:
            bin_data = [None, None]
        

        label = []
        data = []
        for i in distance_data:
            dt_object = datetime.fromtimestamp(i[1])
            label.append("Date-{}-{}-Time: {}-{}".format(dt_object.day, dt_object.month, dt_object.hour, dt_object.minute))
            data.append(i[2])
        
        names.append(bin_data)
        labels.append(label)
        datas.append(data)
        
    jse1={
            "bin1":{
                "bin1_la":labels[0],
                "bin1_da":datas[0]
            },
            "bin2":{
                "bin2_la":labels[1],
                "bin2_da":datas[1]
            },
            "bin3":{
                "bin3_la":labels[2],
                "bin3_da":datas[2]
            },
            "bin4":{
                "bin4_la":labels[3],
                "bin4_da":datas[3]
            }
    }
    db.close()
    return jsonify(jse1)

@app.route('/create', methods=["POST"])
def add_bin():
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        print(name, description)

        db = DBInterface("garbage.db")
        source_id = db.insertBin(name, description)
        db.close()
    return str(source_id)

@app.route('/add/<source_id>', methods=["POST"])
def add_distance(source_id):
    if request.method == "POST":
        timestamp = request.form.get("timestamp")
        distance_value = request.form.get("distance_value")
        print(timestamp, distance_value)

        db = DBInterface("garbage.db")
        db.insertDistance(timestamp, distance_value, source_id)
        db.close()
    return "test"

if __name__ == '__main__':
    app.run(debug=True)





