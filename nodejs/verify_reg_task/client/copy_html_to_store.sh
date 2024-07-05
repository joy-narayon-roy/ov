old=$(ls -1 ./store/html | wc -l)
echo "Store HTML : "$old

html=$(ls -1 ./html | wc -l)
echo "Copy HTML : "$html

find html/ -name '*.html' -print0 | xargs -0 cp -t store/html
nowhtml=$(ls -1 ./store/html | wc -l)
echo "Now Store HTML :" $newhtml
