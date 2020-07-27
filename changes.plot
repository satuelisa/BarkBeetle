set term postscript eps color 18
set output 'changes.eps'
set ylabel 'Number of changes'
set xlabel 'Iteration'
set logscale y
set yrange [10:1000000]
set xrange [-5:cmax+5]
set xtics 0, 20
set pointsize 1.5
set palette defined (0 0 0 0, 1 0 0 1, 3 0 1 0, 4 1 0 0, 6 1 1 1)
set cbtics 1, 1
plot "<awk '{print FNR,$1,$3}' automaton/jun60.log" u 1:2:3 w linespoints pt 1 lw 2 palette t 'Jun 60m', \
 "<awk '{print FNR,$1,$3}' automaton/jul90.log" u 1:2:3 w linespoints pt 3 lw 2 palette t 'Jul 90m', \
 "<awk '{print FNR,$1,$3}' automaton/jul100.log" u 1:2:3 w linespoints pt 5 lw 2 palette t 'Jul 100m', \
 "<awk '{print FNR,$1,$3}' automaton/aug90.log" u 1:2:3 w linespoints pt 7 lw 2 palette t 'Aug 90m', \
 "<awk '{print FNR,$1,$3}' automaton/aug100.log" u 1:2:3 w linespoints pt 9 lw 2 palette t 'Aug 100m' 