# Skolmaten

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs)

- place files in in [homeassistant-base]/custom_components/skolmaten
- get school name from https://skolmaten.se/ (must be same as in URL)
- add to sensors.yaml (or under sensors: in configuration.yaml)

```
- platform: skolmaten
  sensors:
    - school: ankiborgskolan
```
