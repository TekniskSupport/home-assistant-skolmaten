
# Integration no longer working, use the one default in HACS instead.


# Skolmaten

Unfortunately the endpoint has been removed, and thus this integration no longer works.

Now you have to register an application in order to obtain a client-token in order to make requsts to an api.


[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge)](https://github.com/hacs/integration)

- place files in in [homeassistant-base]/custom_components/skolmaten
- get school name from https://skolmaten.se/ (must be same as in URL)
- add to sensors.yaml (or under sensors: in configuration.yaml)

```
- platform: skolmaten
  sensors:
    - school: ankiborgskolan
```
