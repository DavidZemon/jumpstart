/**
 * @file {{ name }}-cli{{ extension }}
 *
{{ license_text_for_cxx }}
 */{% if not cxx %}

#ifdef __cplusplus
extern "C" {
#endif{% endif %}

int run ();{% if not cxx %}

#ifdef __cplusplus
}
#endif{% endif %}
