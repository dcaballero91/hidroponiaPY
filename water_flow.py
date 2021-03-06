import RPi.GPIO as GPIO
import time,sys, datetime
import psycopg2
from psycopg2.extras import execute_values
import mysql.connector

'''
Configure raspberry
'''

GPIO.setmode(GPIO.BCM)
inpt = 26
GPIO.setup(inpt,GPIO.IN)

'''
Configure some global variables
'''

current_input = GPIO.input(inpt)                        # This is used to compare to the new_input later.
total_rotations = 0                                     # This is a counter. It gets reset after the number of seconds in rotation_downtime.
cup_movements = 200                                     # This is how many rotations occur as a cup of liquid passes through.
rotation_downtime = 5                                   # Sets the cut-off time for establishing a water-flow event.
last_movement_time = time.time() + rotation_downtime    # This is used to determine if a new water-flow event should be created.
record_data = False                                     # A flag used to trigger database insert.




print('Control C to exit')

def commit_data(conn):
    

    '''
    This passes data to the data base as a single row. It then resets/empties data.
    '''

    cur = conn.cursor()
    insert_statement = "INSERT INTO flow ('datetime','movements','cups','gallons') VALUES %s".replace("'",'')
    execute_values(cur,insert_statement)
    conn.commit()
    print ('Data sent.')
    cur.close()
    

def prep_and_send(total_rotations):
    global menRes,codRes
    try:
        db=mysql.connector.connect(host='localhost',user='root',passwd='sup3rPw#',database='hidroponia')
    except Exception as e:
        print("ERROR EN: connect db local",str(e))
        codRes= 'ERROR'
        menRes = str(e)
    try:
        db2=mysql.connector.connect(host='5.189.148.10',user='slave',passwd='sup3rPw#',database='hidroponia',port='23306',
                            ssl_ca='/etc/certs/ca.pem',ssl_cert='/etc/certs/client-cert.pem',ssl_key='/etc/certs/client-key2.pem')
    except Exception as e:
        print("ERROR EN: connect db web",str(e))
        codRes= 'ERROR'
        menRes = str(e)

    '''
    Calculates measurements (cups and gallons). Prepares the data into a database-friendly tuple. Appends that tuple to a list. 
    
    It then tries to connect to database. If it is not successful then it does nothing but saves the data; it will try to send 
    the list of data-tuples the next time there is a water-flow event. 
    
    Once the connection is successful data is emptied in commit_data().
    '''

    total_cups = total_rotations/cup_movements
    total_gallons = total_cups/16
    liters = total_gallons * 3.785412
    
    now = datetime.datetime.now() 
    print('{}: Movements: {}. \nCups: {}. \nLitros: {}'.format(now,total_rotations,total_cups,liters))

   
    try:                
        '''
        Establish connection with Db and try to insert.
        '''
        cursor=db.cursor() 
        #Se obtiene pin gpio
        sql="select sensor.id_sensor from sensor inner join station on sensor.id_est = station.id_est where sensor.nombre=%s and sensor.ubi=%s"
        nombre=('flow','central')
        cursor.execute(sql,nombre)
        result=cursor.fetchall()
        #Se convierte a string el resultado del select para poder insertar 
        x=(result[0])
        y = ''.join(map(str,x))
        s=(y)
        print(s)
        sql="insert into flow_meter (movements,cups,litros,id_sensor) values(%s,%s,%s,%s)"
        val=(total_rotations,total_cups,liters,s)
        cursor.execute(sql,val)
        db.commit()
        db.close()
        print(cursor.rowcount,"insertado correctamente local")
        cursor=db2.cursor()
        sql="insert into flow_meter (movements,cups,litros,id_sensor) values(%s,%s,%s,%s)"
        val=(total_rotations,total_cups,liters,s)
        cursor.execute(sql,val)
        db2.commit()
        db2.close()
        print(cursor.rowcount,"insertado correctamente web")
       
        
    except Exception as e:
        '''In case of error does not reset data to [] (see commit_data).'''
        e = e + '\n' + e.__traceback__
        print (e)                      
    

while True:

    '''
    This is what actually runs the whole time. 
    It first checks to see if new_input is different from current_input. This would be the case if there was a rotation.
    Once it detects that the input is different it knows water is flowing.
    It starts tracking the total_rotations and when the last rotation occured. 

    After each rotation it refreshes the value of the last rotation time.

    It waits a few seconds (rotation_downtime) after the last rotation time to make sure the water has stopped. 
    Once the water stops it passes the total_rotations to prep_and_send(). 
    It also passes 'data' which is any previous water-flow events that were not successfully sent at the time they were recorded.
    '''

    new_input = GPIO.input(inpt)
    if new_input != current_input:
        total_rotations += 1
        if time.time() <= last_movement_time: #if it hasn't been more than 10 seconds
            record_data = True
            current_input = new_input
            last_movement_time = time.time() + rotation_downtime
        else: #flow starts
            last_movement_time = time.time() + rotation_downtime

    elif record_data == True and time.time() > last_movement_time: #if it's been x seconds since last change
        prep_and_send(total_rotations)
        record_data = False
        total_rotations = 0
        last_movement_time = time.time() + rotation_downtime
        current_input = new_input

'''
This last part simply prints some helpful information. It also allows for a clean exit if user presses Ctrl + C.
'''

try:
        print('New input: ',new_input, '. Current input: ', current_input, '. Movements: ', total_rotations)
except KeyboardInterrupt:
        print('\nCTRL C - Exiting nicely')
        GPIO.cleanup()
        sys.exit()
