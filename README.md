[![Github last commit](https://img.shields.io/github/last-commit/studiojw/vlaams-verkeerscentrum-ha)](https://github.com/studiojw/vlaams-verkeerscentrum-ha)
[![GitHub repo size](https://img.shields.io/github/repo-size/studiojw/vlaams-verkeerscentrum-ha)](https://github.com/studiojw/vlaams-verkeerscentrum-ha)
[![GitHub issues](https://img.shields.io/github/issues/studiojw/vlaams-verkeerscentrum-ha)](https://github.com/studiojw/vlaams-verkeerscentrum-ha/issues)
[![GitHub license](https://img.shields.io/github/license/studiojw/vlaams-verkeerscentrum-ha)](https://github.com/studiojw/vlaams-verkeerscentrum-ha/blob/main/LICENSE)

# Home Assistant - Vlaams Verkeerscentrum Integration 🇧🇪

This integration provides real-time travel time sensors for specific trajectories in Flanders, Belgium, as defined on the Vlaams Verkeerscentrum ([verkeerscentrum.be](verkeerscentrum.be)) platform. The integration fetches travel times from the Verkeerscentrum API, allowing you to monitor traffic conditions and adjust your plans accordingly.

## How You Can Use It

- Real-time Travel Times: Get up-to-date travel times for your predefined routes.
- Customizable Trajectories: Easily configure the trajectories you want to monitor.
- Alerts and Automations: Integrate with Home Assistant's alerting and automation capabilities to get notified of significant delays or changes in travel times.

## Installation

To install the integration to your Home Assistant, use this button:

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=studiojw&repository=vlaams-verkeerscentrum-ha&category=integration)

### Manual Installation

1. Go to HACS > Integrations
2. Add this repo into your HACS [Custom Repositories](https://hacs.xyz/docs/faq/custom_repositories/)
3. Search for "Vlaams Verkeerscentrum" and download the latest version of the integration.
4. Restart Home Assistant
5. Configure the integration, see [Configuration](README.md#configuration)

## Configuration

### Vlaams Verkeerscentrum

1. Create a new account on the [Vlaams Verkeerscentrum](verkeerscentrum.be) website.
2. In the top right corner of the page, click on **"Mijn trajecten"**.
3. Click on **"Voeg een nieuw traject toe"**.
4. Select 2 trajectory points on the map and give it a name.
5. Click on **"Opslaan"**.
6. Repeat steps 3-5 for all the trajectories you want to monitor.

### Home Assistant

The integration can be set via the user interface, by

1. Go to Settings -> [Devices & Services](https://my.home-assistant.io/redirect/integrations/).
2. In the bottom right corner, click on [Add Integration](https://my.home-assistant.io/redirect/config_flow_start/?domain=vlaams_verkeerscentrum).
3. From the list, select "Vlaams Verkeerscentrum".
4. Follow the instructions on the screen to configure the integration.

## License

See the LICENSE file in the root of this repository for more info.

Copyright © Studio JW
