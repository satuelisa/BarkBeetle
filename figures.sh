# this script assumes the figures to go into the parent folder
cp diameter.png ../fig1a.png # tree spans
cp difference.png ../fig1b.png # span difference

cp aug100_validation.png fig2_raw.png # example validation
convert -transparent black -resize 1000x fig2_raw.png fig2_small.png
convert -transparent black -crop 400x400+200+205 fig2_small.png ../fig2.png

cp examples_green_squares.png ../fig3a.png
cp examples_yellow_squares.png ../fig3b.png
cp examples_red_squares.png ../fig3c.png
cp examples_leafless_squares.png ../fig3d.png

cp jun60_smaller.png ../fig4a.png # scaled down, no processing
cp jul90_smaller.png ../fig4b.png # scaled down, no processing
cp jul100_smaller.png ../fig4c.png # scaled down, no processing
cp aug90_smaller.png ../fig4d.png # scaled down, no processing
cp aug100_smaller.png ../fig4e.png # scaled down, no processing

cp jun60_cropped_enhanced.png ../fig4f.png # scaled down and enhanced
cp jul90_cropped_enhanced.png ../fig4g.png # scaled down and enhanced
cp jul100_cropped_enhanced.png ../fig4h.png # scaled down and enhanced
cp aug90_cropped_enhanced.png ../fig4i.png # scaled down and enhanced
cp aug100_cropped_enhanced.png ../fig4j.png # scaled down and enhanced

cp jun60_eh.png ../fig4k.png # grayscale histograms
cp jul90_eh.png ../fig4l.png # grayscale histograms
cp jul100_eh.png ../fig4m.png # grayscale histograms
cp aug90_eh.png ../fig4n.png # grayscale histograms
cp aug100_eh.png ../fig4o.png # grayscale histograms

cp examples_green_circles.png ../fig5a.png # cut-out class
cp examples_yellow_circles.png ../fig5b.png # cut-out class
cp examples_red_circles.png ../fig5c.png # cut-out class
cp examples_leafless_circles.png ../fig5d.png # cut-out class

cp examples_green_enhanced.png ../fig5e.png # comparison 
cp examples_yellow_enhanced.png ../fig5f.png # comparison 
cp examples_red_enhanced.png ../fig5g.png # comparison 
cp examples_leafless_enhanced.png ../fig5h.png # comparison 

cp green_vs_yellow.png ../fig6b.png
cp green_vs_red.png ../fig6a.png
cp yellow_vs_red.png ../fig6c.png
cp leafless_vs_green.png ../fig6d.png
cp leafless_vs_yellow.png ../fig6e.png
cp leafless_vs_red.png ../fig6f.png

cp jun60_histo.png ../fig7a.png # example channel histogram 60m
cp jul90_histo.png ../fig7b.png # example channel histogram 90m
cp aug100_histo.png ../fig7c.png # example channel histogram 100m

cp jun60_diff.png ../fig8a.png # example difference histogram 60m
cp jul90_diff.png ../fig8b.png # example difference histogram 90m
cp aug100_diff.png ../fig8c.png # example difference histogram 100m

convert -density 300 changes.eps ../fig9.png

cp orig_green.png ../fig10a.png # collage
cp orig_yellow.png ../fig10b.png # collage
cp orig_red.png ../fig10c.png # collage
cp orig_leafless.png ../fig10d.png # collage

cp panel_green.png ../fig10e.png # collage
cp panel_yellow.png ../fig10f.png # collage
cp panel_red.png ../fig10g.png # collage
cp panel_leafless.png ../fig10h.png # collage

cp thr_green.png ../fig10i.png # collage
cp thr_yellow.png ../fig10j.png # collage
cp thr_red.png ../fig10k.png # collage
cp thr_leafless.png ../fig10l.png # collage

convert -crop 600x600+400+400 jun60_smaller.png ../fig11a.png # processing example: original
convert -crop 600x600+400+400 jun60_cropped_enhanced.png ../fig11b.png # processing example: enhanced
convert -crop 600x600+400+400 jun60_thresholded.png ../fig11c.png # processing example: thresholded
convert -crop 600x600+400+400 jun60_automaton.png ../fig11d.png # processing example: automaton

convert -crop 600x600+400+400 jul90_smaller.png ../fig11e.png # processing example: original
convert -crop 600x600+400+400 jul90_cropped_enhanced.png ../fig11f.png # processing example: enhanced
convert -crop 600x600+400+400 jul90_thresholded.png ../fig11g.png # processing example: thresholded
convert -crop 600x600+400+400 jul90_automaton.png ../fig11h.png # processing example: automaton

convert -crop 600x600+400+400 aug100_smaller.png ../fig11i.png # processing example: original
convert -crop 600x600+400+400 aug100_cropped_enhanced.png ../fig11j.png # processing example: enhanced
convert -crop 600x600+400+400 aug100_thresholded.png ../fig11k.png # processing example: thresholded
convert -crop 600x600+400+400 aug100_automaton.png ../fig11l.png # processing example: automaton

convert -crop 800x800+300+300 aug100_origout.png ../fig12a.png 
convert -crop 800x800+300+300 aug100_output.png ../fig12b.png 

sed 's/black/bg/g' conf.tex > ../table3.tex
sed 's/black/bg/g' perf.tex > ../table4.tex
