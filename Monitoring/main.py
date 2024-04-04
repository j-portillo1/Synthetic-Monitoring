import json
import pingparsing
from prometheus_client import start_http_server, Gauge

website = input("Enter Website URL: ")
    
#packet_loss_count = Gauge("packet_loss_count", "Packet loss")
#ping_latency_metric = Gauge('ping_latency_ms', 'Ping latency in milliseconds')
def ping():
    #start_http_server(9090)
    #print("Prometheus HTTP server started on port 9090")
    ping_parser = pingparsing.PingParsing()
    transmitter = pingparsing.PingTransmitter()
    transmitter.destination = website
    transmitter.count = 10
    result = transmitter.ping()

    #packet_loss_count.set(result["packet_loss_count"])
    #ping_latency_metric.set(result["ping_latency_ms"])

    

    print(json.dumps(ping_parser.parse(result).as_dict(), indent=4))



print("[extract ping statistics]")
ping()
