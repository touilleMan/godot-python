{%- block pxd_header %}
{% endblock -%}
{%- block pyx_header %}
from libc.stdint cimport int8_t
{% endblock -%}

{# godot_char_string is not really a bultin type...#}
{{ force_mark_rendered("godot_char_string_destroy") }}
{{ force_mark_rendered("godot_char_string_get_data") }}
{{ force_mark_rendered("godot_char_string_length") }}
{# Those methods are present in gdnative_api.json but not in the Godot documentation... #}
{{ force_mark_rendered("godot_string_ascii") }}
{{ force_mark_rendered("godot_string_ascii_extended") }}
{{ force_mark_rendered("godot_string_begins_with_char_array") }}
{{ force_mark_rendered("godot_string_c_escape_multiline") }}
{{ force_mark_rendered("godot_string_camelcase_to_underscore") }}
{{ force_mark_rendered("godot_string_camelcase_to_underscore_lowercased") }}
{{ force_mark_rendered("godot_string_char_lowercase") }}
{{ force_mark_rendered("godot_string_char_to_double") }}
{{ force_mark_rendered("godot_string_char_to_int") }}
{{ force_mark_rendered("godot_string_char_to_int64_with_len") }}
{{ force_mark_rendered("godot_string_char_to_int_with_len") }}
{{ force_mark_rendered("godot_string_char_uppercase") }}
{{ force_mark_rendered("godot_string_chars_to_utf8") }}
{{ force_mark_rendered("godot_string_chars_to_utf8_with_len") }}
{{ force_mark_rendered("godot_string_chr") }}
{{ force_mark_rendered("godot_string_find_from") }}
{{ force_mark_rendered("godot_string_findmk") }}
{{ force_mark_rendered("godot_string_findmk_from") }}
{{ force_mark_rendered("godot_string_findmk_from_in_place") }}
{{ force_mark_rendered("godot_string_findn_from") }}
{{ force_mark_rendered("godot_string_format_with_custom_placeholder") }}
{{ force_mark_rendered("godot_string_get_slice") }}
{{ force_mark_rendered("godot_string_get_slice_count") }}
{{ force_mark_rendered("godot_string_get_slicec") }}
{{ force_mark_rendered("godot_string_hash64") }}
{{ force_mark_rendered("godot_string_hash_chars") }}
{{ force_mark_rendered("godot_string_hash_chars_with_len") }}
{{ force_mark_rendered("godot_string_hash_utf8_chars") }}
{{ force_mark_rendered("godot_string_hash_utf8_chars_with_len") }}
{{ force_mark_rendered("godot_string_hex_encode_buffer") }}
{{ force_mark_rendered("godot_string_hex_to_int64") }}
{{ force_mark_rendered("godot_string_hex_to_int64_with_prefix") }}
{{ force_mark_rendered("godot_string_hex_to_int_without_prefix") }}
{{ force_mark_rendered("godot_string_is_numeric") }}
{{ force_mark_rendered("godot_string_is_resource_file") }}
{{ force_mark_rendered("godot_string_lpad") }}
{{ force_mark_rendered("godot_string_lpad_with_custom_character") }}
{{ force_mark_rendered("godot_string_md5") }}
{{ force_mark_rendered("godot_string_name_destroy") }}
{{ force_mark_rendered("godot_string_name_get_data_unique_pointer") }}
{{ force_mark_rendered("godot_string_name_get_hash") }}
{{ force_mark_rendered("godot_string_name_get_name") }}
{{ force_mark_rendered("godot_string_name_new") }}
{{ force_mark_rendered("godot_string_name_new_data") }}
{{ force_mark_rendered("godot_string_name_operator_equal") }}
{{ force_mark_rendered("godot_string_name_operator_less") }}
{{ force_mark_rendered("godot_string_naturalnocasecmp_to") }}
{{ force_mark_rendered("godot_string_num") }}
{{ force_mark_rendered("godot_string_num_int64") }}
{{ force_mark_rendered("godot_string_num_int64_capitalized") }}
{{ force_mark_rendered("godot_string_num_real") }}
{{ force_mark_rendered("godot_string_num_scientific") }}
{{ force_mark_rendered("godot_string_num_with_decimals") }}
{{ force_mark_rendered("godot_string_operator_index") }}
{{ force_mark_rendered("godot_string_operator_index_const") }}
{{ force_mark_rendered("godot_string_parse_utf8") }}
{{ force_mark_rendered("godot_string_parse_utf8_with_len") }}
{{ force_mark_rendered("godot_string_path_to") }}
{{ force_mark_rendered("godot_string_path_to_file") }}
{{ force_mark_rendered("godot_string_replace_first") }}
{{ force_mark_rendered("godot_string_rfind_from") }}
{{ force_mark_rendered("godot_string_rfindn_from") }}
{{ force_mark_rendered("godot_string_rpad") }}
{{ force_mark_rendered("godot_string_rpad_with_custom_character") }}
{{ force_mark_rendered("godot_string_simplify_path") }}
{{ force_mark_rendered("godot_string_split_allow_empty") }}
{{ force_mark_rendered("godot_string_split_floats_allows_empty") }}
{{ force_mark_rendered("godot_string_split_floats_mk") }}
{{ force_mark_rendered("godot_string_split_floats_mk_allows_empty") }}
{{ force_mark_rendered("godot_string_split_ints") }}
{{ force_mark_rendered("godot_string_split_ints_allows_empty") }}
{{ force_mark_rendered("godot_string_split_ints_mk") }}
{{ force_mark_rendered("godot_string_split_ints_mk_allows_empty") }}
{{ force_mark_rendered("godot_string_split_spaces") }}
{{ force_mark_rendered("godot_string_sprintf") }}
{{ force_mark_rendered("godot_string_to_double") }}
{{ force_mark_rendered("godot_string_to_int64") }}
{{ force_mark_rendered("godot_string_unicode_char_to_double") }}
{{ force_mark_rendered("godot_string_utf8") }}
{{ force_mark_rendered("godot_string_wchar_to_int") }}
{{ force_mark_rendered("godot_string_wide_str") }}
{{ force_mark_rendered("godot_string_word_wrap") }}
{{ force_mark_rendered("godot_string_xml_escape_with_quotes") }}

@cython.final
cdef class GDString:
{% block cdef_attributes %}
    cdef godot_string _gd_data

    @staticmethod
    cdef inline GDString new()

    @staticmethod
    cdef inline GDString new_with_wide_string(wchar_t *content, int size)

    @staticmethod
    cdef inline GDString from_ptr(const godot_string *_ptr)
{% endblock %}

{% block python_defs %}
    def __init__(self, str pystr=None):
        if not pystr:
            {{ force_mark_rendered("godot_string_new" )}}
            gdapi10.godot_string_new(&self._gd_data)
        else:
            pyobj_to_godot_string(pystr, &self._gd_data)

    @staticmethod
    cdef inline GDString new():
        # Call to __new__ bypasses __init__ constructor
        cdef GDString ret = GDString.__new__(GDString)
        gdapi10.godot_string_new(&ret._gd_data)
        return ret

    @staticmethod
    cdef inline GDString new_with_wide_string(wchar_t *content, int size):
        {{ force_mark_rendered("godot_string_new_with_wide_string") }}
        # Call to __new__ bypasses __init__ constructor
        cdef GDString ret = GDString.__new__(GDString)
        gdapi10.godot_string_new_with_wide_string(&ret._gd_data, content, size)
        return ret

    @staticmethod
    cdef inline GDString from_ptr(const godot_string *_ptr):
        # Call to __new__ bypasses __init__ constructor
        cdef GDString ret = GDString.__new__(GDString)
        # `godot_string` is a cheap structure pointing on a refcounted buffer.
        # Unlike it name could let think, `godot_string_new_copy` only
        # increments the refcount of the underlying structure.
        {{ force_mark_rendered("godot_string_new_copy") }}
        gdapi10.godot_string_new_copy(&ret._gd_data, _ptr)
        return ret

    def __dealloc__(GDString self):
        # /!\ if `__init__` is skipped, `_gd_data` must be initialized by
        # hand otherwise we will get a segfault here
        {{ force_mark_rendered("godot_string_destroy" )}}
        gdapi10.godot_string_destroy(&self._gd_data)

    def __repr__(GDString self):
        return f"<GDString({str(self)!r})>"

    def __str__(GDString self):
        return godot_string_to_pyobj(&self._gd_data)

    {{ render_operator_eq() | indent }}
    {{ render_operator_ne() | indent }}
    {{ render_operator_lt() | indent }}

    {{ render_method("hash", py_name="__hash__") | indent }}
    {{ render_method("operator_plus", py_name="__add__") | indent }}

    {{ render_method("begins_with") | indent }}
    {{ render_method("bigrams") | indent }}
    {{ render_method("c_escape") | indent }}
    {{ render_method("c_unescape") | indent }}
    {{ render_method("capitalize") | indent }}
    {{ render_method("casecmp_to") | indent }}
    {{ render_method("count") | indent }}
    {{ render_method("countn") | indent }}
    {{ render_method("dedent") | indent }}
    {{ render_method("empty") | indent }}
    {{ render_method("ends_with") | indent }}
    {{ render_method("erase") | indent }}
    {{ render_method("find") | indent }}
    {{ render_method("find_last") | indent }}
    {{ render_method("findn") | indent }}
    {{ render_method("format") | indent }}
    {{ render_method("get_base_dir") | indent }}
    {{ render_method("get_basename") | indent }}
    {{ render_method("get_extension") | indent }}
    {{ render_method("get_file") | indent }}
    {{ render_method("hash") | indent }}
    {{ render_method("hex_to_int") | indent }}
    {{ render_method("http_escape") | indent }}
    {{ render_method("http_unescape") | indent }}

    @staticmethod
    def humanize_size(size_t size):
        {{ force_mark_rendered("godot_string_humanize_size") }}
        cdef GDString __ret = GDString.__new__(GDString)
        __ret._gd_data = gdapi10.godot_string_humanize_size(size)
        return __ret

    {{ render_method("insert") | indent }}
    {{ render_method("is_abs_path") | indent }}
    {{ render_method("is_rel_path") | indent }}
    {{ render_method("is_subsequence_of") | indent }}
    {{ render_method("is_subsequence_ofi") | indent }}
    {#- {{ render_method("is_valid_filename") | indent }} # TODO: Missing from binding ! #}
    {{ render_method("is_valid_float") | indent }}
    {{ render_method("is_valid_hex_number") | indent }}
    {{ render_method("is_valid_html_color") | indent }}
    {{ render_method("is_valid_identifier") | indent }}
    {{ render_method("is_valid_integer") | indent }}
    {{ render_method("is_valid_ip_address") | indent }}
    {{ render_method("json_escape") | indent }}
    {{ render_method("left") | indent }}
    {{ render_method("length") | indent }}
    {#- {{ render_method("lstrip") | indent }} # TODO: Missing from binding ! #}
    {{ render_method("match") | indent }}
    {{ render_method("matchn") | indent }}
    {{ render_method("md5_buffer") | indent }}
    {{ render_method("md5_text") | indent }}
    {{ render_method("nocasecmp_to") | indent }}
    {{ render_method("ord_at") | indent }}
    {{ render_method("pad_decimals") | indent }}
    {{ render_method("pad_zeros") | indent }}
    {{ render_method("percent_decode") | indent }}
    {{ render_method("percent_encode") | indent }}
    {{ render_method("plus_file") | indent }}
    {#- {{ render_method("repeat") | indent }} # TODO: Missing from binding ! #}
    {{ render_method("replace") | indent }}
    {{ render_method("replacen") | indent }}
    {{ render_method("rfind") | indent }}
    {{ render_method("rfindn") | indent }}
    {{ render_method("right") | indent }}
    {{ render_method("rsplit") | indent }}
    {{ render_method("rstrip") | indent }}
    {#- {{ render_method("sha1_buffer") | indent }} # TODO: Missing from binding ! #}
    {#- {{ render_method("sha1_text") | indent }} # TODO: Missing from binding ! #}
    {{ render_method("sha256_buffer") | indent }}
    {{ render_method("sha256_text") | indent }}
    {{ render_method("similarity") | indent }}
    {{ render_method("split") | indent }}
    {{ render_method("split_floats") | indent }}
    {{ render_method("strip_edges") | indent }}
    {{ render_method("strip_escapes") | indent }}
    {{ render_method("substr") | indent }}
    {#- {{ render_method("to_ascii") | indent }} # TODO: Missing from binding ! #}
    {{ render_method("to_float") | indent }}
    {{ render_method("to_int") | indent }}
    {{ render_method("to_lower") | indent }}
    {{ render_method("to_upper") | indent }}
    {#- {{ render_method("to_utf8") | indent }} # TODO: Missing from binding ! #}
    {{ render_method("trim_prefix") | indent }}
    {{ render_method("trim_suffix") | indent }}
    {{ render_method("xml_escape") | indent }}
    {{ render_method("xml_unescape") | indent }}

{% endblock %}

{%- block python_consts %}
{% endblock -%}
