#!/bin/bash

declare MATMP TERTF
MATMP=$(mktemp)
TERTF=$(mktemp)

trap 'rm -f $MATMP $TERTF' EXIT

# MAC addresses of machines allowed
# on this network
sed -e 's|^|\^|; s|$|\\>|' <<EOF > "$MATMP"
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

grep -f "${MATMP}" /etc/tertf/tertfinfo_bak > "$TERTF"

if [[ -s "$TERTF" ]]
then
   if cmp --silent '/tmp/tertf/tertfinfo' '/tmp/tertf/tertfinfo_bak'
   then
      cp -f "$TERTF" '/tmp/tertf/tertfinfo'
      cp -f "$TERTF" '/tmp/tertf/tertfinfo_bak'
      cp -f "$TERTF" '/etc/tertf/tertfinfo_bak'
   fi
fi
