# Unofficial Google Model Armor Integration for SecOps SOAR


## Overview

With the [release of Model Armor on Google Cloud](https://cloud.google.com/security-command-center/docs/model-armor-overview), organizations can now leverage Model Armor to assess prompt and model responses for risk. 

## Pre-requisities
- Google Cloud Project - A project, with Model Armor enabled, must be created.
- Service Account JSON Key - To interact with Model Amror, a service account credential must be created.

## Installation
1. Navigate to Releases in this repo and download the .zip package.
2. In Google SOAR/Security Operations, install the integration by opening the IDE and importing the package.
3. Set up an integration via Integrations, providing the project name, service account JSON, and the [region](https://cloud.google.com/security-command-center/docs/model-armor-overview#regional_endpoints) you wish to use.
