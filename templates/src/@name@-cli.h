/**
 * @file {{ name }}-cli{{ extension }}
 *
 * @copyright (C){% now "Y" %} Red Lion Controls, Inc. All rights reserved. Red Lion, the Red Lion logo and Sixnet are registered
 * trademarks of Red Lion Controls, Inc. All other company and product names are trademarks of their respective owners.
 */{% if not cxx %}

#ifdef __cplusplus
extern "C" {
#endif{% endif %}

int run ();{% if not cxx %}

#ifdef __cplusplus
}
#endif{% endif %}
