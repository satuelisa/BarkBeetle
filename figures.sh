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

cp jun60_histo.png ../../fig5a.png # example channel histogram 60m
cp jul90_histo.png ../../fig5b.png # example channel histogram 90m
cp aug100_histo.png ../../fig5c.png # example channel histogram 100m

cp jun60_diff.png ../../fig6a.png # example difference histogram 60m
cp jul90_diff.png ../../fig6b.png # example difference histogram 90m
cp aug100_diff.png ../../fig6c.png # example difference histogram 100m

convert -crop 600x600+600+600 jun60_smaller.png ../../fig7a.png # thresholding example: original
convert -crop 600x600+600+600 jun60_enhanced.png ../../fig7b.png # thresholding example: enhanced
convert -crop 600x600+600+600 jun60_thresholded.png ../../fig7c.png # thresholding example: thresholded

convert -crop 600x600+600+600 jul90_smaller.png ../../fig7d.png # thresholding example: original
convert -crop 600x600+600+600 jul90_enhanced.png ../../fig7e.png # thresholding example: enhanced
convert -crop 600x600+600+600 jul90_thresholded.png ../../fig7f.png # thresholding example: thresholded

convert -crop 600x600+600+600 aug100_smaller.png ../../fig7g.png # thresholding example: original
convert -crop 600x600+600+600 aug100_enhanced.png ../../fig7h.png # thresholding example: enhanced
convert -crop 600x600+600+600 aug100_thresholded.png ../../fig7i.png # thresholding example: thresholded

