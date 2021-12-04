from servman.servman import ServiceManager
from services.pinger_service import pinger_service

if __name__ == "__main__":
    config_path = "./conf/servman_config.json"

    sm = ServiceManager(config_path)
    sm.register_task('pinger_service', pinger_service)
    sm.run()