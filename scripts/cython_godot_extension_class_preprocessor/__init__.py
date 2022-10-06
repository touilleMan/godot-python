"""
Have we gone too far ? Nah, of course patching Cython to add a preprocessor is totally normal ^^

The issue here is we want a clean an simple way to declare Godot extension classes in Cython,
however Godot GDExtension is modeled after Godot internal & Godot-CPP which both rely heavy
on C++ templating and polymorphism.

Long story short, we need compile-time introspection to generate types informations on
the extension class's methods, those informations being then provided to Godot at runtime
when the extension class is registered.

Cython has no support for compile-time introspection & metaprogramming (no hard feeling
on that: what we are doing here is too much of a niche anyway), so this leave us with two
options:

- Generating the Cython code with a template: this is the normal way (and that is what we use
  for generating bindings from `extension_api.json`), however would require to declare the
  class extension's methods in a json format (used as input by the template to generate a .pyx
  file) and also have the methods' bodies in another Cython file (or inlined in the json O_o)

- Patch the Cython compiler to add custom step in the compilation pipeline that would take
  care of generating the boilerplates we need from the AST \o/

The drawback is Cython doesn't provide a public API to plug into it compilation pipeline so
we have no guarantee this will not break in the future (but this part Cython is very central
so it's highly inlikely to change).
"""

from typing import Optional
from dataclasses import dataclass
from Cython.Compiler.ParseTreeTransforms import NormalizeTree
from Cython.Compiler.Visitor import CythonTransform
import Cython.Compiler.Pipeline
from Cython.Compiler.Pipeline import dumptree
from Cython.Compiler.Errors import error
from Cython.Compiler.PyrexTypes import CIntType
from Cython.Compiler import Nodes, ExprNodes
from Cython.Compiler.ExprNodes import NameNode
from Cython.Compiler.StringEncoding import EncodedString, BytesLiteral


_pipeline_patched = False


def patch_cython_pipeline():

    global _pipeline_patched
    assert not _pipeline_patched  # Sanity check to avoid double patching

    vanilla_create_pipeline = Cython.Compiler.Pipeline.create_pipeline

    def godot_python_patched_create_pipeline(context, mode, exclude_classes=()):

        stages = vanilla_create_pipeline(context, mode, exclude_classes)
        index = next(i + 1 for i, x in enumerate(stages) if isinstance(x, NormalizeTree))
        stages.insert(index, GodotExtensionClassAttributes(context))
        return stages

    Cython.Compiler.Pipeline.create_pipeline = godot_python_patched_create_pipeline

    _pipeline_patched = True


ALLOWED_TYPES = {
    # Godot enums
    "Error",
    # Godot classes
    "Script",
    # Godot native structs
    "ScriptLanguageExtensionProfilingInfo*",
    # Builtins types with meta info
    "uint8_t",
    "uint16_t",
    "uint32_t",
    "uint64_t",
    "int8_t",
    "int16_t",
    "int32_t",
    "int64_t",
    "float",
    "double",
    # Special builtins: Variant and Godot class instance
    "gd_variant_t",
    "gd_object_t",
    # Builtins types
    "gd_bool_t",
    "gd_int_t",
    "gd_float_t",
    "gd_string_t",
    "gd_vector2_t",
    "gd_vector2i_t",
    "gd_rect2_t",
    "gd_rect2i_t",
    "gd_vector3_t",
    "gd_vector3i_t",
    "gd_transform2d_t",
    "gd_vector4_t",
    "gd_vector4i_t",
    "gd_plane_t",
    "gd_quaternion_t",
    "gd_aabb_t",
    "gd_basis_t",
    "gd_transform3d_t",
    "gd_projection_t",
    "gd_color_t",
    "gd_string_name_t",
    "gd_node_path_t",
    "gd_rid_t",
    "gd_object_t",
    "gd_callable_t",
    "gd_signal_t",
    "gd_dictionary_t",
    "gd_array_t",
    "gd_packed_byte_array_t",
    "gd_packed_int32_array_t",
    "gd_packed_int64_array_t",
    "gd_packed_float32_array_t",
    "gd_packed_float64_array_t",
    "gd_packed_string_array_t",
    "gd_packed_vector2_array_t",
    "gd_packed_vector3_array_t",
    "gd_packed_color_array_t",
}


TYPES_TO_META = {
    None: "GDNATIVE_EXTENSION_METHOD_ARGUMENT_METADATA_NONE",
    "uint8_t": "GDNATIVE_EXTENSION_METHOD_ARGUMENT_METADATA_INT_IS_UINT8",
    "uint16_t": "GDNATIVE_EXTENSION_METHOD_ARGUMENT_METADATA_INT_IS_UINT16",
    "uint32_t": "GDNATIVE_EXTENSION_METHOD_ARGUMENT_METADATA_INT_IS_UINT32",
    "uint64_t": "GDNATIVE_EXTENSION_METHOD_ARGUMENT_METADATA_INT_IS_UINT64",
    "int8_t": "GDNATIVE_EXTENSION_METHOD_ARGUMENT_METADATA_INT_IS_INT8",
    "int16_t": "GDNATIVE_EXTENSION_METHOD_ARGUMENT_METADATA_INT_IS_INT16",
    "int32_t": "GDNATIVE_EXTENSION_METHOD_ARGUMENT_METADATA_INT_IS_INT32",
    "int64_t": "GDNATIVE_EXTENSION_METHOD_ARGUMENT_METADATA_INT_IS_INT64",
    "float": "GDNATIVE_EXTENSION_METHOD_ARGUMENT_METADATA_REAL_IS_FLOAT",
    "double": "GDNATIVE_EXTENSION_METHOD_ARGUMENT_METADATA_REAL_IS_DOUBLE",
}


class GodotExtensionClassAttributes(CythonTransform):
    def __init__(self, context):
        super().__init__(context)
        self.is_in_godot_extension_class = False
        self.godot_extension_class_methods_nodes = []
        self.godot_extension_class_name = None

    # TODO: visit module level to check godot.hazmat.* is imported ?

    def visit_CClassDefNode(self, node):
        if not node.decorators:
            return node

        decorator_found = False
        filtered_decorators_node = []
        for decorator_node in node.decorators:
            decorator = decorator_node.decorator
            if isinstance(decorator, NameNode) and decorator.name == "godot_extension_class":
                error(
                    decorator.pos,
                    "`@godot_extension_class` decorator must be called with a `parent` parameter !",
                )
                return node

            if (
                isinstance(decorator, ExprNodes.GeneralCallNode)
                and decorator.function.name == "godot_extension_class"
            ):
                if decorator_found:
                    error(decorator.pos, "cannot have multiple `@godot_extension_class` decorators")
                    return node

                decorator_found = True
                if decorator.positional_args.args:
                    error(
                        decorator.positional_args.pos,
                        "`@godot_extension_class` cannot have positional arguments",
                    )
                    return node

                for arg in decorator.keyword_args.key_value_pairs:
                    if arg.key.value != "parent":
                        error(arg.key.pos, f"unknown param `{arg.key.value}`")
                        return node
                    if not isinstance(arg.value, ExprNodes.UnicodeNode):
                        error(arg.value.pos, f"param `parent` must be a unicode literal")
                        return node
                    parent_class_name = arg.value.value

            else:
                filtered_decorators_node.append(decorator_node)

        if not decorator_found:
            return node

        # The class was decorated !
        node.decorators = filtered_decorators_node or None
        self.is_in_godot_extension_class = True

        self.visitchildren(node)

        methods_spec: list[MethodSpec] = []
        for method_node in self.godot_extension_class_methods_nodes:
            method_spec = _extract_method_spec(method_node)
            if method_spec:
                methods_spec.append(method_spec)

        node.body.stats += [
            _generate_func_method_wrapper(node, method_spec) for method_spec in methods_spec
        ]
        node.body.stats += [
            _generate_func_register_extension_class(node, methods_spec, parent_class_name),
            _generate_func_unregister_extension_class(node),
            _generate_func_new(node),
            _generate_func_free(node),
        ]

        self.is_in_godot_extension_class = False

        return node

    def visit_CFuncDefNode(self, node):
        if not node.decorators:
            return node

        filtered_decorators = [
            d
            for d in node.decorators
            if not isinstance(d.decorator, NameNode)
            or d.decorator.name != "godot_extension_class_method"
        ]
        godot_extension_method_decorated_count = len(node.decorators) - len(filtered_decorators)
        node.decorators = filtered_decorators or None
        if godot_extension_method_decorated_count == 0:
            return node
        elif godot_extension_method_decorated_count > 1:
            error(node.pos, "cannot have multiple `@godot_extension_method` decorators")
            return node

        # The method was decorated !
        node.decorators = filtered_decorators or None
        if not self.is_in_godot_extension_class:
            error(
                node.pos,
                "Method decorated with `@godot_extension_class_method` must be within a cdef class decorated with `@godot_extension_class`",
            )
            return node

        self.godot_extension_class_methods_nodes.append(node)

        return node


@dataclass
class MethodSpec:
    name: str
    is_staticmethod: bool
    return_type: Optional[str]
    arguments_type: list[str]
    arguments: dict[str, str]
    method_node: Nodes.Node


def _extract_method_spec(method_node) -> MethodSpec:
    if isinstance(method_node.declarator, Nodes.CPtrDeclaratorNode):
        return_type = f"{method_node.base_type.name}*"
        method_name = method_node.declarator.base.base.name
    else:
        return_type = str(method_node.base_type.name)
        method_name = method_node.declarator.base.name

    is_staticmethod = any(
        isinstance(d, Nodes.DecoratorNode) and d.decorator.name == "staticmethod"
        for d in method_node.decorators or ()
    )

    # Check return value type
    if return_type != "void" and return_type not in ALLOWED_TYPES:
        error(
            method_node.base_type.pos,
            f"bad type `{return_type}`, only allowed types are: {', '.join(ALLOWED_TYPES)}",
        )

    # Check method's arguments types
    if is_staticmethod:
        args_nodes_minus_self = method_node.declarator.args
    else:
        first_arg_node = method_node.declarator.args[0]
        if not (
            isinstance(first_arg_node.base_type, Nodes.CSimpleBaseTypeNode)
            and first_arg_node.base_type.name == "self"
            and isinstance(first_arg_node.declarator, Nodes.CNameDeclaratorNode)
            and first_arg_node.declarator.name == ""
        ):
            error(first_arg_node.pos, "expected first argument to be `self` without type specified")
            return
        args_nodes_minus_self = method_node.declarator.args[1:]
    args_types_minus_self = []
    arguments_minus_self = {}
    for arg_node in args_nodes_minus_self:
        if (
            isinstance(arg_node.declarator, Nodes.CNameDeclaratorNode)
            and arg_node.declarator.name == ""
        ):
            error(arg_node.pos, f"type required")
            return
        if isinstance(arg_node.declarator, Nodes.CPtrDeclaratorNode):
            arg_type_name = f"{arg_node.base_type.name}*"
        else:
            arg_type_name = str(arg_node.base_type.name)
        if arg_type_name not in ALLOWED_TYPES:
            error(
                arg_node.pos,
                f"bad type `{arg_type_name}`, only allowed types are: {', '.join(ALLOWED_TYPES)}",
            )
            return
        arguments_minus_self[str(arg_node.base.name)] = arg_type_name
        args_types_minus_self.append(arg_type_name)

    return MethodSpec(
        name=method_name,
        is_staticmethod=is_staticmethod,
        return_type=return_type,
        arguments_type=args_types_minus_self,
        arguments=arguments_minus_self,
        method_node=method_node,
    )


def _generate_int_literal(class_node, value: int):
    return ExprNodes.IntNode(
        pos=class_node.pos,
        is_c_literal=None,
        value=str(value),
        unsigned="",
        longness="",
        constant_result=0,
        type=CIntType(3),  # Long
    )


def _generate_func_method_wrapper(class_node, method_spec: MethodSpec):
    pos = class_node.pos

    # >>> (<ARG_TYPE_T>p_args[0])[0], <ARG_TYPE_T>p_args[1])[0], ...
    args_node = [
        # >>> <ARG_TYPE_T>p_args[ARG_INDEX])[0]
        ExprNodes.IndexNode(
            pos=pos,
            base=ExprNodes.TypecastNode(
                pos=pos,
                base_type=Nodes.CSimpleBaseTypeNode(
                    pos=pos,
                    name=EncodedString(arg_type_name),
                    module_path=[],
                    is_basic_c_type=0,
                    signed=1,
                    complex=0,
                    longness=0,
                    is_self_arg=0,
                    templates=None,
                ),
                declarator=Nodes.CPtrDeclaratorNode(
                    pos=pos,
                    base=Nodes.CNameDeclaratorNode(
                        pos=pos,
                        name="",
                        cname=None,
                        default=None,
                        calling_convention="",
                    ),
                    calling_convention="",
                ),
                operand=ExprNodes.IndexNode(
                    pos=pos,
                    base=ExprNodes.NameNode(
                        pos=pos,
                        name=EncodedString("p_args"),
                    ),
                    index=_generate_int_literal(class_node, arg_index),
                ),
                typecheck=0,
            ),
            index=_generate_int_literal(class_node, 0),
        )
        for arg_index, arg_type_name in enumerate(method_spec.arguments_type)
    ]

    if method_spec.is_staticmethod:
        # >>> XXX.YYY(ARGS)
        call_node = ExprNodes.SimpleCallNode(
            pos=pos,
            function=ExprNodes.AttributeNode(
                pos=pos,
                obj=ExprNodes.NameNode(
                    pos=pos,
                    name=class_node.class_name,
                ),
                attribute=EncodedString(method_spec.name),
            ),
            args=args_node,
        )
    else:
        # >>> (<XXX>p_instance).YYY(ARGS)
        call_node = ExprNodes.SimpleCallNode(
            pos=pos,
            function=ExprNodes.AttributeNode(
                pos=pos,
                obj=ExprNodes.TypecastNode(
                    pos=pos,
                    base_type=Nodes.CSimpleBaseTypeNode(
                        pos=pos,
                        name=class_node.class_name,
                        module_path=[],
                        is_basic_c_type=0,
                        signed=1,
                        complex=0,
                        longness=0,
                        is_self_arg=0,
                        templates=None,
                    ),
                    declarator=Nodes.CNameDeclaratorNode(
                        pos=pos,
                        name="",
                        cname=None,
                        default=None,
                        calling_convention="",
                    ),
                    operand=ExprNodes.NameNode(
                        pos=pos,
                        name=EncodedString("p_instance"),
                    ),
                    typecheck=0,
                ),
                attribute=EncodedString(method_spec.name),
            ),
            args=args_node,
        )

    if method_spec.return_type == "void":
        # >>> (<XXX>p_instance).YYY((<ARG_TYPE_T>p_args[0])[0], ...)
        body_stats = [Nodes.ExprStatNode(pos=pos, expr=call_node)]
    else:
        # >>> (<RET_TYPE_T*>r_ret)[0] = ...
        body_stats = [
            Nodes.SingleAssignmentNode(
                pos=pos,
                lhs=ExprNodes.IndexNode(
                    pos=pos,
                    base=ExprNodes.TypecastNode(
                        pos=pos,
                        base_type=Nodes.CSimpleBaseTypeNode(
                            pos=pos,
                            name=EncodedString(method_spec.return_type),
                            module_path=[],
                            is_basic_c_type=0,
                            signed=1,
                            complex=0,
                            longness=0,
                            is_self_arg=0,
                            templates=None,
                        ),
                        declarator=Nodes.CPtrDeclaratorNode(
                            pos=pos,
                            base=Nodes.CNameDeclaratorNode(
                                pos=pos,
                                name="",
                                cname=None,
                                default=None,
                                calling_convention="",
                            ),
                            calling_convention="",
                        ),
                        operand=ExprNodes.NameNode(
                            pos=pos,
                            name=EncodedString("r_ret"),
                        ),
                        typecheck=0,
                    ),
                    index=_generate_int_literal(class_node, 0),
                ),
                rhs=call_node,
            )
        ]

    # Generates:
    #
    # @staticmethod
    # cdef void __godot_extension_class_meth_YYY(
    #     void *method_userdata,
    #     GDExtensionClassInstancePtr p_instance,
    #     const GDNativeTypePtr *p_args,
    #     GDNativeTypePtr r_ret,
    # ) with gil:
    #     (<RET_TYPE_T*>r_ret)[0] = (<XXX>p_instance).YYY((<ARG_TYPE_T>p_args[0])[0], ...)
    return Nodes.CFuncDefNode(
        pos=pos,
        visibility="private",
        base_type=Nodes.CSimpleBaseTypeNode(
            pos=pos,
            name="void",
            module_path=[],
            is_basic_c_type=1,
            signed=1,
            complex=0,
            longness=0,
            is_self_arg=0,
            templates=None,
        ),
        declarator=Nodes.CFuncDeclaratorNode(
            pos=pos,
            base=Nodes.CNameDeclaratorNode(
                pos=pos,
                name=EncodedString(f"__godot_extension_class_meth_{method_spec.name}"),
                cname=None,
                default=None,
                calling_convention="",
            ),
            args=[
                Nodes.CArgDeclNode(
                    pos=pos,
                    base_type=Nodes.CSimpleBaseTypeNode(
                        pos=pos,
                        name=EncodedString("void"),
                        module_path=[],
                        is_basic_c_type=1,
                        signed=1,
                        complex=0,
                        longness=0,
                        is_self_arg=True,
                        templates=None,
                    ),
                    declarator=Nodes.CPtrDeclaratorNode(
                        pos=pos,
                        base=Nodes.CNameDeclaratorNode(
                            pos=pos,
                            name=EncodedString("method_userdata"),
                            cname=None,
                            default=None,
                            calling_convention="",
                        ),
                        calling_convention="",
                    ),
                    not_none=0,
                    or_none=0,
                    default=None,
                    annotation=None,
                    kw_only=0,
                ),
                Nodes.CArgDeclNode(
                    pos=pos,
                    base_type=Nodes.CSimpleBaseTypeNode(
                        pos=pos,
                        name=EncodedString("GDExtensionClassInstancePtr"),
                        module_path=[],
                        is_basic_c_type=0,
                        signed=1,
                        complex=0,
                        longness=0,
                        is_self_arg=0,
                        templates=None,
                    ),
                    declarator=Nodes.CNameDeclaratorNode(
                        pos=pos,
                        name=EncodedString("p_instance"),
                        cname=None,
                        default=None,
                        calling_convention="",
                    ),
                    not_none=0,
                    or_none=0,
                    default=None,
                    annotation=None,
                    kw_only=0,
                ),
                Nodes.CArgDeclNode(
                    pos=pos,
                    base_type=Nodes.CConstTypeNode(
                        pos=pos,
                        base_type=Nodes.CSimpleBaseTypeNode(
                            pos=pos,
                            name=EncodedString("GDNativeTypePtr"),
                            module_path=[],
                            is_basic_c_type=0,
                            signed=1,
                            complex=0,
                            longness=0,
                            is_self_arg=0,
                            templates=None,
                        ),
                    ),
                    declarator=Nodes.CPtrDeclaratorNode(
                        pos=pos,
                        base=Nodes.CNameDeclaratorNode(
                            pos=pos,
                            name=EncodedString("p_args"),
                            cname=None,
                            default=None,
                            calling_convention="",
                        ),
                        calling_convention="",
                    ),
                    not_none=0,
                    or_none=0,
                    default=None,
                    annotation=None,
                    kw_only=0,
                ),
                Nodes.CArgDeclNode(
                    pos=pos,
                    base_type=Nodes.CSimpleBaseTypeNode(
                        pos=pos,
                        name=EncodedString("GDNativeTypePtr"),
                        module_path=[],
                        is_basic_c_type=0,
                        signed=1,
                        complex=0,
                        longness=0,
                        is_self_arg=0,
                        templates=None,
                    ),
                    declarator=Nodes.CNameDeclaratorNode(
                        pos=pos,
                        name=EncodedString("r_ret"),
                        cname=None,
                        default=None,
                        calling_convention="",
                    ),
                    not_none=0,
                    or_none=0,
                    default=None,
                    annotation=None,
                    kw_only=0,
                ),
            ],
            has_varargs=0,
            exception_value=None,
            exception_check=0,
            nogil=1,
            with_gil=1,
            overridable=0,
        ),
        body=Nodes.StatListNode(
            pos=pos,
            stats=body_stats,
        ),
        doc=None,
        modifiers=[],
        api=0,
        overridable=0,
        is_const_method=0,
        decorators=[
            Nodes.DecoratorNode(
                pos=pos,
                decorator=ExprNodes.NameNode(
                    pos=pos,
                    name="staticmethod",
                ),
            ),
        ],
    )


def _generate_func_register_extension_class(
    class_node, methods_spec: list[MethodSpec], parent_class_name: str
):
    pos = class_node.pos

    def _generate_method_spec_param_node(method_spec: MethodSpec):
        # >>> True, b"return_type_t", [(b"arg_type_t", b"arg_name"), ...]
        return (
            ExprNodes.BoolNode(
                pos=pos,
                value=method_spec.is_staticmethod,
            ),
            ExprNodes.BytesNode(
                pos=pos,
                value=BytesLiteral(method_spec.return_type.encode("utf8")),
            ),
            ExprNodes.ListNode(
                pos=pos,
                args=[
                    Nodes.TupleNode(
                        pos=pos,
                        args=[
                            ExprNodes.BytesNode(
                                pos=pos,
                                value=BytesLiteral(arg_type.encode("utf8")),
                            ),
                            ExprNodes.BytesNode(
                                pos=pos,
                                value=BytesLiteral(arg_name.encode("utf8")),
                            ),
                        ],
                    )
                    for arg_name, arg_type in method_spec.arguments.items()
                ],
            ),
        )

    # Generates:
    #
    #   @staticmethod
    #   def __godot_extension_register_class():
    #       register_extension_class_creation(
    #           b"XXX",
    #           b"XXX_PARENT",
    #           &XXX.__godot_extension_new,
    #           &XXX.__godot_extension_free,
    #       )
    #       register_extension_class_method(
    #           b"XXX",
    #           b"YYY",
    #           &XXX.__godot_extension_class_meth_YYY,
    #           True,
    #           b"return_type_t",
    #           [(b"arg_type_t", b"arg_name"), ...],
    #       )
    return Nodes.DefNode(
        pos=pos,
        name=EncodedString("__godot_extension_register_class"),
        args=[],
        star_arg=None,
        starstar_arg=None,
        doc=None,
        body=Nodes.StatListNode(
            pos=pos,
            stats=[
                # >>> register_extension_class_creation(
                Nodes.ExprStatNode(
                    pos=pos,
                    expr=ExprNodes.SimpleCallNode(
                        pos=pos,
                        function=ExprNodes.NameNode(
                            pos=pos,
                            name=EncodedString("register_extension_class_creation"),
                        ),
                        args=[
                            ExprNodes.BytesNode(
                                pos=pos,
                                value=BytesLiteral(class_node.class_name.encode("utf8")),
                            ),
                            ExprNodes.BytesNode(
                                pos=pos,
                                value=BytesLiteral(parent_class_name.encode("utf8")),
                            ),
                            ExprNodes.AmpersandNode(
                                pos=pos,
                                operand=ExprNodes.AttributeNode(
                                    pos=pos,
                                    obj=ExprNodes.NameNode(
                                        pos=pos,
                                        name=class_node.class_name,
                                    ),
                                    attribute=EncodedString("__godot_extension_new"),
                                ),
                            ),
                            ExprNodes.AmpersandNode(
                                pos=pos,
                                operand=ExprNodes.AttributeNode(
                                    pos=pos,
                                    obj=ExprNodes.NameNode(
                                        pos=pos,
                                        name=class_node.class_name,
                                    ),
                                    attribute=EncodedString("__godot_extension_free"),
                                ),
                            ),
                        ],
                    ),
                ),
                # >>> register_extension_class_method(
                *[
                    Nodes.ExprStatNode(
                        pos=pos,
                        expr=ExprNodes.SimpleCallNode(
                            pos=pos,
                            function=ExprNodes.NameNode(
                                pos=pos,
                                name=EncodedString("register_extension_class_method"),
                            ),
                            args=[
                                ExprNodes.BytesNode(
                                    pos=pos,
                                    value=BytesLiteral(class_node.class_name.encode("utf8")),
                                ),
                                ExprNodes.BytesNode(
                                    pos=pos,
                                    value=BytesLiteral(method_spec.name.encode("utf8")),
                                ),
                                ExprNodes.AmpersandNode(
                                    pos=pos,
                                    operand=ExprNodes.AttributeNode(
                                        pos=pos,
                                        obj=ExprNodes.NameNode(
                                            pos=pos,
                                            name=class_node.class_name,
                                        ),
                                        attribute=EncodedString(
                                            f"__godot_extension_class_meth_{method_spec.name}"
                                        ),
                                    ),
                                ),
                                *_generate_method_spec_param_node(method_spec),
                            ],
                        ),
                    )
                    for method_spec in methods_spec
                ],
            ],
        ),
        decorators=[
            Nodes.DecoratorNode(
                pos=pos,
                decorator=ExprNodes.NameNode(
                    pos=pos,
                    name=EncodedString("staticmethod"),
                ),
            ),
        ],
        is_async_def=False,
        return_type_annotation=None,
        num_kwonly_args=0,
        num_required_kw_args=0,
        num_required_args=0,
    )


def _generate_func_unregister_extension_class(class_node):
    pos = class_node.pos

    # Generates:
    #
    #   @staticmethod
    #   def __godot_extension_unregister_class():
    #       unregister_extension_class(b"XXX")
    return Nodes.DefNode(
        pos=pos,
        name=EncodedString("__godot_extension_unregister_class"),
        args=[],
        star_arg=None,
        starstar_arg=None,
        is_async_def=False,
        return_type_annotation=None,
        decorators=[
            Nodes.DecoratorNode(pos=pos, decorator=ExprNodes.NameNode(pos=pos, name="staticmethod"))
        ],
        doc=None,
        body=Nodes.StatListNode(
            pos=pos,
            stats=[
                Nodes.ExprStatNode(
                    pos=pos,
                    expr=ExprNodes.SimpleCallNode(
                        pos=pos,
                        function=ExprNodes.NameNode(
                            pos=pos, name=EncodedString("unregister_extension_class")
                        ),
                        args=[
                            ExprNodes.BytesNode(
                                pos=pos,
                                value=BytesLiteral(class_node.class_name.encode("utf8")),
                            ),
                        ],
                    ),
                )
            ],
        ),
    )


def _generate_func_new(class_node):
    pos = class_node.pos

    # Generates:
    #
    #   @staticmethod
    #   cdef GDExtensionClassInstancePtr __godot_extension_new(void* p_userdata) with gil:
    #       cdef XXX obj = XXX()
    #       Py_INCREF(obj)
    #       return <PyObject*>obj
    return Nodes.CFuncDefNode(
        pos=pos,
        visibility="private",
        base_type=Nodes.CSimpleBaseTypeNode(
            pos=pos,
            name=EncodedString("GDExtensionClassInstancePtr"),
            module_path=[],
            is_basic_c_type=0,
            signed=1,
            complex=0,
            longness=0,
            is_self_arg=0,
            templates=None,
        ),
        declarator=Nodes.CFuncDeclaratorNode(
            pos=pos,
            base=Nodes.CNameDeclaratorNode(
                pos=pos,
                name=EncodedString("__godot_extension_new"),
                cname=None,
                default=None,
                calling_convention="",
            ),
            args=[
                # >>> void *p_userdata
                Nodes.CArgDeclNode(
                    pos=pos,
                    base_type=Nodes.CSimpleBaseTypeNode(
                        pos=pos,
                        name=EncodedString("void"),
                        module_path=[],
                        is_basic_c_type=1,
                        signed=1,
                        complex=0,
                        longness=0,
                        is_self_arg=True,
                        templates=None,
                    ),
                    declarator=Nodes.CPtrDeclaratorNode(
                        pos=pos,
                        base=Nodes.CNameDeclaratorNode(
                            pos=pos,
                            name=EncodedString("p_userdata"),
                            cname=None,
                            default=None,
                            calling_convention="",
                        ),
                        calling_convention="",
                    ),
                    not_none=0,
                    or_none=0,
                    default=None,
                    annotation=None,
                    kw_only=0,
                ),
            ],
            has_varargs=0,
            exception_value=None,
            exception_check=0,
            nogil=1,
            with_gil=1,
            overridable=0,
        ),
        body=Nodes.StatListNode(
            pos=pos,
            stats=[
                # >>> cdef XXX obj = XXX()
                Nodes.CVarDefNode(
                    pos=pos,
                    visibility="private",
                    base_type=Nodes.CSimpleBaseTypeNode(
                        pos=pos,
                        name=class_node.class_name,
                        module_path=[],
                        is_basic_c_type=0,
                        signed=1,
                        complex=0,
                        longness=0,
                        is_self_arg=0,
                        templates=None,
                    ),
                    declarators=[
                        Nodes.CNameDeclaratorNode(
                            pos=pos,
                            name=EncodedString("obj"),
                            cname=None,
                            default=ExprNodes.SimpleCallNode(
                                pos=pos,
                                function=ExprNodes.NameNode(pos=pos, name=class_node.class_name),
                                args=[],
                            ),
                            calling_convention="",
                            overridable=0,
                        )
                    ],
                    in_pxd=False,
                    doc=None,
                    api=0,
                    modifiers=[],
                    overridable=0,
                ),
                # >>> Py_INCREF(obj)
                Nodes.ExprStatNode(
                    pos=pos,
                    expr=ExprNodes.SimpleCallNode(
                        pos=pos,
                        function=ExprNodes.NameNode(pos=pos, name=EncodedString("Py_INCREF")),
                        args=[ExprNodes.NameNode(pos=pos, name=EncodedString("obj"))],
                    ),
                ),
                # >>> return <PyObject*>obj
                Nodes.ReturnStatNode(
                    pos=pos,
                    value=ExprNodes.TypecastNode(
                        pos=pos,
                        base_type=Nodes.CSimpleBaseTypeNode(
                            pos=pos,
                            name=EncodedString("PyObject"),
                            module_path=[],
                            is_basic_c_type=0,
                            signed=1,
                            complex=0,
                            longness=0,
                            is_self_arg=0,
                            templates=None,
                        ),
                        declarator=Nodes.CPtrDeclaratorNode(
                            pos=pos,
                            base=Nodes.CNameDeclaratorNode(
                                pos=pos,
                                name=EncodedString(""),
                                cname=None,
                                default=None,
                                calling_convention="",
                            ),
                            calling_convention="",
                        ),
                        operand=ExprNodes.NameNode(pos=pos, name=EncodedString("obj")),
                        typecheck=0,
                    ),
                ),
            ],
        ),
        doc=None,
        modifiers=[],
        api=0,
        overridable=0,
        is_const_method=0,
        decorators=[
            Nodes.DecoratorNode(
                pos=pos,
                decorator=ExprNodes.NameNode(pos=pos, name=EncodedString("staticmethod")),
            )
        ],
    )


def _generate_func_free(class_node):
    pos = class_node.pos

    # Generates:
    #
    #   @staticmethod
    #   cdef void __godot_extension_free(void* p_userdata, GDExtensionClassInstancePtr p_instance) with gil:
    #       Py_DECREF(<XXX>p_instance)
    return Nodes.CFuncDefNode(
        pos=pos,
        visibility="private",
        base_type=Nodes.CSimpleBaseTypeNode(
            pos=pos,
            name=EncodedString("void"),
            module_path=[],
            is_basic_c_type=1,
            signed=1,
            complex=0,
            longness=0,
            is_self_arg=0,
            templates=None,
        ),
        declarator=Nodes.CFuncDeclaratorNode(
            pos=pos,
            base=Nodes.CNameDeclaratorNode(
                pos=pos,
                name=EncodedString("__godot_extension_free"),
                cname=None,
                default=None,
                calling_convention="",
            ),
            args=[
                # >>> void *p_userdata
                Nodes.CArgDeclNode(
                    pos=pos,
                    base_type=Nodes.CSimpleBaseTypeNode(
                        pos=pos,
                        name=EncodedString("void"),
                        module_path=[],
                        is_basic_c_type=1,
                        signed=1,
                        complex=0,
                        longness=0,
                        is_self_arg=True,
                        templates=None,
                    ),
                    declarator=Nodes.CPtrDeclaratorNode(
                        pos=pos,
                        base=Nodes.CNameDeclaratorNode(
                            pos=pos,
                            name=EncodedString("p_userdata"),
                            cname=None,
                            default=None,
                            calling_convention="",
                        ),
                        calling_convention="",
                    ),
                    not_none=0,
                    or_none=0,
                    default=None,
                    annotation=None,
                    kw_only=0,
                ),
                # >>> GDExtensionClassInstancePtr p_instance
                Nodes.CArgDeclNode(
                    pos=pos,
                    base_type=Nodes.CSimpleBaseTypeNode(
                        pos=pos,
                        name=EncodedString("GDExtensionClassInstancePtr"),
                        module_path=[],
                        is_basic_c_type=0,
                        signed=1,
                        complex=0,
                        longness=0,
                        is_self_arg=0,
                        templates=None,
                    ),
                    declarator=Nodes.CNameDeclaratorNode(
                        pos=pos,
                        name=EncodedString("p_instance"),
                        cname=None,
                        default=None,
                        calling_convention="",
                    ),
                    not_none=0,
                    or_none=0,
                    default=None,
                    annotation=None,
                    kw_only=0,
                ),
            ],
            has_varargs=0,
            exception_value=None,
            exception_check=0,
            nogil=1,
            with_gil=1,
            overridable=0,
        ),
        body=Nodes.StatListNode(
            pos=pos,
            stats=[
                # >>> Py_DECREF(<PythonScript>p_instance)
                Nodes.ExprStatNode(
                    pos=pos,
                    expr=ExprNodes.SimpleCallNode(
                        pos=pos,
                        function=ExprNodes.NameNode(
                            pos=pos,
                            name=EncodedString("Py_DECREF"),
                        ),
                        args=[
                            ExprNodes.TypecastNode(
                                pos=pos,
                                base_type=Nodes.CSimpleBaseTypeNode(
                                    pos=pos,
                                    name=class_node.class_name,
                                    module_path=[],
                                    is_basic_c_type=0,
                                    signed=1,
                                    complex=0,
                                    longness=0,
                                    is_self_arg=0,
                                    templates=None,
                                ),
                                declarator=Nodes.CNameDeclaratorNode(
                                    pos=pos,
                                    name=EncodedString(""),
                                    cname=None,
                                    default=None,
                                    calling_convention="",
                                ),
                                operand=ExprNodes.NameNode(
                                    pos=pos,
                                    name=EncodedString("p_instance"),
                                ),
                                typecheck=0,
                            ),
                        ],
                    ),
                )
            ],
        ),
        doc=None,
        modifiers=[],
        api=0,
        overridable=0,
        is_const_method=0,
        decorators=[
            Nodes.DecoratorNode(
                pos=pos,
                decorator=ExprNodes.NameNode(pos=pos, name=EncodedString("staticmethod")),
            )
        ],
    )
