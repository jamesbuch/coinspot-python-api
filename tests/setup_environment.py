import os
import sys

def is_venv_activated():
    return hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)

def activate_virtual_env():
    venv_path = os.path.join(os.path.dirname(__file__), '.venv')
    activate_this = os.path.join(venv_path, 'bin', 'activate')
    
    if os.path.exists(activate_this):
        print("Virtual environment found. Activating...")
        exec(open(activate_this).read(), {'__file__': activate_this})
        return True
    else:
        print("Virtual environment not found. Assuming system Python...")
        return False

def main():
    if 'CI' in os.environ:
        print("Running in CI environment.")
        # No need to activate venv in CI, GitHub Actions will handle this
    else:
        print("Running locally.")
        if not is_venv_activated():
            activate_virtual_env()
        else:
            print("Virtual environment is already activated.")

if __name__ == "__main__":
    main()