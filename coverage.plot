set term postscript eps color 20
set output 'coverage.eps'
set bmargin 8
set lmargin 7
set rmargin 0
set tmargin 1
unset xlabel 
set ylabel 'Percentage assigned to each class'
set yrange [0:100]
set ytics 0, 10
set xrange[0:4]
set xtics ("June 60 m" 0, "July 90 m" 1, "July 100 m" 1.5, "August 90 m" 2.5, "August 100 m" 3)
set tics scale 3,2 rotate by 45
set xtics out offset 0, -4
set style data lines
set key off
plot 'coverage/all.txt' u 1:3:2 w filledcurves lc rgb '#0000ff', \
     'coverage/gyr.txt' u 1:3:2 w filledcurves lc rgb '#ff0000', \
     'coverage/gy.txt' u 1:3:2 w filledcurves lc rgb '#ffff00', \
     'coverage/g.txt' u 1:3:2 w filledcurves lc rgb '#00ff00'


     