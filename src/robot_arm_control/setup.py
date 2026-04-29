from setuptools import setup
import os
from glob import glob

package_name = 'robot_arm_control'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
        (os.path.join('share', package_name, 'urdf'), glob('urdf/*.urdf')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='user',
    description='Robot Arm Control',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'trajectory_server = robot_arm_control.trajectory_server:main',
            'robot_state = robot_arm_control.robot_state:main',
        ],
    },
)
