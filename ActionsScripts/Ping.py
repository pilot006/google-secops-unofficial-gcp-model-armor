from SiemplifyAction import SiemplifyAction
from SiemplifyUtils import unix_now, convert_unixtime_to_datetime, output_handler
from ScriptResult import EXECUTION_STATE_COMPLETED, EXECUTION_STATE_FAILED,EXECUTION_STATE_TIMEDOUT
import google.auth.transport.requests
from google.oauth2 import service_account
import json
import requests

@output_handler
def main():
    siemplify = SiemplifyAction()

    sa_json = siemplify.extract_configuration_param('Integration',"Service Account JSON")
    sa_json = json.loads(sa_json)
    template_id = siemplify.extract_configuration_param('Integration',"Template ID")
    region = siemplify.extract_configuration_param('Integration',"Region")
    project_id = siemplify.extract_configuration_param('Integration',"Project ID")

    credentials = service_account.Credentials.from_service_account_info(
        sa_json, scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )
    request = google.auth.transport.requests.Request()
    credentials.refresh(request)
    hd = {
        "Authorization": "Bearer " + credentials.token,
        "Content-Type": "application/json"
    }
    URL = f"https://modelarmor.{region}.rep.googleapis.com/v1/projects/{project_id}/locations/{region}/templates/{template_id}"
    req = requests.get(URL, headers=hd)
    siemplify.LOGGER.info(req.text)

    if template_id in req.text:
        status = EXECUTION_STATE_COMPLETED
        output_message = "OK"
        result_value = True 
    else:
        output_message = f"Unable to connect to Model Armor API"
        status = EXECUTION_STATE_FAILED
        siemplify.LOGGER.error(output_message)
        result_value = False


    siemplify.end(output_message, result_value, status)


if __name__ == "__main__":
    main()
