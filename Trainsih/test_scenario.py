#!/usr/bin/env python3
"""
Test script to verify the scenario processing works correctly
"""
import json
from scenario_runner import parse_scenario, build_network, build_trains, enforce_headway, detect_block_conflicts, decide_precedence

# Test scenario with realistic data
test_scenario = {
    "trains": [
        {
            "train_id": "NDLS-PNBE-EXP",
            "name": "New Delhi Patna Express",
            "train_type": "passenger",
            "priority_level": "High",
            "speed_kmph": 80,
            "length_m": 200,
            "sched_departure": "08:00",
            "sched_arrival": "18:00",
            "source": "New Delhi",
            "destination": "Patna Jn",
            "route_path": ["New Delhi", "Kanpur Central", "Patna Jn"]
        },
        {
            "train_id": "NDLS-PNBE-ALT",
            "name": "New Delhi Patna Alternative",
            "train_type": "passenger",
            "priority_level": "Medium",
            "speed_kmph": 60,
            "length_m": 180,
            "sched_departure": "08:30",
            "sched_arrival": "19:00",
            "source": "New Delhi",
            "destination": "Patna Jn",
            "route_path": ["New Delhi", "Kanpur Central", "Patna Jn"]
        }
    ],
    "sections": [
        {"from_node": "New Delhi", "to_node": "Kanpur Central", "travel_time_min": 240.0, "availability": "single", "section_capacity": 1, "signalling": "Automatic Block"},
        {"from_node": "Kanpur Central", "to_node": "Patna Jn", "travel_time_min": 290.0, "availability": "single", "section_capacity": 1, "signalling": "Automatic Block"}
    ],
    "stations": [
        {"station_id": "New Delhi", "platform_count": 16, "platform_length_m": 700, "halt_time_min": 2.0, "station_priority": "major_junction"},
        {"station_id": "Kanpur Central", "platform_count": 8, "platform_length_m": 500, "halt_time_min": 3.0, "station_priority": "major_junction"},
        {"station_id": "Patna Jn", "platform_count": 10, "platform_length_m": 600, "halt_time_min": 2.0, "station_priority": "major_junction"}
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

def test_scenario_processing():
    print("Testing scenario processing...")
    print("=" * 50)
    
    try:
        # Parse scenario
        scn = parse_scenario(test_scenario)
        print(f"Parsed scenario with {len(scn.trains)} trains")
        
        # Build network
        network = build_network(scn.sections)
        print(f"Built network with {len(network.nodes)} nodes")
        
        # Build trains
        trains = build_trains(scn)
        print(f"Built {len(trains)} trains with routes")
        
        for train in trains:
            print(f"  - {train.train_id}: {' -> '.join(train.planned_path)}")
        
        # Enforce headway
        enforce_headway(trains, scn.constraints.min_headway_min)
        print("Enforced headway constraints")
        
        # Detect conflicts
        conflicts = detect_block_conflicts(trains)
        print(f"Detected {len(conflicts)} conflicts")
        
        print("\nAlgorithm output:")
        print("Conflicts:")
        for conflict in conflicts:
            print(f"('{conflict[0]}', '{conflict[1]}', '{conflict[2]}', {conflict[3]})")
        
        # Make decisions
        id_pairs = {tuple(sorted((a, b))) for _, a, b, _ in conflicts}
        decisions = decide_precedence(list(id_pairs), {t.train_id: t for t in trains})
        
        print("Decisions:")
        for tid, action in decisions.items():
            print(f"{tid} -> {action}")
        
        print("\n" + "=" * 50)
        print("Test completed successfully!")
        
        return True
        
    except Exception as e:
        print(f"Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_scenario_processing()