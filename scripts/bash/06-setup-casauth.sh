# set permissions on  CASLIB's
/opt/sas/viya/home/bin/sas-viya cas caslibs replace-controls --server cas-shared-default --name  "salesdl" --source-file /gelcontent/gelcorp_initenv/casauth/salescasauths.json --force
/opt/sas/viya/home/bin/sas-viya cas caslibs replace-controls --server cas-shared-default --name "hrdl" --source-file /gelcontent/gelcorp_initenv/casauth/hrcasauths.json --force
/opt/sas/viya/home/bin/sas-viya cas caslibs replace-controls --server cas-shared-default --name "Financial Data" --source-file /gelcontent/gelcorp_initenv/casauth/financecasauths.json --force