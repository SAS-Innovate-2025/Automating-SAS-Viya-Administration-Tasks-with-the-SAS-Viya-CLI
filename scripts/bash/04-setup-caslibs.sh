
# delete the caslibs so that we can create them even if they exist
/opt/sas/viya/home/bin/sas-viya cas caslibs delete --name salesdl --server cas-shared-default  -su --force
/opt/sas/viya/home/bin/sas-viya cas caslibs delete --name hrdl --server cas-shared-default  -su --force
/opt/sas/viya/home/bin/sas-viya cas caslibs delete --name "Financial Data" --server cas-shared-default  -su --force

# create the sales and hr caslibs from the nfs volume mount
/opt/sas/viya/home/bin/sas-viya cas caslibs create path --caslib salesdl --path /gelcontent/gelcorp/sales/data --server cas-shared-default   --description "gelcontent salesdl" -su
/opt/sas/viya/home/bin/sas-viya cas caslibs create path --caslib hrdl --path /gelcontent/gelcorp/hr/data --server cas-shared-default --description "gelcontent hrdl" -su
/opt/sas/viya/home/bin/sas-viya cas caslibs create path --caslib "Financial Data" --path /gelcontent/gelcorp/finance/data --server cas-shared-default --description "gelcontent finance"