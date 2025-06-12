from SiemplifyAction import SiemplifyAction
from SiemplifyUtils import unix_now, convert_unixtime_to_datetime, output_handler
from ScriptResult import EXECUTION_STATE_COMPLETED, EXECUTION_STATE_FAILED,EXECUTION_STATE_TIMEDOUT
import google.auth.transport.requests
from google.oauth2 import service_account
import json
import requests
from google.auth import impersonated_credentials


@output_handler
def main():
    siemplify = SiemplifyAction()

    template_id = siemplify.extract_configuration_param('Integration',"Template ID")
    region = siemplify.extract_configuration_param('Integration',"Region")
    project_id = siemplify.extract_configuration_param('Integration',"Project ID")
    prompt = siemplify.extract_action_param("Prompt", print_value=True)
    workload_email = siemplify.extract_configuration_param('Integration',"Workload Identity Email", print_value=True)
    sa_json = siemplify.extract_configuration_param('Integration',"Service Account JSON")
    if sa_json is not None:
        sa_json = json.loads(sa_json)
    
    # Default to trying to use the workload identity for auth
    if workload_email is not None:
        siemplify.LOGGER.info("Auth via Workload Identity E-mail")
        source_credentials, project = google.auth.default(
            scopes=['https://www.googleapis.com/auth/cloud-platform']
        )
        credentials = impersonated_credentials.Credentials(
            source_credentials=source_credentials,
            target_principal=workload_email,
            target_scopes=['https://www.googleapis.com/auth/cloud-platform'],
            lifetime=300
        )
        request = google.auth.transport.requests.Request()
        credentials.refresh(request)
    else:
        siemplify.LOGGER.info("Auth via Service Account JSON")
        credentials = service_account.Credentials.from_service_account_info(
        sa_json, scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )
        request = google.auth.transport.requests.Request()
        credentials.refresh(request)
    hd = {
        "Authorization": "Bearer " + credentials.token,
        "Content-Type": "application/json"
    }
    body = { 
        "user_prompt_data" : { 
            "text": prompt 
        } 
    }
    URL = f"https://modelarmor.{region}.rep.googleapis.com/v1/projects/{project_id}/locations/{region}/templates/{template_id}:sanitizeUserPrompt"
    req = requests.post(URL, headers=hd, json=body)
    siemplify.LOGGER.info(req.text)

    status = EXECUTION_STATE_COMPLETED
    output_message = "Succesfully executed."
    siemplify.result.add_result_json(req.json())
    result_value = None

    siemplify.LOGGER.info("\n  status: {}\n  result_value: {}\n  output_message: {}".format(status,result_value, output_message))
    siemplify.end(output_message, result_value, status)


if __name__ == "__main__":
    main()
