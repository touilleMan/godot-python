/*
 * This file is part of the Micro Python project, http://micropython.org/
 *
 * The MIT License (MIT)
 *
 * Copyright (c) 2015 Damien P. George
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */

// options to control how Micro Python is built

#define MICROPY_ALLOC_PATH_MAX      (PATH_MAX)
#define MICROPY_ENABLE_GC           (1)
#define MICROPY_ENABLE_FINALISER    (1)
#define MICROPY_STACK_CHECK         (0)  // TODO: disable on release ?
#define MICROPY_COMP_CONST          (1)
#define MICROPY_MEM_STATS           (0)
#define MICROPY_DEBUG_PRINTERS      (0)
#define MICROPY_HELPER_REPL         (1)
#define MICROPY_HELPER_LEXER_UNIX   (1)
#define MICROPY_ENABLE_SOURCE_LINE  (1)
#define MICROPY_ERROR_REPORTING     (MICROPY_ERROR_REPORTING_DETAILED)
#define MICROPY_WARNINGS            (1)
#define MICROPY_ENABLE_EMERGENCY_EXCEPTION_BUF   (0)
#define MICROPY_FLOAT_IMPL          (MICROPY_FLOAT_IMPL_DOUBLE)
#define MICROPY_LONGINT_IMPL        (MICROPY_LONGINT_IMPL_MPZ)
#define MICROPY_STREAMS_NON_BLOCK   (1)
#define MICROPY_OPT_COMPUTED_GOTO   (1)
#define MICROPY_OPT_CACHE_MAP_LOOKUP_IN_BYTECODE (1)
#define MICROPY_CAN_OVERRIDE_BUILTINS (1)
#define MICROPY_BUILTIN_METHOD_CHECK_SELF_ARG (1) // TODO: disable on release ?
#define MICROPY_CPYTHON_COMPAT      (1)
#define MICROPY_COMP_DOUBLE_TUPLE_ASSIGN (1)
#define MICROPY_COMP_TRIPLE_TUPLE_ASSIGN (1)
// Whether to implement attributes on functions
#define MICROPY_PY_FUNCTION_ATTRS (1)
// Whether to support descriptors (__get__ and __set__)
// This costs some code size and makes all load attrs and store attrs slow
#define MICROPY_PY_DESCRIPTORS (1)
// Support for async/await/async for/async with
#define MICROPY_PY_ASYNC_AWAIT (1)
// Issue a warning when comparing str and bytes objects
#define MICROPY_PY_STR_BYTES_CMP_WARN (1)
// Whether str object is proper unicode
#define MICROPY_PY_BUILTINS_STR_UNICODE (1)
// Whether str.center() method provided
#define MICROPY_PY_BUILTINS_STR_CENTER (1)
// Whether str.partition()/str.rpartition() method provided
#define MICROPY_PY_BUILTINS_STR_PARTITION (1)
// Whether str.splitlines() method provided
#define MICROPY_PY_BUILTINS_STR_SPLITLINES (1)
// Whether to support bytearray object
#define MICROPY_PY_BUILTINS_BYTEARRAY (1)
// Whether to support memoryview object
#define MICROPY_PY_BUILTINS_MEMORYVIEW (1)
// Whether to support set object
#define MICROPY_PY_BUILTINS_SET (1)
// Whether to support slice subscript operators and slice object
#define MICROPY_PY_BUILTINS_SLICE (1)
// Whether to support slice attribute read access,
// i.e. slice.start, slice.stop, slice.step
#define MICROPY_PY_BUILTINS_SLICE_ATTRS (1)
// Whether to support frozenset object
#define MICROPY_PY_BUILTINS_FROZENSET (1)
// Whether to support property object
#define MICROPY_PY_BUILTINS_PROPERTY (1)
// Whether to implement the start/stop/step attributes (readback) on
// the "range" builtin type. Rarely used, and costs ~60 bytes (x86).
#define MICROPY_PY_BUILTINS_RANGE_ATTRS (1)
// Whether to support timeout exceptions (like socket.timeout)
#define MICROPY_PY_BUILTINS_TIMEOUTERROR (1)
// Whether to support complete set of special methods
// for user classes, otherwise only the most used
#define MICROPY_PY_ALL_SPECIAL_METHODS (1)
// Whether to support compile function
#define MICROPY_PY_BUILTINS_COMPILE (1)
// Whether to support enumerate function(type)
#define MICROPY_PY_BUILTINS_ENUMERATE (1)
// Whether to support eval and exec functions
// By default they are supported if the compiler is enabled
// #define MICROPY_PY_BUILTINS_EVAL_EXEC (MICROPY_ENABLE_COMPILER)
// Whether to support the Python 2 execfile function
#define MICROPY_PY_BUILTINS_EXECFILE (1)
// Whether to support filter function(type)
#define MICROPY_PY_BUILTINS_FILTER (1)
// Whether to support reversed function(type)
#define MICROPY_PY_BUILTINS_REVERSED (1)
// Whether to define "NotImplemented" special constant
#define MICROPY_PY_BUILTINS_NOTIMPLEMENTED (1)
// Whether to support min/max functions
#define MICROPY_PY_BUILTINS_MIN_MAX (1)

#define MICROPY_PY___FILE__         (1)
#define MICROPY_PY_MICROPYTHON_MEM_INFO (0)
#define MICROPY_PY_GC               (1)
#define MICROPY_PY_GC_COLLECT_RETVAL (0)
#define MICROPY_PY_ARRAY            (1)
#define MICROPY_PY_ARRAY_SLICE_ASSIGN (1)
#define MICROPY_PY_COLLECTIONS      (1)
#define MICROPY_PY_COLLECTIONS_ORDEREDDICT (1)
#define MICROPY_PY_MATH             (1)
#define MICROPY_PY_MATH_SPECIAL_FUNCTIONS (1)
#define MICROPY_PY_CMATH            (1)
#define MICROPY_PY_IO               (1)
#define MICROPY_PY_IO_FILEIO        (1)
#define MICROPY_PY_IO_BUFFEREDWRITER (1)
#define MICROPY_PY_STRUCT           (1)
#define MICROPY_PY_SYS              (1)
#define MICROPY_PY_SYS_EXIT         (0)
#define MICROPY_PY_SYS_PLATFORM     "linux"
#define MICROPY_PY_SYS_MAXSIZE      (1)
#define MICROPY_PY_SYS_STDFILES     (1)
#define MICROPY_PY_SYS_STDIO_BUFFER (1)
#define MICROPY_PY_UERRNO           (1)
#define MICROPY_PY_THREAD           (0)
#define MICROPY_PY_UCTYPES          (1)
#define MICROPY_PY_UZLIB            (1)
#define MICROPY_PY_UJSON            (1)
#define MICROPY_PY_URE              (1)
#define MICROPY_PY_UHEAPQ           (1)
#define MICROPY_PY_UTIMEQ           (1)
// Conflicts with godot/core/io/sha256.c:sha256_init
// #define MICROPY_PY_UHASHLIB         (0)
#define MICROPY_PY_UBINASCII        (1)
#define MICROPY_PY_UBINASCII_CRC32  (1)
#define MICROPY_PY_URANDOM          (1)
#define MICROPY_PY_URANDOM_EXTRA_FUNCS (1)
// undefined reference to `mp_module_ussl'
// #define MICROPY_PY_USSL             (0)
#define MICROPY_PY_WEBSOCKET        (1)
// undefined reference to `mp_module_btree'
// #define MICROPY_PY_BTREE            (0)
#define MICROPY_USE_INTERNAL_PRINTF (0)

extern const struct _mp_obj_module_t mp_module_os;

#define MICROPY_PORT_BUILTINS \
    { MP_ROM_QSTR(MP_QSTR_open), MP_ROM_PTR(&mp_builtin_open_obj) }, \
    // { MP_ROM_QSTR(MP_QSTR_input), MP_ROM_PTR(&mp_builtin_input_obj) },

#define MICROPY_PORT_BUILTIN_MODULES \
    { MP_OBJ_NEW_QSTR(MP_QSTR_uos), (mp_obj_t)&mp_module_os }, \

#define MP_STATE_PORT MP_STATE_VM

#define MICROPY_PORT_ROOT_POINTERS \
    mp_obj_t keyboard_interrupt_obj; \
    mp_obj_dict_t godot_references;

//////////////////////////////////////////
// Do not change anything beyond this line
//////////////////////////////////////////

// Define to 1 to use undertested inefficient GC helper implementation
// (if more efficient arch-specific one is not available).
#ifndef MICROPY_GCREGS_SETJMP
    #ifdef __mips__
        #define MICROPY_GCREGS_SETJMP (1)
    #else
        #define MICROPY_GCREGS_SETJMP (0)
    #endif
#endif

// type definitions for the specific machine

#ifdef __LP64__
typedef long mp_int_t; // must be pointer size
typedef unsigned long mp_uint_t; // must be pointer size
#else
// These are definitions for machines where sizeof(int) == sizeof(void*),
// regardless for actual size.
typedef int mp_int_t; // must be pointer size
typedef unsigned int mp_uint_t; // must be pointer size
#endif

#define BYTES_PER_WORD sizeof(mp_int_t)

// Cannot include <sys/types.h>, as it may lead to symbol name clashes
#if _FILE_OFFSET_BITS == 64 && !defined(__LP64__)
typedef long long mp_off_t;
#else
typedef long mp_off_t;
#endif

// We need to provide a declaration/definition of alloca()
#ifdef __FreeBSD__
#include <stdlib.h>
#else
#include <alloca.h>
#endif
