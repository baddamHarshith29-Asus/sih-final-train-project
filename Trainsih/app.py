from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from scenario_runner import parse_scenario, build_network, build_trains, enforce_headway, detect_block_conflicts, decide_precedence, run_simulation, compute_kpis
from scenario_schema import Scenario
from gemini_integration_fixed import analyze_scenario_with_ai

app = Flask(__name__)
CORS(app, origins=['*'])  # Enable CORS for all origins

@app.route('/run_scenario', methods=['POST'])
def run_scenario():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400

        print("\n" + "="*50)
        print("=== BACKEND RECEIVED DATA ===")
        print(f"Request method: {request.method}")
        print(f"Content-Type: {request.headers.get('Content-Type')}")
        print(f"Raw data keys: {list(data.keys()) if data else 'None'}")
        print(f"Trains count: {len(data.get('trains', []))}")
        for i, train in enumerate(data.get('trains', [])):
            print(f"  Train {i+1}: ID={train.get('train_id', 'Missing')}, Source={train.get('source', 'Missing')}, Dest={train.get('destination', 'Missing')}")
        print(f"Sections count: {len(data.get('sections', []))}")
        print("\nProcessing with algorithm...")
        print("Algorithm output:")
        print("Conflicts:")
        
        scn = parse_scenario(data)
        network = build_network(scn.sections)
        trains = build_trains(scn)
        enforce_headway(trains, scn.constraints.min_headway_min)
        conflicts = detect_block_conflicts(trains)
        
        # Print conflicts in required format
        for conflict in conflicts:
            print(f"('{conflict[0]}', '{conflict[1]}', '{conflict[2]}', {conflict[3]})")
        
        id_pairs = {tuple(sorted((a, b))) for _, a, b, _ in conflicts}
        decisions = decide_precedence(list(id_pairs), {t.train_id: t for t in trains})
        
        print("Decisions:")
        for tid, action in decisions.items():
            print(f"{tid} -> {action}")
        
        print("\n" + "="*50)

        # Format conflicts
        conflicts_list = []
        for conflict in conflicts:
            conflicts_list.append({
                'block': conflict[0],
                'train_a': conflict[1],
                'train_b': conflict[2],
                'overlap': conflict[3]
            })

        # Format decisions
        decisions_dict = {tid: action for tid, action in decisions.items()}

        return jsonify({
            'conflicts': conflicts_list,
            'decisions': decisions_dict,
            'trains': [{'id': t.train_id, 'path': t.planned_path} for t in trains]
        })
    except Exception as e:
        print(f"Error in run_scenario: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/analyze_scenario', methods=['POST'])
def analyze_scenario():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400

        scn = parse_scenario(data)
        network = build_network(scn.sections)
        trains = build_trains(scn)
        enforce_headway(trains, scn.constraints.min_headway_min)
        conflicts = detect_block_conflicts(trains)
        id_pairs = {tuple(sorted((a, b))) for _, a, b, _ in conflicts}
        decisions = decide_precedence(list(id_pairs), {t.train_id: t for t in trains})
        
        # Run simulation for event log and KPIs
        sim_log = run_simulation(trains)
        kpis = compute_kpis(trains, sim_log)
        
        # Format conflicts for analysis
        conflicts_list = []
        for conflict in conflicts:
            conflicts_list.append({
                'block': conflict[0],
                'train_a': conflict[1],
                'train_b': conflict[2],
                'overlap': conflict[3]
            })

        # Generate detailed AI analysis with Gemini
        gemini_result = analyze_scenario_with_ai(conflicts, decisions)
        analysis = generate_ai_analysis(conflicts_list, decisions, trains, kpis, sim_log, scn)
        
        # Add Gemini analysis to response
        analysis['gemini_output'] = gemini_result['algorithm_output']
        analysis['gemini_analysis'] = gemini_result['gemini_analysis']
        
        return jsonify(analysis)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def generate_ai_analysis(conflicts, decisions, trains, kpis, sim_log, scn):
    """Generate structured AI analysis based on the requested format"""
    
    # 1. Analyze conflicts and decisions
    conflict_analysis = []
    for conflict in conflicts:
        train_a_id = conflict['train_a']
        train_b_id = conflict['train_b']
        train_a = next((t for t in trains if t.train_id == train_a_id), None)
        train_b = next((t for t in trains if t.train_id == train_b_id), None)
        
        if train_a and train_b:
            conflict_analysis.append({
                'block': conflict['block'],
                'trains': [train_a_id, train_b_id],
                'overlap_time': conflict['overlap'],
                'train_a_priority': train_a.priority,
                'train_b_priority': train_b.priority,
                'decision_a': decisions.get(train_a_id, 'UNKNOWN'),
                'decision_b': decisions.get(train_b_id, 'UNKNOWN')
            })
    
    # 2. Reasoning for decisions
    reasoning = []
    for analysis in conflict_analysis:
        train_a_id, train_b_id = analysis['trains']
        if analysis['train_a_priority'] > analysis['train_b_priority']:
            reason = f"Train {train_a_id} (priority {analysis['train_a_priority']}) gets PROCEED over Train {train_b_id} (priority {analysis['train_b_priority']}) due to higher priority"
        elif analysis['train_a_priority'] < analysis['train_b_priority']:
            reason = f"Train {train_b_id} (priority {analysis['train_b_priority']}) gets PROCEED over Train {train_a_id} (priority {analysis['train_a_priority']}) due to higher priority"
        else:
            reason = f"Equal priority trains {train_a_id} and {train_b_id} - decision based on arrival timing and headway constraints"
        reasoning.append({
            'conflict_block': analysis['block'],
            'reasoning': reason
        })
    
    # 3. Rerouting/staggering suggestions
    suggestions = []
    if len(conflicts) > 0:
        suggestions.append("Consider staggering departure times by 5-10 minutes to reduce block conflicts")
        suggestions.append("Evaluate alternative routes through different junctions to distribute traffic")
        suggestions.append("Implement dynamic headway adjustment based on train priority and passenger load")
    else:
        suggestions.append("No conflicts detected - current schedule is optimal")
    
    # 4. KPI impact estimation
    kpi_impact = {
        'throughput_impact': f"{'Positive' if kpis['throughput'] > 100 else 'Negative'} - Current throughput: {kpis['throughput']:.1f} trains/hour",
        'delay_impact': f"{'Minimal' if kpis['average_delay'] < 5 else 'Significant'} - Average delay: {kpis['average_delay']:.1f} minutes",
        'safety_impact': f"Safe - {kpis['safety_violations']} violations detected",
        'punctuality_impact': f"{'Good' if kpis['punctuality'] > 85 else 'Poor'} - Punctuality: {kpis['punctuality']:.1f}%"
    }
    
    # 5. Event log (first 10 events)
    event_log = []
    for i, log_entry in enumerate(sim_log[:10]):
        event_log.append({
            'timestamp': log_entry.split()[0],
            'action': log_entry.split()[1],
            'details': ' '.join(log_entry.split()[2:])
        })
    
    # 6. Fairness assessment
    fairness_score = 0
    total_decisions = len(decisions)
    if total_decisions > 0:
        fair_decisions = sum(1 for train_id, action in decisions.items() 
                           if action == 'PROCEED' and next((t.priority for t in trains if t.train_id == train_id), 0) >= 3)
        fairness_score = (fair_decisions / total_decisions) * 100
    
    fairness_assessment = {
        'score': fairness_score,
        'assessment': 'Fair' if fairness_score >= 70 else 'Needs improvement',
        'explanation': f"Algorithm prioritizes higher-priority trains appropriately in {fairness_score:.1f}% of decisions"
    }
    
    # 7. AI optimization explanation
    optimization_explanation = f"""
    The AI decision engine optimizes this scenario through:
    1. Priority-based conflict resolution: Higher priority trains (passenger/express) get precedence
    2. Headway enforcement: Maintains minimum {scn.constraints.min_headway_min} minute separation
    3. Block occupancy optimization: Minimizes overlap time through intelligent scheduling
    4. Delay propagation control: Limits cascade delays by holding lower-priority trains
    5. Throughput maximization: Balances individual train delays with overall network efficiency
    
    Current optimization results in {kpis['throughput']:.1f} trains/hour throughput with {kpis['average_delay']:.1f} minute average delay.
    """
    
    return {
        'conflict_analysis': conflict_analysis,
        'decision_reasoning': reasoning,
        'optimization_suggestions': suggestions,
        'kpi_impact': kpi_impact,
        'event_log': event_log,
        'fairness_assessment': fairness_assessment,
        'ai_optimization': optimization_explanation.strip(),
        'summary': {
            'total_conflicts': len(conflicts),
            'total_trains': len(trains),
            'decisions_made': len(decisions),
            'overall_efficiency': f"{kpis['punctuality']:.1f}% punctuality"
        }
    }

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'message': 'Backend is running'})

@app.route('/test', methods=['GET', 'POST'])
def test():
    return jsonify({'status': 'success', 'message': 'Backend connection working'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
