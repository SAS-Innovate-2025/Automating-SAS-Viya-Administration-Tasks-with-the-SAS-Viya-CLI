 # Add GELCORP groups to Viya Custom groups to enable members as administrators
/opt/sas/viya/home/bin/sas-viya identities add-member --group-id SASAdministrators --group-member-id GELCorpSystemAdmins
/opt/sas/viya/home/bin/sas-viya identities add-member --group-id ApplicationAdministrators --group-member-id GELCorpContentAdmins
/opt/sas/viya/home/bin/sas-viya identities add-member --group-id DataBuilders --group-member-id GELCorpContentAdmins

#Create Data Administrators and add Members
/opt/sas/viya/home/bin/sas-viya identities create-group --id DataAdministrators --name "Data Administrators" --description "Users who can administer data "
/opt/sas/viya/home/bin/sas-viya identities add-member --group-id DataAdministrators --user-member-id Delilah
/opt/sas/viya/home/bin/sas-viya identities add-member --group-id DataAdministrators --user-member-id Douglas
/opt/sas/viya/home/bin/sas-viya identities add-member --group-id DataAdministrators --user-member-id geladm

# Setup CASLIB Management Privileges for Data Administrators
export SAS_CLI_DEFAULT_CAS_SERVER=cas-shared-default
