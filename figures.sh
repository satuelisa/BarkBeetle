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

# examples as circles in original color
cp examples/original/green.png ${location}/fig5a.png 
cp examples/original/yellow.png ${location}/fig5b.png 
cp examples/original/red.png ${location}/fig5c.png 
cp examples/original/leafless.png ${location}/fig5d.png 

# examples as circles in enhanced color
cp examples/enhanced/green.png ${location}/fig5e.png 
cp examples/enhanced/yellow.png ${location}/fig5f.png 
cp examples/enhanced/red.png ${location}/fig5g.png
cp examples/enhanced/leafless.png ${location}/fig5h.png 

# projections
cp projections/green_vs_yellow.png ${location}/fig6b.png
cp projections/green_vs_red.png ${location}/fig6a.png
cp projections/yellow_vs_red.png ${location}/fig6c.png
cp projections/leafless_vs_green.png ${location}/fig6d.png
cp projections/leafless_vs_yellow.png ${location}/fig6e.png
cp projections/leafless_vs_red.png ${location}/fig6f.png

cp histograms/jun60.png ${location}/fig7a.png # example channel histogram 60m
cp histograms/jul90.png ${location}/fig7b.png # example channel histogram 90m
cp histograms/aug100.png ${location}/fig7c.png # example channel histogram 100m

cp histograms/jun60_diff.png ${location}/fig8a.png # example difference histogram 60m
cp histograms/jul90_diff.png ${location}/fig8b.png # example difference histogram 90m
cp histograms/aug100_diff.png ${location}/fig8c.png # example difference histogram 100m

exit

convert -density 300 changes.eps ${location}/fig9.png

# collage panels
cp orig_green.png ${location}/fig10a.png 
cp orig_yellow.png ${location}/fig10b.png
cp orig_red.png ${location}/fig10c.png 
cp orig_leafless.png ${location}/fig10d.png

cp panel_green.png ${location}/fig10e.png 
cp panel_yellow.png ${location}/fig10f.png
cp panel_red.png ${location}/fig10g.png
cp panel_leafless.png ${location}/fig10h.png

cp thr_green.png ${location}/fig10i.png 
cp thr_yellow.png ${location}/fig10j.png
cp thr_red.png ${location}/fig10k.png 
cp thr_leafless.png ${location}/fig10l.png   

convert -crop 600x600+400+400 jun60_smaller.png ${location}/fig11a.png # processing example: original
convert -crop 600x600+400+400 jun60_cropped_enhanced.png ${location}/fig11b.png # processing example: enhanced
convert -crop 600x600+400+400 jun60_thresholded.png ${location}/fig11c.png # processing example: thresholded
convert -crop 600x600+400+400 jun60_automaton.png ${location}/fig11d.png # processing example: automaton

convert -crop 600x600+400+400 jul90_smaller.png ${location}/fig11e.png # processing example: original
convert -crop 600x600+400+400 jul90_cropped_enhanced.png ${location}/fig11f.png # processing example: enhanced
convert -crop 600x600+400+400 jul90_thresholded.png ${location}/fig11g.png # processing example: thresholded
convert -crop 600x600+400+400 jul90_automaton.png ${location}/fig11h.png # processing example: automaton

convert -crop 600x600+400+400 aug100_smaller.png ${location}/fig11i.png # processing example: original
convert -crop 600x600+400+400 aug100_cropped_enhanced.png ${location}/fig11j.png # processing example: enhanced
convert -crop 600x600+400+400 aug100_thresholded.png ${location}/fig11k.png # processing example: thresholded
convert -crop 600x600+400+400 aug100_automaton.png ${location}/fig11l.png # processing example: automaton

convert -crop 800x800+300+300 aug100_origout.png ${location}/fig12a.png 
convert -crop 800x800+300+300 aug100_output.png ${location}/fig12b.png 

sed 's/black/bg/g' conf.tex > ${location}/table3.tex
sed 's/black/bg/g' perf.tex > ${location}/table4.tex
