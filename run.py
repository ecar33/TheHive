from hive import create_app
from hive.config import DevelopmentConfig, ProductionConfig

app = create_app(ProductionConfig)

if __name__ == '__main__':
    app.run(debug=False)