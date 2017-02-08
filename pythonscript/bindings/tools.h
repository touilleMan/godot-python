#ifndef TOOLS_H
#define TOOLS_H

// Godot imports
#include "core/typedefs.h"
// Micropython imports
#include "micropython/micropython.h"


template<class T> class Singleton {
    private:
        static T *_singleton;

    public:
        void static init() {
            if (_singleton == NULL) {
                _singleton = new T();
            }
        }

        void static finish() {
            if (_singleton != NULL) {
                delete _singleton;
                _singleton = NULL;
            }
        }

        _FORCE_INLINE_ static T *get_singleton() { return _singleton; }
};


template <class T>
T *Singleton<T>::_singleton = NULL;


// Helper to provide property support for native micropython class
void attr_with_locals_and_properties(mp_obj_t self_in, qstr attr, mp_obj_t *dest);


#endif
