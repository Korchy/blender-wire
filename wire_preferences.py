# Nikita Akimov
# interplanety@interplanety.org

from bpy.types import AddonPreferences
from bpy.props import FloatVectorProperty, BoolProperty
from bpy.utils import register_class, unregister_class


class WIRE_preferences(AddonPreferences):
    bl_idname = __package__

    wire_color: FloatVectorProperty(
        name='wire_color',
        subtype='COLOR',
        size=4,
        min=0.0,
        max=1.0,
        default=(0.0, 0.0, 0.0, 1.0)
    )
    use_optimal_display: BoolProperty(
        name='use_optimal_display',
        default=True
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, 'wire_color', text='Wireframe color')
        layout.prop(self, 'use_optimal_display', text='Optimal display')


def register():
    register_class(WIRE_preferences)


def unregister():
    unregister_class(WIRE_preferences)
