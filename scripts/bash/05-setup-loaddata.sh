# load data
/opt/sas/viya/home/bin/sas-viya cas tables load --caslib=hrdl --table=* --server=cas-shared-default
/opt/sas/viya/home/bin/sas-viya cas tables load --caslib=salesdl --table=* --server=cas-shared-default
/opt/sas/viya/home/bin/sas-viya cas tables load --caslib="Financial Data" --table=* --server=cas-shared-default