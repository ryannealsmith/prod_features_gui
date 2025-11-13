"""Seed initial configuration data into the database."""
import database

db = database.Database()
db.connect()

# Initial configuration data
initial_configs = [
    # Platforms
    {'config_type': 'Platform', 'code': 'Terberg-1', 'description': 'Terberg autonomous vehicle platform - Generation 1'},
    {'config_type': 'Platform', 'code': 'Terberg-2', 'description': 'Terberg autonomous vehicle platform - Generation 2'},
    
    # ODDs
    {'config_type': 'ODD', 'code': 'CFG-ODD-1', 'description': 'Controlled environment with minimal external traffic'},
    {'config_type': 'ODD', 'code': 'CFG-ODD-2', 'description': 'Semi-controlled environment with limited external traffic'},
    {'config_type': 'ODD', 'code': 'CFG-ODD-3', 'description': 'Open environment with mixed traffic conditions'},
    
    # Environments
    {'config_type': 'Environment', 'code': 'CFG-ENV-1.1', 'description': 'Indoor warehouse - Basic navigation'},
    {'config_type': 'Environment', 'code': 'CFG-ENV-1.2', 'description': 'Indoor warehouse - Advanced operations'},
    {'config_type': 'Environment', 'code': 'CFG-ENV-2.1', 'description': 'Outdoor yard - Controlled area (includes CFG-ENV-1.1)'},
    {'config_type': 'Environment', 'code': 'CFG-ENV-2.2', 'description': 'Outdoor yard - Extended area'},
    {'config_type': 'Environment', 'code': 'CFG-ENV-3.1', 'description': 'Mixed indoor/outdoor - Basic integration'},
    
    # Trailers
    {'config_type': 'Trailer', 'code': 'Standard-20ft', 'description': '20-foot standard trailer configuration'},
    {'config_type': 'Trailer', 'code': 'Standard-40ft', 'description': '40-foot standard trailer configuration'},
    {'config_type': 'Trailer', 'code': 'Flatbed', 'description': 'Flatbed trailer for specialized cargo'},
    {'config_type': 'Trailer', 'code': 'Refrigerated', 'description': 'Temperature-controlled trailer unit'},
    
    # TRLs
    {'config_type': 'TRL', 'code': 'TRL 3', 'description': 'Proof of Concept - Experimental proof of concept validated'},
    {'config_type': 'TRL', 'code': 'TRL 6', 'description': 'Prototype - Technology demonstrated in relevant environment'},
    {'config_type': 'TRL', 'code': 'TRL 9', 'description': 'Production - Actual system proven in operational environment'},
]

# Check if configurations already exist
existing = db.get_configurations()
if not existing:
    print('Seeding initial configuration data...')
    for config in initial_configs:
        try:
            db.add_configuration(config)
            print(f'  Added: {config["config_type"]} - {config["code"]}')
        except Exception as e:
            print(f'  Skipped {config["code"]} (already exists or error): {e}')
    print('Seeding complete!')
else:
    print(f'Database already has {len(existing)} configurations, skipping seed.')

db.close()
