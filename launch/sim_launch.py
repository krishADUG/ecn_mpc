from simple_launch import SimpleLauncher


def generate_launch_description():

    sl = SimpleLauncher()
    manual = sl.declare_arg('manual', False)

    # run simulation
    sl.include('map_simulator', 'simulation2d_launch.py',
        launch_arguments={'map': sl.find('ecn_mpc', 'ecn_map.yaml'),
                                'display': False,
                                'map_server': True})

    # spawn Zoe vehicle
    sl.include('ecn_mpc', 'zoe_launch.py',
               launch_arguments={'manual': manual, 'x': 190.35, 'y': 67.36, 'theta': 0.14})

    # run RViz
    sl.rviz(sl.find('ecn_mpc', 'zoe.rviz'))

    # run global planner
    with sl.group(ns = 'zoe'):
        sl.node('nav2_planner', 'planner_server',
                parameters = [sl.find('ecn_mpc', 'nav2.yaml')],
                remappings = {'/zoe/map': '/map','map': '/map'})
        sl.node('nav2_lifecycle_manager','lifecycle_manager',name='lifecycle_manager',
                output='screen',
                parameters=[{'autostart': True,
                            'node_names': ['planner_server']}])

        sl.node('ecn_mpc', 'navigator')

    return sl.launch_description()
