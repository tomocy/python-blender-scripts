import bpy
import math

bl_info = {
    "name": "Rename materials to hex colors",
    "blender": (2, 80, 0),
    "category": "Object",
}


class ObjectRenameMaterialsToHexColors(bpy.types.Operator):
    """Rename the materials of the selected object \
        to the hex colors of those"""

    bl_idname = "object.rename_materials_to_hex_colors"
    bl_label = "Rename materials to hex colors"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        selected = context.selected_objects
        if len(selected) < 1:
            self._log("no object is selected")
            return {"FINISHED"}

        obj = selected[0]
        for material in obj.data.materials:
            rgb = list(
                map(
                    color_factor_to_hex,
                    material.diffuse_color[0:3],
                ),
            )
            r, g, b = (
                rgb[0],
                rgb[1],
                rgb[2],
            )

            material.name = "%02x%02x%02x" % (r, g, b)

        self._log("rename the materials to hex colors")

        return {"FINISHED"}

    def _log(self, message):
        print(f"{self.bl_idname}: {message}")


def color_factor_to_hex(factor):
    if factor < 0.0031308:
        srgb = 0.0 if factor < 0.0 else factor * 12.92
    else:
        srgb = 1.055 * math.pow(factor, 1.0 / 2.4) - 0.055

    return max(min(int(srgb * 255 + 0.5), 255), 0)


def menu_item(self, context):
    self.layout.operator(ObjectRenameMaterialsToHexColors.bl_idname)


def register():
    bpy.utils.register_class(ObjectRenameMaterialsToHexColors)
    bpy.types.VIEW3D_MT_object.append(menu_item)


def unregister():
    bpy.utils.unregister_class(ObjectRenameMaterialsToHexColors)


if __name__ == "__main__":
    register()
