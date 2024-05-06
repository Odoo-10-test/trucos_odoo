```
Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit

  Common options:
    -c CONFIG, --config=CONFIG
                        specify alternate config file
    -s, --save          save configuration to ~/.openerp_serverrc
    -i INIT, --init=INIT
                        install one or more modules (comma-separated list, use
                        "all" for all modules), requires -d
    -u UPDATE, --update=UPDATE
                        update one or more modules (comma-separated list, use
                        "all" for all modules). Requires -d.
    --without-demo=WITHOUT_DEMO
                        disable loading demo data for modules to be installed
                        (comma-separated, use "all" for all modules). Requires
                        -d and -i. Default is none
    -P IMPORT_PARTIAL, --import-partial=IMPORT_PARTIAL
                        Use this for big data importation, if it crashes you
                        will be able to continue at the current state. Provide
                        a filename to store intermediate importation states.
    --pidfile=PIDFILE   file where the server pid will be stored
    --addons-path=ADDONS_PATH
                        specify additional addons paths (separated by commas).
    --load=SERVER_WIDE_MODULES
                        Comma-separated list of server-wide modules.
    -D DATA_DIR, --data-dir=DATA_DIR
                        Directory where to store Odoo data

  XML-RPC Configuration:
    --xmlrpc-interface=XMLRPC_INTERFACE
                        Specify the TCP IP address for the XML-RPC protocol.
                        The empty string binds to all interfaces.
    --xmlrpc-port=XMLRPC_PORT
                        specify the TCP port for the XML-RPC protocol
    --no-xmlrpc         disable the XML-RPC protocol
    --proxy-mode        Enable correct behavior when behind a reverse proxy
    --longpolling-port=LONGPOLLING_PORT
                        specify the TCP port for longpolling requests

  Web interface Configuration:
    --db-filter=REGEXP  Filter listed database

  Testing Configuration:
    --test-file=TEST_FILE
                        Launch a python or YML test file.
    --test-report-directory=TEST_REPORT_DIRECTORY
                        If set, will save sample of all reports in this
                        directory.
    --test-enable       Enable YAML and unit tests.
    --test-commit       Commit database changes performed by YAML or XML
                        tests.

  Logging Configuration:
    --logfile=LOGFILE   file where the server log will be stored
    --logrotate         enable logfile rotation
    --syslog            Send the log to the syslog server
    --log-handler=PREFIX:LEVEL
                        setup a handler at LEVEL for a given PREFIX. An empty
                        PREFIX indicates the root logger. This option can be
                        repeated. Example: "openerp.orm:DEBUG" or
                        "werkzeug:CRITICAL" (default: ":INFO")
    --log-request       shortcut for --log-
                        handler=openerp.http.rpc.request:DEBUG
    --log-response      shortcut for --log-
                        handler=openerp.http.rpc.response:DEBUG
    --log-web           shortcut for --log-handler=openerp.http:DEBUG
    --log-sql           shortcut for --log-handler=openerp.sql_db:DEBUG
    --log-db=LOG_DB     Logging database
    --log-db-level=LOG_DB_LEVEL
                        Logging database level
    --log-level=LOG_LEVEL
                        specify the level of the logging. Accepted values:
                        ['info', 'debug_rpc', 'warn', 'test', 'critical',
                        'debug_sql', 'error', 'debug', 'debug_rpc_answer',
                        'notset'].

  SMTP Configuration:
    --email-from=EMAIL_FROM
                        specify the SMTP email address for sending email
    --smtp=SMTP_SERVER  specify the SMTP server for sending email
    --smtp-port=SMTP_PORT
                        specify the SMTP port
    --smtp-ssl          if passed, SMTP connections will be encrypted with SSL
                        (STARTTLS)
    --smtp-user=SMTP_USER
                        specify the SMTP username for sending email
    --smtp-password=SMTP_PASSWORD
                        specify the SMTP password for sending email

  Database related options:
    -d DB_NAME, --database=DB_NAME
                        specify the database name
    -r DB_USER, --db_user=DB_USER
                        specify the database user name
    -w DB_PASSWORD, --db_password=DB_PASSWORD
                        specify the database password
    --pg_path=PG_PATH   specify the pg executable path
    --db_host=DB_HOST   specify the database host
    --db_port=DB_PORT   specify the database port
    --db_maxconn=DB_MAXCONN
                        specify the the maximum number of physical connections
                        to posgresql
    --db-template=DB_TEMPLATE
                        specify a custom database template to create a new
                        database

  Internationalisation options:
    Use these options to translate Odoo to another language.See i18n
    section of the user manual. Option '-d' is mandatory.Option '-l' is
    mandatory in case of importation

    --load-language=LOAD_LANGUAGE
                        specifies the languages for the translations you want
                        to be loaded
    -l LANGUAGE, --language=LANGUAGE
                        specify the language of the translation file. Use it
                        with --i18n-export or --i18n-import
    --i18n-export=TRANSLATE_OUT
                        export all sentences to be translated to a CSV file, a
                        PO file or a TGZ archive and exit
    --i18n-import=TRANSLATE_IN
                        import a CSV or a PO file with translations and exit.
                        The '-l' option is required.
    --i18n-overwrite    overwrites existing translation terms on updating a
                        module or importing a CSV or a PO file.
    --modules=TRANSLATE_MODULES
                        specify modules to export. Use in combination with
                        --i18n-export

  Security-related options:
    --no-database-list  disable the ability to return the list of databases

  Advanced options:
    --dev               enable developper mode
    --debug             enable debug mode
    --stop-after-init   stop the server after its initialization
    --osv-memory-count-limit=OSV_MEMORY_COUNT_LIMIT
                        Force a limit on the maximum number of records kept in
                        the virtual osv_memory tables. The default is False,
                        which means no count-based limit.
    --osv-memory-age-limit=OSV_MEMORY_AGE_LIMIT
                        Force a limit on the maximum age of records kept in
                        the virtual osv_memory tables. This is a decimal value
                        expressed in hours, and the default is 1 hour.
    --max-cron-threads=MAX_CRON_THREADS
                        Maximum number of threads processing concurrently cron
                        jobs (default 2).
    --unaccent          Use the unaccent function provided by the database
                        when available.
    --geoip-db=GEOIP_DATABASE
                        Absolute path to the GeoIP database file.

  Multiprocessing options:
    --workers=WORKERS   Specify the number of workers, 0 disable prefork mode.
    --limit-memory-soft=LIMIT_MEMORY_SOFT
                        Maximum allowed virtual memory per worker, when
                        reached the worker be reset after the current request
                        (default 671088640 aka 640MB).
    --limit-memory-hard=LIMIT_MEMORY_HARD
                        Maximum allowed virtual memory per worker, when
                        reached, any memory allocation will fail (default
                        805306368 aka 768MB).
    --limit-time-cpu=LIMIT_TIME_CPU
                        Maximum allowed CPU time per request (default 60).
    --limit-time-real=LIMIT_TIME_REAL
                        Maximum allowed Real time per request (default 120).
    --limit-request=LIMIT_REQUEST
                        Maximum number of request to be processed per worker
                        (default 8192).
```
