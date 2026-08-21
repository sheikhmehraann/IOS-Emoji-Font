#!/system/bin/sh
##########################################################################################
#
#  iOS Bold Font & iOS 26.4 Emoji - Background Daemon
# Author: sheikhmehraan
#
##########################################################################################

MODPATH=${0%/*}
LOGFILE="$MODPATH/service.log"
MAX_LOG_SIZE=$((5 * 1024 * 1024))
MAX_LOG_FILES=3
MAX_LOG_AGE_DAYS=7

FACEBOOK_APPS="com.facebook.orca com.facebook.katana com.facebook.lite com.facebook.mlite"
GMS_FONT_PROVIDER="com.google.android.gms/com.google.android.gms.fonts.provider.FontsProvider"
GMS_FONT_UPDATER="com.google.android.gms/com.google.android.gms.fonts.update.UpdateSchedulerService"
GMS_FONT_DIR_PATTERN="com.google.android.gms/files/fonts"
DATA_FONTS_DIR="/data/fonts"
ORCA_FONT_DIR1="/data/data/com.facebook.orca/files/fonts"
ORCA_FONT_DIR2="/data/user/0/com.facebook.orca/files/fonts"

mkdir -p "$MODPATH"

log() {
    find "$MODPATH" -name "$(basename "$LOGFILE")*" -type f -mtime +$MAX_LOG_AGE_DAYS -exec rm -f {} \; 2>/dev/null
    if [ -f "$LOGFILE" ] && [ $(stat -c%s "$LOGFILE" 2>/dev/null || echo 0) -gt $MAX_LOG_SIZE ]; then
        for i in $(seq $MAX_LOG_FILES -1 1); do
            if [ -f "$LOGFILE.$i" ]; then
                mv "$LOGFILE.$i" "$LOGFILE.$((i+1))"
            fi
        done
        mv "$LOGFILE" "$LOGFILE.1"
    fi
    local log_message="$(date '+%Y-%m-%d %H:%M:%S') - $1"
    echo "$log_message" >> "$LOGFILE"
}

log "================================================"
log " iOS Bold Font & iOS Emoji Service Daemon"
log "Author: sheikhmehraan"
log "Brand: $(getprop ro.product.brand)"
log "Device: $(getprop ro.product.model)"
log "Android Version: $(getprop ro.build.version.release)"
log "================================================"

while [ "$(getprop sys.boot_completed)" != "1" ]; do
    sleep 5
done

while [ ! -d /sdcard ]; do
    sleep 5
done

log "INFO: Boot completed. Running emoji & font background services..."

# Replace in-app emoji fonts
replace_emoji_fonts() {
    if [ ! -f "$MODPATH/system/fonts/NotoColorEmoji.ttf" ]; then
        log "ERROR: Source emoji font not found."
        return
    fi

    EMOJI_FONTS=$(find /data/data /data/user/0 -iname "*emoji*.ttf" 2>/dev/null)
    for font in $EMOJI_FONTS; do
        if [ -w "$font" ]; then
            cp -f "$MODPATH/system/fonts/NotoColorEmoji.ttf" "$font" 2>/dev/null
            chmod 644 "$font" 2>/dev/null
            log "INFO: Replaced in-app emoji font: $font"
        fi
    done
}

replace_emoji_fonts

# Lock Messenger / Facebook emoji
lock_messenger_emoji() {
    for pkg in $FACEBOOK_APPS; do
        if [ -d "/data/data/$pkg" ]; then
            target="/data/data/$pkg/app_ras_blobs/FacebookEmoji.ttf"
            mkdir -p "/data/data/$pkg/app_ras_blobs" 2>/dev/null
            cp -f "$MODPATH/system/fonts/NotoColorEmoji.ttf" "$target" 2>/dev/null
            chmod 444 "$target" 2>/dev/null
            chattr +i "$target" 2>/dev/null
            log "INFO: Locked emoji file for $pkg"
        fi
    done
}

lock_messenger_emoji

# Clean Messenger font cache
for dir in "$ORCA_FONT_DIR1" "$ORCA_FONT_DIR2"; do
    if [ -d "$dir" ]; then
        rm -rf "$dir"/* 2>/dev/null
        chmod 000 "$dir" 2>/dev/null
    fi
done

# Force stop Facebook apps to reload fonts
for app in $FACEBOOK_APPS; do
    am force-stop "$app" 2>/dev/null
done

sleep 2

# Disable GMS font services
disable_gms_font_services() {
    USERS=$(ls -d /data/user/* 2>/dev/null)
    for userpath in $USERS; do
        USERID=${userpath##*/}
        pm disable --user "$USERID" "$GMS_FONT_PROVIDER" >/dev/null 2>&1
        pm disable --user "$USERID" "$GMS_FONT_UPDATER" >/dev/null 2>&1
        log "INFO: Disabled GMS font services for user $USERID"
    done
}

disable_gms_font_services

# Cleanup GMS dynamic fonts
cleanup_gms_fonts() {
    if [ -d "$DATA_FONTS_DIR" ]; then
        rm -rf "$DATA_FONTS_DIR"/* 2>/dev/null
        log "INFO: Cleaned $DATA_FONTS_DIR"
    fi
    find /data -type d -path "*$GMS_FONT_DIR_PATTERN*" 2>/dev/null | while read dir; do
        rm -rf "$dir" 2>/dev/null
    done
}

cleanup_gms_fonts

log "INFO: Background service completed successfully."
log "================================================"
