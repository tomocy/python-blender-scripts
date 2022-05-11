import bpy
from mathutils import Matrix, Vector

bl_info = {
    "name": "Set origin to bottom center",
    "blender": (2, 80, 0),
    "category": "Object",
}


class ObjectSetOriginToBottomCenter(bpy.types.Operator):
    """Set the origin of the selected object to bottom center"""

    bl_idname = "object.set_origin_to_bottom_center"
    bl_label = "Set Origin to Bottom center"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        selected = context.selected_objects
        if len(selected) < 1:
            self._log("no object is selected")
            return {"FINISHED"}

        obj = selected[0]
        verts = [obj.matrix_world @ Vector(v[:]) for v in obj.bound_box]

        origin = sum(verts, Vector()) / 8
        origin.z = min(v.z for v in verts)
        origin = obj.matrix_world.inverted() @ origin

        obj.data.transform(Matrix.Translation(-origin))
        obj.matrix_world.translation = obj.matrix_world @ origin
        self._log("set the origin to bottom center")

        return {"FINISHED"}

    def _log(self, message):
        print(f"{self.bl_idname}: {message}")


def menu_item(self, context):
    self.layout.operator(ObjectSetOriginToBottomCenter.bl_idname)


def register():
    bpy.utils.register_class(ObjectSetOriginToBottomCenter)
    bpy.types.VIEW3D_MT_object.append(menu_item)


def unregister():
    bpy.utils.unregister_class(ObjectSetOriginToBottomCenter)


if __name__ == "__main__":
    register()
