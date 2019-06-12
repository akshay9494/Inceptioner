import os

class Configuration:
    def __init__(self):
        self.port = os.environ.get('PORT', 8080)

        self.home_dir = os.path.join(os.path.dirname(__file__), '..', 'home')
        os.makedirs(self.home_dir, exist_ok=True)

        self.log_dir = os.path.join(self.home_dir, 'logs')
        os.makedirs(self.log_dir, exist_ok=True)

        self.model_path = os.path.join(os.path.dirname(__file__), '..', 'dl_models', 'inception_v3_weights_tf_dim_ordering_tf_kernels.h5')


config = Configuration()