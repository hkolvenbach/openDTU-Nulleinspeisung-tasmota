#!/usr/bin/env python3
import requests, time, sys, os
from requests.auth import HTTPBasicAuth

from dotenv import load_dotenv

load_dotenv()

# Diese Daten müssen angepasst werden:
serial = os.getenv('DTU_INVERTER_SERIAL') # Seriennummer des Hoymiles Wechselrichters
maximum_wr = 150 # Maximale Ausgabe des Wechselrichters
minimum_wr =0 # Minimale Ausgabe des Wechselrichters

dtu_ip = os.getenv('DTU_IP') # '192.168.2.148' # IP Adresse von OpenDTU
dtu_nutzer = os.getenv('DTU_USER') # 'admin' # OpenDTU Nutzername
dtu_passwort = os.getenv("DTU_PASSWORD") # OpenDTU Passwort

# shelly_ip = '192.100.100.30' # IP Adresse von Shelly 3EM
tasmota_ip = os.getenv('TASMOTA_IP') # IP Adresse von Tasmota

# Schreibe Configurationsdaten
print(f'Inverter Serial: {serial} \nDTU IP: {dtu_ip} \nDTU Nutzer: {dtu_nutzer} \nDTU Passwort: {dtu_passwort} \nTasmota IP: {tasmota_ip}')


while True:
    try:
        # Nimmt Daten von der openDTU Rest-API und übersetzt sie in ein json-Format
        r = requests.get(url = f'http://{dtu_ip}/api/livedata/status/inverters' ).json()

        # Selektiert spezifische Daten aus der json response
        reachable   = r['inverters'][0]['reachable'] # Ist DTU erreichbar?
        producing   = int(r['inverters'][0]['producing']) # Produziert der Wechselrichter etwas?
        altes_limit = int(r['inverters'][0]['limit_absolute']) # Altes Limit
        power_dc    = r['inverters'][0]['AC']['0']['Power DC']['v']  # Lieferung DC vom Panel
        power       = r['inverters'][0]['AC']['0']['Power']['v'] # Abgabe BKW AC in Watt

        # print current values
        print(f'Produktion: {producing  } W, Limit: {altes_limit} W, DC: {power_dc} W, AC: {power} W')
    except:
        print('Fehler beim Abrufen der Daten von openDTU')
    try:
        # Lese daten aus tasmota API <TASMOTA_IP>/cm?cmnd=status%208
        # Beispieldaten:
        # {"StatusSNS":{"Time":"2024-05-25T19:36:02","DTZ":{"E_in":5211.131,"E_out":17.899,"Power":800,"volt_p1":0.0,"volt_p2":0.0,"volt_p3":0.0,"amp_p1":0.0,"amp_p2":0.0,"amp_p3":0.0,"phase_angle_l2_l1":0.0,"phase_angle_l3_l1":0.0,"phase_angle_p1":0.0,"phase_angle_p2":0.0,"phase_angle_p3":0.0,"freq":0}}}
        # Power = Aktueller Bezug in Watt
        tasmota_data = requests.get(f'http://{tasmota_ip}/cm?cmnd=status%208').json()
        grid_sum = tasmota_data['StatusSNS']['DTZ']['Power']


        # Nimmt Daten von der Shelly 3EM Rest-API und übersetzt sie in ein json-Format
        # phase_a     = requests.get(f'http://{shelly_ip}/emeter/0', headers={'Content-Type': 'application/json'}).json()['power']
        # phase_b     = requests.get(f'http://{shelly_ip}/emeter/1', headers={'Content-Type': 'application/json'}).json()['power']
        # phase_c     = requests.get(f'http://{shelly_ip}/emeter/2', headers={'Content-Type': 'application/json'}).json()['power']
        # grid_sum    = phase_a + phase_b + phase_c # Aktueller Bezug - rechnet alle Phasen zusammen

        # print current values
        print(f'Bezug: {grid_sum} W')
    except:
        # print exception

        print('Fehler beim Abrufen der Daten von Shelly 3EM')

    # Werte setzen
    print(f'\nBezug: {round(grid_sum, 1)} W, Produktion: {round(power, 1)} W, Verbrauch: {round(grid_sum + power, 1)} W')
    if reachable:
        setpoint = grid_sum + altes_limit - 5 # Neues Limit in Watt

        # Fange oberes Limit ab
        if setpoint > maximum_wr:
            setpoint = maximum_wr
            print(f'Setpoint auf Maximum: {maximum_wr} W')
        # Fange unteres Limit ab
        elif setpoint < minimum_wr:
            setpoint = minimum_wr
            print(f'Setpoint auf Minimum: {minimum_wr} W')
        else:
            print(f'Setpoint berechnet: {round(grid_sum, 1)} W + {round(altes_limit, 1)} W - 5 W = {round(setpoint, 1)} W')

        if setpoint != altes_limit:
            print(f'Setze Inverterlimit von {round(altes_limit, 1)} W auf {round(setpoint, 1)} W... ', end='')
            # Neues Limit setzen
            try:
                r = requests.post(
                    url = f'http://{dtu_ip}/api/limit/config',
                    data = f'data={{"serial":"{serial}", "limit_type":0, "limit_value":{setpoint}}}',
                    auth = HTTPBasicAuth(dtu_nutzer, dtu_passwort),
                    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
                )
                print(f'Konfiguration gesendet ({r.json()["type"]})')
            except:
                print('Fehler beim Senden der Konfiguration')

    sys.stdout.flush() # write out cached messages to stdout
    time.sleep(5) # wait
