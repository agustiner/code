
while read -r line; do
    if ! test -f "$line.mp4"; then
	echo "no"
    fi
done < dl
