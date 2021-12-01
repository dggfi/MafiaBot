from servman.servman import ServiceManager

if __name__ == "__main__":
    config_path = "./conf/connection_config.json"

    sm = ServiceManager(config_path)
    sm.run()