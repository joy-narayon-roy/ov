html=$(find ./html -type f | wc -l)
logs=$(find ./log -type f | wc -l)
echo "HTML :" $html 
echo "Errors :" $logs
