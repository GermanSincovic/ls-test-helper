import requests
from lxml import html


def get_health_pages():
    health_data = []

    devtest = requests.get("http://ls-tools-ls-g.dev-i.net:8091/health-status/").json()
    preprod = requests.get("https://preprod-component-monitoring.livescore.com/health-status/").json()
    prod = requests.get("https://component-monitoring.livescore.com/health-status/").json()
    loadtest = requests.get("http://35.246.114.214:8091/health-status/").json()
    loadtest_iron = {"loadtest-iron": requests.get("http://35.246.114.214:8092/health-status/").json()['loadtest']}

    tree = html.fromstring(requests.get("http://ls-tools-ls-g.dev-i.net:8060/").content)
    headers = list()
    lines = list()
    sr_keys = {"sr-keys": []}
    for header in tree.xpath("//th/text()"):
        headers.append(header)
    for line in tree.xpath("//td/*/text()"):
        lines.append(line)
    for i in range(0, len(lines)):
        if len(sr_keys["sr-keys"]) < i // len(headers) + 1:
            sr_keys["sr-keys"].append({})
        sr_keys["sr-keys"][i // len(headers)].update({headers[i % len(headers)]: lines[i]})

    for env in devtest:
        health_data.append({env: devtest[env]})
    for env in preprod:
        health_data.append({env: preprod[env]})
    for env in prod:
        health_data.append({env: prod[env]})
    for env in loadtest:
        health_data.append({env: loadtest[env]})
    for env in loadtest_iron:
        health_data.append({env: loadtest_iron[env]})
    health_data.append(sr_keys)

    return health_data, 200
