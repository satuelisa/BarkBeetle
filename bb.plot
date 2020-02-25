set term postscript eps color 15
set xlabel "Longitude (W)"
set ylabel "Latitude (N)"
set output "bb.eps"
set size 1.5, 1.5
# Shared longitude (S-N) goes from -99.89974722222223 to -99.89813333333333
set xrange [-99.90060833333334:-99.8971638888889]
# Shared latitude (W-E) goes from 24.2087 to 24.209930555555555
set yrange [24.207919444444446:24.21045833333333]
set arrow 1 from -99.89974722222223, 24.2087 to -99.89974722222223, 24.209930555555555 nohead lc rgb "#dddddd" lw 20
set arrow 2 from -99.89813333333333, 24.2087 to -99.89813333333333, 24.209930555555555 nohead lc rgb "#dddddd" lw 20
set arrow 3 from -99.89813333333333, 24.209930555555555 to -99.89974722222223, 24.209930555555555 nohead lc rgb "#dddddd" lw 20
set arrow 4 from -99.89813333333333, 24.2087 to -99.89974722222223, 24.2087 nohead lc rgb "#dddddd" lw 20
# crop jun60 0 0 9348 7778 (9348, 7778) 24.209930555555555 24.2087 -99.89974722222223 -99.89813333333333
set label 5 "June 60 m" at -99.89893611111111, 24.208695833333334 right textcolor "#ff0000" offset character 1, 1
set arrow 5 from -99.89975555555556, 24.209930555555555 to -99.89813333333333, 24.20993888888889 nohead lc rgb "#ff0000" lw 4
set arrow 6 from -99.89813333333333, 24.20993888888889 to -99.89812500000001, 24.2087 nohead lc rgb "#ff0000" lw 4
set arrow 7 from -99.89812500000001, 24.2087 to -99.89974722222223, 24.208691666666667 nohead lc rgb "#ff0000" lw 4
set arrow 8 from -99.89974722222223, 24.208691666666667 to -99.89975555555556, 24.209930555555555 nohead lc rgb "#ff0000" lw 4
# crop jul90 1411 59 9216 6581 (11931, 8113) 24.209941666666666 24.20841111111111 -99.9000388888889 -99.89757222222222
set label 9 "July 90 m" at -99.89881111111112, 24.20995 right textcolor "#00cc00" offset character 1, 1
set arrow 9 from -99.90005000000001, 24.209941666666666 to -99.89757222222222, 24.209958333333333 nohead lc rgb "#00cc00" lw 4
set arrow 10 from -99.89757222222222, 24.209958333333333 to -99.89756111111112, 24.20841111111111 nohead lc rgb "#00cc00" lw 4
set arrow 11 from -99.89756111111112, 24.20841111111111 to -99.9000388888889, 24.20839722222222 nohead lc rgb "#00cc00" lw 4
set arrow 12 from -99.9000388888889, 24.20839722222222 to -99.90005000000001, 24.209941666666666 nohead lc rgb "#00cc00" lw 4
# crop jul100 2570 656 10145 6967 (12115, 9361) 24.210058333333333 24.208233333333332 -99.90029444444446 -99.8977138888889
set label 13 "July 100 m" at -99.89901111111112, 24.21006527777778 right textcolor "#66cc33" offset character 1, 1
set arrow 13 from -99.90030833333334, 24.210058333333333 to -99.8977138888889, 24.210072222222223 nohead lc rgb "#66cc33" lw 4
set arrow 14 from -99.8977138888889, 24.210072222222223 to -99.8977, 24.208233333333332 nohead lc rgb "#66cc33" lw 4
set arrow 15 from -99.8977, 24.208233333333332 to -99.90029444444446, 24.208219444444445 nohead lc rgb "#66cc33" lw 4
set arrow 16 from -99.90029444444446, 24.208219444444445 to -99.90030833333334, 24.210058333333333 nohead lc rgb "#66cc33" lw 4
# crop aug90 1789 111 10168 7113 (13587, 8663) 24.20995 24.20842777777778 -99.90009166666667 -99.897475
set label 17 "August 90 m" at -99.89877777777778, 24.208419444444445 right textcolor "#0000cc" offset character 1, 1
set arrow 17 from -99.90010277777779, 24.20995 to -99.897475, 24.20996388888889 nohead lc rgb "#0000cc" lw 4
set arrow 18 from -99.897475, 24.20996388888889 to -99.8974638888889, 24.20842777777778 nohead lc rgb "#0000cc" lw 4
set arrow 19 from -99.8974638888889, 24.20842777777778 to -99.90009166666667, 24.20841111111111 nohead lc rgb "#0000cc" lw 4
set arrow 20 from -99.90009166666667, 24.20841111111111 to -99.90010277777779, 24.20995 nohead lc rgb "#0000cc" lw 4
# crop aug100 2606 1122 10449 7661 (13015, 10097) 24.210141666666665 24.208241666666666 -99.90028333333333 -99.89760555555556
set label 21 "August 100 m" at -99.8989375, 24.208233333333332 right textcolor "#6633cc" offset character 1, 1
set arrow 21 from -99.90029722222222, 24.210141666666665 to -99.89760555555556, 24.210158333333332 nohead lc rgb "#6633cc" lw 4
set arrow 22 from -99.89760555555556, 24.210158333333332 to -99.89759166666667, 24.208241666666666 nohead lc rgb "#6633cc" lw 4
set arrow 23 from -99.89759166666667, 24.208241666666666 to -99.90028333333333, 24.208225 nohead lc rgb "#6633cc" lw 4
set arrow 24 from -99.90028333333333, 24.208225 to -99.90029722222222, 24.210141666666665 nohead lc rgb "#6633cc" lw 4
plot NaN t ""