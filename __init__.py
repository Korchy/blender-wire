# Nikita Akimov
# interplanety@interplanety.org

from .addon import Addon
from . import wire_ops
from . import wire_panel
from . import wire_preferences


bl_info = {
    'name': 'wire',
    'category': 'Render',
    'author': 'Nikita Akimov',
    'version': (1, 0, 0),
    'blender': (2, 80, 0),
    'location': 'N-panel - Wire tab',
    'wiki_url': 'https://b3d.interplanety.org/en/blender-add-on-wire/',
    'tracker_url': 'https://b3d.interplanety.org/en/blender-add-on-wire/',
    'description': 'Render with wireframe'
}


def register():
    if not Addon.dev_mode():
        wire_ops.register()
        wire_panel.register()
        wire_preferences.register()
    else:
        print('It seems you are trying to use the dev version of the ' + bl_info['name'] + ' add-on. It may work not properly. Please download and use the release version!')


def unregister():
    if not Addon.dev_mode():
        wire_preferences.unregister()
        wire_panel.unregister()
        wire_ops.unregister()


if __name__ == '__main__':
    register()
