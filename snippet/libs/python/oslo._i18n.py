# coding: utf-8
import oslo_i18n

# Enable lazy translation
oslo_i18n.enable_lazy()

_translators = oslo_i18n.TranslatorFactory(domain='myapp', localedir=None)

# The primary translation function using the well-known name "_"
_ = _translators.primary

# The contextual translation function using the name "_C"
_C = _translators.contextual_form

# The plural translation function using the name "_P"
_P = _translators.plural_form

# Translators for log levels.
#
# The abbreviated names are meant to reflect the usual use of a short
# name like '_'. The "L" is for "log" and the other letter comes from
# the level.
_LI = _translators.log_info
_LW = _translators.log_warning
_LE = _translators.log_error
_LC = _translators.log_critical
