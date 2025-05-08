
<!-- omit in toc -->
# SAS Innovate : Automating SAS Viya Administration Tasks

- [Getting Started: Installation and Configuration Steps](#getting-started-installation-and-configuration-steps)
- [Profiles and Authentication](#profiles-and-authentication)
- [Quick Test and Demo of features](#quick-test-and-demo-of-features)
- [Use the CLI to perform a series of Administration Tasks](#use-the-cli-to-perform-a-series-of-administration-tasks)
  - [Create Folder Structure](#create-folder-structure)
  - [Load Content](#load-content)
  - [Create a CASLIB and Load Data](#create-a-caslib-and-load-data)
  - [Run a SAS Program](#run-a-sas-program)
- [Demo of the Containerized CLI](#demo-of-the-containerized-cli)
  - [Pull and use the SAS Provided sas-viya cli image](#pull-and-use-the-sas-provided-sas-viya-cli-image)
  - [Authenticate and run a command](#authenticate-and-run-a-command)
- [Use pre-built administration CLI images](#use-pre-built-administration-cli-images)
- [Use Apache Airflow to orchestrate processing using the sas-viya CLI container](#use-apache-airflow-to-orchestrate-processing-using-the-sas-viya-cli-container)
  - [Copy the scripts and configuration files](#copy-the-scripts-and-configuration-files)
  - [Create the Python script that defines the flow](#create-the-python-script-that-defines-the-flow)
- [Run the flow and review the results](#run-the-flow-and-review-the-results)
- [Validate](#validate)

## Getting Started: Installation and Configuration Steps

1. Download the executable from support.sas.com: https://support.sas.com/downloads/package.htm?pid=2512. I have saved it in it's default location but I have a symlink to it in /usr/bin. The CLI is also available on Windows and MacOS.

    ```bash
    ls -ln /usr/bin/sas-*
    ```

2. Execute sas-viya to get HELP.

    ```bash
    sas-viya
    ```

3. List repositories

    ```bash
    sas-viya plugins list-repos
    ```

4. List repository plug-ins.

    ```bash
    sas-viya plugins list-repo-plugins
    ```

5. Install a plug-in fron the default SAS repository

    ```bash
    sas-viya plugins install --repo SAS fonts
    ```

6. Force a reinstall

    ```bash
    sas-viya plugins install --repo SAS --force fonts
    ```

7. Install all plugins from the repository. Notice what happens with fonts. Plugins are installed in the .sas directory of the users home directory.

    ```bash
    sas-viya plugins install --repo SAS all
    ```

## Profiles and Authentication

1. Authentication is based on profiles. View the profile commands.

    ```bash
    sas-viya profile
    ```

2. Create a new profile.

    ```bash
    sas-viya --profile new profile init
    ```

3. List the profiles

    ```bash
    sas-viya profile list
    ```

4. To use a profile either use the --profile option or set the environment variable `SAS_CLI_PROFILE`. If neither is set then the **Default** profile is used.

    ```bash
    sas-viya --profile new profile show
    ```

    ```bash
    sas-viya --profile gelcorp profile show
    ```

    ```bash
    export SAS_CLI_PROFILE=gelcorp
    sas-viya profile show
    ```

5. We will use gelcorp for the rest of the hands-on. Authenticate using uid and password (there are other authenticatin methods.) A 1 hour token is stored in .sas/credentials.json in the users home-directory. A refresh token is also generated which is valid for 14 days.

    ```bash
    sas-viya auth login -u geladm -p lnxsas
    sas-viya profile show
    #Current date UTC is 
    date -u +"%Y-%m-%dT%H:%M:%SZ"
    ```

6. Show the credentials file.

    ```bash
    cat ~/.sas/credentials.json
    ```

## Quick Test and Demo of features


1. Get help on a plugin or command.

    ```bash
    sas-viya identities help
    ```


4. Identities whoami and who are the SAS Administrators? Output is in JSON.

    ```bash
    sas-viya identities whoami
    ```

5. Add **--output json**.

    ```bash
    sas-viya --output text identities whoami
    ```

5. Add **--output text**.

    ```bash
    sas-viya --output text identities whoami
    ```

<!---
1. List groups and then list members of a group.

    ```bash
    sas-viya --output text identities list-groups
    sas-viya --output text identities list-members --group-id SASAdministrators
    ```

2. Add a new Viya Administrator
   
    ```bash
    sas-viya --output text identities add-member --group-id SASAdministrators --user-member-id Ahmed
    sas-viya --output text identities list-members --group-id SASAdministrators
    ```
--->

## Use the CLI to perform a series of Administration Tasks

### Create Folder Structure


1. List the current folders.

    ```bash
    sas-viya --output text folders list-members --path "/"
    ```

2. Create a new folder.

    ```bash
    sas-viya folders create --name gelcontent
    ```

3. Create a sub-folder.

    ```bash
    sas-viya --output json folders create --description "Sales" --name "Sales" --parent-path /gelcontent
    ```

4. View the what we have done.

    ```bash
    sas-viya --output text folders list-members --path /gelcontent/ --recursive --tree
    ```

    > NOTE: In many cases you will need the `id` or the `uri` to pass to another command. This is the case when we want to set authorization on a folder. We need to build the URI of the folder. URI at https://developer.sas.com/rest-apis

5. Id is in the output. 

    ```bash
    sas-viya --output json folders show --path /gelcontent
    ```

6. You can also use third-part tools like jq, or grep to

    * retrieve what you want from the output
    * store it in an environment variable for use in later steps.


    ```bash
    folderid=$(sas-viya --output json folders show --path /gelcontent | jq -r '.["id"]')
    echo "The folder id is: " ${folderid}
    ```

7. Use the folder id to set the authorization.

    ```bash
    sas-viya --output json authorization create-rule grant --permissions read,create,update,delete,add,remove,secure --group Sales --object-uri /folders/folders/${folderid}/** --container-uri /folders/folders/${folderid} --description "gn-rule-001"
    ```

### Load Content

1. Upload a Package File and inspect its content.

    ```bash
    sas-viya --output json transfer upload --file "/mnt/shared/forinnovate/content/sales_for_demo.json"

    packageid=$(sas-viya --output json transfer upload --file "/mnt/shared/forinnovate/content/sales_for_demo.json" | jq | jq -r '.["id"]')
    echo ID of the uploaded package is $packageid
    sas-viya --output text transfer show --id ${packageid} --details
    ```

1. Import the package.

    ```bash
    #import the package using the id
    sas-viya -q --output text transfer import --id $packageid
    ```

1. View the folders.

    ```bash
    sas-viya --output text folders list-members --path /gelcontent --recursive --tree
    ```

### Create a CASLIB and Load Data

1. View existing CASLIB's

    ```bash
    sas-viya --output text cas caslibs list --server cas-shared-default
    ```

1. Create a CASLIB

    ```bash
    sas-viya --output text cas caslibs create path --name salesdl --path /gelcontent/gelcorp/sales/data --server cas-shared-default
    ```

1. Many of the tools also accept JSON input. This can be very useful in terms of automation.

    ```bash
    cat /mnt/shared/forinnovate/cas/hrdl.json
    sas-viya cas caslibs create path --source-file /mnt/shared/forinnovate/cas/hrdl.json
    ```

1. View data in the CASLIBS source path.

    ```bash
    sas-viya --output text cas caslibs sources list --server cas-shared-default --caslib salesdl
    ```

2. Set Authorization on the data.

    ```bash
    sas-viya --output text cas caslibs add-control --server cas-shared-default --caslib salesdl --group Sales --grant ReadInfo
    sas-viya --output text cas caslibs add-control --server cas-shared-default --caslib salesdl --group Sales --grant Select
    sas-viya --output text cas caslibs add-control --server cas-shared-default --caslib salesdl --group Sales --grant LimitedPromote
    ```

3. Load the data to CAS.

    ```bash
    sas-viya --output text cas tables load --table=* --server cas-shared-default --caslib salesdl
    ```

4. Show information about a loaded table.

    ```bash
    sas-viya --output text cas tables show-info --table=SALESMASTER --server cas-shared-default --caslib salesdl
    ```

### Run a SAS Program

1. Use the batch plugin to run a SAS program. In a MobaXterm session on **sasnode01** create the following code on a shared location accessible to the compute server.

    ```bash
    tee /shared/gelcontent/gelcorp/shared/code/view_data.sas > /dev/null << EOF

    /* rootdir inside the pod */
    %let rootdir=/gelcontent/gelcorp;

    libname sdata    "&rootdir/sales/data";
    libname ssource  "&rootdir/sales/srcdata";

    proc datasets lib=sdata;

    run;
    quit;

    EOF
    ```

2. Submit the SAS code in batch.

    ```bash
    sas-viya --profile ${SAS_CLI_PROFILE} batch jobs submit-pgm --rem-pgm-path /gelcontent/gelcorp/shared/code/view_data.sas --context default  --watchoutput --waitnoresults  --results-dir /tmp
    ```

3. Undo what we just did.
   
    ```bash
    #delete the caslibs
    /opt/sas/viya/home/bin/sas-viya -y cas caslibs delete --caslib salesdl --server cas-shared-default   --force --su
    /opt/sas/viya/home/bin/sas-viya -y cas caslibs delete --caslib hrdl --server cas-shared-default --force --su

    # remove the authorization rule
    gelfolderid=$(sas-viya --output json folders show --path /gelcontent | jq -r '.["id"]')
    echo "The folder id is: " ${gelfolderid}

    ruleid=$(/opt/pyviyatools/getruleid.py -p Sales -u /folders/folders/$gelfolderid/** --output simplejson | jq -r '.items[]["id"]')
    if [ -z "$ruleid" ]
    then
        echo "\rule does not exist"
    else
        echo "delete rule=$ruleid"
        /opt/sas/viya/home/bin/sas-viya -y authorization remove-rule --id $ruleid
    fi

    # delete folders and content
    /opt/sas/viya/home/bin/sas-viya -y folders delete --path /gelcontent --recursive
    ```

## Demo of the Containerized CLI

### Pull and use the SAS Provided sas-viya cli image

1. The sas-viya CLI Container image is available with a SAS Viya license. To pull the image you need the certificates that are included with your order. In this step we will use mirrormanager to return the image name of the sas-viya cli image in our order.

    ```bash
    source /opt/gellow_work/vars/vars.txt
    climage=$(mirrormgr list remote docker tags --deployment-data /home/cloud-user/project/deploy/license/SASViyaV4_${GELLOW_ORDER}_certs.zip --cadence ${GELLOW_CADENCE_NAME}-${GELLOW_CADENCE_VERSION} | grep sas-viya-cli:${GELLOW_CADENCE_NAME}-${GELLOW_CADENCE_VERSION})
    echo  Order Number is ${GELLOW_ORDER} and latest image is ${climage}
    ```

    Expected output:
    
    ```log
    Order Number is 9CYNLY and latest image is cr.sas.com/viya-4-x64_oci_linux_2-docker/sas-viya-cli:1.1.0-20240319.1710834807264
    ```

3. Use mirror manager to retrieve the logon credentials and logon to the docker registry.

    ```bash
    logincmd=$(mirrormgr list remote docker login --deployment-data /home/cloud-user/project/deploy/license/SASViyaV4_${GELLOW_ORDER}_certs.zip)
    echo $logincmd
    eval $logincmd
    ```

4. Get CLI image tags and pull the image.

    ```bash
    climage=$(mirrormgr list remote docker tags --deployment-data /home/cloud-user/project/deploy/license/SASViyaV4_${GELLOW_ORDER}_certs.zip --cadence ${GELLOW_CADENCE_NAME}-${GELLOW_CADENCE_VERSION} |  grep sas-viya-cli:${GELLOW_CADENCE_NAME}-${GELLOW_CADENCE_VERSION})
    echo ${climage}
    ```


5. Pull the image and tag it as sas-viya-cli:v1.


    ```bash
    docker pull ${climage}
    docker tag ${climage} sas-viya-cli:v1
    ```

5. Use `docker container run` to test the image. Initially lets just view the CLI help.

    ```bash
    docker container run -it sas-viya-cli:v1 --help
    ```


### Authenticate and run a command

1. To authenticate with userid and password set `VIYA_USER`, `VIYA_PASSWORD` and `SAS_SERVICES_ENDPOINT` environment variables. Use the docker run command to authenticate as **sasadm** and run `sas-viya identities whoami`.

    > NOTE: in this syntax you must use the export command to set the environment variables.

    ```bash
    export VIYA_USER=sasadm
    export VIYA_PASSWORD=lnxsas
    export SAS_SERVICES_ENDPOINT=https://${current_namespace}.$(hostname -f)
    docker run -it -e SAS_SERVICES_ENDPOINT -v /tmp:/security -e VIYA_USER -e VIYA_PASSWORD sas-viya-cli:v1 -k --output text identities whoami
    ```

    Expected output:
    
    ```log
    https://gelcorp.pdcesx02038.race.sas.com
    Login succeeded. Token saved.
    Id                  sasadm
    Name                SAS Administrator
    Title
    EmailAddresses      [map[value:sasadm@gelcorp.com]]
    PhoneNumbers
    Addresses           [map[country: locality:Cary postalCode: region:]]
    State               active
    ProviderId          ldap
    CreationTimeStamp
    ModifiedTimeStamp
    ```

1. Exec into the container and run your CLI processing there.
   
    ```bash
    docker run -it -e SAS_SERVICES_ENDPOINT -v /tmp:/security -e VIYA_USER -e VIYA_PASSWORD sas-viya-cli:v1 -k
    ```

2. Run commands inside the container.

    ```bash
    sas-viya -k --output text identities whoami
    sas-viya -k --output text reports list
    ```


## Use pre-built administration CLI images

You can build your own docker image based on the SAS provided sas-viya cli image. This allows you to add additional tools to the cli image. For the rest of class we will use an image built from the SAS provided Viya CLI image. The image has been pre-built and stored in the gelharbor docker registry.  The container images are automatically re-built weekly using a Jenkins process. The docker files and scripts are stored in gitlab [here](https://gitlab.sas.com/GEL/utilities/gel-sas-admin).

1. Pull the latest build of the sas-viya cli container and test by displaying the version number.

    ```bash
    docker pull gelharbor.race.sas.com/admin-toolkit/sas-viya-cli:latest
    docker tag gelharbor.race.sas.com/admin-toolkit/sas-viya-cli:latest sas-viya-cli:latest
    docker container run -it sas-viya-cli:latest ./sas-viya --version
    ```

    Expected output:
    
    ```log
     latest: Pulling from admin-toolkit/sas-viya-cli
     Digest: sha256:02650157e29f0950b62b9508c6b9e4bc105a7213f46c53bd2427d0c348ddab9b
     Status: Image is up to date for gelharbor.race.sas.com/admin-toolkit/sas-viya-cli:latest
     gelharbor.race.sas.com/admin-toolkit/sas-viya-cli:latest
      sas-viya version 1.22.3
     ```
3. There is a lot more typing to use the containerized CLI. In the class environment we have defined two functions that will allow us to run ad hoc commands and scripts more easily. Review the functions.

    ```sh
    cat ~/geladmin_common_functions.shinc | grep gel_sas_viya -A 24
    ```

    Expected output:

    ```log
    gel_sas_viya () {
    # if env var not set set it to Default
    SAS_CLI_PROFILE=${SAS_CLI_PROFILE:=Default}

    # run the sas-admin cli in a container
    docker container run -it \
    -v /tmp:/tmp \
    -v ${SSL_CERT_FILE}:/cli-home/.certs/`basename ${SSL_CERT_FILE}` \
    -v ~/.sas/config.json:/cli-home/.sas/config.json \
    -v ~/.sas/credentials.json:/cli-home/.sas/credentials.json \
    -e SSL_CERT_FILE=/cli-home/.certs/`basename ${SSL_CERT_FILE}` \
    -e REQUESTS_CA_BUNDLE=/cli-home/.certs/`basename ${SSL_CERT_FILE}` \
    -e SAS_CLI_PROFILE=$SAS_CLI_PROFILE gelharbor.race.sas.com/admin-toolkit/sas-viya-cli sas-viya $@
    }

    gel_sas_viya_batch () {

    if [ $# -eq 0 ]; then
    echo "ERROR: pass the function the full path to a script"
    return
    fi

    # if env var not set set it to Default
    SAS_CLI_PROFILE=${SAS_CLI_PROFILE:=Default}


    # run the sas-admin cli in a container
    docker container run -it  \
    -v /tmp:/tmp \
    -v /shared/gelcontent:/gelcontent \
    -v ${SSL_CERT_FILE}:/cli-home/.certs/`basename ${SSL_CERT_FILE}` \
    -v ~/.sas/config.json:/cli-home/.sas/config.json \
    -v ~/.sas/credentials.json:/cli-home/.sas/credentials.json \
    -e SSL_CERT_FILE=/cli-home/.certs/`basename ${SSL_CERT_FILE}` \
    -e REQUESTS_CA_BUNDLE=/cli-home/.certs/`basename ${SSL_CERT_FILE}` \
    -e SAS_CLI_PROFILE=$SAS_CLI_PROFILE gelharbor.race.sas.com/admin-toolkit/sas-viya-cli sh $@
    }
    ```

4. Here we can run the same cli command using the function gel_sas_viya. Now the command to use the containerized cli is basically the same as using the downloaded cli.

   ```sh
   gel_sas_viya --output text identities whoami
   ```

## Use Apache Airflow to orchestrate processing using the sas-viya CLI container
The flow will execute scripts that run series of sas-viya commands to perform a specific administration tasks The scripts are stored on an NFS server and will be mounted into the PODS in the flow.

The following scripts will be executed

   * Setup identities : 01-setup-identities.sh
   * Create a preliminary folder structure : 02-create-folders.sh
   * Apply an authorization schema to the folder structure: 03-setup-authorization
   * Create some caslibs for data access: 04-setup-caslibs.sh
   * Load Data: 05-setup-loaddata.sh
   * Apply CAS authorization: 06-setup-casauth.sh
   * Load content from Viya Packiges: 07-load-content.sh
   * Validate the success of the process: 08-validate.sh

### Copy the scripts and configuration files

2. Copy the SAS Viya CLI configuration and credential files to the project directory. The sas-viya cli uses a profile to store the connection information for the Viya environment, a credentials file to store the access token used to access the environment, and needs to be able to references the certificates for the Viya environment.  In this step these files will be copied to our project directory and then we will generate configMaps that include their content. Ultimately the configmaps will be mounted into the sas-viya CLI container so that it can access Viya.

    ```bash
    /opt/pyviyatools/loginviauthinfo.py
    mkdir -p ~/project/admincli/${current_namespace}
    cp -p ~/.sas/config.json -p ~/project/admincli/${current_namespace}/
    cp -p ~/.sas/credentials.json -p ~/project/admincli/${current_namespace}/
    cp -p ~/.certs/${current_namespace}_trustedcerts.pem -p ~/project/admincli/${current_namespace}/trustedcerts.pem

    tee ~/project/admincli/${current_namespace}/kustomization.yaml > /dev/null << EOF
    ---
    generatorOptions:
      disableNameSuffixHash: true
    configMapGenerator:
      - name: cli-config
        files:
        - config.json
      - name: cli-token
        files:
        - credentials.json
      - name: cert-file
        files:
        - trustedcerts.pem
    EOF

    cd ~/project/admincli/${current_namespace}
    kustomize build -o ~/project/admincli/${current_namespace}/configmaps.yaml
    kubectl -n airflow apply --server-side=true -f ~/project/admincli/${current_namespace}/configmaps.yaml
    ```

### Create the Python script that defines the flow

The workflow is created as a python script. In this step we will review the script and copy it to the airflow dags directory.

Notice the following in the flow definition:

* the dag item defines each task,the order of execution and dependencies for the tasks
* each task runs a script that is mounted into the POD from the NFS server
* the container image used is gelharbor.race.sas.com/admin-toolkit/sas-viya-cli:latest
* the credentials, certifcates and CLI profile are mounted into the POD from config maps.

1. Copy the python file that defines the flow to the airflow DAG directory and review the content.

    ```bash
    cp /home/cloud-user/PSGEL260-sas-viya-4.0.1-administration/files/dags/001-load-content.py  /shared/gelcontent/airflow/dags/001-load-content.py
    cat /shared/gelcontent/airflow/dags/001-load-content.py
    ```

## Run the flow and review the results

1. In a MobaXterm session on sasnode01, generate the Airflow URL and logon using `admin:admin`.

    ```sh
    gellow_urls | grep Airflow
    ```

2. In the DAG's tab notice we have a flow  `01-load-content-flow`. The flow has been loaded to Airflow because the software is configured to register flows from any python scripts copied to those directory. Open `01-load-content-flow`. Review the flow diagram.

3. Select `Graph`

4. Select the `Run` icon and select `Trigger DAG`. The flow should run and if it is succesful all the nodes should turn green.

    <!---
    ```bash
    echo "NOTE: run the flow, sleep to give airflow time to pickup the dag def"
    sleep 60
    kubectl exec $(kubectl -n airflow get pods | grep scheduler | awk '{print $1}') -n airflow -- airflow dags trigger 01-load-content-flow
    kubectl exec $(kubectl -n airflow get pods | grep scheduler | awk '{print $1}') -n airflow -- airflow dags unpause 01-load-content-flow
    ```
    --->
5. Click on `task-04-setup-caslibs` and then select `Logs` to view the log from the step.

6. We can also view the log of each task using kubectl.

    ```sh
    kubectl -n airflow logs -l task_id=task-04-setup-caslibs --tail 50
    ```

    Expected output:
    
    ```log
    <partial output>
    The requested caslib "hrdl" has been added successfully.

        Caslib Properties
        Name                hrdl
        Server              cas-shared-default
        Description         gelcontent hrdl
        Source Type         PATH
        Path                /gelcontent/gelcorp/hr/data/
        Scope               global

        Caslib Attributes
        active              true
        personal            false
        subDirs             false
        The requested caslib "Financial Data" has been added successfully.

        Caslib Properties
        Name                Financial Data
        Server              cas-shared-default
        Description         gelcontent finance
        Source Type         PATH
        Path                /gelcontent/gelcorp/finance/data/
        Scope               global

        Caslib Attributes
        active              true
        personal            false
        subDirs             false

    ```

7. If we look at the PODS in the airflow namespace we will see there is a POD with the status **Completed** for each node in the flow.

    ```sh
    kubectl get pods -n airflow | grep task
    ```
    
    Expected output:

    ```log
        task-01-setup-identities-ed8va44f      0/1     Completed   0          22m
        task-02-setup-folders-2jmd0504         0/1     Completed   0          22m
        task-03-setup-authorization-7262tzvh   0/1     Completed   0          22m
        task-04-setup-caslibs-krhgav20         0/1     Completed   0          22m
        task-05-setup-loaddata-7wp8rnjw        0/1     Completed   0          22m
        task-06-setup-casauth-37cs2f7n         0/1     Completed   0          21m
        task-07-load-content-rl3i11i4          0/1     Completed   0          21m
        task-08-validate-dgaurcjg              0/1     Completed   0          21m
    ```


2. View logs with kubectl.

    ```bash
     kubectl logs task-02-setup-folders-v6qhkxt2 -n airflow

    ```
    
    Expected output:

    ```log
    NOTE: Creating folder /gelcontent
    NOTE: Creating folder /gelcontent/GELCorp
    NOTE: Creating folder /gelcontent/GELCorp/Sales
    NOTE: Creating folder /gelcontent/GELCorp/Sales/Analyses
    NOTE: Creating folder /gelcontent/GELCorp/Sales/Reports
    NOTE: Creating folder /gelcontent/GELCorp/Sales/WorkinProgress
    NOTE: Creating folder /gelcontent/GELCorp/HR
    NOTE: Creating folder /gelcontent/GELCorp/HR/Analyses
    NOTE: Creating folder /gelcontent/GELCorp/HR/Reports
    NOTE: Creating folder /gelcontent/GELCorp/HR/WorkinProgress
    ```


## Validate

The validation is run in the last step of the flow.

1. View the Validation Report. In MobaXterm **sasnode1** sftp tab navigate to /shared/gelcontent/gelcorp_initenv/.
2. Select the html file that starts with **report-**, right-click, select **Open with** and open the report with **Google Chrome**.
3. Review the report to check what the folders for content were created, the caslib is running and new caslibs are available.

4. We could also use the CLI to validate for example, list folders

    ```sh
    gel_sas_viya --output text folders list-members --path /gelcontent --recursive --tree
    ```

    Expected output;

    ```log
    |—— gelcontent
        |  |—— GELCorp
        |  |  |—— Finance
        |  |  |  |—— Reports
        |  |  |  |  |—— RevenueTrend (report)
        |  |  |  |  |—— FinanceOverTime (report)
        |  |  |  |  |—— Profit Pie Chart (jobDefinition)
        |  |  |  |  |—— Profit Bar Chart (jobDefinition)
        |  |  |  |  |—— Map of Profit by State (jobDefinition)
        |  |  |  |  |—— LossMakingProductRank (report)
        |  |  |  |—— Data
        |  |  |  |  |—— FinanceLASRAppendTables1 (dataPlan)
        |  |  |  |  |—— Source Data
        |  |  |—— Shared
        |  |  |  |—— Reports
        |  |  |  |  |—— GELCORP Shared HR Summary Report (report)
        |  |  |—— HR
        |  |  |  |—— Code
        |  |  |  |  |—— HRAnalysysProject
        |  |  |  |  |  |—— 4_LoadDataInCAS.sas (file)
        |  |  |  |  |  |—— 2_CreateDataInSAS.sas (file)
        |  |  |  |  |  |—— 1_CreateFormatsInSAS.sas (file)
        |  |  |  |  |  |—— 3_LoadFormatsInSAS.sas (file)
        |  |  |  |—— Work in Progress
        |  |  |  |—— Data Plans
        |  |  |  |—— WorkinProgress
        |  |  |  |—— Reports
        |  |  |  |  |—— Employee measure histograms (report)
        |  |  |  |  |—— Employee Attrition Overview (report)
        |  |  |  |  |—— Employee attrition factors heatmap (report)
        |  |  |  |  |—— Employee attrition factors correlation (report)
        |  |  |  |—— Analyses
        |  |  |  |  |—— Cluster Analysis for employees who left (report)
        |  |  |  |  |—— EmployeeSurveyDecisionTree (report)
        |  |  |  |  |—— Regression Analysis of Employee Attrition (report)
        |  |  |—— Sales
        |  |  |  |—— Data Plans
        |  |  |  |—— Work in Progress
        |  |  |  |—— WorkinProgress
        |  |  |  |—— Reports
        |  |  |  |  |—— Sales Forecast (report)
        |  |  |  |  |—— Sales Correlation (report)
        |  |  |  |  |—— Sales Overview (report)
        |  |  |  |—— Analyses
        |  |  |  |  |—— TemperaturevSales (report)
        |  |  |  |  |—— Sales Regression Analysis (report)
    ```

1.  View validation report at /shared/gelcontent/gelcorp_initenv/report*.html