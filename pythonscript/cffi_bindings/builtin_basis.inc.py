class Basis:
    GD_TYPE = lib.GODOT_VARIANT_TYPE_BASIS

    @classmethod
    def build_from_gd_ptr(cls, gd_ptr):
        # TODO: optimize this
        v = cls()
        v._gd_ptr = gd_ptr
        return v

    @staticmethod
    def check_param_type(argname, arg, type):
        if not isinstance(arg, type):
            raise TypeError('Param `%s` should be of type `%s`' % (argname, type))

    @staticmethod
    def check_param_float(argname, arg):
        if not isinstance(arg, (int, float)):
            raise TypeError('Param `%s` should be of type `float`' % argname)

    @classmethod
    def build_from_rows(cls, row0, row1, row2):
        cls.check_param_type('row0', row0, Vector3)
        cls.check_param_type('row1', row1, Vector3)
        cls.check_param_type('row2', row2, Vector3)
        ret = cls()
        lib.godot_basis_new_with_rows(ret._gd_ptr, row0._gd_obj, row1._gd_obj, row2._gd_obj)
        return ret

    @classmethod
    def build_from_euler(cls, euler):
        ret = cls()
        if isinstance(euler, Vector3):
            lib.godot_basis_new_with_euler(ret._gd_ptr, euler._gd_obj)
        elif isinstance(euler, Quat):
            lib.godot_basis_new_with_euler_quat(ret._gd_ptr, euler._gd_ptr[0])
        else:
            raise TypeError("Param `euler` should be of type `%s`" % (Vector3, Quat))
        return ret

    @classmethod
    def build_from_axis_and_angle(cls, axis, phi):
        cls.check_param_type('axis', axis, Vector3)
        cls.check_param_float('phi', phi)
        ret = cls()
        lib.godot_basis_new_with_axis_and_angle(ret._gd_ptr, axis._gd_obj, phi)
        return ret

    AXIS_X = 0
    AXIS_Y = 1
    AXIS_Z = 2

    def __init__(self):
        self._gd_ptr = ffi.new('godot_basis*')
        lib.godot_basis_new(self._gd_ptr)

    def __repr__(self):
        gd_repr = lib.godot_basis_to_string(self._gd_ptr)
        raw_str = lib.godot_string_unicode_str(ffi.addressof(gd_repr))
        return "<%s%s>" % (type(self).__name__, ffi.string(raw_str))

    def __eq__(self, other):
        return (isinstance(other, Basis) and other.x == self.x and
                other.y == self.y and other.z == self.z)

    def __neg__(self):
        return type(self)(-self.x, -self.y, -self.z)

    def __pos__(self):
        return self

    # Properties

    @property
    def x(self):
        return Vector3.build_from_gd_obj(lib.godot_basis_get_axis(self._gd_ptr, self.AXIS_X))

    @property
    def y(self):
        return Vector3.build_from_gd_obj(lib.godot_basis_get_axis(self._gd_ptr, self.AXIS_Y))

    @property
    def z(self):
        return Vector3.build_from_gd_obj(lib.godot_basis_get_axis(self._gd_ptr, self.AXIS_Z))

    @x.setter
    def x(self, val):
        self.check_param_type('val', val, Vector3)
        lib.godot_basis_set_axis(self._gd_ptr, self.AXIS_X, val._gd_obj)

    @y.setter
    def y(self, val):
        self.check_param_type('val', val, Vector3)
        lib.godot_basis_set_axis(self._gd_ptr, self.AXIS_Y, val._gd_obj)

    @z.setter
    def z(self, val):
        self.check_param_type('val', val, Vector3)
        lib.godot_basis_set_axis(self._gd_ptr, self.AXIS_Z, val._gd_obj)

    # Methods

    def determinant(self):
        return lib.godot_basis_determinant(self._gd_ptr)

    def get_euler(self):
        gd_obj = lib.godot_basis_get_euler(self._gd_ptr)
        return Vector3.build_from_gd_obj(gd_obj)

    def get_orthogonal_index(self):
        return lib.godot_basis_get_orthogonal_index(self._gd_ptr)

    def get_scale(self):
        gd_obj = lib.godot_basis_get_scale(self._gd_ptr)
        return Vector3.build_from_gd_obj(gd_obj)

    def inverse(self):
        gd_ptr = ffi.new("godot_basis*")
        lib.godot_basis_inverse(gd_ptr, self._gd_ptr)
        return Basis.build_from_gd_ptr(gd_ptr)

    def orthonormalized(self):
        gd_ptr = ffi.new("godot_basis*")
        lib.godot_basis_orthonormalized(gd_ptr, self._gd_ptr)
        return Basis.build_from_gd_ptr(gd_ptr)

    def rotated(self, axis, phi):
        self.check_param_type('axis', axis, Vector3)
        gd_ptr = ffi.new("godot_basis*")
        lib.godot_basis_rotated(gd_ptr, self._gd_ptr, axis._gd_obj, phi)
        return Basis.build_from_gd_ptr(gd_ptr)

    def scaled(self, scale):
        self.check_param_type('scale', scale, Vector3)
        gd_ptr = ffi.new("godot_basis*")
        lib.godot_basis_scaled(gd_ptr, self._gd_ptr, scale._gd_obj)
        return Basis.build_from_gd_ptr(gd_ptr)

    def tdotx(self, with_):
        self.check_param_type('with_', with_, Vector3)
        return lib.godot_basis_tdotx(self._gd_ptr, with_._gd_obj)

    def tdoty(self, with_):
        self.check_param_type('with_', with_, Vector3)
        return lib.godot_basis_tdoty(self._gd_ptr, with_._gd_obj)

    def tdotz(self, with_):
        self.check_param_type('with_', with_, Vector3)
        return lib.godot_basis_tdotz(self._gd_ptr, with_._gd_obj)

    def transposed(self):
        gd_ptr = ffi.new("godot_basis*")
        lib.godot_basis_transposed(gd_ptr, self._gd_ptr)
        return Basis.build_from_gd_ptr(gd_ptr)

    def xform(self, vect):
        self.check_param_type('vect', vect, Vector3)
        gd_obj = lib.godot_basis_xform(self._gd_ptr, vect._gd_obj)
        return Vector3.build_from_gd_obj(gd_obj)

    def xform_inv(self, vect):
        self.check_param_type('vect', vect, Vector3)
        gd_obj = lib.godot_basis_xform_inv(self._gd_ptr, vect._gd_obj)
        return Vector3.build_from_gd_obj(gd_obj)
