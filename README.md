 Discontinued, if you search for a functional script look here https://github.com/PimDoos/kia_connect

# Hassio KIA

A plugin which send all your myKIA data to your MQTT.

![alt text](https://github.com/peet47/hassio_kia/raw/master/pic/card.png)

##  HowTo:

Just enter the mqtt data in the script.

```python
mqtt_host = "<IP>"
mqtt_port = 1883
mqtt_username = "<USER>"
mqtt_password = "<PASSWORD>"
```

Also, you have to login to the service and extract the SessionID and enter into the script.
```python
cookies = {
    'ASP.NET_SessionId': '<SESSIONID>',
    'NL_MyKiaLogin': '_LoginGuid=<EMAIL>',
}
```

Everything done? Greate your data should now appear in the MQTT.

## configuration.yaml in Hassio
```python

#Charge Level
  - platform: mqtt
    name: "Battery_KIA"
    state_topic: "mashina/status/ev/soc"

#Doors Locked
  - platform: mqtt
    name: "Doors_KIA"
    state_topic: "mashina/status/DoorsLocked"
    
#Range
  - platform: mqtt
    name: "Range_KIA"
    state_topic: "mashina/status/Range"

#Cable plugged
  - platform: mqtt
    name: "Plugged_in"
    state_topic: "mashina/status/ev/isPlugged"
    
#Charging
  - platform: mqtt
    name: "Charging_KIA"
    state_topic: "mashina/status/ev/charging"
    
#Remaining charge time
  - platform: mqtt
    name: "Charging_remain"
    state_topic: "mashina/status/ev/timeUntillCharged"
```

## Entities card

```python
entities:
  - entity: sensor.range_kia
    icon: 'mdi:car'
    name: Available range
  - entity: sensor.doors_kia
    icon: 'mdi:car-door-lock'
    name: Doors Locked
  - entity: sensor.battery_kia
    icon: 'mdi:battery'
    name: Battery charge percentage
  - entity: sensor.charging_kia
    icon: 'mdi:battery-charging'
    name: Charging status
  - entity: sensor.plugged_in
    icon: 'mdi:power-plug'
    name: Car plugged in
  - entity: sensor.charging_remain
    icon: 'mdi:timer'
    name: Remaining charge time
show_header_toggle: false
title: Kia
type: entities
```

## Device_Tracker
![alt text](https://github.com/peet47/hassio_kia/raw/master/pic/device_tracker.jpeg)

you can even build a device tracker based on this mqtt message
```python
mashina/status/Geo/location
```
HowTo: https://www.home-assistant.io/integrations/device_tracker/
