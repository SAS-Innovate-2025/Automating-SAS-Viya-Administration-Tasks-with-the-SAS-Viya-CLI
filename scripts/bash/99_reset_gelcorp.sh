 # Cleanup Users and Groups

 export SAS_CLI_DEFAULT_CAS_SERVER=cas-shared-default
/opt/sas/viya/home/bin/sas-viya -y cas caslibs remove-control --caslib _GLOBAL --superuser --grant manageAccess --group DataAdministrators --force


/opt/sas/viya/home/bin/sas-viya identities remove-member --group-id SASAdministrators --group-member-id GELCorpSystemAdmins
/opt/sas/viya/home/bin/sas-viya identities remove-member --group-id ApplicationAdministrators --group-member-id GELCorpContentAdmins
/opt/sas/viya/home/bin/sas-viya identities remove-member --group-id DataBuilders --group-member-id GELCorpContentAdmins

/opt/sas/viya/home/bin/sas-viya identities delete-group --id DataAdministrators

# delete folders
/opt/sas/viya/home/bin/sas-viya -y folders delete --path /gelcontent --recursive

# delete caslibs
/opt/sas/viya/home/bin/sas-viya -y cas caslibs delete --caslib salesdl --server cas-shared-default   --force --su
/opt/sas/viya/home/bin/sas-viya -y cas caslibs delete --caslib hrdl --server cas-shared-default --force --su
/opt/sas/viya/home/bin/sas-viya -y cas caslibs delete --caslib "Financial Data" --server cas-shared-default --force --su
