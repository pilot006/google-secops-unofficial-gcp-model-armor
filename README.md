# Unofficial Google Model Armor Integration for SecOps SOAR


## Overview

With the [release of Model Armor on Google Cloud](https://cloud.google.com/security-command-center/docs/model-armor-overview), organizations can now leverage Model Armor to assess prompt and model responses for risk. 

## Pre-requisities
- Google Cloud Project - A project, with Model Armor enabled, must be created.

## Authentication
This integration supports both service account JSON and workload identity e-mail authenication. Upon creating a service account either:
- Create serivce account JSON and provide in integration configuration
- Grant SOAR workload identity e-mail right to impersonate your service account. Details here: https://www.googlecloudcommunity.com/gc/SecOps-SOAR/How-to-authenticate-to-Google-Cloud-integrations-using-Workload/m-p/864858

## Installation
1. Navigate to Releases in this repo and download the .zip package.
2. In Google SOAR/Security Operations, install the integration by opening the IDE and importing the package.
3. Set up an integration via Integrations, providing the project name, service account JSON, and the [region](https://cloud.google.com/security-command-center/docs/regional-endpoints#locations-model-armor) you wish to use.
