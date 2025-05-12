# Apply access controls to the /gelcontent folder
export gcid=$(/opt/sas/viya/home/bin/sas-viya --output json folders show --path "/gelcontent" | jq -r '.["id"]')
echo "The gelcontent ID is" $gcid
/opt/sas/viya/home/bin/sas-viya authorization grant --object-uri /folders/folders/$gcid/** --authenticated-users --permissions read

# Apply access controls to the /gelcontent/GELCorp folder
gcid=$(/opt/sas/viya/home/bin/sas-viya --output json folders show --path "/gelcontent/GELCorp" | jq -r '.["id"]')
/opt/sas/viya/home/bin/sas-viya authorization grant --object-uri /folders/folders/$gcid/** --group gelcorp --permissions read
/opt/sas/viya/home/bin/sas-viya authorization grant --object-uri /folders/folders/$gcid/**  --container-uri /folders/folders/$gcid --group GELCorpContentAdmins --permissions read,update,delete,secure,add,remove

# Apply access controls to the /gelcontent/GELCorp/HR folder
hrid=$(/opt/sas/viya/home/bin/sas-viya --output json folders show --path "/gelcontent/GELCorp/HR" | jq -r '.["id"]')
/opt/sas/viya/home/bin/sas-viya authorization grant --object-uri /folders/folders/$hrid/** --container-uri /folders/folders/$hrid --group HR --permissions read

# Apply access controls to the /gelcontent/GELCorp/Sales folder
salesid=$(/opt/sas/viya/home/bin/sas-viya --output json folders show --path "/gelcontent/GELCorp/Sales" | jq -r '.["id"]')
/opt/sas/viya/home/bin/sas-viya authorization grant --object-uri /folders/folders/$salesid/** --container-uri /folders/folders/$salesid --group Sales --permissions read