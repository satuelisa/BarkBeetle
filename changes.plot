set term postscript eps color 18
set output 'changes.eps'
set ylabel 'Number of changes'
set xlabel 'Iteration'
set logscale y
set yrange [0.5:1000000]
set xrange [-5:125]
set xtics 0, 20
set pointsize 1.2
plot "<awk '{print FNR,$0}' jun60.log" u 1:2 lw 3 t 'Jun 60m', \
 "<awk '{print FNR,$0}' jul90.log" u 1:2 lw 3 t 'Jul 90m', \
 "<awk '{print FNR,$0}' jul100.log" u 1:2 lw 3 t 'Jul 100m', \
 "<awk '{print FNR,$0}' aug90.log" u 1:2 lw 3 t 'Aug 90m', \
 "<awk '{print FNR,$0}' aug100.log" u 1:2 lw 3 t 'Aug 100m'