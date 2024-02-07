import os, sys, requests, json, base64

SLACK_URL='https://hooks.slack.com/services/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' #sm projects
ENV = 'test branch'

def send_message(message):
    requests.post(SLACK_URL, json={'text': '%s :%s' % (ENV, message)})


def clean_results(project_id):
    url = f"https://allure.integrichain.net/allure-docker-service/clean-results?project_id={project_id}"
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    print(f"Clean results reponse: {response.text}")

print(sys.argv)
# This directory is where you have all your results locally, generally named as `allure-results`
allure_results_directory = sys.argv[3]
# This url is where the Allure container is deployed. We are using localhost as example
allure_server = 'https://allure.integrichain.net'
# Project ID according to existent projects in your Allure container - Check endpoint for project creation >> `[POST]/projects`
project_id = sys.argv[2]


current_directory = os.path.dirname(os.path.realpath(__file__))
results_directory = current_directory + allure_results_directory
print('RESULTS DIRECTORY PATH: ' + results_directory)

files = os.listdir(results_directory)

print('FILES:')
results = []
for file in files:
    result = {}

    file_path = results_directory + "/" + file
    print(file_path)

    if os.path.isfile(file_path):
        try:
            with open(file_path, "rb") as f:
                content = f.read()
                if content.strip():
                    b64_content = base64.b64encode(content)
                    result['file_name'] = file
                    result['content_base64'] = b64_content.decode('UTF-8')
                    results.append(result)
                else:
                    print('Empty File skipped: '+ file_path)
        finally :
            f.close()
    else:
        print('Directory skipped: '+ file_path)

headers = {'Content-type': 'application/json'}
request_body = {
    "results": results
}
json_request_body = json.dumps(request_body)

ssl_verification = True
clean_results(project_id)

print("------------------SEND-RESULTS------------------")
response = requests.post(allure_server + '/allure-docker-service/send-results?project_id=' + project_id, headers=headers, data=json_request_body, verify=ssl_verification)
print("STATUS CODE:")
print(response.status_code)
print("RESPONSE:")
json_response_body = json.loads(response.content)
json_prettier_response_body = json.dumps(json_response_body, indent=4, sort_keys=True)
print(json_prettier_response_body)

# If you want to generate reports on demand use the endpoint `GET /generate-report` and disable the Automatic Execution >> `CHECK_RESULTS_EVERY_SECONDS: NONE`
print("------------------GENERATE-REPORT------------------")
execution_name = 'execution from Jenkins'
execution_from = sys.argv[1]
execution_type = 'jenkins'
response = requests.get(allure_server + '/allure-docker-service/generate-report?project_id=' + project_id + '&execution_name=' + execution_name + '&execution_from=' + execution_from + '&execution_type=' + execution_type, headers=headers, verify=ssl_verification)
print("STATUS CODE:")
print(response.status_code)
print("RESPONSE:")
json_response_body = json.loads(response.content)
json_prettier_response_body = json.dumps(json_response_body, indent=4, sort_keys=True)
print(json_prettier_response_body)
print('ALLURE REPORT URL:')
report_url = json_response_body['data']['report_url']
print(report_url)
send_message(f'Allure report url for {project_id}: {report_url}')

