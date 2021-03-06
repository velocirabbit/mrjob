EMR runner options
==================

All options from :doc:`configs-all-runners` and :doc:`configs-hadoopy-runners`
are available to the emr runner.

Amazon credentials
------------------

See :ref:`amazon-setup` and :ref:`ssh-tunneling` for specific instructions
about setting these options.

.. mrjob-opt::
    :config: aws_access_key_id
    :type: :ref:`string <data-type-string>`
    :set: emr
    :default: ``None``

    "Username" for Amazon web services.

    There isn't a command-line switch for this option because credentials are
    supposed to be secret! Use the environment variable
    :envvar:`AWS_ACCESS_KEY_ID` instead.

.. mrjob-opt::
    :config: aws_secret_access_key
    :switch: --aws-secret-access-key
    :type: :ref:`string <data-type-string>`
    :set: emr
    :default: ``None``

    Your "password" on AWS.

    There isn't a command-line switch for this option because credentials are
    supposed to be secret! Use the environment variable
    :envvar:`AWS_SECRET_ACCESS_KEY` instead.

.. mrjob-opt::
    :config: aws_session_token
    :type: :ref:`string <data-type-string>`
    :set: emr
    :default: ``None``

    Temporary AWS session token, used along with :mrjob-opt:`aws_access_key_id`
    and :mrjob-opt:`aws_secret_access_key` when using temporary credentials.

    There isn't a command-line switch for this option because credentials are
    supposed to be secret! Use the environment variable
    :envvar:`AWS_SESSION_TOKEN` instead.

    .. versionchanged:: 0.5.10

       this used to be called *aws_security_token*.

.. mrjob-opt::
    :config: ec2_key_pair
    :switch: --ec2-key-pair
    :type: :ref:`string <data-type-string>`
    :set: emr
    :default: ``None``

    name of the SSH key you set up for EMR.

.. mrjob-opt::
    :config: ec2_key_pair_file
    :switch: --ec2-key-pair-file
    :type: :ref:`path <data-type-path>`
    :set: emr
    :default: ``None``

    path to file containing the SSH key for EMR

Cluster creation and configuration
-----------------------------------

.. mrjob-opt::
    :config: additional_emr_info
    :switch: --additional-emr-info
    :type: special
    :set: emr
    :default: ``None``

    Special parameters to select additional features, mostly to support beta
    EMR features. Pass a JSON string on the command line or use data
    structures in the config file (which is itself basically JSON).

.. mrjob-opt::
   :config: applications
   :switch: --application
   :type: :ref:`string list <data-type-string-list>`
   :set: emr
   :default: ``[]``

   Additional applications to run on 4.x AMIs (e.g. ``'Ganglia'``,
   ``'Mahout'``, ``'Spark'``).

   You do not need to specify ``'Hadoop'``; mrjob will always include it
   automatically. In most cases it'll auto-detect when to include ``'Spark'``
   as well.

   See `Applications <http://docs.aws.amazon.com/ElasticMapReduce/latest/ReleaseGuide/emr-release-components.html>`_ in the EMR docs for more details.

   .. versionadded:: 0.5.2

   .. versionchanged:: 0.5.9

      This used to be called *emr_applications*.

.. mrjob-opt::
    :config: extra_cluster_params
    :switch: --extra-cluster-param
    :type: :ref:`dict <data-type-plain-dict>`
    :set: emr
    :default: ``{}``

    Additional parameters to pass directly to the EMR API when creating a
    cluster. This allows old versions of `mrjob` to access new API features.
    See `the API documentation for RunJobFlow`_ for the full list of options.

    .. _`the API documentation for RunJobFlow`:
        http://docs.aws.amazon.com/ElasticMapReduce/latest/API/API_RunJobFlow.html

    Option names are strings, and values are data structures. On the command
    line, ``--extra-cluster-param name=value``:

    .. code-block:: sh

        --extra-cluster-param SupportedProducts='["mapr-m3"]'
        --extra-cluster-param AutoScalingRole=HankPym

    *value* can be either a JSON or a string (unless it starts with ``{``,
    ``[``, or ``"``, so that we don't convert malformed JSON to strings).
    Parameters can be suppressed by setting them to ``null``:

    .. code-block:: sh

        --extra-cluster-param LogUri=null

    This also works with Google dataproc:

    .. code-block:: sh

       --extra-cluster-param labels='{"name": "wrench"}'

    In the config file, `extra_cluster_param` is a dict:

    .. code-block:: yaml

        runners:
          emr:
            extra_cluster_params:
              AutoScalingRole: HankPym
              LogUri: null  # !clear works too
              SupportedProducts:
              - mapr-m3

    .. versionadded:: 0.6.0

       This replaces the old `emr_api_params` option, which only worked
       with :py:mod:`boto` 2.

.. mrjob-opt::
    :config: emr_configurations
    :switch: --emr-configuration
    :type: list of dicts
    :set: emr
    :default: ``[]``

    Configurations for 4.x AMIs. For example:

    .. code-block:: yaml

        runners:
          emr:
            emr_configurations:
            - Classification: core-site
              Properties:
                hadoop.security.groups.cache.secs: 250

    On the command line, configurations should be JSON-encoded:

    .. code-block:: sh

        --emr-configuration '{"Classification": "core-site", ...}

    See `Configuring Applications <http://docs.aws.amazon.com/ElasticMapReduce/latest/ReleaseGuide/emr-configure-apps.html>`_ in the EMR docs for more details.

    .. versionadded:: 0.5.3

.. mrjob-opt::
    :config: emr_endpoint
    :switch: --emr-endpoint
    :type: :ref:`string <data-type-string>`
    :set: emr
    :default: infer from :mrjob-opt:`region`

    Force mrjob to connect to EMR on this endpoint (e.g.
    ``us-west-1.elasticmapreduce.amazonaws.com``).

    Mostly exists as a workaround for network issues.

.. mrjob-opt::
    :config: hadoop_streaming_jar_on_emr
    :switch: --hadoop-streaming-jar-on-emr
    :type: :ref:`string <data-type-string>`
    :set: emr
    :default: AWS default

    .. deprecated:: 0.5.4

       Prepend ``file://`` and pass that to :mrjob-opt:`hadoop_streaming_jar`
       instead.

.. mrjob-opt::
    :config: iam_endpoint
    :switch: --iam-endpoint
    :type: :ref:`string <data-type-string>`
    :set: emr
    :default: (automatic)

    Force mrjob to connect to IAM on this endpoint (e.g.
    ``iam.us-gov.amazonaws.com``).

    Mostly exists as a workaround for network issues.

.. mrjob-opt::
    :config: iam_instance_profile
    :switch: --iam-instance-profile
    :type: :ref:`string <data-type-string>`
    :set: emr
    :default: (automatic)

    Name of an IAM instance profile to use for EC2 clusters created by EMR. See
    http://docs.aws.amazon.com/ElasticMapReduce/latest/DeveloperGuide/emr-iam-roles.html
    for more details on using IAM with EMR.

.. mrjob-opt::
    :config: iam_service_role
    :switch: --iam-service-role
    :type: :ref:`string <data-type-string>`
    :set: emr
    :default: (automatic)

    Name of an IAM role for the EMR service to use. See
    http://docs.aws.amazon.com/ElasticMapReduce/latest/DeveloperGuide/emr-iam-roles.html
    for more details on using IAM with EMR.

.. mrjob-opt::
    :config: image_version
    :switch: --image-version
    :type: :ref:`string <data-type-string>`
    :set: emr
    :default: ``'5.8.0'``

    EMR AMI (Amazon Machine Image) version to use. This controls which Hadoop
    version(s) are available and which version of Python is installed, among
    other things; see `the AWS docs on specifying the AMI version`_.  for
    details.

    .. _`the AWS docs on specifying the AMI version`:
        http://docs.amazonwebservices.com/ElasticMapReduce/latest/DeveloperGuide/EnvironmentConfig_AMIVersion.html

    This works for 4.x AMIs as well; mrjob will just prepend ``emr-`` and
    use that as the :mrjob-opt:`release_label`.

    .. versionchanged:: 0.5.4

       This used to be called *ami_version*.

    .. versionchanged:: 0.5.7

       Default used to be ``'3.11.0'``.

    .. warning::

       The deprecated *ami_version* alias for this option is completely
       ignored by mrjob 0.5.4 (it works in later 0.5.x versions).

    .. warning::

       The 2.x series of AMIs is deprecated by Amazon and not recommended.

    .. warning::

        The 1.x series of AMIs is no longer supported because they use Python
        2.5.

.. mrjob-opt::
    :config: instance_fleets
    :switch: --instance-fleet
    :set: emr
    :default: ``None``

    A list of instance fleet definitions to pass to the EMR API. Pass a JSON
    string on the command line or use data structures in the config file
    (which is itself basically JSON).

    *instance_fleets* overrides :mrjob-opt:`instance_groups` and other
    instance configuration options.

    .. code-block:: yaml

        runners:
          emr:
            instance_fleets:
            - InstanceFleetType: MASTER
              InstanceTypeConfigs:
              - InstanceType: m1.medium
              TargetOnDemandCapacity: 1
            - InstanceFleetType: CORE
              TargetSpotCapacity: 2
              TargetOnDemandCapacity: 2
              LaunchSpecifications:
                SpotSpecification:
                  TimeoutDurationMinutes: 20
                  TimeoutAction: SWITCH_TO_ON_DEMAND
              InstanceTypeConfigs:
              - InstanceType: m1.medium
                BidPriceAsPercentageOfOnDemandPrice: 50
                WeightedCapacity: 1
              - InstanceType: m1.large
                BidPriceAsPercentageOfOnDemandPrice: 50
                WeightedCapacity: 2

.. mrjob-opt::
    :config: instance_groups
    :switch: --instance-groups
    :set: emr
    :default: ``None``

    A list of instance group definitions to pass to the EMR API. Pass a JSON
    string on the command line or use data structures in the config file
    (which is itself basically JSON).

    This is the primary way to configure EBS volumes. For example:

    .. code-block:: yaml

        runners:
          emr:
            instance_groups:
            - InstanceRole: MASTER
              InstanceCount: 1
              InstanceType: m1.medium
            - InstanceRole: CORE
              InstanceCount: 10
              InstanceType: c1.xlarge
              EbsConfiguration:
                EbsOptimized: true
                EbsBlockDeviceConfigs:
                - VolumeSpecification:
                    SizeInGB: 100
                    VolumeType: gp2

.. mrjob-opt::
    :config: max_hours_idle
    :switch: --max-hours-idle
    :type: :ref:`string <data-type-string>`
    :set: emr
    :default: 0.5

    Automatically terminate persistent/pooled clusters that have been idle at
    least this many hours, if we're within :mrjob-opt:`mins_to_end_of_hour` of
    an EC2 billing hour.

    .. versionchanged:: 0.6.0

       All clusters launched by mrjob now auto-terminate when idle. In previous
       versions, you needed to set this option explicitly, or use
       :ref:`terminate-idle-clusters`.

.. mrjob-opt::
    :config: mins_to_end_of_hour
    :switch: --mins-to-end-of-hour
    :type: :ref:`string <data-type-string>`
    :set: emr
    :default: 5.0

    If :mrjob-opt:`max_hours_idle` is set, controls how close to the end of an
    EC2 billing hour the cluster can automatically terminate itself.

.. mrjob-opt::
    :config: region
    :switch: --region
    :type: :ref:`string <data-type-string>`
    :set: emr
    :default: ``'us-west-2'``

    region to run EMR jobs on (e.g.  ``us-west-1``). Also used by mrjob
    to create temporary buckets if you don't set :mrjob-opt:`cloud_tmp_dir`
    explicitly.

    .. versionchanged:: 0.5.4

       This option used to be named *aws_region*.

.. mrjob-opt::
    :config: release_label
    :switch: --release-label
    :type: :ref:`string <data-type-string>`
    :set: emr
    :default: ``None``

    EMR Release to use (e.g. ``emr-4.0.0``). This overrides
    :mrjob-opt:`image_version`.

    For more information about Release Labels, see
    `Differences Introduced in 4.x`_.

    .. _`Differences Introduced in 4.x`:
        http://docs.aws.amazon.com/ElasticMapReduce/latest/ReleaseGuide/emr-release-differences.html

    .. versionadded:: 0.5.0

.. mrjob-opt::
   :config: subnet
   :switch: --subnet
   :type: :ref:`string <data-type-string>`
   :set: emr
   :default: ``None``

   ID of Amazon VPC subnet to launch cluster in (e.g. ``'subnet-12345678'``).
   If this is not set, or an empty string, cluster will be launched in the
   normal AWS cloud.

   .. versionadded:: 0.5.3

.. mrjob-opt::
    :config: tags
    :switch: --tag
    :type: :ref:`dict <data-type-plain-dict>`
    :set: emr
    :default: ``{}``

    Metadata tags to apply to the EMR cluster after its
    creation. See `Tagging Amazon EMR Clusters`_ for more information
    on applying metadata tags to EMR clusters.

    .. _`Tagging Amazon EMR Clusters`:
        http://docs.aws.amazon.com/ElasticMapReduce/latest/DeveloperGuide/emr-plan-tags.html

    Tag names and values are strings. On the command line, to set a tag
    use ``--tag KEY=VALUE``:

    .. code-block:: sh

        --tag team=development

    In the config file, ``tags`` is a dict:

    .. code-block:: yaml

        runners:
          emr:
            tags:
              team: development
              project: mrjob

    .. versionchanged:: 0.5.4

       This option used to be named *emr_tags*

.. mrjob-opt::
    :config: visible_to_all_users
    :switch: --visible-to-all-users, --no-visible-to-all-users
    :type: boolean
    :set: emr
    :default: ``True``

    If true (the default) EMR clusters will be visible to all IAM users.
    Otherwise, the cluster will only be visible to the IAM user that created
    it.

    .. deprecated:: 0.6.0

       Hiding clusters from other users on the same account is not very useful.
       If you don't want to share pooled clusters, try :mrjob-opt:`pool_name`.

.. mrjob-opt::
    :config: zone
    :switch: zone
    :type: :ref:`string <data-type-string>`
    :set: emr
    :default: AWS default

    Availability zone to run the job in

    .. versionchanged:: 0.5.4

       This option used to be named *aws_availability_zone*

Bootstrapping
-------------

These options apply at *bootstrap time*, before the Hadoop cluster has
started. Bootstrap time is a good time to install Debian packages or compile
and install another Python binary.

.. mrjob-opt::
    :config: bootstrap
    :switch: --bootstrap
    :type: :ref:`string list <data-type-string-list>`
    :set: all
    :default: ``[]``

    A list of lines of shell script to run once on each node in your cluster,
    at bootstrap time.

    This option is complex and powerful; the best way to get started is to
    read the :doc:`emr-bootstrap-cookbook`.

    Passing expressions like ``path#name`` will cause
    *path* to be automatically uploaded to the task's working directory
    with the filename *name*, marked as executable, and interpolated into the
    script by their absolute path on the machine running the script.

    *path*
    may also be a URI, and ``~`` and environment variables within *path*
    will be resolved based on the local environment. *name* is optional.
    For details of parsing, see :py:func:`~mrjob.setup.parse_setup_cmd`.

    Unlike with :mrjob-opt:`setup`, archives are not supported (unpack them
    yourself).

    Remember to put ``sudo`` before commands requiring root privileges!

.. mrjob-opt::
    :config: bootstrap_actions
    :switch: --bootstrap-actions
    :type: :ref:`string list <data-type-string-list>`
    :set: emr
    :default: ``[]``

    A list of raw bootstrap actions (essentially scripts) to run prior to any
    of the other bootstrap steps. Any arguments should be separated from the
    command by spaces (we use :py:func:`shlex.split`). If the action is on the
    local filesystem, we'll automatically upload it to S3.

    This has little advantage over :mrjob-opt:`bootstrap`; it is included
    in order to give direct access to the EMR API.

.. mrjob-opt::
   :config: bootstrap_python
   :switch: --bootstrap-python, --no-bootstrap-python
   :type: boolean
   :set: emr
   :default: (automatic)

   Attempt to install a compatible (major) version of Python at bootstrap time,
   including header files and :command:`pip` (see :ref:`using-pip`).

   In Python 2, this never does anything.

   In Python 3, this runs
   :command:`sudo yum install -y python34 python34-devel python34-pip`
   by default on AMIs prior to 4.6.0 (starting with AMI 4.6.0, Python 3 is
   pre-installed).

   .. versionadded:: 0.5.0

   .. versionchanged:: 0.5.4

      no longer installs Python 3 on AMI version 4.6.0+ by default

.. mrjob-opt::
   :config: bootstrap_spark
   :switch: --bootstrap-spark, --no-bootstrap-spark
   :type: boolean
   :set: emr
   :default: (automatic)

   Install Spark on the cluster. This works on AMI version 3.x and later.

   By default, we automatically install Spark only if our job has Spark steps.

   .. versionadded:: 0.5.7

   In case you're curious, here's how mrjob determines you're using Spark:

   * any :py:class:`~mrjob.step.SparkStep` or
     :py:class:`~mrjob.step.SparkScriptStep` in your job's steps (including
     implicitly through the :py:class:`~mrjob.job.MRJob.spark` method)
   * "Spark" included in :mrjob-opt:`applications` option
   * any bootstrap action (see :mrjob-opt:`bootstrap_actions`) ending in
     ``/spark-install`` (this is how you install Spark on 3.x AMIs)


Monitoring the cluster
-----------------------

.. mrjob-opt::
    :config: check_cluster_every
    :switch: --check-cluster-every
    :type: :ref:`string <data-type-string>`
    :set: emr
    :default: 30

    How often to check on the status of EMR jobs in seconds. If you set this
    too low, AWS will throttle you.

    .. versionchanged:: 0.5.4

       This used to be called *check_emr_status_every*

.. mrjob-opt::
    :config: enable_emr_debugging
    :switch: --enable-emr-debugging
    :type: boolean
    :set: emr
    :default: ``False``

    store Hadoop logs in SimpleDB

Number and type of instances
----------------------------

.. mrjob-opt::
    :config: instance_type
    :switch: --instance-type
    :type: :ref:`string <data-type-string>`
    :set: emr
    :default: (automatic)

    By default, mrjob picks the cheapest instance type that will work at all.
    This is usually ``m1.medium``, with two exceptions:

    * ``m1.large`` if you're running Spark (see :mrjob-opt:`bootstrap_spark`)
    * ``m1.small`` if you're running on the (deprecated) 2.x AMIs

    Once you've tested a job and want to run it at scale, it's usually a good
    idea to use instances larger than the default; see
    http://aws.amazon.com/ec2/instance-types/ for options.

    If you're running multiple nodes (see :mrjob-opt:`num_core_instances`),
    this option *doesn't* apply to the master node because it's just
    coordinating tasks, not running them. Use :mrjob-opt:`master_instance_type`
    instead.

    .. versionchanged:: 0.5.6

       Used to default to ``m1.medium`` in all cases.

    .. versionchanged:: 0.5.4

       This option used to be named *ec2_instance_type*.

.. mrjob-opt::
    :config: core_instance_type
    :switch: --core-instance-type
    :type: :ref:`string <data-type-string>`
    :set: emr
    :default: value of :mrjob-opt:`instance_type`

    like :mrjob-opt:`instance_type`, but only for the core Hadoop nodes; these
    nodes run tasks and host HDFS. Usually you just want to use
    :mrjob-opt:`instance_type`.

    .. versionchanged:: 0.5.4

       This replaces the ``ec2_core_instance_type`` and
       ``ec2_slave_instance_type`` options.

.. mrjob-opt::
    :config: core_instance_bid_price
    :switch: --core-instance-bid-price
    :type: :ref:`string <data-type-string>`
    :set: emr
    :default: ``None``

    When specified and not "0", this creates the core Hadoop nodes as spot
    instances at this bid price.  You usually only want to set bid price for
    task instances.

    .. versionchanged:: 0.5.4

       This option used to be named *ec2_core_instance_bid_price*.

.. mrjob-opt::
    :config: master_instance_type
    :switch: --master-instance-type
    :type: :ref:`string <data-type-string>`
    :set: emr
    :default: (automatic)

    like :mrjob-opt:`instance_type`, but only for the master Hadoop node.
    This node hosts the task tracker/resource manager and HDFS, and runs tasks
    if there are no other nodes.

    If you're running a single node (no :mrjob-opt:`num_core_instances` or
    :mrjob-opt:`num_task_instances`), this will default to the value of
    :mrjob-opt:`instance_type`.

    Otherwise, defaults to ``m1.medium`` (exception: ``m1.small`` on the
    deprecated 2.x AMIs), which is usually adequate for all but the largest
    jobs.

    .. versionchanged:: 0.5.4

       This option used to be named *ec2_master_instance_type*.

.. mrjob-opt::
    :config: master_instance_bid_price
    :switch: --master-instance-bid-price
    :type: :ref:`string <data-type-string>`
    :set: emr
    :default: ``None``

    When specified and not "0", this creates the master Hadoop node as a spot
    instance at this bid price. You usually only want to set bid price for
    task instances unless the master instance is your only instance.

    .. versionchanged:: 0.5.4

       This option used to be named *ec2_master_instance_bid_price*.

.. mrjob-opt::
    :config: task_instance_type
    :switch: --task-instance-type
    :type: :ref:`string <data-type-string>`
    :set: emr
    :default: value of :mrjob-opt:`core_instance_type`

    like :mrjob-opt:`instance_type`, but only for the task Hadoop nodes;
    these nodes run tasks but do not host HDFS. Usually you just want to use
    :mrjob-opt:`instance_type`.

    .. versionchanged:: 0.5.4

       This option used to be named *ec2_task_instance_type*.

.. mrjob-opt::
    :config: task_instance_bid_price
    :switch: --task-instance-bid-price
    :type: :ref:`string <data-type-string>`
    :set: emr
    :default: ``None``

    When specified and not "0", this creates the master Hadoop node as a spot
    instance at this bid price.  (You usually only want to set bid price for
    task instances.)

    .. versionchanged:: 0.5.4

       This option used to be named *ec2_task_instance_bid_price*.

.. mrjob-opt::
    :config: num_core_instances
    :switch: --num-core-instances
    :type: :ref:`string <data-type-string>`
    :set: emr
    :default: 0

    Number of core instances to start up. These run your job and
    host HDFS. This is in addition to the single master instance.

    .. versionchanged:: 0.5.4

       This option used to be named *num_ec2_core_instances*.

.. mrjob-opt::
    :config: num_task_instances
    :switch: --num-task-instances
    :type: :ref:`string <data-type-string>`
    :set: emr
    :default: 0

    Number of task instances to start up.  These run your job but do not host
    HDFS. If you use this,
    you must set :mrjob-opt:`num_core_instances`; EMR does not allow you to
    run task instances without core instances (because there's nowhere to host
    HDFS).

    .. versionchanged:: 0.5.4

       This used to be called *num_ec2_task_instances*.

Choosing/creating a cluster to join
------------------------------------

.. mrjob-opt::
    :config: cluster_id
    :switch: --cluster-id
    :type: :ref:`string <data-type-string>`
    :set: emr
    :default: automatically create a cluster and use it

    The ID of a persistent EMR cluster to run jobs in.  It's fine for other
    jobs to be using the cluster; we give our job's steps a unique ID.

.. mrjob-opt::
    :config: emr_action_on_failure
    :switch: --emr-action-on-failure
    :type: :ref:`string <data-type-string>`
    :set: emr
    :default: (automatic)

    What happens if step of your job fails

    * ``'CANCEL_AND_WAIT'`` cancels all steps on the cluster
    * ``'CONTINUE'`` continues to the next step (useful when submitting several
        jobs to the same cluster)
    * ``'TERMINATE_CLUSTER'`` shuts down the cluster entirely

    The default is ``'CANCEL_AND_WAIT'`` when using pooling (see
    :mrjob-opt:`pool_clusters`) or an existing cluster (see
    :mrjob-opt:`cluster_id`), and ``'TERMINATE_CLUSTER'`` otherwise.

.. mrjob-opt::
    :config: pool_name
    :switch: --pool-name
    :type: :ref:`string <data-type-string>`
    :set: emr
    :default: ``'default'``

    Specify a pool name to join. Does not imply :mrjob-opt:`pool_clusters`.

.. mrjob-opt::
    :config: pool_clusters
    :switch: --pool-clusters
    :type: :ref:`string <data-type-string>`
    :set: emr
    :default: ``True``

    Try to run the job on a ``WAITING`` pooled cluster with the same
    bootstrap configuration. Prefer the one with the most compute units. Use
    S3 to "lock" the cluster and ensure that the job is not scheduled behind
    another job. If no suitable cluster is `WAITING`, create a new pooled
    cluster.

    .. versionchanged:: 0.6.0

       This used to be turned off by default. If you want to enable this
       option in older versions of mrjob, make sure to set
       :mrjob-opt:`max_hours_idle` too, or your clusters will run
       (costing you money) forever.

    .. versionchanged:: 0.5.4

       Pooling now gracefully recovers from joining a cluster that was
       in the process of shutting down (see :mrjob-opt:`max_hours_idle`).

.. mrjob-opt::
    :config: pool_wait_minutes
    :switch: --pool-wait-minutes
    :type: :ref:`string <data-type-string>`
    :set: emr
    :default: 0

    If pooling is enabled and no cluster is available, retry finding a cluster
    every 30 seconds until this many minutes have passed, then start a new
    cluster instead of joining one.


S3 paths and options
--------------------
MRJob uses boto3 to manipulate/access S3.

.. mrjob-opt::
    :config: cloud_log_dir
    :switch: --cloud-log-dir
    :type: :ref:`string <data-type-string>`
    :set: emr
    :default: append ``logs`` to :mrjob-opt:`cloud_tmp_dir`

    Where on S3 to put logs, for example ``s3://yourbucket/logs/``. Logs for
    your cluster will go into a subdirectory, e.g.
    ``s3://yourbucket/logs/j-CLUSTERID/``.

    .. versionchanged:: 0.5.4

       This option used to be named *s3_log_uri*

.. mrjob-opt::
    :config: cloud_tmp_dir
    :switch: --cloud-tmp-dir
    :type: :ref:`string <data-type-string>`
    :set: emr
    :default: (automatic)

    S3 directory (URI ending in ``/``) to use as temp space, e.g.
    ``s3://yourbucket/tmp/``.

    By default, mrjob looks for a bucket belong to you whose name starts with
    ``mrjob-`` and which matches :mrjob-opt:`region`. If it can't find
    one, it creates one with a random name. This option is then set to `tmp/`
    in this bucket (e.g. ``s3://mrjob-01234567890abcdef/tmp/``).

    .. versionchanged:: 0.5.4

       This used to be called *s3_tmp_dir*.

    .. versionchanged:: 0.5.0

       This used to be called *s3_scratch_uri*.

.. mrjob-opt::
    :config: cloud_fs_sync_secs
    :switch: --cloud_fs_sync_secs
    :type: :ref:`string <data-type-string>`
    :set: emr
    :default: 5.0

    How long to wait for S3 to reach eventual consistency. This is typically
    less than a second (zero in U.S. West), but the default is 5.0 to be safe.

    .. versionchanged:: 0.5.4

       This used to be called *s3_sync_wait_time*

.. mrjob-opt::
   :config: cloud_upload_part_size
   :switch: --cloud-upload-part-size
   :type: integer
   :set: emr
   :default: 100

   Upload files to S3 in parts no bigger than this many megabytes
   (technically, `mebibytes`_). Default is 100 MiB, as
   `recommended by Amazon`_. Set to 0 to disable multipart uploading
   entirely.

   Currently, Amazon `requires parts to be between 5 MiB and 5 GiB`_.
   mrjob does not enforce these limits.

   .. _`mebibytes`:
       http://en.wikipedia.org/wiki/Mebibyte
   .. _`recommended by Amazon`:
       http://docs.aws.amazon.com/AmazonS3/latest/dev/UploadingObjects.html
   .. _`requires parts to be between 5 MiB and 5 GiB`:
       http://docs.aws.amazon.com/AmazonS3/latest/dev/qfacts.html

   .. versionchanged:: 0.5.4

      This used to be called *s3_upload_part_size*.

.. mrjob-opt::
    :config: s3_endpoint
    :switch: --s3-endpoint
    :type: :ref:`string <data-type-string>`
    :set: emr
    :default: (automatic)

    Force mrjob to connect to S3 on this endpoint, rather than letting it
    choose the appropriate endpoint for each S3 bucket.

    Mostly exists as a workaround for network issues.

    .. warning:: If you set this to a region-specific endpoint
                 (e.g. ``'s3-us-west-1.amazonaws.com'``) mrjob will not
                 be able to access buckets located in other regions.


SSH access and tunneling
------------------------

.. mrjob-opt::
    :config: ssh_bin
    :switch: --ssh-bin
    :type: :ref:`command <data-type-command>`
    :set: emr
    :default: ``'ssh'``

    Path to the ssh binary; may include switches (e.g.  ``'ssh -v'`` or
    ``['ssh', '-v']``). Defaults to :command:`ssh`

.. mrjob-opt::
    :config: ssh_bind_ports
    :switch: --ssh-bind-ports
    :type: special
    :set: emr
    :default: ``range(40001, 40841)``

    A list of ports that are safe to listen on. The command line syntax looks
    like ``2000[:2001][,2003,2005:2008,etc]``, where commas separate ranges and
    colons separate range endpoints.

.. mrjob-opt::
    :config: ssh_tunnel
    :switch: --ssh-tunnel, --no-ssh-tunnel
    :type: boolean
    :set: emr
    :default: ``False``

    If True, create an ssh tunnel to the job tracker/resource manager and
    listen on a randomly chosen port. This requires you to set
    :mrjob-opt:`ec2_key_pair` and :mrjob-opt:`ec2_key_pair_file`. See
    :ref:`ssh-tunneling` for detailed instructions.

    .. versionchanged:: 0.5.0

       This option used to be named *ssh_tunnel_to_job_tracker*.

.. mrjob-opt::
    :config: ssh_tunnel_is_open
    :switch: --ssh-tunnel-is-open
    :type: boolean
    :set: emr
    :default: ``False``

    if True, any host can connect to the job tracker through the SSH tunnel
    you open.  Mostly useful if your browser is running on a different machine
    from your job runner.
