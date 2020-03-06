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

gap=30
gaps="-background transparent -splice ${gap}x0+0+0 +append -chop ${gap}x0+0+0"
vgaps="-background transparent -splice 0x${gap}+0+0 -append -chop 0x${gap}+0+0"

# example sample areas (square)
convert examples/squares/green.png examples/squares/yellow.png examples/squares/red.png examples/squares/leafless.png $(echo $gaps) fig3.png
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
convert -transparent black fig4b.png ${location}/fig4b.png 

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

convert -trim ruleperf.png ${location}/fig8.png

cmax=`wc -l automaton/*.log | grep automaton | awk '{print $1}' | sort -g | tail -n 1`
gnuplot -e "cmax=$cmax" changes.plot # update the convergence figure for the manuscript
convert -density 300 changes.eps ${location}/fig9.png

h=500
convert -resize x$h -rotate 90 collages/original/green.png fig10a1.png 
convert -resize x$h -rotate 90 collages/original/yellow.png fig10a2.png
convert -resize x$h -rotate 90 collages/original/red.png fig10a3.png 
convert -resize x$h -rotate 90 collages/original/leafless.png fig10a4.png
convert -resize x$h -rotate 90 collages/enhanced/green.png fig10b1.png 
convert -resize x$h -rotate 90 collages/enhanced/yellow.png fig10b2.png
convert -resize x$h -rotate 90 collages/enhanced/red.png fig10b3.png
convert -resize x$h -rotate 90 collages/enhanced/leafless.png fig10b4.png
convert -resize x$h -rotate 90 collages/thresholded/green.png fig10c1.png 
convert -resize x$h -rotate 90 collages/thresholded/yellow.png fig10c2.png
convert -resize x$h -rotate 90 collages/thresholded/red.png fig10c3.png 
convert -resize x$h -rotate 90 collages/thresholded/leafless.png fig10c4.png   
convert fig10a?.png $(echo $gaps) fig10a.png
convert fig10b?.png $(echo $gaps) fig10b.png
convert fig10c?.png $(echo $gaps) fig10c.png
convert fig10?.png $(echo $vgaps) fig10.png
convert -transparent black fig10.png ${location}/fig10.png

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
convert -crop ${w}x${h}+${x}+${y} scaled/original/aug100.png fig11c1.png
convert -crop ${w}x${h}+${x}+${y} scaled/enhanced/aug100.png fig11c2.png
convert -crop ${w}x${h}+${x}+${y} thresholded/aug100.png fig11c3.png
convert -crop ${w}x${h}+${x}+${y} automaton/aug100.png fig11c4.png
convert fig11a?.png $(echo $gaps) fig11a.png
convert fig11b?.png $(echo $gaps) fig11b.png
convert fig11c?.png $(echo $gaps) fig11c.png
convert fig11?.png $(echo $vgaps) fig11.png
convert -transparent black fig11.png ${location}/fig11.png

convert examples/original/green.png examples/original/yellow.png examples/original/red.png examples/original/leafless.png $(echo $gaps) fig12a.png
convert examples/enhanced/green.png examples/enhanced/yellow.png examples/enhanced/red.png examples/enhanced/leafless.png $(echo $gaps) fig12b.png
convert examples/thresholded/green.png examples/thresholded/yellow.png examples/thresholded/red.png examples/thresholded/leafless.png $(echo $gaps) fig12c.png
convert examples/automaton/green.png examples/automaton/yellow.png examples/automaton/red.png examples/automaton/leafless.png $(echo $gaps) fig12d.png
convert fig12?.png $(echo $vgaps) fig12.png
convert -transparent black fig12.png ${location}/fig12.png

w=900
h=900
x=50
y=50
convert -crop ${w}x${h}+${x}+${y} output/air/original/aug100.png fig13a1.png 
convert -crop ${w}x${h}+${x}+${y} output/air/enhanced/aug100.png fig13a2.png
convert -crop ${w}x${h}+${x}+${y} output/air/thresholded/aug100.png fig13b1.png
convert -crop ${w}x${h}+${x}+${y} output/air/automaton/aug100.png fig13b2.png 
convert fig13a?.png $(echo $gaps) fig13a.png
convert fig13b?.png $(echo $gaps) fig13b.png
convert fig13?.png $(echo $vgaps) fig13.png
convert -transparent black fig13.png ${location}/fig13.png

convert -density 300 coverage.eps ${location}/fig14.png

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

convert examples/ground/original/green.png examples/ground/enhanced/green.png examples/ground/thresholded/green.png examples/ground/automaton/green.png $(echo $vgaps) fig15a.png
convert examples/ground/original/yellow.png examples/ground/enhanced/yellow.png examples/ground/thresholded/yellow.png examples/ground/automaton/yellow.png $(echo $vgaps) fig15b.png
convert examples/ground/original/red.png examples/ground/enhanced/red.png examples/ground/thresholded/red.png examples/ground/automaton/red.png $(echo $vgaps) fig15c.png
convert examples/ground/original/leafless.png examples/ground/enhanced/leafless.png examples/ground/thresholded/leafless.png examples/ground/automaton/leafless.png $(echo $vgaps) fig15d.png

# bigger gaps between groups
gap=80 
gaps="-background transparent -splice ${gap}x0+0+0 +append -chop ${gap}x0+0+0"
convert fig15?.png $(echo $gaps) fig15.png
convert -transparent black fig15.png ${location}/fig15.png

cp examples/ground/original/
