import charms_openstack.charm
import charmhelpers.core.hookenv as ch_hookenv  # noqa

from charmhelpers.contrib.openstack.utils import (
    get_os_codename_package,
    CompareOpenStackReleases,
)


charms_openstack.charm.use_defaults('charm.default-select-release')


class Cinder{{ cookiecutter.driver_name }}Charm(
        charms_openstack.charm.CinderStoragePluginCharm):

    name = 'cinder_{{ cookiecutter.driver_name_lc }}'
    version_package = '{{ cookiecutter.package_name }}'
    release = '{{ cookiecutter.release }}'
    packages = [version_package]
    stateless = True
    # Specify any config that the user *must* set.
    mandatory_config = []

    def cinder_configuration(self):
        # Specify the volume driver
        volume_driver = ''

        if self.config.get('volume-backend-name'):
            volume_backend_name = self.config.get('volume-backend-name')
        else:
            volume_backend_name = ch_hookenv.service_name()

        driver_options = [
            ('volume_driver', volume_driver),
            ('volume_backend_name', volume_backend_name),
            # Add config options that needs setting on cinder.conf
        ]

        os_codename = get_os_codename_package('cinder-common')
        if CompareOpenStackReleases(os_codename) >= "pike" \
                and self.config.get('backend-availability-zone'):
            driver_options.append(
                ('backend_availability_zone',
                 self.config.get('backend-availability-zone')))

        return driver_options


class Cinder{{ cookiecutter.driver_name }}CharmRocky(Cinder{{ cookiecutter.driver_name }}Charm):

    # Rocky needs py3 packages.
    release = 'rocky'
    version_package = '{{ cookiecutter.package3_name }}'
    packages = [version_package]
