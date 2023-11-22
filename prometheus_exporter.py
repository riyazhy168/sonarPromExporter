from prometheus_client.core import GaugeMetricFamily
import prometheus_client as prom
import time
from sonarqube_exporter import get_all_projects_with_metrics
from prometheus_client import REGISTRY, PROCESS_COLLECTOR, PLATFORM_COLLECTOR

class CustomSonarExporter:

    def __init__(self):
        pass

    def collect(self):
        projects = get_all_projects_with_metrics()

        for project in projects:
            for metric in project.metrics:
                label_list = ['id', 'key', 'name']
                label_values = []
                value_to_set = None

                label_values.append(project.id)
                label_values.append(project.key)
                label_values.append(project.name)
                for metric_value in metric.values:
                    if metric_value[0] == 'value':
                        value_to_set = metric_value[1]
                    else:
                        label_list.append(metric_value[0])
                        label_values.append(metric_value[1])

                gauge = GaugeMetricFamily(
                    name="sonar_{}".format(metric.key),
                    
                    documentation=metric.description,
                    labels=label_list
                )
                # print(gauge)
                gauge.add_metric(
                    labels=label_values,
                    # labels='',
                    value=value_to_set
                )
                # print(gauge,'------------------------')
                yield gauge

if __name__ == "__main__":
    custom_exporter = CustomSonarExporter()
    # print(custom_exporter)
    prom.REGISTRY.register(custom_exporter)

    # REGISTRY.unregister(PROCESS_COLLECTOR)
    # REGISTRY.unregister(PLATFORM_COLLECTOR)
    # REGISTRY.unregister(REGISTRY._names_to_collectors['python_gc_duration_seconds_sum'])
    # REGISTRY.unregister(REGISTRY._names_to_collectors['python_gc_objects_collected_total'])
    
    # REGISTRY.unregister(REGISTRY._names_to_collectors['python_gc_uncollectable_objects_sum'])
    # REGISTRY.unregister(REGISTRY._names_to_collectors['python_gc_collected_objects_sum'])

    # [REGISTRY.unregister(c) for c in [PROCESS_COLLECTOR, PLATFORM_COLLECTOR, REGISTRY._names_to_collectors['python_gc_duration_seconds_sum'], REGISTRY._names_to_collectors['python_gc_uncollectable_objects_sum'], REGISTRY._names_to_collectors['python_gc_collected_objects_sum']]]
    
    # prom.start_http_server(port=9091,addr='http://10.127.98.243')
    prom.start_http_server(9092)

    while True:
        time.sleep(2)