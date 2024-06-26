import json
import pingparsing 
from prometheus_client import start_http_server, Gauge
import time
import yaml

#check and read yaml file 
def read_yaml(): 
    path = "Monitoring/Configurations/config.yaml" 

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
packet_loss_count = Gauge("packet_loss_count", "Packet loss", ['host'])
packet_loss_rate = Gauge("packet_loss_rate","Packet Loss Rate",['host'])
packet_transmit = Gauge('packet_transmit', "Packets Trasmitted",['host']) 
packet_receive = Gauge('packet_receive', "Packets Recieved",['host'])
rtt_min = Gauge('rtt_min', "Round trip time minimum",['host'])
rtt_avg = Gauge('rtt_avg', "Round trip time average",['host'])
rtt_max = Gauge('rtt_max', "Round trip time maximum",['host'])

def ping(website, duration):
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

    # Return the metrics as a dictionary
    return {
        'latency': latency,
        'latency_min': latency_min,
        'latency_max': latency_max,
        'packets_received': packets_received,
        'packets_transmitted': packets_transmited,
        'packets_lost': packets_lost,
        'packets_lost_rt': packets_lost_rt
    }
        
        
def set_metrics(website, metrics):
        #set metric values 
        rtt_min.labels(host=website).set(metrics['latency'])
        rtt_avg.labels(host=website).set(metrics['latency_min'])
        rtt_max.labels(host=website).set(metrics['latency_max'])
        packet_receive.labels(host=website).set(metrics['packets_received'])
        packet_transmit.labels(host=website).set(metrics['packets_transmitted'])
        packet_loss_count.labels(host=website).set(metrics['packets_lost'])
        packet_loss_rate.labels(host=website).set(metrics['packets_lost_rt'])
        time.sleep(3)
        

def main():
    yaml_data = read_yaml()
    if yaml_data is not None:
        print("Prometheus HTTP server started on port 8989")
        start_http_server(8989)

        while True:
            for website_info in yaml_data['monitor_targets']:
                website = website_info['website']
                duration = yaml_data['duration']
               
                metrics = ping(website,duration)
                if metrics is not None:
                    print("Metrics collected successfully")
                    set_metrics(website, metrics)
                else:
                    print("Failed to collect metrics")
    else:
        print("Error with YAML file")

main()