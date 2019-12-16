{%- set gd_functions = cook_c_signatures("""
// GDAPI: 1.0
void godot_string_new(godot_string* r_dest)
void godot_string_new_copy(godot_string* r_dest, godot_string* p_src)
void godot_string_new_with_wide_string(godot_string* r_dest, wchar_t* p_contents, int p_size)
// wchar_t* godot_string_operator_index(godot_string* p_self, godot_int p_idx)
wchar_t godot_string_operator_index_const(godot_string* p_self, godot_int p_idx)
// wchar_t* godot_string_wide_str(godot_string* p_self)
godot_bool godot_string_operator_equal(godot_string* p_self, godot_string* p_b)
godot_bool godot_string_operator_less(godot_string* p_self, godot_string* p_b)
godot_string godot_string_operator_plus(godot_string* p_self, godot_string* p_b)
godot_int godot_string_length(godot_string* p_self)
// signed char godot_string_casecmp_to(godot_string* p_self, godot_string* p_str)
// signed char godot_string_nocasecmp_to(godot_string* p_self, godot_string* p_str)
// signed char godot_string_naturalnocasecmp_to(godot_string* p_self, godot_string* p_str)
godot_bool godot_string_begins_with(godot_string* p_self, godot_string* p_string)
godot_bool godot_string_begins_with_char_array(godot_string* p_self, char* p_char_array)
godot_array godot_string_bigrams(godot_string* p_self)
godot_string godot_string_chr(wchar_t p_character)
godot_bool godot_string_ends_with(godot_string* p_self, godot_string* p_string)
godot_int godot_string_find(godot_string* p_self, godot_string p_what)
godot_int godot_string_find_from(godot_string* p_self, godot_string p_what, godot_int p_from)
godot_int godot_string_findmk(godot_string* p_self, godot_array* p_keys)
godot_int godot_string_findmk_from(godot_string* p_self, godot_array* p_keys, godot_int p_from)
godot_int godot_string_findmk_from_in_place(godot_string* p_self, godot_array* p_keys, godot_int p_from, godot_int* r_key)
godot_int godot_string_findn(godot_string* p_self, godot_string p_what)
godot_int godot_string_findn_from(godot_string* p_self, godot_string p_what, godot_int p_from)
godot_int godot_string_find_last(godot_string* p_self, godot_string p_what)
// godot_string godot_string_format(godot_string* p_self, godot_variant* p_values)
// godot_string godot_string_format_with_custom_placeholder(godot_string* p_self, godot_variant* p_values, char* p_placeholder)
godot_string godot_string_hex_encode_buffer(uint8_t* p_buffer, godot_int p_len)
godot_int godot_string_hex_to_int(godot_string* p_self)
godot_int godot_string_hex_to_int_without_prefix(godot_string* p_self)
godot_string godot_string_insert(godot_string* p_self, godot_int p_at_pos, godot_string p_string)
godot_bool godot_string_is_numeric(godot_string* p_self)
godot_bool godot_string_is_subsequence_of(godot_string* p_self, godot_string* p_string)
godot_bool godot_string_is_subsequence_ofi(godot_string* p_self, godot_string* p_string)
godot_string godot_string_lpad(godot_string* p_self, godot_int p_min_length)
godot_string godot_string_lpad_with_custom_character(godot_string* p_self, godot_int p_min_length, godot_string* p_character)
godot_bool godot_string_match(godot_string* p_self, godot_string* p_wildcard)
godot_bool godot_string_matchn(godot_string* p_self, godot_string* p_wildcard)
godot_string godot_string_md5(uint8_t* p_md5)
godot_string godot_string_num(double p_num)
godot_string godot_string_num_int64(int64_t p_num, godot_int p_base)
godot_string godot_string_num_int64_capitalized(int64_t p_num, godot_int p_base, godot_bool p_capitalize_hex)
godot_string godot_string_num_real(double p_num)
godot_string godot_string_num_scientific(double p_num)
godot_string godot_string_num_with_decimals(double p_num, godot_int p_decimals)
godot_string godot_string_pad_decimals(godot_string* p_self, godot_int p_digits)
godot_string godot_string_pad_zeros(godot_string* p_self, godot_int p_digits)
godot_string godot_string_replace_first(godot_string* p_self, godot_string p_key, godot_string p_with)
godot_string godot_string_replace(godot_string* p_self, godot_string p_key, godot_string p_with)
godot_string godot_string_replacen(godot_string* p_self, godot_string p_key, godot_string p_with)
godot_int godot_string_rfind(godot_string* p_self, godot_string p_what)
godot_int godot_string_rfindn(godot_string* p_self, godot_string p_what)
godot_int godot_string_rfind_from(godot_string* p_self, godot_string p_what, godot_int p_from)
godot_int godot_string_rfindn_from(godot_string* p_self, godot_string p_what, godot_int p_from)
godot_string godot_string_rpad(godot_string* p_self, godot_int p_min_length)
godot_string godot_string_rpad_with_custom_character(godot_string* p_self, godot_int p_min_length, godot_string* p_character)
godot_real godot_string_similarity(godot_string* p_self, godot_string* p_string)
godot_string godot_string_sprintf(godot_string* p_self, godot_array* p_values, godot_bool* p_error)
godot_string godot_string_substr(godot_string* p_self, godot_int p_from, godot_int p_chars)
double godot_string_to_double(godot_string* p_self)
godot_real godot_string_to_float(godot_string* p_self)
godot_int godot_string_to_int(godot_string* p_self)
godot_string godot_string_camelcase_to_underscore(godot_string* p_self)
godot_string godot_string_camelcase_to_underscore_lowercased(godot_string* p_self)
godot_string godot_string_capitalize(godot_string* p_self)
double godot_string_char_to_double(char* p_what)
godot_int godot_string_char_to_int(char* p_what)
int64_t godot_string_wchar_to_int(wchar_t* p_str)
godot_int godot_string_char_to_int_with_len(char* p_what, godot_int p_len)
int64_t godot_string_char_to_int64_with_len(wchar_t* p_str, int p_len)
int64_t godot_string_hex_to_int64(godot_string* p_self)
int64_t godot_string_hex_to_int64_with_prefix(godot_string* p_self)
int64_t godot_string_to_int64(godot_string* p_self)
// double godot_string_unicode_char_to_double(wchar_t* p_str, wchar_t** r_end)
godot_int godot_string_get_slice_count(godot_string* p_self, godot_string p_splitter)
godot_string godot_string_get_slice(godot_string* p_self, godot_string p_splitter, godot_int p_slice)
godot_string godot_string_get_slicec(godot_string* p_self, wchar_t p_splitter, godot_int p_slice)
godot_array godot_string_split(godot_string* p_self, godot_string* p_splitter)
godot_array godot_string_split_allow_empty(godot_string* p_self, godot_string* p_splitter)
godot_array godot_string_split_floats(godot_string* p_self, godot_string* p_splitter)
godot_array godot_string_split_floats_allows_empty(godot_string* p_self, godot_string* p_splitter)
godot_array godot_string_split_floats_mk(godot_string* p_self, godot_array* p_splitters)
godot_array godot_string_split_floats_mk_allows_empty(godot_string* p_self, godot_array* p_splitters)
godot_array godot_string_split_ints(godot_string* p_self, godot_string* p_splitter)
godot_array godot_string_split_ints_allows_empty(godot_string* p_self, godot_string* p_splitter)
godot_array godot_string_split_ints_mk(godot_string* p_self, godot_array* p_splitters)
godot_array godot_string_split_ints_mk_allows_empty(godot_string* p_self, godot_array* p_splitters)
godot_array godot_string_split_spaces(godot_string* p_self)
wchar_t godot_string_char_lowercase(wchar_t p_char)
wchar_t godot_string_char_uppercase(wchar_t p_char)
godot_string godot_string_to_lower(godot_string* p_self)
godot_string godot_string_to_upper(godot_string* p_self)
godot_string godot_string_get_basename(godot_string* p_self)
godot_string godot_string_get_extension(godot_string* p_self)
godot_string godot_string_left(godot_string* p_self, godot_int p_pos)
wchar_t godot_string_ord_at(godot_string* p_self, godot_int p_idx)
godot_string godot_string_plus_file(godot_string* p_self, godot_string* p_file)
godot_string godot_string_right(godot_string* p_self, godot_int p_pos)
godot_string godot_string_strip_edges(godot_string* p_self, godot_bool p_left, godot_bool p_right)
godot_string godot_string_strip_escapes(godot_string* p_self)
void godot_string_erase(godot_string* p_self, godot_int p_pos, godot_int p_chars)
godot_char_string godot_string_ascii(godot_string* p_self)
godot_char_string godot_string_ascii_extended(godot_string* p_self)
godot_char_string godot_string_utf8(godot_string* p_self)
godot_bool godot_string_parse_utf8(godot_string* p_self, char* p_utf8)
godot_bool godot_string_parse_utf8_with_len(godot_string* p_self, char* p_utf8, godot_int p_len)
godot_string godot_string_chars_to_utf8(char* p_utf8)
godot_string godot_string_chars_to_utf8_with_len(char* p_utf8, godot_int p_len)
uint32_t godot_string_hash(godot_string* p_self)
uint64_t godot_string_hash64(godot_string* p_self)
uint32_t godot_string_hash_chars(char* p_cstr)
uint32_t godot_string_hash_chars_with_len(char* p_cstr, godot_int p_len)
uint32_t godot_string_hash_utf8_chars(wchar_t* p_str)
uint32_t godot_string_hash_utf8_chars_with_len(wchar_t* p_str, godot_int p_len)
godot_pool_byte_array godot_string_md5_buffer(godot_string* p_self)
godot_string godot_string_md5_text(godot_string* p_self)
godot_pool_byte_array godot_string_sha256_buffer(godot_string* p_self)
godot_string godot_string_sha256_text(godot_string* p_self)
godot_bool godot_string_empty(godot_string* p_self)
godot_string godot_string_get_base_dir(godot_string* p_self)
godot_string godot_string_get_file(godot_string* p_self)
godot_string godot_string_humanize_size(size_t p_size)
godot_bool godot_string_is_abs_path(godot_string* p_self)
godot_bool godot_string_is_rel_path(godot_string* p_self)
godot_bool godot_string_is_resource_file(godot_string* p_self)
godot_string godot_string_path_to(godot_string* p_self, godot_string* p_path)
godot_string godot_string_path_to_file(godot_string* p_self, godot_string* p_path)
godot_string godot_string_simplify_path(godot_string* p_self)
godot_string godot_string_c_escape(godot_string* p_self)
godot_string godot_string_c_escape_multiline(godot_string* p_self)
godot_string godot_string_c_unescape(godot_string* p_self)
godot_string godot_string_http_escape(godot_string* p_self)
godot_string godot_string_http_unescape(godot_string* p_self)
godot_string godot_string_json_escape(godot_string* p_self)
godot_string godot_string_word_wrap(godot_string* p_self, godot_int p_chars_per_line)
godot_string godot_string_xml_escape(godot_string* p_self)
godot_string godot_string_xml_escape_with_quotes(godot_string* p_self)
godot_string godot_string_xml_unescape(godot_string* p_self)
godot_string godot_string_percent_decode(godot_string* p_self)
godot_string godot_string_percent_encode(godot_string* p_self)
godot_bool godot_string_is_valid_float(godot_string* p_self)
godot_bool godot_string_is_valid_hex_number(godot_string* p_self, godot_bool p_with_prefix)
godot_bool godot_string_is_valid_html_color(godot_string* p_self)
godot_bool godot_string_is_valid_identifier(godot_string* p_self)
godot_bool godot_string_is_valid_integer(godot_string* p_self)
godot_bool godot_string_is_valid_ip_address(godot_string* p_self)
void godot_string_destroy(godot_string* p_self)
// GDAPI: 1.1
godot_string godot_string_dedent(godot_string* p_self)
godot_string godot_string_rstrip(godot_string* p_self, godot_string* p_chars)
godot_pool_string_array godot_string_rsplit(godot_string* p_self, godot_string* p_divisor, godot_bool p_allow_empty, godot_int p_maxsplit)
godot_string godot_string_trim_prefix(godot_string* p_self, godot_string* p_prefix)
godot_string godot_string_trim_suffix(godot_string* p_self, godot_string* p_suffix)
// GDAPI: 1.2
""") -%}

{%- block pxd_header %}
{% endblock -%}
{%- block pyx_header %}
{% endblock -%}


@cython.final
cdef class GDString:
{% block cdef_attributes %}
    cdef godot_string _gd_data
{% endblock %}

{% block python_defs %}
    def __init__(self, str pystr=None):
        if not pystr:
            gdapi10.godot_string_new(&self._gd_data)
        else:
            pyobj_to_godot_string(pystr, &self._gd_data)

    def __dealloc__(GDString self):
        # /!\ if `__init__` is skipped, `_gd_data` must be initialized by
        # hand otherwise we will get a segfault here
        gdapi10.godot_string_destroy(&self._gd_data)

    def __repr__(GDString self):
        return f"<GDString({str(self)!r})>"

    def __str__(GDString self):
        return godot_string_to_pyobj(&self._gd_data)

    {{ render_operator_eq() | indent }}
    {{ render_operator_ne() | indent }}
    {{ render_operator_lt() | indent }}

{%set hash_specs = gd_functions['hash'] | merge(pyname="__hash__") %}
    {{ render_method(**hash_specs) | indent }}
{%set hash_specs = gd_functions['operator_plus'] | merge(pyname="__add__") %}
    {{ render_method(**hash_specs) | indent }}

    {{ render_method(**gd_functions["begins_with"]) | indent }}
    {{ render_method(**gd_functions["bigrams"]) | indent }}
    {{ render_method(**gd_functions["c_escape"]) | indent }}
    {{ render_method(**gd_functions["c_unescape"]) | indent }}
    {{ render_method(**gd_functions["capitalize"]) | indent }}
    {{ render_method(**gd_functions["dedent"]) | indent }}
    {{ render_method(**gd_functions["empty"]) | indent }}
    {{ render_method(**gd_functions["ends_with"]) | indent }}
    {{ render_method(**gd_functions["erase"]) | indent }}
    {{ render_method(**gd_functions["find"]) | indent }}
    {{ render_method(**gd_functions["find_last"]) | indent }}
    {{ render_method(**gd_functions["findn"]) | indent }}
    {{ render_method(**gd_functions["get_base_dir"]) | indent }}
    {{ render_method(**gd_functions["get_basename"]) | indent }}
    {{ render_method(**gd_functions["get_extension"]) | indent }}
    {{ render_method(**gd_functions["get_file"]) | indent }}
    {{ render_method(**gd_functions["hash"]) | indent }}
    {{ render_method(**gd_functions["hex_to_int"]) | indent }}
    {{ render_method(**gd_functions["insert"]) | indent }}
    {{ render_method(**gd_functions["is_abs_path"]) | indent }}
    {{ render_method(**gd_functions["is_rel_path"]) | indent }}
    {{ render_method(**gd_functions["is_subsequence_of"]) | indent }}
    {{ render_method(**gd_functions["is_subsequence_ofi"]) | indent }}
    {{ render_method(**gd_functions["is_valid_float"]) | indent }}
    {{ render_method(**gd_functions["is_valid_hex_number"]) | indent }}
    {{ render_method(**gd_functions["is_valid_html_color"]) | indent }}
    {{ render_method(**gd_functions["is_valid_identifier"]) | indent }}
    {{ render_method(**gd_functions["is_valid_integer"]) | indent }}
    {{ render_method(**gd_functions["is_valid_ip_address"]) | indent }}
    {{ render_method(**gd_functions["json_escape"]) | indent }}
    {{ render_method(**gd_functions["left"]) | indent }}
    {{ render_method(**gd_functions["length"]) | indent }}
    {{ render_method(**gd_functions["match"]) | indent }}
    {{ render_method(**gd_functions["matchn"]) | indent }}
    {{ render_method(**gd_functions["md5_buffer"]) | indent }}
    {{ render_method(**gd_functions["md5_text"]) | indent }}
    {{ render_method(**gd_functions["pad_decimals"]) | indent }}
    {{ render_method(**gd_functions["pad_zeros"]) | indent }}
    {{ render_method(**gd_functions["percent_decode"]) | indent }}
    {{ render_method(**gd_functions["percent_encode"]) | indent }}
    {{ render_method(**gd_functions["plus_file"]) | indent }}
    {{ render_method(**gd_functions["replace"]) | indent }}
    {{ render_method(**gd_functions["replacen"]) | indent }}
    {{ render_method(**gd_functions["rfind"]) | indent }}
    {{ render_method(**gd_functions["rfindn"]) | indent }}
    {{ render_method(**gd_functions["right"]) | indent }}
    {{ render_method(**gd_functions["rsplit"]) | indent }}
    {{ render_method(**gd_functions["rstrip"]) | indent }}
    {{ render_method(**gd_functions["sha256_buffer"]) | indent }}
    {{ render_method(**gd_functions["sha256_text"]) | indent }}
    {{ render_method(**gd_functions["similarity"]) | indent }}
    {{ render_method(**gd_functions["split"]) | indent }}
    {{ render_method(**gd_functions["split_floats"]) | indent }}
    {{ render_method(**gd_functions["strip_edges"]) | indent }}
    {{ render_method(**gd_functions["substr"]) | indent }}
    {{ render_method(**gd_functions["to_float"]) | indent }}
    {{ render_method(**gd_functions["to_int"]) | indent }}
    {{ render_method(**gd_functions["to_lower"]) | indent }}
    {{ render_method(**gd_functions["to_upper"]) | indent }}
    {{ render_method(**gd_functions["trim_prefix"]) | indent }}
    {{ render_method(**gd_functions["trim_suffix"]) | indent }}
    {{ render_method(**gd_functions["xml_escape"]) | indent }}
    {{ render_method(**gd_functions["xml_unescape"]) | indent }}
{% endblock %}

{%- block python_consts %}
{% endblock -%}
