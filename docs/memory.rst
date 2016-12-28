Object conversion model
=======================


Base object types
-----------------

Godot Variant
- standalone: bool, int, real
- pointer to builtin type (e.g. ``Matrix32``, ``AABB``, etc.)
- pointer to generic ``Object``

Python mp_obj_t
- standalone: bool, small int, real (depend of implementation), qstr
- pointer to generic struct (must have ``mp_obj_base_t base`` as first attribute)

.. note:
	Variant and mp_obj_t instances are only used by copy, no memory management
	needed on themselves.

Naming conventions:
- GST: Godot STandalone
- GPB: Godot Pointer Builtin
- GPO: Godot Pointer Object
- PST: Python STandalone
- PPB: Python Pointer Binding (proxy to Godot data)
- PPE: Python Pointer Exposed (defined with `@exposed` decorator)
- PPI: Python Pointer Internal


Variant memory management
-------------------------

For GPO, Variant contains a raw pointer on the Object and (not necessary) a
reference on the Object.
- If a reference is present, ref counting is at work.
- If not, user need to do manual memory management by calling ``free`` method.

For GPB, there is 3 possibilities:
- No allocated memory for data (e.g. ``Rect2``), so nothing is done.
- Data is stored in a memory pool (e.g. ``Dictionary``), so data's destructor
  is called which make use of ref counting to know what to do.
- Classic C++ allocation for data (e.g. ``Matrix3``) so regular ``delete``
  is called on it.


Conversions implicating a standalone
------------------------------------

Standalone doesn't need garbage collection and doesn't hold reference on
other objects. Hence conversion is trivial.


Conversion Godot -> Python
--------------------------

Each GPB has a corresponding PPB, acting like a proxy from within the
Python interpreter.

GPO binding is done dynamically with the ``DynamicBinder`` using Godot
introspection (i.e. ``ObjectTypeDB``).

It is possible in the future that to create static proxy for core GPO and rely
on dynamic method as a fall-back for unknown classes (i.g. added by 3rd party).


Conversion Python -> Godot
--------------------------

PPB -> GPB described earlier.

PPI objects cannot be converted back to Godot.

PPE instance are exposed as ``PyInstance`` (class exposed as ``PyScript``).
