#!/system/bin/sh
MODPATH="${0%/*}"
set +o standalone 2>/dev/null
unset ASH_STANDALONE 2>/dev/null
sh "$MODPATH/service.sh" && echo " Done." || echo " Failed." >&2
