width=1000 # to what width to scale the images (dowm from enormous)
location='/Users/elisa/Dropbox/Research/Topics/Arboles/manuscripts/plaga'
cp diameter.png ${location}/fig1a.png # tree spans
cp difference.png ${location}/fig1b.png # span difference

# example validation
cp validation/aug100.png fig2_raw.png 
convert -transparent black -resize $width fig2_raw.png fig2_small.png
convert -transparent black -crop 400x400+200+205 fig2_small.png ${location}/fig2.png

# example sample areas (square)
cp examples/squares/green.png ${location}/fig3a.png
cp examples/squares/yellow.png ${location}/fig3b.png
cp examples/squares/red.png ${location}/fig3c.png
cp examples/squares/leafless.png ${location}/fig3d.png

# unmodified colors
convert -transparent black -resize $width orthomosaics/jun60.tiff ${location}/fig4a.png
convert -transparent black -resize $width orthomosaics/jul90.tiff ${location}/fig4b.png
convert -transparent black -resize $width orthomosaics/jul100.tiff ${location}/fig4c.png
convert -transparent black -resize $width orthomosaics/aug90.tiff ${location}/fig4d.png
convert -transparent black -resize $width orthomosaics/aug100.tiff ${location}/fig4e.png

# enhanced
convert -transparent black -resize $width  enhanced/jun60.png ${location}/fig4f.png 
convert -transparent black -resize $width  enhanced/jul90.png ${location}/fig4g.png 
convert -transparent black -resize $width  enhanced/jul100.png ${location}/fig4h.png
convert -transparent black -resize $width  enhanced/aug90.png ${location}/fig4i.png 
convert -transparent black -resize $width  enhanced/aug100.png ${location}/fig4j.png

# grayscale histograms
cp histograms/jun60_uniform.png ${location}/fig4k.png 
cp histograms/jul90_uniform.png ${location}/fig4l.png 
cp histograms/jul100_uniform.png ${location}/fig4m.png 
cp histograms/aug90_uniform.png ${location}/fig4n.png 
cp histograms/aug100_uniform.png ${location}/fig4o.png 

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

convert -density 300 changes.eps ${location}/fig8.png

# collage panels
cp collages/original/green.png ${location}/fig9a.png 
cp collages/original/yellow.png ${location}/fig9b.png
cp collages/original/red.png ${location}/fig9c.png 
cp collages/original/leafless.png ${location}/fig9d.png

cp collages/enhanced/green.png ${location}/fig9e.png 
cp collages/enhanced/yellow.png ${location}/fig9f.png
cp collages/enhanced/red.png ${location}/fig9g.png
cp collages/enhanced/leafless.png ${location}/fig9h.png

cp collages/thresholded/green.png ${location}/fig9i.png 
cp collages/thresholded/yellow.png ${location}/fig9j.png
cp collages/thresholded/red.png ${location}/fig9k.png 
cp collages/thresholded/leafless.png ${location}/fig9l.png   

convert -crop 600x600+400+400 scaled/original/jun60.png ${location}/fig10a.png # processing example: original
convert -crop 600x600+400+400 scaled/enhanced/jun60.png ${location}/fig10b.png # processing example: enhanced
convert -crop 600x600+400+400 thresholded/jun60.png ${location}/fig10c.png # processing example: thresholded
convert -crop 600x600+400+400 automaton/jun60.png ${location}/fig10d.png # processing example: automaton

convert -crop 600x600+400+400 scaled/original/jul90.png ${location}/fig10e.png # processing example: original
convert -crop 600x600+400+400 scaled/enhanced/jul90.png ${location}/fig10f.png # processing example: enhanced
convert -crop 600x600+400+400 thresholded/jul90.png ${location}/fig10g.png # processing example: thresholded
convert -crop 600x600+400+400 automaton/jul90.png ${location}/fig10h.png # processing example: automaton

convert -crop 600x600+400+400 scaled/original/aug100.png ${location}/fig10i.png # processing example: original
convert -crop 600x600+400+400 scaled/enhanced/aug100.png ${location}/fig10j.png # processing example: enhanced
convert -crop 600x600+400+400 thresholded/aug100.png ${location}/fig10k.png # processing example: thresholded
convert -crop 600x600+400+400 automaton/aug100.png ${location}/fig10l.png # processing example: automaton

# examples as circles in original color
cp examples/original/green.png ${location}/fig11a.png 
cp examples/original/yellow.png ${location}/fig11b.png 
cp examples/original/red.png ${location}/fig11c.png 
cp examples/original/leafless.png ${location}/fig11d.png 

# examples as circles in enhanced color
cp examples/enhanced/green.png ${location}/fig11e.png 
cp examples/enhanced/yellow.png ${location}/fig11f.png 
cp examples/enhanced/red.png ${location}/fig11g.png
cp examples/enhanced/leafless.png ${location}/fig11h.png 

# examples as circles threholded
cp examples/thresholded/green.png ${location}/fig11i.png 
cp examples/thresholded/yellow.png ${location}/fig11j.png 
cp examples/thresholded/red.png ${location}/fig11k.png
cp examples/thresholded/leafless.png ${location}/fig11l.png 

# examples as circles after automaton
cp examples/automaton/green.png ${location}/fig11m.png 
cp examples/automaton/yellow.png ${location}/fig11n.png 
cp examples/automaton/red.png ${location}/fig11o.png
cp examples/automaton/leafless.png ${location}/fig11p.png 

convert -crop 800x800+300+300 output/air/original/aug100.png ${location}/fig12a.png 
convert -crop 800x800+300+300 output/air/enhanced/aug100.png ${location}/fig12b.png
convert -crop 800x800+300+300 output/air/thresholded/aug100.png ${location}/fig12c.png
convert -crop 800x800+300+300 output/air/automaton/aug100.png ${location}/fig12d.png 

python3 times.py > ${location}/table3.tex
sed 's/black/bg/g' conf.tex > ${location}/table4.tex
sed 's/black/bg/g' perf.tex > ${location}/table5.tex
python3 forecast.py ground.txt > ${location}/table6.tex


