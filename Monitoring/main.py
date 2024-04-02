import json
import pingparsing

website = input("Enter Website URL: ")
    

def ping():
    ping_parser = pingparsing.PingParsing()
    transmitter = pingparsing.PingTransmitter()
    transmitter.destination = website
    transmitter.count = 10
    result = transmitter.ping()

    print(json.dumps(ping_parser.parse(result).as_dict(), indent=4))



print("[extract ping statistics]")
ping()
