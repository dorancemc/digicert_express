import loggers
import config
import os

from base_platform import BasePlatform

class CentosPlatform(BasePlatform):
    APACHE_SERVICE = 'httpd'
    DEPS = ['openssl', 'augeas-libs', 'augeas', 'mod_ssl']

    def check_dependencies(self):
        logger = loggers.get_logger(__name__)
        try:
            logger.info("Checking for required dependencies")
            import yum
            yb = yum.YumBase()
            packages = yb.rpmdb.returnPackages()

            installed_packages = []
            ignored_packages = []
            for package_name in self.DEPS:
                if package_name in [x.name for x in packages]:
                    continue
                else:
                    if raw_input('Install: {0} (Y/n) '.format(package_name)).lower().strip() == 'n':
                        ignored_packages.append(package_name)
                        continue
                    else:
                        logger.info("Installing package {0}...".format(package_name))
                        os.system('yum -y install {0} &>> {1}'.format(package_name, config.LOG_FILE))
                        installed_packages.append(package_name)
                        continue
            if not installed_packages and not ignored_packages:
                logger.info("All dependencies are met.")
            return ignored_packages
        except ImportError:
            pass
