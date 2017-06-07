from ansible.plugins.action import ActionBase
from ansible.utils.vars import merge_hash


class ActionModule(ActionBase):

    def run(self, tmp=None, task_vars=None):

        # setup module
        results = super(ActionModule, self).run(tmp, task_vars)
        remote_user = task_vars.get('ansible_ssh_user') or self._play_context.remote_user
        results = merge_hash(results, task_vars)

        # get args
        # the_args.get('something')
        # the_args.has_key('something')
        the_args = self._task.args
        bypass_update = True if the_args.has_key('update') and the_args.get('update') == '1' else False
        where_to_get_egg = the_args.get('core_url') if the_args.has_key('core_url') else 'https://cert-api.access.redhat.com/r/insights/static/insights-core.egg' 
        bypass_gpg = True if the_args.has_key('no_gpg') and the_args.get('no_gpg') == 'yes' else False

        # import the egg
        import pkgutil
        package = pkgutil.get_loader('insights_core')
        location_to_the_egg = package.archive

        # is the core actually installed?
        current_version = None
        version_endpoint = None
        if package and not bypass_update:

            # check current egg version
            import insights_core
            current_version = insights_core.constants.version

            # curl version endpoint
            import urllib
            version_endpoint_response = urllib.urlopen("https://cert-api.access.redhat.com/r/insights/static/insights-core.version")
            version_endpoint = version_endpoint_response.read()

        # download the egg and install the egg if its out of date
        if ( current_version < version_endpoint ) or ( not package and not bypass_update ):

            # download the egg
            import tempfile
            tmp_dir = tempfile.mkdtemp()
            egg_download_response = urllib.urlretrieve(where_to_get_egg, tmp_dir)

            # verify the egg
            # gpg --verify $GPG_KEY $EGG_LOCATION > /dev/null 2>&1
            gpg_checks_out = True
            egg_verfication = True if gpg_checks_out or bypass_gpg else False

            # install the egg
            if egg_verification:
                # easy_install??
                pass
            else:
                # do some other stuff
                pass

        # copy our egg
        remote_path = None
        if package and location_to_the_egg:
            tmp = self._make_tmp_path(remote_user)
            source_full = self._loader.get_real_file(location_to_the_egg)
            tmp_src = self._connection._shell.join_path(tmp, 'insights')
            remote_path = self._transfer_file(source_full, tmp_src)
        results = merge_hash(results, self._execute_module(module_args={"egg_path": remote_path}, 
                module_name="insights", tmp=tmp, task_vars=task_vars))
        return results
