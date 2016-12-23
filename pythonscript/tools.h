// Shamelessly inspired from micropython-wrap

#define MP_WRAP_CALL(f) \
	MP_WRAP_CALL_EX(f, [](mp_obj_t ret_val) {})

#define MP_WRAP_CALL_EX(f, ex) \
    nlr_buf_t nlr; \
    if (nlr_push(&nlr) == 0) { \
      f(); \
      nlr_pop(); \
    } else { \
      ex(nlr.ret_val); \
    }
