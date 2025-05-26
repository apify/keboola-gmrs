# Keboola Google Maps Reviews Scraper

## Running locally

Create `data` directory by copying `sample-config`:

```sh
cp component_config/sample-config data
```

Then, in `data/config.json`, replace `<YOUR_APIFY_API_TOKEN>` with your Apify API token. Finally, run the component:

```sh
KBC_DATADIR=data python src/component.py
```

## Deploying from terminal

you need to set the following environment variables:
- `KBC_DEVELOPERPORTAL_APP`
- `KBC_DEVELOPERPORTAL_USERNAME`
- `KBC_DEVELOPERPORTAL_VENDOR`
- `KBC_DEVELOPERPORTAL_PASSWORD`

You'll find the values in repo's [secrets](https://github.com/apify/keboola-gmrs/settings/secrets/actions) and [variables](https://github.com/apify/keboola-gmrs/settings/variables/actions).

```sh
APP_IMAGE=keboola.component
GITHUB_TAG=0.0.4
docker build -t APP_IMAGE:latest .

# Deploy the container
sh deploy.sh

# Update compontent's configs and descriptions
sh scripts/deleloper_portal/update_properties.sh
```

Deploying from terminal should not be needed. To deploy a new version, we need to push a new tag to the default branch and GH actions should handle the deployment.
