while read -r line; do
echo "Downloading ${line}"
filename=$(echo ${line} | grep -oP '(?<=120\/).*(?=\/)')
echo "Filename ${filename}"
curl --fail -o "${filename}.pdf" -L --limit-rate 400k "${line}"
sleep 4
done < dl
