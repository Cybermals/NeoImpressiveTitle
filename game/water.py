from panda3d.bullet import (
    BulletBoxShape,
    BulletGhostNode,
    BulletPlaneShape,
    BulletRigidBodyNode
)
from panda3d.core import (
    CullFaceAttrib,
    Geom,
    GeomNode,
    GeomTriangles,
    GeomVertexData,
    GeomVertexFormat,
    GeomVertexWriter,
    Material,
    SamplerState,
    Shader,
    TextureStage,
    TransformState,
    TransparencyAttrib,
    Vec3,
    Vec4
)


# Classes
# =======
class WaterPlane(object):
    water_shader = Shader.load(
        Shader.SL_GLSL,
        "shaders/Water.vert.glsl",
        "shaders/Water.frag.glsl"
    )
    water_mat = None
    plane_mesh = None

    def __init__(self, pos, scale, sound, is_solid):
        # Choose a shape for the physics body based on the size of the water
        terrain_size = base.map_mgr.terrain_size

        if scale[0] >= terrain_size.x and scale[1] >= terrain_size.y:
            water_shape = BulletPlaneShape(Vec3(0, 0, 1), 0)
            self.is_ocean = True

        else:
            water_shape = BulletBoxShape(Vec3(.5, .5, 128))
            self.is_ocean = False

        # Create a ghost node or rigid body for the water
        if not is_solid:
            self.water_body = base.render.attach_new_node(BulletGhostNode("WaterBody"))
            self.water_body.node().add_shape(water_shape)
            self.is_solid = False

        else:
            self.water_body = base.render.attach_new_node(BulletRigidBodyNode("WaterBody"))
            self.water_body.node().add_shape(water_shape)
            self.is_solid = True

        self.water_body.set_pos(Vec3(*pos) + Vec3(0, 0, -128))
        self.water_body.set_scale(*scale)
        base.map_mgr.physics_world.attach(self.water_body.node())

        # Initialize water material if necessary
        if self.water_mat is None:
            WaterPlane.water_mat = Material()
            self.water_mat.set_base_color(Vec4(0, .225, .5, .8))
            self.water_mat.set_metallic(0)
            self.water_mat.set_emission(Vec4(0, 0, 0, 1))
            self.water_mat.set_roughness(.2)
            self.water_mat.set_refractive_index(1)

        # Initialize plane mesh if necessary
        if self.plane_mesh is None:
            # Get V3N3T2 format
            vtx_format = GeomVertexFormat.get_v3()

            # Allocate vertex data
            vertices = GeomVertexData("WaterPlane", vtx_format, Geom.UH_static)
            vertices.reserve_num_rows(4)

            # Write vertex data
            vertex = GeomVertexWriter(vertices, "vertex")
            vertex.add_data3(-.5, .5, 0)
            vertex.add_data3(.5, .5, 0)
            vertex.add_data3(-.5, -.5, 0)
            vertex.add_data3(.5, -.5, 0)

            # Allocate primitive data
            triangles = GeomTriangles(Geom.UH_static)
            triangles.reserve_num_vertices(6)

            # Write primitive data
            triangles.add_vertices(0, 2, 1)
            triangles.add_vertices(1, 2, 3)

            # Create plane mesh
            WaterPlane.plane_mesh = Geom(vertices)
            self.plane_mesh.add_primitive(triangles)

        # Load textures
        self.dudv_map_tex = base.loader.load_texture("images/terrain/WaterDUDV.png")
        self.dudv_map_tex.minfilter = SamplerState.FT_linear_mipmap_linear
        self.dudv_map_tex.magfilter = SamplerState.FT_linear_mipmap_linear

        self.normal_map_tex = base.loader.load_texture("images/terrain/WaterNormal.png")
        self.normal_map_tex.minfilter = SamplerState.FT_linear_mipmap_linear
        self.normal_map_tex.magfilter = SamplerState.FT_linear_mipmap_linear

        # Create water plane
        self.plane = base.render.attach_new_node(GeomNode("WaterPlane"))
        self.plane.node().add_geom(self.plane_mesh)
        self.plane.set_pos(*pos)
        self.plane.set_scale(*scale)

        self.plane.set_shader(self.water_shader)
        self.plane.set_shader_input("waveSpeed", .01 * (not self.is_solid))

        stage1 = TextureStage("NormalMap")

        self.plane.set_texture(self.dudv_map_tex)
        self.plane.set_texture(stage1, self.normal_map_tex)

        self.plane.set_material(self.water_mat)
        self.plane.set_attrib(TransparencyAttrib.make(TransparencyAttrib.M_alpha))
        self.plane.set_attrib(CullFaceAttrib.make(CullFaceAttrib.M_cull_none))

        # TODO: Create water sound effect here.

    def __del__(self):
        # Remove water
        base.map_mgr.physics_world.remove(self.water_body.node())
        self.water_body.remove_node()
        self.plane.remove_node()
