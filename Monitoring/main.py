import json
import pingparsing 
from prometheus_client import start_http_server, Gauge
import time
import yaml

#check and read yaml file 
def read_yaml(): 
    path = str(input("Please Enter file path: "))

    try:
        with open(path, 'r') as file:
            yaml_data = yaml.safe_load(file)
        return yaml_data

    except FileNotFoundError:
        print("File not Found")

    except yaml.YAMLError as error:
        print("Error: Invalid YAML format.")
        print(error)

#intialize metric types     
packet_loss_count = Gauge("packet_loss_count", "Packet loss")
packet_loss_rate = Gauge("packet_loss_rate","Packet Loss Rate")
packet_transmit = Gauge('packet_transmit', "Packets Trasmitted") 
packet_receive = Gauge('packet_receive', "Packets Recieved")
rtt_min = Gauge('rtt_min', "Round trip time minimum")
rtt_avg = Gauge('rtt_avg', "Round trip time average")
rtt_max = Gauge('rtt_max', "Round trip time maximum")

def ping(http_port, website, duration):
    start_http_server(http_port)
    print("Prometheus HTTP server started on port 8989")
    while True: 
        ping_parser = pingparsing.PingParsing()
        transmitter = pingparsing.PingTransmitter()
        transmitter.destination = website
        transmitter.count = duration
        result = transmitter.ping()
        ping_result = ping_parser.parse(result).as_dict()
        print(json.dumps(ping_parser.parse(result).as_dict(), indent=4))
        print(ping_result)

        #creating metric variables 
        latency = ping_result['rtt_avg']
        latency_min = ping_result['rtt_min']
        latency_max = ping_result['rtt_max']
        packets_received = ping_result['packet_receive']
        packets_transmited = ping_result['packet_transmit']
        packets_lost = ping_result['packet_loss_count']
        packets_lost_rt = ping_result['packet_loss_rate']
        
        #set metric values 
        rtt_min.set(latency)
        rtt_avg.set(latency_min)
        rtt_max.set(latency_max)
        packet_receive.set(packets_received)
        packet_transmit.set(packets_transmited)
        packet_loss_count.set(packets_lost)
        packet_loss_rate.set(packets_lost_rt)
        time.sleep(3)
        

def main():
    yaml_data = read_yaml()
    if yaml_data is not None:
            for website_info in yaml_data['monitor_targets']:
                website = website_info['website']
                duration = website_info['duration']
                http_port = website_info['port']

                metrics = ping(http_port, website,duration)
                if metrics is not None:
                    print("Metrics collected successfully")
                else:
                    print("Failed to collect metrics")

    else:
        print("Error with YAML file")

main()


