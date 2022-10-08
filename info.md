# Skolmaten integration

## Installation/Configuration:

Add the following to resources in your sensors.yaml:

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
