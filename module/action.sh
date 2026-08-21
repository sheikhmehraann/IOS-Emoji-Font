#!/system/bin/sh
MODPATH="${0%/*}"

set +o standalone 2>/dev/null
unset ASH_STANDALONE 2>/dev/null

SCRIPT="$MODPATH/service.sh"
if [ ! -f "$SCRIPT" ]; then
    echo -e "\nERROR: Missing service.sh" >&2
    exit 1
fi

if ! sh "$SCRIPT"; then
    echo -e "\nERROR: service.sh execution failed" >&2
    exit 1
fi

echo -e "\n iOS Font & Emoji maintenance completed successfully!\n"
exit 0
