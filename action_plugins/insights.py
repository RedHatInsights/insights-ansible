from ansible.plugins.action import ActionBase
from ansible.utils.vars import merge_hash


class ActionModule(ActionBase):

    def run(self, tmp=None, task_vars=None):

        # setup module
        results = super(ActionModule, self).run(tmp, task_vars)
        remote_user = task_vars.get('ansible_ssh_user') or self._play_context.remote_user
        # put
        # some
        # flags
        # need:
        # 0) bypass auto-update
        # 1) bypass version check?
        # 2) egg endpoint (where to get the egg)
        # 3) bypass gpg check
        # 4) which gpg file to use

        # import the egg
        import pkgutil
        package = pkgutil.get_loader('insights_core')
        location_to_the_egg = package.archive

        # is the core actually installed?
        if package:

        # check current egg version
        import insights_core
        current_version = insights_core.constants.version

        # curl version endpoint
        import urllib
        version_endpoint_response = urllib.urlopen("https://cert-api.access.redhat.com/r/insights/static/insights-core.version")
        version_endpoint = version_endpoint_response.read()

        # download the egg and install the egg if its out of date
        if current_version < version_endpoint:

            # download the egg
            import tempfile
            tmp_dir = tempfile.mkdtemp()
            egg_download_response = urllib.urlretrieve('https://cert-api.access.redhat.com/r/insights/static/insights-core.egg', tmp_dir)

            # verify the egg
            # gpg --verify $GPG_KEY $EGG_LOCATION > /dev/null 2>&1
            egg_verification = True

            # install the egg
            if egg_verification:
                # easy_install??
            else:
                # do some other stuff

        # copy our egg
        tmp = self._make_tmp_path(remote_user)
        source_full = self._loader.get_real_file(location_to_the_egg)
        tmp_src = self._connection._shell.join_path(tmp, 'insights')
        remote_path = self._transfer_file(source_full, tmp_src)
        results = merge_hash(results, self._execute_module(module_args={"egg_path": remote_path}, 
            module_name="insights", tmp=tmp, task_vars=task_vars))
        return results
