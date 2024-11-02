import yaml
from flasgger import Swagger, swag_from

swagger = Swagger()


def init_swagger(app):
    # 加载 YAML 文件并初始化 Swagger
    with open("swagger_docs/swagger_docs.yml", "r") as f:
        swagger_template = yaml.safe_load(f)
    swagger.template = swagger_template
    swagger.init_app(app)
