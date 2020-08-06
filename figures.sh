#!/bin/zsh

width=1000 
location='/Users/elisa/Dropbox/Research/Topics/Arboles/manuscripts/plaga'
cp diameter.png ${location}/fig1a.png 
cp difference.png ${location}/fig1b.png 
gnuplot bb.plot
convert -density 200 bb.eps ${location}/fig2a.png
cp validation/aug100_both.png fig2_raw.png  
convert -transparent black -resize $width fig2_raw.png fig2_small.png
convert -transparent black -crop 800x600+100+100 fig2_small.png ${location}/fig2b.png

gap=25
gaps="-background transparent -splice ${gap}x0+0+0 +append -chop ${gap}x0+0+0"
vgaps="-background transparent -splice 0x${gap}+0+0 -append -chop 0x${gap}+0+0"

biggap=100 
bighgaps="-background transparent -splice ${biggap}x0+0+0 +append -chop ${biggap}x0+0+0"
bigvgaps="-background transparent -splice 0x${biggap}+0+0 -append -chop 0x${biggap}+0+0"

# example sample areas (square)
convert examples/highlight/green.png examples/highlight/yellow.png examples/highlight/red.png examples/highlight/leafless.png examples/squares/ground.png $(echo $vgaps) fig3.png
convert -transparent black fig3.png ${location}/fig3.png 

# unmodified colors
convert -transparent black scaled/original/jun60.png fig4a1.png
convert -transparent black scaled/original/jul90.png fig4a2.png
convert -transparent black scaled/original/jul100.png fig4a3.png
convert -transparent black scaled/original/aug90.png fig4a4.png
convert -transparent black scaled/original/aug100.png fig4a5.png
# enhanced
convert -transparent black scaled/enhanced/jun60.png fig4b1.png 
convert -transparent black scaled/enhanced/jul90.png fig4b2.png 
convert -transparent black scaled/enhanced/jul100.png fig4b3.png
convert -transparent black scaled/enhanced/aug90.png fig4b4.png 
convert -transparent black scaled/enhanced/aug100.png fig4b5.png
# grayscale histograms
cp histograms/jun60_uniform.png fig4c1.png 
cp histograms/jul90_uniform.png fig4c2.png 
cp histograms/jul100_uniform.png fig4c3.png 
cp histograms/aug90_uniform.png fig4c4.png 
cp histograms/aug100_uniform.png fig4c5.png 

convert fig4a?.png $(echo $gaps) fig4a_top.png 
convert fig4b?.png $(echo $gaps) fig4a_bot.png
convert fig4c?.png $(echo $gaps) fig4b.png 
convert fig4a_top.png fig4a_bot.png $(echo $vgaps) fig4a.png
convert -transparent black fig4a.png ${location}/fig4a.png
cp fig4b.png ${location}/fig4b.png 

# projections
cp projections/green_vs_yellow.png ${location}/fig5b.png
cp projections/green_vs_red.png ${location}/fig5a.png
cp projections/yellow_vs_red.png ${location}/fig5c.png
cp projections/leafless_vs_green.png ${location}/fig5d.png
cp projections/leafless_vs_yellow.png ${location}/fig5e.png
cp projections/leafless_vs_red.png ${location}/fig5f.png

cp histograms/jun60.png ${location}/fig6a.png # example channel histogram 60m
cp histograms/jul90.png ${location}/fig6b.png # example channel histogram 90m
cp histograms/aug100.png ${location}/fig6c.png # example channel histogram 100m

cp histograms/jun60_diff.png ${location}/fig7a.png # example difference histogram 60m
cp histograms/jul90_diff.png ${location}/fig7b.png # example difference histogram 90m
cp histograms/aug100_diff.png ${location}/fig7c.png # example difference histogram 100m

convert -trim -fuzz 2% ruleperf.png ${location}/fig8.png

h=500
convert -resize x$h -rotate 90 collages/original/green.png fig9a1.png 
convert -resize x$h -rotate 90 collages/original/yellow.png fig9a2.png
convert -resize x$h -rotate 90 collages/original/red.png fig9a3.png 
convert -resize x$h -rotate 90 collages/original/leafless.png fig9a4.png
convert -resize x$h -rotate 90 collages/original/ground.png fig9a5.png
convert -resize x$h -rotate 90 collages/enhanced/green.png fig9b1.png 
convert -resize x$h -rotate 90 collages/enhanced/yellow.png fig9b2.png
convert -resize x$h -rotate 90 collages/enhanced/red.png fig9b3.png
convert -resize x$h -rotate 90 collages/enhanced/leafless.png fig9b4.png
convert -resize x$h -rotate 90 collages/enhanced/ground.png fig9b5.png
convert -resize x$h -rotate 90 collages/thresholded/green.png fig9c1.png 
convert -resize x$h -rotate 90 collages/thresholded/yellow.png fig9c2.png
convert -resize x$h -rotate 90 collages/thresholded/red.png fig9c3.png 
convert -resize x$h -rotate 90 collages/thresholded/leafless.png fig9c4.png
convert -resize x$h -rotate 90 collages/thresholded/ground.png fig9c5.png   
convert fig9a?.png $(echo $bighgaps) fig9a.png
convert fig9b?.png $(echo $bighgaps) fig9b.png
convert fig9c?.png $(echo $bighgaps) fig9c.png
convert fig9?.png $(echo $bigvgaps) fig9.png
convert -transparent black fig9.png ${location}/fig9.png

cmax=`wc -l automaton/*.log | grep automaton | awk '{print $1}' | sort -g | tail -n 1`
gnuplot -e "cmax=$cmax" changes.plot # update the convergence figure for the manuscript
convert -density 300 changes.eps ${location}/fig10.png

x=150
y=150
w=300
h=300

convert -crop ${w}x${h}+${x}+${y} scaled/original/jun60.png fig11a1.png 
convert -crop ${w}x${h}+${x}+${y} scaled/enhanced/jun60.png fig11a2.png 
convert -crop ${w}x${h}+${x}+${y} thresholded/jun60.png fig11a3.png 
convert -crop ${w}x${h}+${x}+${y} automaton/jun60.png fig11a4.png 

convert -crop ${w}x${h}+${x}+${y} scaled/original/jul90.png fig11b1.png
convert -crop ${w}x${h}+${x}+${y} scaled/enhanced/jul90.png fig11b2.png
convert -crop ${w}x${h}+${x}+${y} thresholded/jul90.png fig11b3.png
convert -crop ${w}x${h}+${x}+${y} automaton/jul90.png fig11b4.png

convert -crop ${w}x${h}+${x}+${y} scaled/original/jul100.png fig11c1.png
convert -crop ${w}x${h}+${x}+${y} scaled/enhanced/jul100.png fig11c2.png
convert -crop ${w}x${h}+${x}+${y} thresholded/jul100.png fig11c3.png
convert -crop ${w}x${h}+${x}+${y} automaton/jul100.png fig11c4.png

convert -crop ${w}x${h}+${x}+${y} scaled/original/aug90.png fig11d1.png
convert -crop ${w}x${h}+${x}+${y} scaled/enhanced/aug90.png fig11d2.png
convert -crop ${w}x${h}+${x}+${y} thresholded/aug90.png fig11d3.png
convert -crop ${w}x${h}+${x}+${y} automaton/aug90.png fig11d4.png

convert -crop ${w}x${h}+${x}+${y} scaled/original/aug100.png fig11e1.png
convert -crop ${w}x${h}+${x}+${y} scaled/enhanced/aug100.png fig11e2.png
convert -crop ${w}x${h}+${x}+${y} thresholded/aug100.png fig11e3.png
convert -crop ${w}x${h}+${x}+${y} automaton/aug100.png fig11e4.png

convert fig11a?.png $(echo $gaps) fig11a.png
convert fig11b?.png $(echo $gaps) fig11b.png
convert fig11c?.png $(echo $gaps) fig11c.png
convert fig11d?.png $(echo $gaps) fig11d.png
convert fig11e?.png $(echo $gaps) fig11e.png
convert fig11?.png $(echo $vgaps) fig11.png
convert -transparent black fig11.png ${location}/fig11.png

convert examples/original/green.png examples/original/yellow.png examples/original/red.png examples/original/leafless.png $(echo $vgaps) fig12a.png
convert examples/enhanced/green.png examples/enhanced/yellow.png examples/enhanced/red.png examples/enhanced/leafless.png $(echo $vgaps) fig12b.png
convert examples/thresholded/green.png examples/thresholded/yellow.png examples/thresholded/red.png examples/thresholded/leafless.png $(echo $vgaps) fig12c.png
convert examples/automaton/green.png examples/automaton/yellow.png examples/automaton/red.png examples/automaton/leafless.png $(echo $vgaps) fig12d.png
convert fig12?.png $(echo $bighgaps) fig12.png
convert -transparent black fig12.png ${location}/fig12.png

cp ml.png ${location}/fig13.png

convert -density 300 coverage.eps ${location}/fig14.png

python3 gsd.py > ${location}/table1.tex
cp trees.tex ${location}/table2.tex
ls -1 timestamps/*start* | awk -F '_' '{print $1}' | cut -c 12-40 > measured.txt
python3 times.py measured.txt > ${location}/table3.tex
sed 's/black/bg/g' conf.tex > ${location}/table4.tex
sed 's/black/bg/g' perf.tex > ${location}/table5.tex
python3 forecast.py ground.txt > table6.tex
cp table6.tex ${location}/table6.tex
fgrep '& 0 ' table6.tex | awk '{print $1}' > mismatched.txt
python3 mismatches.py
cp mismatches.png ${location}/fig16.png

convert examples/walk/original/green.png examples/walk/enhanced/green.png examples/walk/thresholded/green.png examples/walk/automaton/green.png $(echo $vgaps) fig15a.png
convert examples/walk/original/yellow.png examples/walk/enhanced/yellow.png examples/walk/thresholded/yellow.png examples/walk/automaton/yellow.png $(echo $vgaps) fig15b.png
convert examples/walk/original/red.png examples/walk/enhanced/red.png examples/walk/thresholded/red.png examples/walk/automaton/red.png $(echo $vgaps) fig15c.png
convert examples/walk/original/leafless.png examples/walk/enhanced/leafless.png examples/walk/thresholded/leafless.png examples/walk/automaton/leafless.png $(echo $vgaps) fig15d.png

convert fig15?.png $(echo $bighgaps) fig15.png
convert -transparent black fig15.png ${location}/fig15.png


