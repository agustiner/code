# get the pdf fles from the page

url=$@

curl -o firstpage "$url"
sed -i -e '/\.pdf/!d' firstpage
grep -oP '(?<=href=").*(?=">)' firstpage > secondpage

dlbase="https://nsarchive2.gwu.edu/nsa/cuba_mis_cri/"

while read -r line; do
echo "Downloading ${line}"
wget --limit-rate 1M "${dlbase}/${line}"
sleep 10
done < secondpage
