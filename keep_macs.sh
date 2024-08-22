#!/bin/sh

# Cull list of clients on Gl.iNet
# OpenWRT
# August 22, 2024

declare IPTMP TERTF tf
IPTMP=$(mktemp)
TERTF=$(mktemp)

trap 'rm -f $IPTMP $TERTF' EXIT

# MAC addresses of machines allowed
# on this network
sed -e 's|^|\^|; s|$|\\>|' <<EOF > "$IPTMP"
a4:77:a5:a6:b5:b6
a4:77:a5:a6:b5:b6
a4:77:a5:a6:b5:b6
a4:77:a5:a6:b5:b6
a4:77:a5:a6:b5:b6
a4:77:a5:a6:b5:b6
a4:77:a5:a6:b5:b6
a4:77:a5:a6:b5:b6
a4:77:a5:a6:b5:b6
EOF

cmpsum(){
   if [[ $(md5sum $1|awk '{print $1}') == $(md5sum $2|awk '{print $1}') ]]
   then
      return 0
   fi
   return 1
}

grep -f "${IPTMP}" /etc/tertf/tertfinfo_bak > "$TERTF"

if [[ -s "$TERTF" ]]
then
   if cmpsum '/tmp/tertf/tertfinfo' '/tmp/tertf/tertfinfo_bak'
   then
      cp -f "$TERTF" '/tmp/tertf/tertfinfo'
      cp -f "$TERTF" '/tmp/tertf/tertfinfo_bak'
      cp -f "$TERTF" '/etc/tertf/tertfinfo_bak'
   fi
fi
