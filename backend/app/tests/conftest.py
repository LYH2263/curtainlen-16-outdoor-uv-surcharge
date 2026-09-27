import os
import tempfile

# 在导入任何 app 模块前把数据库指到临时目录，避免测试碰真实数据
os.environ["DATA_DIR"] = tempfile.mkdtemp(prefix="curtainlen-test-")
