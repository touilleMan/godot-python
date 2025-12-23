from .hazmat cimport gdapi
from .hazmat.gdtypes cimport *
from .builtins cimport StringName


cdef class BaseGDObject:
    cdef gd_object_t _gd_ptr

    @staticmethod
    cdef inline object steal_cast_from_variant(const gd_variant_t *gdvar):
        """
        Return `None` if the variant is not an object (and in this case the caller
        is responsible to delete `gdvar`).
        Don't increase the refcount if the variant is a refcounted object (hence the
        "steal" in the name).
        """
        cdef gd_object_t obj = gdapi.gd_object_steal_from_variant(gdvar)
        if obj == NULL:
            return None
        return BaseGDObject.steal_cast_from_object(obj)

    @staticmethod
    cdef inline object steal_cast_from_object(gd_object_t obj):
        """
        Return `None` if object is NULL.
        Don't increase the refcount if the variant is a refcounted object (hence the
        "steal" in the name).
        """
        if obj == NULL:
            return None
        cdef object class_name = _object_call(obj, StringName("get_class"), [])
        # TODO: Kind of wasteful to have to convert Godot string here...
        cdef object klass = _load_class(str(class_name))
        return klass._steal_from_ptr(<size_t>obj)


cdef object _load_class(str name)
cpdef BaseGDObject _load_singleton(str name)
cdef void _cleanup_loaded_classes_and_singletons()
cdef object _object_call(gd_object_t obj, StringName meth, list args)
