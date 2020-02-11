cp diameter.png ../../fig1a.png # tree spans
cp difference.png ../../fig1b.png # span difference

cp aug100_validation.png ../../fig2_raw.png # example validation

cp jun60_smaller.png ../../fig3a.png # scaled down, no processing
cp jul90_smaller.png ../../fig3b.png # scaled down, no processing
cp jul100_smaller.png ../../fig3c.png # scaled down, no processing
cp aug90_smaller.png ../../fig3d.png # scaled down, no processing
cp aug100_smaller.png ../../fig3e.png # scaled down, no processing

cp jun60_enhanced.png ../../fig3f.png # scaled down and enhanced
cp jul90_enhanced.png ../../fig3g.png # scaled down and enhanced
cp jul100_enhanced.png ../../fig3h.png # scaled down and enhanced
cp aug90_enhanced.png ../../fig3i.png # scaled down and enhanced
cp aug100_enhanced.png ../../fig3j.png # scaled down and enhanced

cp jun60_eh.png ../../fig3k.png # grayscale histograms
cp jul90_eh.png ../../fig3l.png # grayscale histograms
cp jul100_eh.png ../../fig3m.png # grayscale histograms
cp aug90_eh.png ../../fig3n.png # grayscale histograms
cp aug100_eh.png ../../fig3o.png # grayscale histograms

cp aug100_green.png ../../fig4a.png # cut-out class
cp aug100_yellow.png ../../fig4b.png # cut-out class
cp aug100_red.png ../../fig4c.png # cut-out class
cp aug100_leafless.png ../../fig4d.png # cut-out class

cp aug100_orig_green.png ../../fig4e.png # comparison 
cp aug100_orig_yellow.png ../../fig4f.png # comparison 
cp aug100_orig_red.png ../../fig4g.png # comparison 
cp aug100_orig_leafless.png ../../fig4h.png # comparison 

cp green_vs_yellow.png ../../fig5b.png
cp green_vs_red.png ../../fig5a.png
cp yellow_vs_red.png ../../fig5c.png
cp leafless_vs_green.png ../../fig5d.png
cp leafless_vs_yellow.png ../../fig5e.png
cp leafless_vs_red.png ../../fig5f.png

cp jun60_histo.png ../../fig6a.png # example channel histogram 60m
cp jul90_histo.png ../../fig6b.png # example channel histogram 90m
cp aug100_histo.png ../../fig6c.png # example channel histogram 100m

cp jun60_diff.png ../../fig7a.png # example difference histogram 60m
cp jul90_diff.png ../../fig7b.png # example difference histogram 90m
cp aug100_diff.png ../../fig7c.png # example difference histogram 100m

cp orig_green.png ../../fig8a.png # collage
cp orig_yellow.png ../../fig8b.png # collage
cp orig_red.png ../../fig8c.png # collage
cp orig_leafless.png ../../fig8d.png # collage

cp green.png ../../fig8e.png # collage
cp yellow.png ../../fig8f.png # collage
cp red.png ../../fig8g.png # collage
cp leafless.png ../../fig8h.png # collage

cp thr_green.png ../../fig8i.png # collage
cp thr_yellow.png ../../fig8j.png # collage
cp thr_red.png ../../fig8k.png # collage
cp thr_leafless.png ../../fig8l.png # collage

convert -crop 600x600+400+400 jun60_smaller.png ../../fig9a.png # processing example: original
convert -crop 600x600+400+400 jun60_enhanced.png ../../fig9b.png # processing example: enhanced
convert -crop 600x600+400+400 jun60_thresholded.png ../../fig9c.png # processing example: thresholded
convert -crop 600x600+400+400 jun60_majority.png ../../fig9d.png # processing example: majority

convert -crop 600x600+400+400 jul90_smaller.png ../../fig9e.png # processing example: original
convert -crop 600x600+400+400 jul90_enhanced.png ../../fig9f.png # processing example: enhanced
convert -crop 600x600+400+400 jul90_thresholded.png ../../fig9g.png # processing example: thresholded
convert -crop 600x600+400+400 jul90_majority.png ../../fig9h.png # processing example: majority

convert -crop 600x600+400+400 aug100_smaller.png ../../fig9i.png # processing example: original
convert -crop 600x600+400+400 aug100_enhanced.png ../../fig9j.png # processing example: enhanced
convert -crop 600x600+400+400 aug100_thresholded.png ../../fig9k.png # processing example: thresholded
convert -crop 600x600+400+400 aug100_majority.png ../../fig9l.png # processing example: majority


