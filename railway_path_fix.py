import os
import sys
import re

def fix_paths_for_railway():
    """
    Fix hardcoded paths in Python files for Railway deployment.
    """
    print("Fixing hardcoded paths for Railway deployment...")
    
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    # Files to fix
    files_to_fix = [
        'app/routes/predictions.py',
        'app/routes/main.py',
        'app/routes/api.py',
        'app/__init__.py',
        'app/api/live_data_pipeline.py',
        'app/api/sportradar_client.py',
        'run.py',
        'deploy.py',
        'data_pipeline.py',
        'data_pipeline_scheduled.py'
    ]
    
    # Patterns to replace
    patterns = [
        (r"logging\.FileHandler\(['\"]\/home\/ubuntu\/sports_predictor_web\/logs\/([^'\"]+)['\"]", r"logging.FileHandler('logs/\1'"),
        (r"logging\.FileHandler\(['\"]\/home\/ubuntu\/sports_predictor\/home\/ubuntu\/neural_sports_predictor\/logs\/([^'\"]+)['\"]", r"logging.FileHandler('logs/\1'"),
        (r"os\.path\.join\(os\.path\.dirname\(os\.path\.dirname\(__file__\)\), 'logs\/([^']+)'\)", r"os.path.join('logs', '\1')"),
        (r"predictor_output_dir = ['\"]\/home\/ubuntu\/sports_predictor\/home\/ubuntu\/neural_sports_predictor\/output\/predictions['\"]", r"predictor_output_dir = 'output/predictions'"),
        (r"WEB_APP_PATH = ['\"]\/home\/ubuntu\/sports_predictor_web['\"]", r"WEB_APP_PATH = '.'")
    ]
    
    # Process each file
    for file_path in files_to_fix:
        if not os.path.exists(file_path):
            print(f"Warning: File {file_path} not found, skipping...")
            continue
            
        print(f"Processing {file_path}...")
        
        # Read file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Apply all patterns
        modified = False
        for pattern, replacement in patterns:
            new_content, count = re.subn(pattern, replacement, content)
            if count > 0:
                content = new_content
                modified = True
                print(f"  - Fixed {count} occurrences in {file_path}")
        
        # Special case for any remaining hardcoded paths
        if '/home/ubuntu/sports_predictor_web/logs/' in content:
            content = content.replace('/home/ubuntu/sports_predictor_web/logs/', 'logs/')
            modified = True
            print(f"  - Fixed additional hardcoded paths in {file_path}")
        
        # Write back if modified
        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  - Updated {file_path}")
        else:
            print(f"  - No changes needed in {file_path}")
    
    print("\nCreating output directories...")
    os.makedirs('output/predictions', exist_ok=True)
    
    print("\nPath fixes completed. You can now commit and push these changes to deploy to Railway.")

if __name__ == "__main__":
    fix_paths_for_railway()
