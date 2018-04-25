# #!/usr/bin/env python
# # -*- coding: utf-8 -*-

# import os
# import time

# from fabric.api import cd, run, local, sudo, env, hosts


# env.hosts = ["matt@api.ubskin.net:48022"]

# project_name = "ubskin"
# db_name = "ubs_db"

# base_dir = os.path.dirname(os.path.abspath(__file__))
# webwork_dir = os.path.join(base_dir, "")
# webwork_backup_dir = os.path.join("/Users/matt/Projects/backup/", project_name, "webWork", "")
# websecret_dir = os.path.join(base_dir, "secrets", "")
# site_dir = os.path.join(base_dir, "site", "webWork", "")
# static_dir = os.path.join(base_dir, "static", "")

# curr_time = time.strftime("%y%m%d")
# local_backup_path = "".join(["~/Projects/backup/", project_name, "/"])
# remote_backup_path = "".join(["/data/", project_name, "/backup/"])
# remote_db_backup_filename = "".join([remote_backup_path, "mysql_backup_", curr_time, ".gz"])

# rsync_excludes_common = "--exclude=.settings "\
#     "--exclude=.project --exclude=.buildpath --exclude=.DS_Store --exclude=.idea/ "\
#     "--exclude=/scripts/ --exclude=/static/index_data/ --exclude=/static/pics/ "\
#     "--exclude=/webWork/logs/ --exclude=/config_local.pyc --exclude=*.md --exclude=/ENV/ "\
#     "--exclude=/fabfile.pyc --exclude=/dockers/ --exclude=/static/ --exclude=/ENV/ "\
#     "--exclude=config_local.pyc --exclude=/conf/supervisor.conf --exclude=/static/photos/ "\
#     "--exclude=/static/files/ --exclude=/static/apk/ --exclude=.git --exclude=.gitignore "
# rsync_excludes = rsync_excludes_common + " --exclude=*.py "
# rsync_excludes_source = rsync_excludes_common + " --exclude=*.pyc "
# rsync_excludes_static = "--exclude=.DS_Store --exclude=/photos/ --exclude=/files/ "\
#     "--exclude=/apk/"

# cmd_rsync_static = "sh ~/Projects/"+project_name+"/scripts/rsync_static.sh"
# cmd_rsync_webwork = "sh ~/Projects/"+project_name+"/scripts/rsync_webwork.sh"
# cmd_rsync_webwork_test = "sh ~/Projects/"+project_name+"/scripts/rsync_webwork_test.sh"


# def rsync_static():
#     local("rsync -azv --dry-run --progress --delete -e \"ssh -p 48022\" " +\
#         rsync_excludes_static + " " + static_dir + \
#         " matt@api.ubskin.net:/data/ubskin/static/"
#     )

# def rsync_static_run():
#     local("rsync -azv --progress --delete -e \"ssh -p 48022\" " +\
#         rsync_excludes_static + " " + static_dir + \
#         " matt@api.ubskin.net:/data/ubskin/static/"
#     )


# def rsync_webwork():
#     local("python -m compileall "+webwork_dir)
#     local("rsync -avz --dry-run --progress --delete -e \"ssh -p 48022\" " + \
#         rsync_excludes + " " + webwork_dir + \
#         " matt@api.ubskin.net:/data/ubskin/webWork/"
#     )
#     # local(cmd_rsync_webwork)

# def rsync_webwork_run():
#     local("python -m compileall "+webwork_dir)
#     local("rsync -avz --progress --delete -e \"ssh -p 48022\" " + \
#         rsync_excludes + " " + webwork_dir + \
#         " matt@api.ubskin.net:/data/ubskin/webWork/"
#     )
#     # local(cmd_rsync_webwork+" run")

# def restart_webwork():
#     run("sudo supervisorctl restart "+project_name+"_web:")


# # DEAL WITH WEB WORK ON DEV SERVER

# def pull_webwork_dev():
#     local("rsync -avz --dry-run --progress --delete -e \"ssh -p 48022\" " + \
#         rsync_excludes_source + "matt@dev.ubskin.net:/data/source/webWork/ " + \
#         webwork_backup_dir
#     )
#     # local(cmd_rsync_webwork)

# def pull_webwork_dev_run():
#     local("rsync -avz --progress --delete -e \"ssh -p 48022\" " + \
#         rsync_excludes_source + "matt@dev.ubskin.net:/data/source/webWork/ " + \
#         webwork_backup_dir
#     )
#     # local(cmd_rsync_webwork)


# def push_webwork_dev():
#     local("rsync -avz --dry-run --progress --delete -e \"ssh -p 48022\" " + \
#         rsync_excludes_source + " " + webwork_backup_dir + \
#         " matt@dev.ubskin.net:/data/source/webWork/"
#     )
#     # local(cmd_rsync_webwork)

# def push_webwork_dev_run():
#     local("rsync -avz --progress --delete -e \"ssh -p 48022\" " + \
#         rsync_excludes_source + " " + webwork_backup_dir + \
#         " matt@dev.ubskin.net:/data/source/webWork/"
#     )
#     # local(cmd_rsync_webwork)




# def rsync_secrets():
#     local("rsync -avz --dry-run --progress --delete -e \"ssh -p 48022\" " + \
#         rsync_excludes + " " + websecret_dir + \
#         " matt@api.ubskin.net:/data/ubskin/secrets/"
#     )

# def rsync_secrets_run():
#     local("rsync -avz --progress --delete -e \"ssh -p 48022\" " + \
#         rsync_excludes + " " + websecret_dir + \
#         " matt@api.ubskin.net:/data/ubskin/secrets/"
#     )


# def rsync_site():
#     local("rsync -avz --dry-run --progress --delete -e \"ssh -p 48022\" " + \
#         "--exclude=/phpmyadmin/ " + \
#         rsync_excludes + " " + site_dir + \
#         " matt@api.ubskin.net:/data/site/webWork/"
#     )

# def rsync_site_run():
#     local("rsync -avz --progress --delete -e \"ssh -p 48022\" " + \
#         "--exclude=/phpmyadmin/ " + \
#         rsync_excludes + " " + site_dir + \
#         " matt@api.ubskin.net:/data/site/webWork/"
#     )



# def rsync_webwork_test():
#     local("python -m compileall "+webwork_dir)
#     local("rsync -avz --dry-run --progress --delete " + \
#         rsync_excludes + " " + webwork_dir + \
#         " matt@10.0.0.101:/data/ubskin/webWork/"
#     )

# def rsync_webwork_test_run():
#     local("python -m compileall "+webwork_dir)
#     local("rsync -avz --progress --delete " + \
#         rsync_excludes + " " + webwork_dir + \
#         " matt@10.0.0.101:/data/ubskin/webWork/"
#     )


# @hosts("matt@10.0.0.101")
# def restart_webwork_test():
#     env.hosts = ["matt@10.0.0.101"]
#     run("sudo supervisorctl restart "+project_name+"_web:")


# def clean_webwork():
#     cmd_clean = "find ~/Dropbox/"+project_name+"/webWork/ -name '*.pyc' -delete"
#     local(cmd_clean)

