#!/bin/sh

#
# If someone's overridden the config with their own custom config, then
# just exit silently
#

if [ -n "${X_CONF}" ]; then
    exit
fi

OUT_FILE="/etc/X11/xorg.conf"
ORIG_CONSOLE=$(fgconsole)
HOME=/tmp                   # Needed because in nfs root, Xorg -configure
export HOME                 # tries to write to /, and fails.

# Xorg writes some temp files, which fails if we're running an NFS mounted
# root, because it tries to write to /.  Setting HOME avoids this.

HOME=/tmp
export HOME

clear

# Generate initial file
TEMPFILE=$(mktemp)
LANG=C Xorg -configure :1 > ${TEMPFILE} 2>&1

if [ $? -ne 0 ]; then
    logger -t LTSP "Xorg failed to autodetect this card"
    exit 1;
fi

INPUT_FILE=$(cat ${TEMPFILE} | grep "Your xorg.conf file is " | tr -d '\n' | cut -d' ' -f5)

rm ${TEMPFILE}

# Handle keyboard settings, default to console-setup settings
handle_keyboard_settings() {
    XKBOPTIONS_TMP="$XKBOPTIONS"
    if [ -z "$XKBLAYOUT" ] && [ -z "$XKBMODEL" ]; then
        if [ -e /etc/default/console-setup ];then
            . /etc/default/console-setup
        fi
    fi
    test -z "$XKBRULES" && XKBRULES="xorg"
    test -z "$XKBMODEL" && XKBMODEL="pc105"
    test -z "$XKBLAYOUT" && XKBLAYOUT="en"
    test -z "$XKBOPTIONS_TMP" && XKBOPTIONS=$XKBOPTIONS_TMP

    KBSTRING="Option\t\"XkbRules\"\t\"$XKBRULES\"\n\tOption\t\"XkbModel\"\t\"$XKBMODEL\"\n\tOption\t\"XkbLayout\"\t\"$XKBLAYOUT\""

    if [ -n "$XKBVARIANT" ]; then
        KBSTRING="${KBSTRING}\n\tOption\t\"XkbVariant\"\t\"$XKBVARIANT\""
    fi
    if [ -n "$XKBOPTIONS" ]; then
        KBSTRING="${KBSTRING}\n\tOption\t\"XKbOptions\"\t\"$XKBOPTIONS\""
    fi
    if [ "$(grep -c XkbLayout $INPUT_FILE)" = 0 ];then
        sed -i /'Driver.*"kbd"'/a\ "\\\t$KBSTRING" $INPUT_FILE
    fi
}

# Handle additional mouse settings (/dev/psaux is used by synaptics already, we dont
# want anything to use /dev/input/mice, serial mice are handled by inputattach)
handle_mouse_settings() {
    if [ -n "$X_MOUSE_DEVICE" ] &&
        [ -z "$(echo $X_MOUSE_DEVICE | grep '/dev/tty')" ] &&
        [ -z "$(echo $X_MOUSE_DEVICE | grep '/dev/input/mice')" ] &&
        [ -z "$(echo $X_MOUSE_DEVICE | grep '/dev/psaux')" ];then
        X_MOUSE_DEVICE=$(echo $X_MOUSE_DEVICE |sed -e s/'\/'/'\\\/'/g)
        test -z $X_MOUSE_PROTOCOL && X_MOUSE_PROTOCOL="auto"
        EXTRAMOUSE="EndSection\n\nSection \"InputDevice\"\n\tIdentifier\t\"Mouse1\"\n\tDriver\t\"mouse\"\n\tOption\t"Device"\t$X_MOUSE_DEVICE\n\tOption\t\"Protocol\"\t$X_MOUSE_PROTOCOL\nEndSection"
        sed -i /'Identifier  "Mouse0"'/,/'EndSection'/s/'EndSection'/"$EXTRAMOUSE"/g $INPUT_FILE
        sed -i /'Section "ServerLayout"'/,/'EndSection'/s/'EndSection'/"\tInputDevice\t\"Mouse1\"\nEndSection"/g $INPUT_FILE
    fi

    if [ "$X_MOUSE_EMULATE3BTN" != "False" ];then
        sed -i /'Identifier  "Mouse0"'/,/'EndSection'/s/'EndSection'/'\tOption\t"Emulate3Buttons"\t"true"\nEndSection'/ $INPUT_FILE
        if [ !"$(grep Mouse1 $INPUT_FILE)" ];then
            sed -i /'Identifier\t"Mouse1"'/,/'EndSection'/s/'EndSection'/'\tOption\t"Emulate3Buttons"\t"true"\nEndSection'/ $INPUT_FILE
        fi
    fi
}

# Handle driver options
handle_driver(){
    if [ -n "$XSERVER" ] && [ "$XSERVER" != "auto" ]; then
        SERVERLINE="Driver\t\"$XSERVER\""
        sed -i /'Section "Device"'/,/'EndSection'/s/'Driver.*'/$SERVERLINE/g $INPUT_FILE
    fi
}

# Set Videoram
set_videoram(){
    if [ -n "$X_VIDEO_RAM" ];then
        RAMLINE="\tOption\t\"VideoRam\"\t\"$X_VIDEO_RAM\"\nEndSection"
        sed -i /'Section "Device"'/,/'EndSection'/s/'EndSection'/$RAMLINE/g $INPUT_FILE
    fi
}

# Set Options, if any
set_options() {
    for OPT in 01 02 03 04 05 06 07 08 09 10 11 12; do
        eval CURROPT=\$X_OPTION_${OPT}
        if [ -n "${CURROPT}" ]; then
            OPTLINE="\tOption\t"
            for O in ${CURROPT}; do
                OPTLINE="${OPTLINE}\t${O}"
            done
            OPTLINE="${OPTLINE}\nEndSection"
            sed -i /'Section "Device"'/,/'EndSection'/s/'EndSection'/${OPTLINE}/g $INPUT_FILE
        fi
    done
}

# FIXME
# Handle Monitor settings
set_sync_ranges(){
    # beware, Xorg -configure sometimes writes these values in the bootstrapped file,
    # so we need replacement code as well
    if [ -n "$X_HORZSYNC" ] && [ -n "$X_VERTREFRESH" ]; then
        if [ -z "$(grep HorizSync $INPUT_FILE)"] && [ -z "$(grep VertRefresh $INPUT_FILE)"];then
            sed -i -e '/Section "Monitor"/,3aVertRefresh\t'$X_VERTREFRESH'\nHorizSync\t'$X_HORZSYNC'' $INPUT_FILE
        else
            sed -i -e 's/^\s*VertRefresh.*$/\tVertRefresh\t'$X_VERTREFRESH'/' $INPUT_FILE
            sed -i -e 's/^\s*HorizSync.*$/\tHorizSync\t'$X_HORZSYNC'/' $INPUT_FILE
        fi
    fi
}

# Handle modes
handle_modes(){
    if [ -n "$X_MODE_0" ] || [ -n "$X_MODE_1" ] || [ -n "$X_MODE_2" ];then
        # We only want to add modes if there arent any in the file yet (add fix to replace exisiting ones)
        X_MODE=""
        X_MODE_0=$( echo "$X_MODE_0" | sed -r 's/^ +//g;s/ *$//g')
        X_MODE_1=$( echo "$X_MODE_1" | sed -r 's/^ +//g;s/ *$//g')
        X_MODE_2=$( echo "$X_MODE_2" | sed -r 's/^ +//g;s/ *$//g')
        [ -n "$X_MODE_0" ] && X_MODE="$X_MODE \"$X_MODE_0\""
        [ -n "$X_MODE_1" ] && X_MODE="$X_MODE \"$X_MODE_1\""
        [ -n "$X_MODE_2" ] && X_MODE="$X_MODE \"$X_MODE_2\""
        if [ "$(grep Modes $INPUT_FILE|sed -e 's/\t*.[0-9]//g' -e 's/\t//g'|grep -c ^Modes)" = 0 ];then
            MODELINES="SubSection \"Display\"\n\t\tModes\t\t$X_MODE"
            sed -i s/'SubSection "Display"'/"$MODELINES"/g $INPUT_FILE
        else 
            sed -i -e 's/^.*Modes.*$/\t\tModes\t\t'${X_MODE}'/'  
        fi
    fi
}

# Set default Depth if specified
set_default_depth(){
    if [ -n "$X_COLOR_DEPTH" ];then
        # Prepend DefaultDepth line above the first occurence of 'SubSection "Display"'
        DEPTH="DefaultDepth $X_COLOR_DEPTH\n\tSubSection \"Display\""
        if [ -z "$(grep DefaultDepth $INPUT_FILE)" ];then
            sed -i 1,/'SubSection "Display"'/s/'SubSection "Display"'/"$DEPTH"/ $INPUT_FILE
        fi
    fi
}

# FIXME
# Handle XFS (do we really want to support that ? most apps use server sided fonts anyway)
handle_xfs(){
    echo $XFS_SERVER >/dev/null
}

# Add hardcoded devcies for ubuntu (synaptics and wacom tablet support)
hardcoded_devices(){
    HARDCODED_DEVS="EndSection\n\n\
Section \"InputDevice\"\n\
\tIdentifier\t\"Synaptics Touchpad\"\n\
\tDriver\t\"synaptics\"\n\
\tOption\t\"SendCoreEvents\"\t\"true\"\n\
\tOption\t\"Device\"\t\"\/dev\/psaux\"\n\
\tOption\t\"Protocol\"\t\"auto-dev\"\n\
\tOption\t\"HorizScrollDelta\"\t\"0\"\n\
EndSection\n\n\
Section \"InputDevice\"\n\
\tDriver\t\"wacom\"\n\
\tIdentifier\t\"stylus\"\n\
\tOption\t\"Device\"\t\"\/dev\/input\/wacom\"\n\
\tOption\t\"Type\"\t\t\"stylus\"\n\
\tOption\t\"ForceDevice\"\t\"ISDV4\"\t\# Tablet PC ONLY\n\
EndSection\n\n\
Section \"InputDevice\"\n\
\tDriver\t\"wacom\"\n\
\tIdentifier\t\"eraser\"\n\
\tOption\t\"Device\"\t\"\/dev\/input\/wacom\"\n\
\tOption\t\"Type\"\t\t\"eraser\"\n\
\tOption\t\"ForceDevice\"\t\"ISDV4\"\t\# Tablet PC ONLY\n\
EndSection\n\n\
Section \"InputDevice\"\n\
\tDriver\t\"wacom\"\n\
\tIdentifier\t\"cursor\"\n\
\tOption\t\"Device\"\t\"\/dev\/input\/wacom\"\n\
\tOption\t\"Type\"\t\t\"cursor\"\n\
\tOption\t\"ForceDevice\"\t\"ISDV4\"\t\# Tablet PC ONLY\n\
EndSection"

    sed -i /'Identifier  "Mouse0"'/,/'EndSection'/s/'EndSection'/"$HARDCODED_DEVS"/g $INPUT_FILE

    HARDCODED_LAYOUT="\tInputDevice\t\"stylus\"\t\"SendCoreEvents\"\n\
\tInputDevice\t\"cursor\"\t\"SendCoreEvents\"\n\
\tInputDevice\t\"eraser\"\t\"SendCoreEvents\"\n\
\tInputDevice\t\"Synaptics Touchpad\"\n\
EndSection"

    sed -i /'Section "ServerLayout"'/,/'EndSection'/s/'EndSection'/"$HARDCODED_LAYOUT"/g $INPUT_FILE
}

# Append DRI section if not there yet
append_dri(){
    if [ "$(grep -c 0666 $INPUT_FILE)" = 0 ];then
        cat <<EOF >> $INPUT_FILE
Section "DRI"
        Mode    0666
EndSection
EOF
    fi
}

# add_touchscreen
add_touchscreen(){
    if [ "${USE_TOUCH}" = "Y" ]; then
        sed -i -e '/ServerLayout/a\\tInputDevice\t"Touchscreen"\t"SendCoreEvents"' $INPUT_FILE
        cat <<-EOF >> $INPUT_FILE

Section "InputDevice"
       Identifier  "TouchScreen"
       Driver      "${X_TOUCH_DRIVER:-elographics}"
       Option      "Device"           "${X_TOUCH_DEVICE:-/dev/ttyS0}"
       Option      "DeviceName"       "Elo"
EOF
        [ -n "${X_TOUCH_MINX}" ] && cat <<-EOF >> $INPUT_FILE
       Option      "MinX"             "${X_TOUCH_MINX:-433}"
       Option      "MaxX"             "${X_TOUCH_MAXX:-3588}"
       Option      "MinY"             "${X_TOUCH_MINY:-569}"
       Option      "MaxY"             "${X_TOUCH_MAXY:-3526}"
EOF
        [ -n "${X_TOUCH_UNDELAY}" ] && cat <<-EOF >> $INPUT_FILE
       Option      "UntouchDelay"     "${X_TOUCH_UNDELAY:-10}"
EOF
        [ -n "${X_TOUCH_RPTDELAY}" ] && cat <<-EOF >> $INPUT_FILE
       Option      "ReportDelay"      "${X_TOUCH_RPTDELAY:-10}"
EOF
        cat <<-EOF >> $INPUT_FILE
       Option      "AlwaysCore"
EndSection
EOF
fi
}

handle_keyboard_settings || true
handle_mouse_settings || true
handle_driver || true
set_videoram || true
set_options || true
handle_modes || true
set_default_depth || true
hardcoded_devices || true
append_dri || true
add_touchscreen || true
set_sync_ranges || true

mv $INPUT_FILE $OUT_FILE

clear
