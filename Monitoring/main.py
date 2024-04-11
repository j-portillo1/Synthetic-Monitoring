import json
import pingparsing 
from prometheus_client import start_http_server, Gauge
import time

#website = input("Enter Website URL: ")
#intialize metric types     
packet_loss_count = Gauge("packet_loss_count", "Packet loss")
packet_loss_rate = Gauge("packet_loss_rate","Packet Loss Rate")
packet_transmit = Gauge('packet_transmit', "Packets Trasmitted") #,['host'])
packet_receive = Gauge('packet_receive', "Packets Recieved")#,['host'])
rtt_min = Gauge('rtt_min', "Round trip time minimum")#,['host'])
rtt_avg = Gauge('rtt_avg', "Round trip time average")#,['host'])
rtt_max = Gauge('rtt_max', "Round trip time maximum")#,['host'])

def ping():
    start_http_server(8989)
    print("Prometheus HTTP server started on port 8989")
    while True: 
        ping_parser = pingparsing.PingParsing()
        transmitter = pingparsing.PingTransmitter()
        transmitter.destination = "www.google.com"
        transmitter.count = 10
        result = transmitter.ping()
        ping_result = ping_parser.parse(result).as_dict()
        print(json.dumps(ping_parser.parse(result).as_dict(), indent=4))
        print(ping_result)

        
        latency = ping_result['rtt_avg']
        latency_min = ping_result['rtt_min']
        latency_max = ping_result['rtt_max']
        packets_received = ping_result['packet_receive']
        packets_transmited = ping_result['packet_transmit']
        packets_lost = ping_result['packet_loss_count']
        packets_lost_rt = ping_result['packet_loss_rate']
        
        print(latency)
        print(latency_min)
        print(latency_max)
        print(packets_received)
        print(packets_transmited)
        print(packets_lost)
        print(packets_lost_rt)
        
        #set metric values 
        rtt_min.set(latency)
        rtt_avg.set(latency_min)
        rtt_max.set(latency_max)
        packet_receive.set(packets_received)
        packet_transmit.set(packets_transmited)
        packet_loss_count.set(packets_lost)
        packet_loss_rate.set(packets_lost_rt)
        time.sleep(3)
        


#print("[extract ping statistics]")
ping()
