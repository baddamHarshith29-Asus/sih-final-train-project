import requests
import json

def test_backend():
    try:
        # Test health endpoint
        response = requests.get('http://localhost:5000/health', timeout=5)
        print(f"Health check: {response.status_code} - {response.json()}")
        
        # Test analyze_scenario endpoint
        test_data = {
            "trains": [
                {
                    "train_id": "TEST-001",
                    "name": "Test Train 1",
                    "train_type": "passenger",
                    "priority_level": "High",
                    "speed_kmph": 80,
                    "length_m": 200,
                    "sched_departure": "08:00",
                    "sched_arrival": "12:00",
                    "source": "A",
                    "destination": "B",
                    "route_path": ["A", "B"]
                },
                {
                    "train_id": "TEST-002",
                    "name": "Test Train 2",
                    "train_type": "passenger",
                    "priority_level": "Medium",
                    "speed_kmph": 60,
                    "length_m": 150,
                    "sched_departure": "08:15",
                    "sched_arrival": "13:00",
                    "source": "A",
                    "destination": "B",
                    "route_path": ["A", "B"]
                }
            ],
            "sections": [
                {"from_node": "A", "to_node": "B", "travel_time_min": 60.0, "availability": "single", "section_capacity": 1, "signalling": "Automatic Block"}
            ],
            "stations": [
                {"station_id": "A", "platform_count": 4, "platform_length_m": 400, "halt_time_min": 2.0, "station_priority": "major_junction"},
                {"station_id": "B", "platform_count": 4, "platform_length_m": 400, "halt_time_min": 2.0, "station_priority": "major_junction"}
            ],
            "constraints": {
                "min_headway_min": 2.0,
                "allow_overtake": True,
                "crossing_rule": "passenger_first",
                "track_conflict_rule": "single_line_opposite_forbidden"
            },
            "simulation": {
                "simulation_speed": "realtime",
                "num_trains": 2,
                "scenario_type": "normal",
                "optimization_goal": "prioritize_passenger"
            }
        }
        
        response = requests.post('http://localhost:5000/analyze_scenario', 
                               json=test_data, 
                               timeout=10)
        print(f"Analyze scenario: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print("Backend is working correctly!")
            return True
        else:
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"Backend test failed: {e}")
        return False

if __name__ == "__main__":
    test_backend()