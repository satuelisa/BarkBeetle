dir='/Users/elisa/Dropbox/Research/Topics/Arboles/manuscripts/plaga/flights'
for dataset in jun60 jul90 jul100 aug90 aug100
do
    docker run -ti --rm -v ${dir}/${dataset}:/datasets/code opendronemap/odm --project-path /datasets
    cp ${dir}/${dataset}/odm_orthophoto/odm_orthophoto.tif orthomosaics/${dataset}.tif
    gdalinfo orthomosaics/${dataset}.tif > annotations/${dataset}.info
done

