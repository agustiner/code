baseurl="https://webcast.in2p3.fr"

while read -r line; do
echo "Downloading ${line}"
curl -o firstpage "${baseurl}/video/${line}"
sed -i -e '/\/player\//!d' firstpage
video=$(grep -oP '(?<=player/).*(?=\?)' firstpage)
curl -o secondpage "${baseurl}/player/${video}"
sed -i -e '/stripSlash/!d' secondpage
mpfour=$(grep -oP '(?<=").*(?=")' secondpage)
curl -o "${line}.mp4" -L --limit-rate 800k "${baseurl}${mpfour}"
done < dl
