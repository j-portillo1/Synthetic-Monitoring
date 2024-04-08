import json
import pingparsing 
from prometheus_client import start_http_server, Gauge

#website = input("Enter Website URL: ")
    
packet_loss_count = Gauge("packet_loss_count", "Packet loss")
packet_loss_rate = Gauge("packet_loss_rate","Packet Loss Rate")
packet_transmit = Gauge("packet_transmit", "Packets Trasmitted")
packet_receive = Gauge("packet_recieve", "Packets Recieved")
rtt_min = Gauge("rtt_min", "Round trip time minimum")
rtt_avg = Gauge("rtt_avg", "Round trip time average")
rtt_max = Gauge("rtt_max", "Round trip time maximum")

def ping():
    start_http_server(9090)
    print("Prometheus HTTP server started on port 9090")
    ping_parser = pingparsing.PingParsing()
    transmitter = pingparsing.PingTransmitter()
    transmitter.destination = "www.google.com"
    transmitter.count = 10
    result = transmitter.ping()
    ping_result = ping_parser.parse(result)
    #.as_dict()
    print(ping_result)
    #print(json.dumps(ping_parser.parse(result).as_dict(), indent=4))

    if ping_result.packet_loss_count is not None:
    #print(packet_loss_count.set(ping_result["packet_loss_count"]))
        print(packet_loss_count.set(ping_result.packet_loss_count))

    #packet_loss_rate.set(ping_result["packet_loss_rate"])
    if ping_result.packet_loss_rate is not None:
        print(packet_loss_count.set(ping_result.packet_loss_rate))

    if ping_result.packet_transmit is not None:
        print(packet_transmit.set(ping_result.packet_transmit))
    
    if ping_result.packet_receive is not None:
        print(packet_receive.set(ping_result.packet_receive))

    if ping_result.rtt_min is not None:
        print(rtt_min.set(ping_result.rtt_min))

    if ping_result.rtt_avg is not None:
        print(rtt_avg.set(ping_result.rtt_avg))

    if ping_result.rtt_max is not None: 
        print(rtt_max.set(ping_result.rtt_max))
    

    

    #print(json.dumps(ping_parser.parse(result).as_dict(), indent=4))



print("[extract ping statistics]")
ping()
