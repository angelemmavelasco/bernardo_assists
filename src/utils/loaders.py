import os
import yaml

def load_prompts():
    """
    load prompts from the YAML file and return them as a dictionary.
    """
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, "prompts.yaml")
    
    with open(file_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)
    
PROMPTS = load_prompts()