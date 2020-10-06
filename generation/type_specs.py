# Describe all base types (i.e. scalar such as int and Godot builtins)

from dataclasses import dataclass


@dataclass
class TypeSpec:
    # Type used within Godot api.json
    gdapi_type: str
    # Type used when calling C api functions
    c_type: str
    # Type used in Cython, basically similar to c_type for scalars&enums
    # and to py_type for Godot objects&builtins
    cy_type: str
    # TODO: typing should be divided between argument and return (e.g. `Union[str, NodePath]` vs `NodePath`)
    # Type used for PEP 484 Python typing
    py_type: str = ""
    # Type is a Godot object (i.e. defined in api.json)
    is_object: bool = False
    # Type is a Godot builtin (e.g. Vector2)
    is_builtin: bool = False
    # Type is a scalar (e.g. int, float) or void
    is_base_type: bool = False
    # Type doesn't use the heap (hence no need for freeing it)
    is_stack_only: bool = False
    # Type is an enum (e.g. godot_error, Camera::KeepAspect)
    is_enum: bool = False

    @property
    def is_void(self) -> bool:
        return self.c_type == "void"

    @property
    def is_variant(self) -> bool:
        return self.c_type == "godot_variant"

    def __post_init__(self):
        self.py_type = self.py_type or self.cy_type
        if self.is_object:
            assert not self.is_builtin
            assert not self.is_base_type
            assert not self.is_stack_only
        if self.is_builtin:
            assert not self.is_base_type


# Base types
TYPE_VOID = TypeSpec(
    gdapi_type="void", c_type="void", cy_type="None", is_base_type=True, is_stack_only=True
)
TYPE_BOOL = TypeSpec(
    gdapi_type="bool",
    c_type="godot_bool",
    cy_type="bint",
    py_type="bool",
    is_base_type=True,
    is_stack_only=True,
)
TYPE_INT = TypeSpec(
    gdapi_type="int", c_type="godot_int", cy_type="int", is_base_type=True, is_stack_only=True
)
TYPE_FLOAT = TypeSpec(
    gdapi_type="float", c_type="godot_real", cy_type="float", is_base_type=True, is_stack_only=True
)
TYPE_ERROR = TypeSpec(
    gdapi_type="enum.Error",
    c_type="godot_error",
    cy_type="godot_error",
    py_type="Error",
    is_base_type=True,
    is_stack_only=True,
    is_enum=True,
)
TYPE_VECTOR3_AXIS = TypeSpec(
    gdapi_type="enum.Vector3::Axis",
    c_type="godot_vector3_axis",
    cy_type="godot_vector3_axis",
    py_type="Vector3.Axis",
    is_base_type=True,
    is_stack_only=True,
    is_enum=True,
)
TYPE_VARIANT_TYPE = TypeSpec(
    gdapi_type="enum.Variant::Type",
    c_type="godot_variant_type",
    cy_type="godot_variant_type",
    py_type="VariantType",
    is_base_type=True,
    is_stack_only=True,
    is_enum=True,
)
TYPE_VARIANT_OPERATOR = TypeSpec(
    gdapi_type="enum.Variant::Operator",
    c_type="godot_variant_operator",
    cy_type="godot_variant_operator",
    py_type="VariantOperator",
    is_base_type=True,
    is_stack_only=True,
    is_enum=True,
)

# Stack&heap types
TYPE_VARIANT = TypeSpec(
    gdapi_type="Variant", c_type="godot_variant", cy_type="object", is_builtin=True
)
TYPE_STRING = TypeSpec(
    gdapi_type="String",
    c_type="godot_string",
    cy_type="GDString",
    py_type="Union[str, GDString]",
    is_builtin=True,
)

# Stack only types
TYPE_AABB = TypeSpec(
    gdapi_type="AABB", c_type="godot_aabb", cy_type="AABB", is_builtin=True, is_stack_only=True
)
TYPE_ARRAY = TypeSpec(
    gdapi_type="Array", c_type="godot_array", cy_type="Array", is_builtin=True, is_stack_only=True
)
TYPE_BASIS = TypeSpec(
    gdapi_type="Basis", c_type="godot_basis", cy_type="Basis", is_builtin=True, is_stack_only=True
)
TYPE_COLOR = TypeSpec(
    gdapi_type="Color", c_type="godot_color", cy_type="Color", is_builtin=True, is_stack_only=True
)
TYPE_DICTIONARY = TypeSpec(
    gdapi_type="Dictionary",
    c_type="godot_dictionary",
    cy_type="Dictionary",
    is_builtin=True,
    is_stack_only=True,
)
TYPE_NODEPATH = TypeSpec(
    gdapi_type="NodePath",
    c_type="godot_node_path",
    cy_type="NodePath",
    py_type="Union[str, NodePath]",
    is_builtin=True,
    is_stack_only=True,
)
TYPE_PLANE = TypeSpec(
    gdapi_type="Plane", c_type="godot_plane", cy_type="Plane", is_builtin=True, is_stack_only=True
)
TYPE_QUAT = TypeSpec(
    gdapi_type="Quat", c_type="godot_quat", cy_type="Quat", is_builtin=True, is_stack_only=True
)
TYPE_RECT2 = TypeSpec(
    gdapi_type="Rect2", c_type="godot_rect2", cy_type="Rect2", is_builtin=True, is_stack_only=True
)
TYPE_RID = TypeSpec(
    gdapi_type="RID", c_type="godot_rid", cy_type="RID", is_builtin=True, is_stack_only=True
)
TYPE_TRANSFORM = TypeSpec(
    gdapi_type="Transform",
    c_type="godot_transform",
    cy_type="Transform",
    is_builtin=True,
    is_stack_only=True,
)
TYPE_TRANSFORM2D = TypeSpec(
    gdapi_type="Transform2D",
    c_type="godot_transform2d",
    cy_type="Transform2D",
    is_builtin=True,
    is_stack_only=True,
)
TYPE_VECTOR2 = TypeSpec(
    gdapi_type="Vector2",
    c_type="godot_vector2",
    cy_type="Vector2",
    is_builtin=True,
    is_stack_only=True,
)
TYPE_VECTOR3 = TypeSpec(
    gdapi_type="Vector3",
    c_type="godot_vector3",
    cy_type="Vector3",
    is_builtin=True,
    is_stack_only=True,
)
TYPE_POOLBYTEARRAY = TypeSpec(
    gdapi_type="PoolByteArray",
    c_type="godot_pool_byte_array",
    cy_type="PoolByteArray",
    is_builtin=True,
    is_stack_only=True,
)
TYPE_POOLINTARRAY = TypeSpec(
    gdapi_type="PoolIntArray",
    c_type="godot_pool_int_array",
    cy_type="PoolIntArray",
    is_builtin=True,
    is_stack_only=True,
)
TYPE_POOLREALARRAY = TypeSpec(
    gdapi_type="PoolRealArray",
    c_type="godot_pool_real_array",
    cy_type="PoolRealArray",
    is_builtin=True,
    is_stack_only=True,
)
TYPE_POOLSTRINGARRAY = TypeSpec(
    gdapi_type="PoolStringArray",
    c_type="godot_pool_string_array",
    cy_type="PoolStringArray",
    is_builtin=True,
    is_stack_only=True,
)
TYPE_POOLVECTOR2ARRAY = TypeSpec(
    gdapi_type="PoolVector2Array",
    c_type="godot_pool_vector2_array",
    cy_type="PoolVector2Array",
    is_builtin=True,
    is_stack_only=True,
)
TYPE_POOLVECTOR3ARRAY = TypeSpec(
    gdapi_type="PoolVector3Array",
    c_type="godot_pool_vector3_array",
    cy_type="PoolVector3Array",
    is_builtin=True,
    is_stack_only=True,
)
TYPE_POOLCOLORARRAY = TypeSpec(
    gdapi_type="PoolColorArray",
    c_type="godot_pool_color_array",
    cy_type="PoolColorArray",
    is_builtin=True,
    is_stack_only=True,
)


ALL_TYPES_EXCEPT_OBJECTS = [
    TYPE_VOID,
    TYPE_BOOL,
    TYPE_INT,
    TYPE_FLOAT,
    TYPE_ERROR,
    TYPE_VECTOR3_AXIS,
    TYPE_VARIANT_TYPE,
    TYPE_VARIANT_OPERATOR,
    TYPE_VARIANT,
    TYPE_STRING,
    TYPE_AABB,
    TYPE_ARRAY,
    TYPE_BASIS,
    TYPE_COLOR,
    TYPE_DICTIONARY,
    TYPE_NODEPATH,
    TYPE_PLANE,
    TYPE_QUAT,
    TYPE_RECT2,
    TYPE_RID,
    TYPE_TRANSFORM,
    TYPE_TRANSFORM2D,
    TYPE_VECTOR2,
    TYPE_VECTOR3,
    TYPE_POOLBYTEARRAY,
    TYPE_POOLINTARRAY,
    TYPE_POOLREALARRAY,
    TYPE_POOLSTRINGARRAY,
    TYPE_POOLVECTOR2ARRAY,
    TYPE_POOLVECTOR3ARRAY,
    TYPE_POOLCOLORARRAY,
]
