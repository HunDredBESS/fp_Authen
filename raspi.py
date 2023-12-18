import serial
import time
import pandas as pd
import random
import string
import os
import requests
import urllib.parse
import numpy as np
import datetime

LINE_ACCESS_TOKEN = "uGJChf8u6taAwBwwJ36FjuzeXZwMXKCSL2dMybDRHPP"
URL_LINE = "https://notify-api.line.me/api/notify" 

path_csv = "/home/kong/code/fp_Authen/Data_ID.csv"
# path_FingerPrint = r"C:\Users\roika\Documents\Project_Arduino\FingerprintAndImage\data_fingerprintTemplate"

# Replace 'COM3' with the actual port your Arduino is connected to
arduino_port = '/dev/ttyUSB0'
baud_rate = 9600

ser = serial.Serial(arduino_port, baud_rate, timeout=1)

def receive_data_Student_ID():
    # Buffer to store received data
    data_buffer = []
    start = 0
    end = 0
    while start==0:
        data = ser.readline().decode('utf-8').strip()
        if data:
            print("Arduino Data:", data)
            # print("step 01")
        if(data == 'Receive_Student_ID'):
            # print("Step02")
            while end == 0:
                # Read a line from the serial port
                data_byte = ser.readline().decode('utf-8').strip()

                # Check if data is available
                if (data_byte == "Receive_End"):
		
                    # Append data byte to the buffer
                    print("Student ID:", data_buffer)
                    print("Arduino Data:", data_byte)
                    start = 1
                    end = 1
                    return data_buffer
                else:
                    # Check if buffer has enough data
                    data_buffer = data_byte
                    # print("Student ID:", data_buffer)
        else:
            time.sleep(0.1)

def receive_data():
    # Buffer to store received data
    data_buffer = []
    start = 0
    end = 0
    while start==0:
        data = ser.readline().decode('utf-8').strip()
        if data:
            print("Arduino Data:", data)
            
        if(data == 'LOGIN'):
            
            break
        elif(data == 'enroll'):
            break
    return data
    

def find_ID_indatabase(df,Student_ID):
    try:
        # Find row index where Name == "Charlie"
        row_index = df[df['ID'] == Student_ID].index[0]
        # print(row_index)
        row_data = df[df['ID'] == Student_ID]
        ID_data = row_data['ID'].values[0]
        Name_data = row_data['Name'].values[0]
        StudentID_data = row_data['StudentID'].values[0]
        Finger_data = row_data['FingerPrintTemplate'].values[0]
        Img_data = row_data['Face_Img'].values[0]
        # print(row_data)
        print(" ")
        print("ID: ",ID_data)
        print("Name: ",Name_data)
        print("Student ID: ",StudentID_data)
        print("FingerPrint: ",Finger_data)
        print(" ")
        return ID_data,Name_data,Finger_data,StudentID_data,Img_data
    except:
        # print("An exception occurred")
        return "No data SudentID"

def Check_Student_ID():
        # Read the CSV file into a DataFrame
        Read_data_csv = pd.read_csv(path_csv)
        # Print the DataFrame
        # print(Read_data_csv)
        data_studen = receive_data_Student_ID()
        try:
            ID_data,Name_data,Finger_data,StudentID_data,Img_data = find_ID_indatabase(Read_data_csv,int(data_studen))
            return ID_data,Name_data,Finger_data,StudentID_data,Img_data
        except:
            # print("An exception occurred")
            # print(find_ID_indatabase(int(data_studen)))
            Name_data = "unknow"
            Finger_data = "unknow"
            Img_data = "unknow"
            StudentID_data = "unknow"
            return 0,Name_data,Finger_data,StudentID_data,Img_data

def Enroll_Student_ID():
        # Read the CSV file into a DataFrame
        Read_data_csv = pd.read_csv(path_csv)
        # Print the DataFrame
        # print(Read_data_csv)
        data_studen = receive_data_Student_ID()
        try:
            # Find row index where Name == "Charlie"
            ID_data,Name_data,Finger_data,StudentID_data,Img_data = find_ID_indatabase(Read_data_csv,int(data_studen))
            FingerPrintTemplate_save = Scan_Finger()
            # save_txtfile("fingerPrint_"+ f"{int(data_studen):03}",str(FingerPrintTemplate_save))
            print("Updated fingerprint")

        except:
        #     # print("An exception occurred")
        #     # Add new row
            print("no")
            new_row = pd.DataFrame({
                "StudentID": [int(generate_id())],
                "Name": ['New user'],
                "ID": [int(data_studen)],
                "FingerPrintTemplate": ["fingerPrint_" +f"{int(data_studen):03}"],
                "Face_Img": "R1ZG2FRL2D.jpg"
            })
            Read_data_csv = pd.concat([Read_data_csv, new_row], ignore_index=True)
            # Read_data_csv = Read_data_csv.append(new_row, ignore_index=True)
            # Save to CSV
            Read_data_csv.to_csv(path_csv, index=False)
            print(Read_data_csv)
            print("Data saved to data.csv")
            FingerPrintTemplate_save = Scan_Finger()
            # save_txtfile("fingerPrint_"+ f"{int(data_studen):03}",str(FingerPrintTemplate_save))
            print("Enrolled")

def generate_id():
  return ''.join(random.choice(string.digits) for _ in range(10))

def receive_fingerPrint():
    # Buffer to store received data
    FingerPrintTemplate = []
    data_buffer = []
    data_buffer2 = ()
    start = 0
    start1 = 0
    while start1 == 0:
        data = ser.readline().decode('utf-8').strip()
        if data:
            # print("Arduino Data:", data)
            
            if(data == 'startSendfinger'):
                row = 0
                while start == 0:
                    # Read a line from the serial port
                    data_byte = ser.readline().decode('utf-8').strip()

                    # Check if data is available
                    if data_byte:
                        # Append data byte to the buffer
                        if (data_byte == "stopSendfinger"):
                            start = 1
                            start1 = 1
                            FingerPrintTemplate = data_buffer
                            print("FingerPrint Template:", FingerPrintTemplate)
                            # print("FingerPrint Template:", lst_tuple)
                            converted_list = [tuple(s.split(',')) for s in FingerPrintTemplate]
                            return converted_list
                        else:                    
                            data_buffer.append(data_byte)
                            # print("Data:", data_byte)
                        
                    # else:
                    #     # Check if buffer has enough data
                    #     if len(data_buffer) >= 255:
                    #         # Write the entire buffer to the serial port
                    #         print("FingerPrint Template:", data_buffer)
                    #         # Clear the buffer for next data chunk
                    #         data_buffer = []
                    #         start = 1
            # if(data =="stopSendfinger"):
            #     start1 = 1
        else:
            time.sleep(0.1)           

# def save_txtfile(name_file,data_save):
#     # Open the file in write mode
#     with open(path_FingerPrint+f"\{name_file}.txt", "w") as f:
#         # Write the content to the file
#         f.write(data_save)

def read_file(path_file):
    # Open the file in binary read mode
    fd = os.open(path_file, os.O_RDONLY)
    # Read the file content as bytes
    content = os.read(fd, os.fstat(fd).st_size)
    # Close the file explicitly
    os.close(fd)
    # Decode the content to a string
    content = content.decode("utf-8")
    # Print the contents of the file

    print(content)
    print(type(content))

    # Remove brackets at the beginning and end of the string
    data_str = content[1:-1]

    # Split the string into individual tuples
    tuple_str_list = data_str.split("), (")
    tuple_str_list[0] = tuple_str_list[0] + ")"
    tuple_str_list[-1] = tuple_str_list[-1][:-1]

    # Convert each tuple string to a tuple
    data_list = [tuple(eval(t)) for t in tuple_str_list]
    print(data_list)
    print(type(data_list))

    # Using list comprehension and unpacking
    flat_list = [item for sublist in data_list for item in sublist]
    # Convert the remaining elements to integers
    int_data = [int(x, 16) for x in flat_list]

    # Print the result
    print(int_data)
    # print(type(converted_list))
    return int_data

def line_text(message):	
    msg = urllib.parse.urlencode({"message":message})
    LINE_HEADERS = {'Content-Type':'application/x-www-form-urlencoded',"Authorization":"Bearer "+LINE_ACCESS_TOKEN}
    session = requests.Session()
    session_post = session.post(URL_LINE, headers=LINE_HEADERS, data=msg)
    print(session_post.text)

def Scan_Finger():
    if not(ser.is_open):
                print("Open")
                ser.open()
                time.sleep(1)
    print("New fingerprint.....")
    ser.write(str.encode("1"))
    print("New fingerprint....2")
    FingerPrintTemplate_save = receive_fingerPrint()
    return FingerPrintTemplate_save

def Send_dataToArduino(msg_txt):
    if not(ser.is_open):
                print("Open")
                ser.open()
                time.sleep(1)
    print("send",msg_txt)
    ser.write(str.encode(msg_txt))


try:
    # Read the CSV file into a DataFrame
    Read_data_csv = pd.read_csv(path_csv)
    # Print the DataFrame
    print(Read_data_csv)

    while (True):
        # try:
            conditio_S = receive_data()
            print("condition: ",conditio_S)
            if (conditio_S=='LOGIN'):
                print("condition: ",conditio_S)
                ID_Data,Name_Data,Finger_Data,StudentID_data,Img_Data = Check_Student_ID()
                if (ID_Data!=0):
                    Send_dataToArduino(str(ID_Data))
                    Send_dataToArduino("\n")
                    Send_dataToArduino(Name_Data)
                    Send_dataToArduino("\n")
                    time.sleep(0.1) 
                    Send_dataToArduino(StudentID_data)
                    
                    print(Finger_Data)
                    # minutiae1 = read_file(path_FingerPrint+f"\{Finger_Data}"+".txt")
                    # time.sleep(2)
                    # Scan_FingerPrintTemplate = Scan_Finger()
                    # get the current date and time

                    now = datetime.datetime.now()
                    line_text("\nName: "+Name_Data+"\nStudent ID: "+StudentID_data+f"\ndate: +{str(now)}")
                    print("send message To line")
                    time.sleep(1)
                else:
                    print("NO Student ID in data base...!!!")
                    Send_dataToArduino("No_data")
                    time.sleep(0.1) 


            elif (conditio_S=='enroll'):
                print("condition: ",conditio_S)
                # Enroll_Student_ID()

        # except:
        #     print("An exception occurred")
            

except KeyboardInterrupt:
    print("\nProgram terminated.")
finally:
    ser.close()

