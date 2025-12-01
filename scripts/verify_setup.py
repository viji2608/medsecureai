#!/usr/bin/env python3
"""Verify Phase 1 setup is complete"""

import os
import sys

def check_setup():
    checks = []
    
    # Check 1: Directory structure
    required_dirs = ['data', 'src', 'logs', 'docs', 'web', 'scripts']
    for dir_name in required_dirs:
        exists = os.path.exists(dir_name)
        checks.append(('Directory: ' + dir_name, exists))
    
    # Check 2: Python modules
    try:
        import torch
        import pandas
        import sentence_transformers
        from fastapi import FastAPI
        checks.append(('Dependencies installed', True))
    except ImportError as e:
        checks.append(('Dependencies installed', False))
        print(f"Missing: {e}")
    
    # Check 3: Data file
    data_exists = os.path.exists('data/synthetic_records.csv')
    checks.append(('Synthetic data generated', data_exists))
    
    # Check 4: Source files
    src_files = ['data_prep.py', 'embedding.py', 'cyborg_client.py']
    for file in src_files:
        exists = os.path.exists(f'src/{file}')
        checks.append((f'Source file: {file}', exists))
    
    # Print results
    print("=" * 60)
    print("🔍 Phase 1 Setup Verification")
    print("=" * 60)
    
    all_passed = True
    for check_name, passed in checks:
        status = "✅" if passed else "❌"
        print(f"{status} {check_name}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    if all_passed:
        print("🎉 Phase 1 Complete! Ready for Phase 2.")
    else:
        print("⚠️  Some checks failed. Review setup steps.")
        sys.exit(1)

if __name__ == "__main__":
    check_setup()
