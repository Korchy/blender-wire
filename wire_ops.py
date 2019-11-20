# Nikita Akimov
# interplanety@interplanety.org

from bpy.types import Operator
from bpy.utils import register_class, unregister_class
from .wire import Wire


class WIRE_OT_main(Operator):
    bl_idname = 'wire.main'
    bl_label = 'wire: main'
    bl_description = 'wire - main operator'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # render with wireframe
        Wire.wireframe_render(context=context)
        return {'FINISHED'}


class WIRE_OT_clear(Operator):
    bl_idname = 'wire.clear'
    bl_label = 'wire: clear'
    bl_description = 'wire - clear scene'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # clear after wireframe rendering
        Wire.clear_composite_wireframe(context=context)
        return {'FINISHED'}


def register():
    register_class(WIRE_OT_main)
    register_class(WIRE_OT_clear)


def unregister():
    unregister_class(WIRE_OT_clear)
    unregister_class(WIRE_OT_main)
