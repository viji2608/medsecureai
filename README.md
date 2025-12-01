# MedSecureAI - HIPAA-Compliant Clinical Assistant

## Quick Start
```bash
# Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run pipeline
python scripts/run_full_pipeline.py

# Start web interface
python src/chatbot.py
```

## Project Structure
- `src/` - Core application code
- `data/` - Medical records (synthetic)
- `web/` - Demo interface
- `docs/` - Evaluation reports
