set terminal png
set xtics nomirror
set ytics nomirror
set xlabel "n"
set grid ytics

set output "swaps.png"
set title "Swaps"
set ylabel "Number of swaps"
plot "swaps.txt" u 1:2 w l notitle

set output "shuffles.png"
set title "Shuffles"
set ylabel "Number of shuffles"
plot "shuffles.txt" u 1:2 w l notitle

set output "laterals.png"
set title "Laterals"
set ylabel "Percent of time lateral swaps are best option"
plot "laterals.txt" u 1:2 w l notitle