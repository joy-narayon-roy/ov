import requests as req
import json


def my_ip():
    res = req.get("http://ip-api.com/json")
    res.raise_for_status()
    return res.json()


def print_my_ip():
    ip_details = my_ip()
    print("\nMy IP :")
    for details in ip_details:
        print("\t",str(details).capitalize(),":",ip_details[details])
    print("\n")

print_my_ip()
