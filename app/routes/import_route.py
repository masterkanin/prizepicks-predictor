from flask import Blueprint, jsonify
import subprocess
import os

import_bp = Blueprint('import', __name__)

@import_bp.route('/run-import', methods=['GET'])
def run_import():
    try:
        # Run the import script
        result = subprocess.run(['python', 'import_predictions.py'], 
                               capture_output=True, text=True)
        
        if result.returncode == 0:
            return jsonify({
                'success': True,
                'message': 'Predictions imported successfully',
                'details': result.stdout
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Error importing predictions',
                'details': result.stderr
            }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Exception: {str(e)}'
        }), 500
