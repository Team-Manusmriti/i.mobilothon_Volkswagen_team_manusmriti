import carla

def find_blueprints_broad():
    try:
        client = carla.Client('localhost', 2000)
        client.set_timeout(5.0)
        world = client.get_world()
        blueprint_library = world.get_blueprint_library()

        print("\n--- 1. Available 'particle' blueprints ---")
        particle_bps = blueprint_library.filter('particle')
        for bp in particle_bps:
            print(bp.id)
        if not particle_bps:
            print("(No 'particle' blueprints found)")

        print("\n--- 2. Available 'static.prop' blueprints (walls, ramps, etc.) ---")
        prop_bps = blueprint_library.filter('static.prop')
        for bp in prop_bps:
            print(bp.id)
        if not prop_bps:
            print("(No 'static.prop' blueprints found)")

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please ensure the Carla simulator is running.")

if __name__ == '__main__':
    find_blueprints_broad()