import time
import random
import requests
import json
from datetime import datetime

# Generate test metrics and traces for SigNoz
def send_test_metrics():
    """Send some test metrics to the OTLP HTTP endpoint"""
    
    # Sample metrics payload
    metrics_payload = {
        "resourceMetrics": [
            {
                "resource": {
                    "attributes": [
                        {"key": "service.name", "value": {"stringValue": "database-automation-test"}},
                        {"key": "service.version", "value": {"stringValue": "1.0.0"}}
                    ]
                },
                "scopeMetrics": [
                    {
                        "scope": {"name": "database-automation"},
                        "metrics": [
                            {
                                "name": "mysql_connections_active",
                                "description": "Active MySQL connections",
                                "unit": "1",
                                "gauge": {
                                    "dataPoints": [
                                        {
                                            "timeUnixNano": str(int(time.time() * 1e9)),
                                            "asInt": str(random.randint(1, 10))
                                        }
                                    ]
                                }
                            },
                            {
                                "name": "database_query_duration",
                                "description": "Database query execution time",
                                "unit": "ms",
                                "histogram": {
                                    "dataPoints": [
                                        {
                                            "timeUnixNano": str(int(time.time() * 1e9)),
                                            "count": str(random.randint(10, 100)),
                                            "sum": random.uniform(100, 1000),
                                            "bucketCounts": ["0", "5", "10", "15"],
                                            "explicitBounds": [0.1, 0.5, 1.0, 5.0]
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                ]
            }
        ]
    }
    
    try:
        response = requests.post(
            "http://localhost:4318/v1/metrics",
            headers={"Content-Type": "application/json"},
            json=metrics_payload,
            timeout=5
        )
        print(f"Metrics sent: {response.status_code}")
        return response.status_code == 200
    except Exception as e:
        print(f"Failed to send metrics: {e}")
        return False

def send_test_traces():
    """Send test traces to the OTLP HTTP endpoint"""
    
    trace_id = format(random.getrandbits(128), '032x')
    span_id = format(random.getrandbits(64), '016x')
    
    traces_payload = {
        "resourceSpans": [
            {
                "resource": {
                    "attributes": [
                        {"key": "service.name", "value": {"stringValue": "database-automation"}},
                        {"key": "service.version", "value": {"stringValue": "1.0.0"}}
                    ]
                },
                "scopeSpans": [
                    {
                        "scope": {"name": "database-automation"},
                        "spans": [
                            {
                                "traceId": trace_id,
                                "spanId": span_id,
                                "name": "mysql_query_execution",
                                "kind": 1,
                                "startTimeUnixNano": str(int((time.time() - 1) * 1e9)),
                                "endTimeUnixNano": str(int(time.time() * 1e9)),
                                "attributes": [
                                    {"key": "db.system", "value": {"stringValue": "mysql"}},
                                    {"key": "db.operation", "value": {"stringValue": "SELECT"}},
                                    {"key": "db.table", "value": {"stringValue": "person"}}
                                ],
                                "status": {"code": 1}
                            }
                        ]
                    }
                ]
            }
        ]
    }
    
    try:
        response = requests.post(
            "http://localhost:4318/v1/traces",
            headers={"Content-Type": "application/json"},
            json=traces_payload,
            timeout=5
        )
        print(f"Traces sent: {response.status_code}")
        return response.status_code == 200
    except Exception as e:
        print(f"Failed to send traces: {e}")
        return False

def main():
    print("🚀 Sending test telemetry data to SigNoz...")
    
    # Send data multiple times to populate the dashboard
    for i in range(5):
        print(f"\n📊 Round {i+1}/5")
        
        metrics_ok = send_test_metrics()
        traces_ok = send_test_traces()
        
        if metrics_ok or traces_ok:
            print("✅ Data sent successfully")
        else:
            print("❌ Failed to send data")
        
        time.sleep(2)
    
    print("\n🎯 Test data generation complete!")
    print("🌐 Check SigNoz at http://localhost:8081")
    print("📱 Navigate to Services, Traces, or Dashboards to see the data")

if __name__ == "__main__":
    main()
