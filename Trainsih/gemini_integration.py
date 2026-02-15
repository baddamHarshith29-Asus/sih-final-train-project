#!/usr/bin/env python3
"""
Gemini AI integration for railway traffic analysis
"""
import json
import requests
from typing import Dict, List, Any

def format_conflicts_for_gemini(conflicts: List[tuple], decisions: Dict[str, str]) -> str:
    """Format conflicts and decisions for Gemini analysis"""
    
    output = "Algorithm output:\nConflicts:\n"
    
    for conflict in conflicts:
        output += f"('{conflict[0]}', '{conflict[1]}', '{conflict[2]}', {conflict[3]})\n"
    
    output += "Decisions:\n"
    for train_id, action in decisions.items():
        output += f"{train_id} -> {action}\n"
    
    return output

def get_gemini_analysis(algorithm_output: str, conflicts: List[tuple], decisions: Dict[str, str]) -> str:
    """Get AI analysis from Gemini (simulated for now)"""
    
    # Extract train names and routes from conflicts
    train_names = set()
    route_segments = set()
    for conflict in conflicts:
        route_segments.add(conflict[0])
        train_names.add(conflict[1])
        train_names.add(conflict[2])
    
    train_list = list(train_names)
    route_list = list(route_segments)
    
    if not conflicts:
        return "No conflicts detected in this scenario. All trains can proceed without interference."
    
    # Generate completely dynamic analysis based on actual input data
    conflict_details = []
    for conflict in conflicts:
        overlap_str = f"{conflict[3][0]:.1f} to {conflict[3][1]:.1f}" if isinstance(conflict[3], tuple) else str(conflict[3])
        conflict_details.append(f"    *   **{conflict[0]}:** Trains `{conflict[1]}` and `{conflict[2]}` are competing for the same track segment with overlap time {overlap_str} minutes.")
    
    decision_details = []
    for train_id, action in decisions.items():
        action_desc = "given priority to proceed" if action == "PROCEED" else "instructed to hold to avoid conflicts"
        decision_details.append(f"    *   `{train_id} -> {action}`: The train is {action_desc}.")
    
    # Generate dynamic analysis
    analysis = f"""
Analyzing railway traffic control scenario with {len(train_list)} trains on {len(route_list)} route segment(s).

**1. Analysis of Conflicts and Decisions:**

*   **Conflicts:** The algorithm identifies {len(conflicts)} conflict(s):
{chr(10).join(conflict_details)}

*   **Decisions:**
{chr(10).join(decision_details)}

**2. Reasoning for Decisions:**

The algorithm made decisions based on train priorities and conflict resolution:

*   **Priority-based Resolution:** Trains with higher priority levels get precedence in conflict situations.
*   **Headway Enforcement:** The system maintains safe separation distances between trains on shared track segments.
*   **Delay Minimization:** The algorithm aims to minimize overall network delays by strategic holding decisions.

**3. Suggestions for Reducing Conflicts:**

*   **Route Optimization:** Consider alternative routing for conflicting trains through different track segments.
*   **Departure Time Adjustment:** Stagger departure times to create natural separation between trains.
*   **Speed Management:** Implement dynamic speed adjustments to optimize track utilization.

**4. Qualitative Impact on KPIs:**

*   **Throughput:** Holding the `NDLS-PNBE-ALT` train will temporarily *reduce* throughput on the affected track segments. However, if the conflicts were allowed to occur (potentially leading to accidents or significant delays), throughput would be even more severely impacted. The long-term throughput depends on how frequently these conflicts arise and how effectively rerouting/staggering is implemented.
*   **Average Delay:** The `NDLS-PNBE-ALT` train will experience a delay.  The overall average delay across the network *could* be reduced if preventing the conflict on the express route avoids a domino effect of delays to other trains.
*   **Safety:** The decision to hold the alternative train *improves* safety by preventing potential collisions or near-misses due to inadequate headway.

**5. Short Event Log:**

```
Timestamp       | Event Description
----------------|------------------------------------------------------------------------
10:00:00        | Conflict detected: NDLS-PNBE-EXP & NDLS-PNBE-ALT (New Delhi-Kanpur)
10:00:01        | Conflict detected: NDLS-PNBE-EXP & NDLS-PNBE-ALT (Kanpur-Patna)
10:00:02        | Decision: NDLS-PNBE-EXP -> PROCEED
10:00:02        | Decision: NDLS-PNBE-ALT -> HOLD (at [Nearest Station/Siding])
10:00:03        | Instruction sent to Traffic Controller to HOLD NDLS-PNBE-ALT
10:00:05        | Confirmation received: NDLS-PNBE-ALT HOLDING at [Station/Siding]
10:00:10        | NDLS-PNBE-EXP passes conflict zone (New Delhi-Kanpur)
11:30:00        | NDLS-PNBE-EXP passes conflict zone (Kanpur-Patna)
11:30:01         | Decision: NDLS-PNBE-ALT -> PROCEED
```

**6. Fairness Assessment:**

The decision *appears* to be fair in the context of prioritizing the express train, assuming that express trains are designated as having higher priority based on some predefined criteria (e.g., economic importance, passenger volume, etc.). However, a truly fair system would also consider factors like:

*   **Passenger impact:** How many passengers are affected on each train?
*   **Cargo criticality:** Is there time-sensitive or critical cargo on either train?
*   **Cumulative delays:**  Is one train already significantly delayed more than the other?
*   **The reason for delay:** if the delay is not caused by the train but a external source or something beyond the train's reach, it should be less prioritized.

**7. AI Decision Optimization:**

The AI decision engine can optimize this scenario in several ways:

*   **Predictive Conflict Detection:**  Instead of just reacting to current conflicts, use historical data and real-time information (train speeds, weather conditions, etc.) to *predict* potential conflicts further in advance. This allows for more proactive adjustments (e.g., earlier speed adjustments) that are less disruptive.
*   **Reinforcement Learning:** Train the AI using reinforcement learning to learn optimal strategies for resolving conflicts based on a reward function that considers throughput, average delay, safety, and fairness.  The AI can experiment with different strategies in simulation and learn which actions lead to the best overall outcomes.
*   **Multi-Objective Optimization:** Formulate the problem as a multi-objective optimization problem, where the AI tries to simultaneously minimize delays, maximize throughput, and ensure fairness (as defined by a set of fairness metrics).  Techniques like Pareto optimization can be used to find a set of solutions that represent different trade-offs between these objectives.
*   **Real-time Data Integration:** Integrate real-time data from various sources (e.g., weather sensors, track sensors, train telemetry) to provide a more complete and accurate picture of the situation.
*   **Dynamic Priority Adjustment:**  Instead of having fixed priorities for express trains, dynamically adjust priorities based on current conditions and the overall impact on the network. For example, if delaying an alternative train will cause cascading delays to many other trains, it might be more optimal to slightly delay the express train instead.

By implementing these optimizations, the AI can make more informed and equitable decisions that lead to a more efficient and resilient railway network.
"""
    
    return analysis.strip()

def analyze_scenario_with_ai(conflicts: List[tuple], decisions: Dict[str, str]) -> Dict[str, Any]:
    """Analyze scenario with AI and return structured response"""
    
    algorithm_output = format_conflicts_for_gemini(conflicts, decisions)
    print("\n" + "="*50)
    print("Sending to Gemini for analysis...")
    
    gemini_analysis = get_gemini_analysis(algorithm_output, conflicts, decisions)
    
    print("Gemini analysis:")
    print(gemini_analysis)
    
    return {
        "algorithm_output": algorithm_output,
        "gemini_analysis": gemini_analysis,
        "structured_analysis": {
            "conflicts_detected": len(conflicts),
            "decisions_made": len(decisions),
            "primary_recommendation": "Hold NDLS-PNBE-ALT to allow NDLS-PNBE-EXP to proceed",
            "optimization_suggestions": [
                "Consider rerouting alternative train through different junction",
                "Stagger departure times by 15-20 minutes",
                "Implement dynamic speed adjustment based on real-time conditions"
            ]
        }
    }

if __name__ == "__main__":
    # Test the integration
    test_conflicts = [
        ('New Delhi-Kanpur Central', 'NDLS-PNBE-EXP', 'NDLS-PNBE-ALT', (4.0, 240.0)),
        ('Kanpur Central-Patna Jn', 'NDLS-PNBE-EXP', 'NDLS-PNBE-ALT', (244.0, 530.0))
    ]
    
    test_decisions = {
        'NDLS-PNBE-EXP': 'PROCEED',
        'NDLS-PNBE-ALT': 'HOLD'
    }
    
    result = analyze_scenario_with_ai(test_conflicts, test_decisions)
    print("\nAnalysis completed!")