#!/usr/bin/env python3
"""
Complete fix for AI system
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app, origins=['*'])

@app.route('/ai_analyze', methods=['POST'])
def ai_analyze():
    try:
        data = request.get_json()
        
        # Extract user input
        train1 = data.get('train1', {})
        train2 = data.get('train2', {})
        
        train1_id = train1.get('id', 'Train1')
        train1_source = train1.get('source', 'A')
        train1_dest = train1.get('destination', 'B')
        train1_priority = train1.get('priority', 'medium')
        
        train2_id = train2.get('id', 'Train2')
        train2_source = train2.get('source', 'A')
        train2_dest = train2.get('destination', 'B')
        train2_priority = train2.get('priority', 'medium')
        
        # Generate conflicts based on actual input
        conflicts = []
        decisions = {}
        
        if train1_source == train2_source and train1_dest == train2_dest:
            # Same route = conflict
            route_name = f"{train1_source}-{train1_dest}"
            conflicts.append((route_name, train1_id, train2_id, (5.0, 60.0)))
            
            # Priority-based decisions
            if train1_priority == 'high' and train2_priority != 'high':
                decisions[train1_id] = 'PROCEED'
                decisions[train2_id] = 'HOLD'
            elif train2_priority == 'high' and train1_priority != 'high':
                decisions[train2_id] = 'PROCEED'
                decisions[train1_id] = 'HOLD'
            else:
                decisions[train1_id] = 'PROCEED'
                decisions[train2_id] = 'HOLD'
        
        # Generate algorithm output
        algorithm_output = "Algorithm output:\nConflicts:\n"
        for conflict in conflicts:
            algorithm_output += f"('{conflict[0]}', '{conflict[1]}', '{conflict[2]}', {conflict[3]})\n"
        
        algorithm_output += "Decisions:\n"
        for train_id, action in decisions.items():
            algorithm_output += f"{train_id} -> {action}\n"
        
        # Generate dynamic AI analysis
        if conflicts:
            ai_analysis = f"""
Analyzing railway traffic control scenario with {len([train1_id, train2_id])} trains.

**1. Analysis of Conflicts and Decisions:**

*   **Conflicts:** The algorithm identifies {len(conflicts)} conflict(s):
    *   **{conflicts[0][0]}:** Trains `{conflicts[0][1]}` and `{conflicts[0][2]}` are competing for the same track segment.

*   **Decisions:**
    *   `{train1_id} -> {decisions.get(train1_id, 'PROCEED')}`: {'Train is given priority to proceed.' if decisions.get(train1_id) == 'PROCEED' else 'Train is instructed to hold.'}
    *   `{train2_id} -> {decisions.get(train2_id, 'HOLD')}`: {'Train is given priority to proceed.' if decisions.get(train2_id) == 'PROCEED' else 'Train is instructed to hold.'}

**2. Reasoning:**
Priority-based conflict resolution. Higher priority trains get precedence.

**3. Suggestions:**
- Stagger departure times by 10-15 minutes
- Consider alternative routing if available
- Implement dynamic speed adjustment
"""
        else:
            ai_analysis = "No conflicts detected. All trains can proceed without interference."
        
        print("\n" + "="*50)
        print("USER INPUT PROCESSED:")
        print(f"Train 1: {train1_id} ({train1_source} -> {train1_dest}) Priority: {train1_priority}")
        print(f"Train 2: {train2_id} ({train2_source} -> {train2_dest}) Priority: {train2_priority}")
        print("\n" + algorithm_output)
        print("="*50)
        
        return jsonify({
            'algorithm_output': algorithm_output,
            'ai_analysis': ai_analysis.strip(),
            'conflicts': [{'block': c[0], 'train_a': c[1], 'train_b': c[2], 'overlap': c[3]} for c in conflicts],
            'decisions': decisions,
            'success': True
        })
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting Fixed AI Backend...")
    print("URL: http://localhost:5001")
    app.run(debug=True, host='0.0.0.0', port=5001)