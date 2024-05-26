# OpenDTU Nulleinspeisung fuer Hoymiles + Tasmota

## Beschreibung

Dies ist ein Python-Skript, das den aktuellen Hausverbrauch aus einem Tasmota ausließt, die Nulleinspeisung berechnet und die Ausgangsleistung eines Hoymiles-Wechselrichters mit Hilfe der OpenDTU entsprechend anpasst. Somit wird kein unnötiger Strom ins Betreibernetz abgegeben.

### Konfiguration
- Die Konfiguration erfolgt via `stack.env`, als Beispiel siehe `example.env`. Für OpenDTU müssen die IP (`DTU_IP`), Username (`DTU_USER`), Password (`DTU_PASSWORD`) und Hoymiles Seriennummer (`DTU_INVERTER_SERIAL`) angegeben werden. Für Tasmota muss die IP (`TASMOTA_IP`) angegeben werden, der Zugriff erfolgt via API.

Minimal- und Maximalleistung des Wechselrichters müssen ebenfalls angegeben werden (`DTU_INVERTER_MIN_POWER`, `DTU_INVERTER_MAX_POWER`) in Watt. Die Maximalleistung kann auch niedriger als die Nennleistung des Wechselrichters sein.


## Autoren und Anerkennung
- Dieses Skript ist ein Fork von: https://github.com/Selbstbau-PV/Selbstbau-PV-Hoymiles-nulleinspeisung-mit-OpenDTU-und-Shelly3EM, was wiederum ein Fork von ist https://gitlab.com/p3605/hoymiles-tarnkappe
- Ein großes Lob und Dank an die OpenDTU community: https://github.com/tbnobody/OpenDTU

## Wiki
- Weitere Informationen finden Sie auf unserer Seite: https://selbstbau-pv.de/wissensbasis/nulleinspeisung-hoymiles-hm-1500-mit-opendtu-python-steuerung/

## Lizenz
Benutzung auf eigene Gefahr. Dieses Skript ist unter der MIT-Lizenz veröffentlicht.