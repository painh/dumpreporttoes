import yaml


class Config:
    loaded = False
    config = {}

    @staticmethod
    def load():
        with open('config.yml') as f:
            Config.config = yaml.load(f, Loader=yaml.FullLoader)

    @staticmethod
    def get(x):
        if not Config.loaded:
            Config.load()
            Config.loaded = True

        return Config.config[x]
