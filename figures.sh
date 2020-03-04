width=1000 # to what width to scale the images (dowm from enormous)
location='/Users/elisa/Dropbox/Research/Topics/Arboles/manuscripts/plaga'
cp diameter.png ${location}/fig1a.png # tree spans
cp difference.png ${location}/fig1b.png # span difference

# example validation
gnuplot bb.plot
convert -density 200 bb.eps ${location}/fig2a.png
cp validation/aug100_both.png fig2_raw.png 
convert -transparent black -resize $width fig2_raw.png fig2_small.png
convert -transparent black -crop 800x600+100+100 fig2_small.png ${location}/fig2b.png

gap=30
gaps="-background transparent -splice ${gap}x0+0+0 +append -chop ${gap}x0+0+0"
vgaps="-background transparent -splice 0x${gap}+0+0 -append -chop 0x${gap}+0+0"

# example sample areas (square)
convert examples/squares/green.png examples/squares/yellow.png examples/squares/red.png examples/squares/leafless.png $gaps +append ${location}/fig3.png 

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
convert -transparent black scaled/enhanced/aug100.png figb4.png
# grayscale histograms
cp histograms/jun60_uniform.png fig4c1.png 
cp histograms/jul90_uniform.png fig4c2.png 
cp histograms/jul100_uniform.png fig4c3.png 
cp histograms/aug90_uniform.png fig4c4.png 
cp histograms/aug100_uniform.png fig4c5.png 

convert fig4a?.png $gaps fig4a_top.png 
convert fig4b?.png $gaps fig4a_bot.png
convert fig4c?.png $gaps ${location}/fig4b.png 
convert fig4a_top.png fig4a_bot.png $vgaps ${location}/fig4a.png

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
convert -resize x$h -rotate 90 collages/original/red.png fig10a2.png 
convert -resize x$h -rotate 90 collages/original/leafless.png fig10a4.png
convert -resize x$h -rotate 90 collages/enhanced/green.png fig10b1.png 
convert -resize x$h -rotate 90 collages/enhanced/yellow.png fig10b2.png
convert -resize x$h -rotate 90 collages/enhanced/red.png fig10b3.png
convert -resize x$h -rotate 90 collages/enhanced/leafless.png fig10b4.png
convert -resize x$h -rotate 90 collages/thresholded/green.png fig10c1.png 
convert -resize x$h -rotate 90 collages/thresholded/yellow.png fig10c2.png
convert -resize x$h -rotate 90 collages/thresholded/red.png fig10c3.png 
convert -resize x$h -rotate 90 collages/thresholded/leafless.png fig10c3.png   
convert fig10a?.png $gaps fig10a.png
convert fig10b?.png $gaps fig10b.png
convert fig10c?.png $gaps fig10c.png
convert fig10?.png $vgaps ${location}/fig10.png

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
convert -crop ${w}x${h}+${x}+${y} scaled/enhanced/aug100.png fig11c1.png
convert -crop ${w}x${h}+${x}+${y} thresholded/aug100.png fig11c1.png
convert -crop ${w}x${h}+${x}+${y} automaton/aug100.png fig11c1.png
convert fig11a?.png $gaps fig11a.png
convert fig11b?.png $gaps fig11b.png
convert fig11c?.png $gaps fig11c.png
convert fig11?.png $vgaps ${location}/fig11.png

convert examples/original/green.png examples/original/yellow.png examples/original/red.png examples/original/leafless.png $gaps fig12a.png
convert examples/enhanced/green.png examples/enhanced/yellow.png examples/enhanced/red.png examples/enhanced/leafless.png $gaps fig12b.png
convert examples/thresholded/green.png examples/thresholded/yellow.png examples/thresholded/red.png examples/thresholded/leafless.png $gaps fig12c.png
convert examples/automaton/green.png examples/automaton/yellow.png examples/automaton/red.png examples/automaton/leafless.png $gaps fig12d.png
convert fig12?.png $vgaps ${location}/fig12.png

w=800
h=800
x=50
y=50
convert -crop ${w}x${h}+${x}+${y} output/air/original/aug100.png fig13a1.png 
convert -crop ${w}x${h}+${x}+${y} output/air/enhanced/aug100.png fig13a1.png
convert -crop ${w}x${h}+${x}+${y} output/air/thresholded/aug100.png fig13b1.png
convert -crop ${w}x${h}+${x}+${y} output/air/automaton/aug100.png fig13b2.png 
convert fig13a?.png $gaps fig13a.png
convert fig13b?.png $gaps fig13b.png
convert fig13?.png $vgaps ${location}/fig13.png

convert -density 300 coverage.eps ${location}/fig14.png

cp trees.tex ${location}/table2.tex
ls -1 timestamps/*start* | awk -F '_' '{print $1}' | cut -c 12-40 > measured.txt
python3 times.py measured.txt > ${location}/table3.tex
sed 's/black/bg/g' conf.tex > ${location}/table4.tex
sed 's/black/bg/g' perf.tex > ${location}/table5.tex
python3 forecast.py ground.txt > ${location}/table6.tex


