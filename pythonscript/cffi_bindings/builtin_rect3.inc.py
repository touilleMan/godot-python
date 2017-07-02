class Rect3(BaseBuiltin):
    __slots__ = ()
    GD_TYPE = lib.GODOT_VARIANT_TYPE_RECT3

    @staticmethod
    def _copy_gdobj(gdobj):
        return godot_rect3_alloc(gdobj[0])

    def __init__(self, position=Vector3(), size=Vector3()):
        self._check_param_type('position', position, Vector3)
        self._check_param_type('size', size, Vector3)
        self._gd_ptr = godot_rect3_alloc()
        lib.godot_rect3_new(self._gd_ptr, position._gd_ptr, size._gd_ptr)

    def __eq__(self, other):
        return isinstance(other, Rect3) and lib.godot_rect3_operator_equal(self._gd_ptr, other._gd_ptr)

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return "<%s(position=%s, size=%s)>" % (type(self).__name__, self.position, self.size)

    # Properties

    @property
    def position(self):
        return Vector3.build_from_gdobj(lib.godot_rect3_get_position(self._gd_ptr))

    @position.setter
    def position(self, val):
        self._check_param_type('val', val, Vector3)
        lib.godot_rect3_set_position(self._gd_ptr, val._gd_ptr)

    @property
    def size(self):
        return Vector3.build_from_gdobj(lib.godot_rect3_get_size(self._gd_ptr))

    @size.setter
    def size(self, val):
        self._check_param_type('val', val, Vector3)
        lib.godot_rect3_set_size(self._gd_ptr, val._gd_ptr)

    # Methods

    def get_area(self):
        return lib.godot_rect3_get_area(self._gd_ptr)

    def has_no_area(self):
        return bool(lib.godot_rect3_has_no_area(self._gd_ptr))

    def has_no_surface(self):
        return bool(lib.godot_rect3_has_no_surface(self._gd_ptr))

    def intersects(self, with_):
        return bool(lib.godot_rect3_intersects(self._gd_ptr, with_._gd_ptr))

    def encloses(self, with_):
        return bool(lib.godot_rect3_encloses(self._gd_ptr, with_._gd_ptr))

    def merge(self, with_):
        raw = lib.godot_rect3_merge(self._gd_ptr, with_._gd_ptr)
        return Rect3.build_from_gdobj(raw)

    def intersection(self, with_):
        raw = lib.godot_rect3_intersection(self._gd_ptr, with_._gd_ptr)
        return Rect3.build_from_gdobj(raw)

    def intersects_plane(self, plane):
        return bool(lib.godot_rect3_intersects_plane(self._gd_ptr, plane._gd_ptr))

    def intersects_segment(self, from_, to):
        return bool(lib.godot_rect3_intersects_segment(self._gd_ptr, from_._gd_ptr, to._gd_ptr))

    def has_point(self, point):
        return bool(lib.godot_rect3_has_point(self._gd_ptr, point._gd_ptr))

    def get_support(self, dir):
        raw = lib.godot_rect3_get_support(self._gd_ptr, dir._gd_ptr)
        return Vector3.build_from_gdobj(raw)

    def get_longest_axis(self):
        raw = lib.godot_rect3_get_longest_axis(self._gd_ptr)
        return Vector3.build_from_gdobj(raw)

    def get_longest_axis_index(self):
        return lib.godot_rect3_get_longest_axis_index(self._gd_ptr)

    def get_longest_axis_size(self):
        return lib.godot_rect3_get_longest_axis_size(self._gd_ptr)

    def get_shortest_axis(self):
        raw = lib.godot_rect3_get_shortest_axis(self._gd_ptr)
        return Vector3.build_from_gdobj(raw)

    def get_shortest_axis_index(self):
        return lib.godot_rect3_get_shortest_axis_index(self._gd_ptr)

    def get_shortest_axis_size(self):
        return lib.godot_rect3_get_shortest_axis_size(self._gd_ptr)

    def expand(self, to_point):
        raw = lib.godot_rect3_expand(self._gd_ptr, to_point._gd_ptr)
        return Rect3.build_from_gdobj(raw)

    def grow(self, by):
        raw = lib.godot_rect3_grow(self._gd_ptr, by)
        return Rect3.build_from_gdobj(raw)

    def get_endpoint(self, idx):
        raw = lib.godot_rect3_get_endpoint(self._gd_ptr, idx)
        return Vector3.build_from_gdobj(raw)
