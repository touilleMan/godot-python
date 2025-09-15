from .hazmat cimport gdapi
from .hazmat.gdtypes cimport *


cdef class BaseGDObject:
    cdef gd_object_t _gd_ptr

    @staticmethod
    cdef inline object cast_from_variant(const gd_variant_t *gdvar):
        # TODO: cast to remove const due to `GDExtensionTypeFromVariantConstructorFunc`
        cdef gd_object_t obj = gdapi.gd_object_from_variant(<gd_variant_t *>gdvar)
        if obj == NULL:
            return None
        cdef object class_name = _object_call(obj, "get_class", [])
        # TODO: Kind of wasteful to have to convert Godot string here...
        cdef object klass = _load_class(str(class_name))
        return klass._from_ptr(<size_t>obj)

    @staticmethod
    cdef inline object cast_from_object(gd_object_t obj):
        if obj == NULL:
            return None
        cdef object class_name = _object_call(obj, "get_class", [])
        # TODO: Kind of wasteful to have to convert Godot string here...
        cdef object klass = _load_class(str(class_name))
        return klass._from_ptr(<size_t>obj)


cdef object _load_class(str name)
cpdef BaseGDObject _load_singleton(str name)
cdef void _cleanup_loaded_classes_and_singletons()
cdef object _object_call(gd_object_t obj, str meth, list args)
