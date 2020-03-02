set term postscript eps color 20
set output 'coverage.eps'
set bmargin 8
set lmargin 7
set rmargin 0
set tmargin 1
unset xlabel
set lmargin 8
set rmargin 2
set tmargin 2
set bmargin 8
set ylabel '% per class'
set yrange [0 : 100]
set ytics 0, 10
set xrange[0 : 4]
unset grid
set xtics ("June 60 m" 0, "July 90 m" 1, "July 100 m" 2, "August 90 m" 3, "August 100 m" 4)
set xtics scale 3, 2 rotate by 90
set xtics out offset -1, -5
set style data lines
set key off
plot 'coverage/all.txt' u 1:3:2 w filledcurves lc rgb '#000000', \
     'coverage/gyrl.txt' u 1:3:2 w filledcurves lc rgb '#0000ff', \
     'coverage/gyr.txt' u 1:3:2 w filledcurves lc rgb '#ff0000', \
     'coverage/gy.txt' u 1:3:2 w filledcurves lc rgb '#ffff00', \
     'coverage/g.txt' u 1:3:2 w filledcurves lc rgb '#00ff00'


     