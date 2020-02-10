cat ulysses.txt | tr -s ' ' '\n' | sort | uniq -c | sort -n > output.txt
tail -n 1 output.txt

awk '{ print length(), $0 | "sort -n" }' output.txt > output1.txt

tail -n 1 output1.txt

tail -n 1 output3.txt
