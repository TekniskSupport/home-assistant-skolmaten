
# This integration has stopped working. use the one in HACS instead.


# Skolmaten integration

## Installation/Configuration:
Install the integration and reboot HA to load it.

Add the following to resources in your sensors.yaml
(or under sensor: in your configuration.conf):

```yaml
- platform: skolmaten
  sensors:
    - school: ankiborgskolan
```


```yaml
- platform: skolmaten
  type: weeks
  offset: 1
  sensors:
    - school: ankiborgskolan
```

```yaml
- platform: skolmaten
  type: days
  offset: -2
  limit: 10
  sensors:
    - school: ankiborgskolan
```

Replace ankiborgskolan the actual name in url from skolmaten.se

To display in lovelace, you can use the custom:list-card with this configuration:
```yaml
  - type: custom:list-card
    columns:
      - title: ' '
        field: day
      - field: food
        title: ' '
    entity:  sensor.skolmaten_ankiborgskolan
    feed_attribute: entries
    title: Matsedel Skolan
  ```

And lastly restart your HA again to get your new sensor!
