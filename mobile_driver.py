import speech_recognition as sr
import pyttsx3
import socket
import sys
import pickle

HEADERSIZE = 10
commander = {'R_LED': 0, 'Y_LED': 0, 'W_LED': 0, 'B_LED': 0, 'BUZZER_1': 0, 'BUZZER_5': 0, 'DISPLAY': '', 'KILL': 0}

listener = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('rate', 150)
voices = engine.getProperty('voices')

def watch_for_call():
    while True:
        watch_word = take_initial_command()

        if watch_word == 'hello ':
            talk("Hello...I am your Personal Assistant")
            talk("how can i help you?")
            while True:
                
                run_neptune()

def connect_to_server():
    #TO WORK WITH PORT FORWARDING ON 7052
    # "127.0.0.1"  # The server's hostname or IP address
    host = '127.0.0.1'
    port = 7052 #random

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    watch_for_call()

def talk(text):
    engine.say(text)
    engine.runAndWait()

def take_initial_command():
    try:
        with sr.Microphone() as source:
            watch = 'empty'
            listener.adjust_for_ambient_noise(source)
            print('listening for watch word...')
            voice = listener.listen(source)
            watch = listener.recognize_google(voice)
            watch = watch.lower()
            print(watch)
    except KeyboardInterrupt:
        exit(0)
    except:
        pass
    return watch

def take_command():
    try:

        with sr.Microphone() as source:
            command = 'empty'
            listener.adjust_for_ambient_noise(source)
            print('listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'neptune' in command:
                command = command.replace('neptune', '')
                print(command)
    except KeyboardInterrupt:
        exit(0)
    except:
        pass
    return command        

def led_dict_logic(command):
    if 'led' in command:
        command.replace('led', '')

        if 'yellow' in command:
            command.replace('yellow','')
            if 'on' in command:
                commander.update({'Y_LED':1})
                print(commander)
                send_to_server(commander)
                
                return "Turned on Yellow LED."
            elif 'off' in command:
                commander.update({'Y_LED':0})
                print(commander)
                send_to_server(commander)                
                
                return "Turned off Yellow LED."
            elif 'blink' in command:
                commander.update({'Y_LED_B':1, 'Y_LED':0})
                dict_updated = True
                return "Blinking Yellow LED 5 times..."
            else:
                return "I did not understand what to do with the Yellow LED."
        elif 'red' in command:
            command.replace('red','')
            if 'on' in command:
                commander.update({'R_LED':1})
                print(commander)
                send_to_server(commander)
                
                return "Turned on Red LED."
            elif 'off' in command:
                commander.update({'R_LED':0})
                send_to_server(commander)
                
                return "Turned off Red LED."
            elif 'blink' in command:
                commander.update({'R_LED_B':1, 'R_LED':0})
                dict_updated = True
                return "Blinking Red LED 5 times..."
            else:
                return "I did not understand what to do with the Red LED."
        elif 'white' in command:
            command.replace('white','')
            if 'on' in command:
                commander.update({'W_LED':1})
                print(commander)
                send_to_server(commander)
                return "Turned on White LED."
            elif 'off' in command:
                commander.update({'W_LED':0})
                print(commander)
                send_to_server(commander)
                return "Turned off White LED."
            elif 'blink' in command:
                commander.update({'W_LED_B':1, 'W_LED':0})
                dict_updated = True
                return "Blinking White LED 5 times..."
            else:
                return "I did not understand what to do with the White LED."
        elif 'blue' in command:
            command.replace('blue','')
            if 'on' in command:
                commander.update({'B_LED':1})
                print(commander)
                send_to_server(commander)
                return "Turned on Blue LED."
            elif 'off' in command:
                commander.update({'B_LED':0})
                print(commander)
                send_to_server(commander)
                return "Turned off Blue LED."
            elif 'blink' in command:
                commander.update({'B_LED_B':1, 'B_LED':0})
                dict_updated = True
                return "Blinking Blue LED 5 times..."
            else:
                return "I did not understand what to do with the Blue LED."
        elif 'warm' in command:
            command.replace('warm','')
            if 'on' in command:
                commander.update({'R_LED':1, 'Y_LED':1})
                print(commander)
                send_to_server(commander)
                return "Turned on warm colours."
            elif 'off' in command:
                commander.update({'R_LED':0, 'Y_LED':0})
                print(commander)
                send_to_server(commander)
                return "Turned off warm colours"
            else:
                return "Please specify an action"
        elif 'cool' in command:
            command.replace('cool','')
            if 'on' in command:
                commander.update({'B_LED':1, 'W_LED':1})
                print(commander)
                send_to_server(commander)
                return "Turned on cool colours."
            elif 'off' in command:
                commander.update({'B_LED':0, 'W_LED':0})
                print(commander)
                send_to_server(commander)
                return "Turned off cool colours"
            else:
                return "Please specify an action"
        elif 'all' in command:
            command.replace('all','')
            if 'on' in command:
                commander.update({'R_LED':1, 'Y_LED':1, 'B_LED':1, 'W_LED':1})
                print(commander)
                send_to_server(commander)
                return "Turned on LEDs"
            elif 'off' in command:
                commander.update({'R_LED':0, 'Y_LED':0, 'B_LED':0, 'W_LED':0})
                print(commander)
                send_to_server(commander)
                return "Turned off LEDs"
            else:
                return "I'm not sure what you want all the LEDs to do."
        else:
            return "Did not understand which colour you want to perform action on."    

def buzzer_dict_logic(command):
    if 'buzzer' in command:
        command.replace('buzzer','')
        if 'buzz' in command:
            command.replace('buzz','')
            if 'one time' in command:
                commander.update({'BUZZER_1':1})
                print(commander)
                send_to_server(commander)
                return "Beep"
            else:
                commander.update({'BUZZER_5':1})
                print(commander)
                send_to_server(commander)
                return "Beep Beep Beep Beep Beep"
        else:
            return "I'm sorry I don't understand what you want me to do with the buzzer."

def display_dict_logic(command):
    if 'display' in command:
        string  = command.replace('display', '')
        string  = string.lstrip()
        commander.update({'DISPLAY': string.upper()})
        print(commander)
        send_to_server(commander)
        return "Data sent to LCD"

def run_neptune():
    command = take_command()
    print(command)
    if 'empty' == command:
        talk('')
    elif 'display' in command:
        talk("sending to LCD")
        res = display_dict_logic(command.lower())
        print(res)
    elif 'shutdown' in command:
        commander.update({'KILL':1})
        send_to_server("KILL")
    elif 'led' in command:
        res = led_dict_logic(command)
        print(res)
    elif 'buzz' in command:
        res = buzzer_dict_logic(command)
        print(res)
    elif 'bye' in command:
        talk("Until we meet again")
        watch_for_call()
    else:
        talk('I did not catch that')

''' NOTE: THIS CODE HAS A BUG
def send_to_server(command):
    print("SENDING TO SERVER")
    if command == "KILL":
        #send KILL request to server pi
        msg = pickle.dumps(command, -1)
        msg = bytes(f"{len(msg):<{HEADERSIZE}}", 'utf-8')+msg
        s.sendall(msg)
        s.close()
        exit("SUCCESSFUL RUN OF PROGRAM")
    msg = pickle.dumps(command, -1)
    msg = bytes(f"{len(msg):<{HEADERSIZE}}", 'utf-8')+msg
    s.sendall(msg)
    print("SENT TO SERVER")
    command.update({'DISPLAY':'', 'BUZZER_1':0, 'BUZZER_5':0})
    reply = s.recv(1024)
    print(reply.decode('utf-8'))
 '''


if __name__ == "__main__":
    connect_to_server()
