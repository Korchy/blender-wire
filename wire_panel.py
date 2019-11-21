# Nikita Akimov
# interplanety@interplanety.org

from bpy.types import Panel
from bpy.utils import register_class, unregister_class


class WIRE_PT_panel(Panel):
    bl_idname = 'WIRE_PT_panel'
    bl_label = 'wire'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'wire'

    def draw(self, context):
        layout = self.layout
        layout.operator('wire.main', icon='RESTRICT_RENDER_OFF', text='Add wireframe to render')
        layout.prop(context.preferences.addons[__package__].preferences, 'wire_color', text='Wireframe color')
        layout.prop(context.preferences.addons[__package__].preferences, 'use_optimal_display', text='Optimal display')
        split = layout.split(factor=0.5)
        col1 = split.column()
        col2 = split.column()
        col2.operator('wire.clear', icon='CANCEL', text='Clear')


def register():
    register_class(WIRE_PT_panel)


def unregister():
    unregister_class(WIRE_PT_panel)
