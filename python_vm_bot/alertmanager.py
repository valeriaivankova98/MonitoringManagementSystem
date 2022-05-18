import requests


def create_from_template(name, status, description):
    return {
        "receiver": "admins",
        "status": status,
        "alerts": [
            {
                "status": status,
                "labels": {
                    "alertname": name,
                    "env": "prod",
                    "instance": "bot",
                    "job": "node",
                    "service": "prometheus_bot",
                    "severity": "warning",
                    "supervisor": "runit"
                },
                "annotations": {
                    "summary": description
                },
                "startsAt": "2016-04-27T20:46:37.903Z",
                "endsAt": "0001-01-01T00:00:00Z",
                "generatorURL": "https://example.com/graph#..."
            }
        ],
        "groupLabels": {
            "alertname": name,
            "instance": "Y.Cloud Server"
        },
        "commonLabels": {
            "alertname": name,
            "env": "prod",
            "instance": "Y.Cloud Server",
            "job": "node",
            "service": "prometheus_bot",
            "severity": status,
            "supervisor": "runit"
        },
        "commonAnnotations": {
            "summary": description,
        },
        "externalURL": "https://alert-manager.example.com",
        "version": "3",
        "groupKey": 43434343434343434343
    }


def request_log(chat_id, name, status, description):
    print(create_from_template(name, status, description))
    print(chat_id)
    r = requests.post(f'http://127.0.0.1:9087/alert/{chat_id}', json=create_from_template(name, status, description))
    print(r, r.text)
