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
    prompt = siemplify.extract_action_param("Prompt", print_value=True)

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
    URL = f"https://modelarmor.us-east4.rep.googleapis.com/v1/projects/gen-ai-apps/locations/us-east4/templates/{template_id}:sanitizeUserPrompt"
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
