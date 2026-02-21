import yaml

def load_workspace_from_yaml(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    workspace = data.get('Workspace', {})
    return workspace


def is_save_position(pos):
    workspace = load_workspace_from_yaml('pose.yaml')
    x, y, z = pos
    if workspace['X_min'] <= x <= workspace['X_max'] and \
       workspace['Y_min'] <= y <= workspace['Y_max'] and \
       workspace['Z_min'] <= z <= workspace['Z_max']:
        return True
    return False