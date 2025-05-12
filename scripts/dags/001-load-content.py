# import packages
from datetime import datetime, timedelta
from airflow import DAG
from kubernetes.client import models as k8s
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator

# setup volumes mounts to cli configuration files and NFS server
volume_mounts_var = [
            k8s.V1VolumeMount(mount_path="/cli-home/.sas/config.json", name="cli-config", sub_path="config.json", read_only=True),
            k8s.V1VolumeMount(mount_path="/cli-home/.sas/credentials.json", name="cli-token", sub_path="credentials.json", read_only=True),
            k8s.V1VolumeMount(mount_path="/cli-home/.certs/trustedcerts.pem", name="cert-file", sub_path="trustedcerts.pem", read_only=True),
            k8s.V1VolumeMount(mount_path="/gelcontent", name="sas-viya-mycode-volume")
            ]

# setup volumes to provide information to container
volumes_var = [
            k8s.V1Volume(name="cli-config", config_map=k8s.V1ConfigMapVolumeSource(name="cli-config")),
            k8s.V1Volume(name="cli-token", config_map=k8s.V1ConfigMapVolumeSource(name="cli-token")),
            k8s.V1Volume(name="cert-file", config_map=k8s.V1ConfigMapVolumeSource(name="cert-file")),
            k8s.V1Volume(name="sas-viya-mycode-volume", nfs=k8s.V1NFSVolumeSource(path="/shared/gelcontent",server="sasnode01"))
            ]

#setup environment variables for container
environment_variables={
        "SAS_CLI_PROFILE" : "gelcorp",
        "SSL_CERT_FILE" : "/cli-home/.certs/trustedcerts.pem",
        "REQUESTS_CA_BUNDLE" : "/cli-home/.certs/trustedcerts.pem"
        }

# create DAG
dag = DAG(
    "01-load-content-flow",
    schedule_interval=None,
    catchup=False,
    default_args={
        "owner": "admin",
        "depends_on_past": False,
        "start_date": datetime(2020, 8, 7),
        "email_on_failure": False,
        "email_on_retry": False,
        "retries": 0,
        "retry_delay": timedelta(seconds=30),
        "sla": timedelta(hours=23),
    },
)

with dag:
    

    task_1 = KubernetesPodOperator(
        image="gelharbor.race.sas.com/admin-toolkit/sas-viya-cli:latest",
        namespace="airflow",
        cmds=["bash", "-cx"],
        arguments=["/gelcontent/gelcorp_initenv/scripts/01-setup-identities.sh "],
        labels={"app": "sas-viya-cli"},
        name="task-01-setup-identities",
        task_id="task-01-setup-identities",
        volumes=volumes_var,
        volume_mounts=volume_mounts_var,
        env_vars=environment_variables,          
        is_delete_operator_pod=False,
        in_cluster=True,
    )
    task_2 = KubernetesPodOperator(
        image="gelharbor.race.sas.com/admin-toolkit/sas-viya-cli:latest",
        namespace="airflow",
        cmds=["bash", "-cx"],
        arguments=["/gelcontent/gelcorp_initenv/scripts/02-setup-folders.sh "],
        labels={"app": "sas-viya-cli"},
        name="task-02-setup-folders",
        task_id="task-02-setup-folders",
        volumes=volumes_var,
        volume_mounts=volume_mounts_var,
        env_vars=environment_variables,          
        is_delete_operator_pod=False,
        in_cluster=True,
    )
    task_3 = KubernetesPodOperator(
        image="gelharbor.race.sas.com/admin-toolkit/sas-viya-cli:latest",
        namespace="airflow",
        cmds=["bash", "-cx"],
        arguments=["/gelcontent/gelcorp_initenv/scripts/03-setup-authorization.sh "],
        labels={"app": "sas-viya-cli"},
        name="task-03-setup-authorization",
        task_id="task-03-setup-authorization",
        volumes=volumes_var,
        volume_mounts=volume_mounts_var,
        env_vars=environment_variables,          
        is_delete_operator_pod=False,
        in_cluster=True,
    )
    task_4 = KubernetesPodOperator(
        image="gelharbor.race.sas.com/admin-toolkit/sas-viya-cli:latest",
        namespace="airflow",
        cmds=["bash", "-cx"],
        arguments=["/gelcontent/gelcorp_initenv/scripts/04-setup-caslibs.sh "],
        labels={"app": "sas-viya-cli"},
        name="task-04-setup-caslibs",
        task_id="task-04-setup-caslibs",
        volumes=volumes_var,
        volume_mounts=volume_mounts_var,
        env_vars=environment_variables,          
        is_delete_operator_pod=False,
        in_cluster=True,
    )
    task_5 = KubernetesPodOperator(
        image="gelharbor.race.sas.com/admin-toolkit/sas-viya-cli:latest",
        namespace="airflow",
        cmds=["bash", "-cx"],
        arguments=["/gelcontent/gelcorp_initenv/scripts/05-setup-loaddata.sh "],
        labels={"app": "sas-viya-cli"},
        name="task-05-setup-loaddata",
        task_id="task-05-setup-loaddata",
        volumes=volumes_var,
        volume_mounts=volume_mounts_var,
        env_vars=environment_variables,          
        is_delete_operator_pod=False,
        in_cluster=True,
    )
    task_6 = KubernetesPodOperator(
        image="gelharbor.race.sas.com/admin-toolkit/sas-viya-cli:latest",
        namespace="airflow",
        cmds=["bash", "-cx"],
        arguments=["/gelcontent/gelcorp_initenv/scripts/06-setup-casauth.sh "],
        labels={"app": "sas-viya-cli"},
        name="task-06-setup-casauth",
        task_id="task-06-setup-casauth",
        volumes=volumes_var,
        volume_mounts=volume_mounts_var,
        env_vars=environment_variables,          
        is_delete_operator_pod=False,
        in_cluster=True,
    )
    task_7 = KubernetesPodOperator(
        image="gelharbor.race.sas.com/admin-toolkit/sas-viya-cli:latest",
        namespace="airflow",
        cmds=["bash", "-cx"],
        arguments=["/gelcontent/gelcorp_initenv/scripts/07-load-content.sh "],
        labels={"app": "sas-viya-cli"},
        name="task-07-load-content",
        task_id="task-07-load-content",
        volumes=volumes_var,
        volume_mounts=volume_mounts_var,
        env_vars=environment_variables,          
        is_delete_operator_pod=False,
        in_cluster=True,
    )
    task_8 = KubernetesPodOperator(
        image="gelharbor.race.sas.com/admin-toolkit/sas-viya-cli:latest",
        namespace="airflow",
        cmds=["bash", "-cx"],
        arguments=["/gelcontent/gelcorp_initenv/scripts/08-validate.sh "],
        labels={"app": "sas-viya-cli"},
        name="task-08-validate",
        task_id="task-08-validate",
        volumes=volumes_var,
        volume_mounts=volume_mounts_var,
        env_vars=environment_variables,          
        is_delete_operator_pod=False,
        in_cluster=True,
    )

# setup dependencies 
task_1 >> task_2
task_1 >> task_4
task_4 >> task_5
task_5 >> task_6
task_2 >> task_3
task_3 >> task_7
task_6 >> task_7
task_7 >> task_8

