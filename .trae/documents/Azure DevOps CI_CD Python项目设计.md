## 项目设计方案

### 1. 项目结构
```
azure-devops-demo/
├── src/
│   └── azuredemo/
│       ├── __init__.py
│       ├── main.py
│       └── utils.py
├── tests/
│   ├── __init__.py
│   └── test_utils.py
├── pyproject.toml
├── .gitignore
├── azure-pipelines.yml
└── README.md
```

### 2. 技术栈
- **包管理器**: uv
- **测试框架**: pytest
- **代码覆盖率**: pytest-cov
- **CI/CD**: Azure DevOps Pipelines

### 3. 项目功能
创建一个简单的Azure资源使用量统计工具，读取用户提供的Azure免费额度数据，进行统计分析。

### 4. CI流程
1. 检出代码
2. 安装uv
3. 设置Python环境
4. 安装依赖
5. 运行单元测试（含覆盖率）
6. 上传测试报告和代码到Artifacts

### 5. CD流程
1. 从Artifacts下载构建产物
2. 部署到目标虚拟机

### 6. 需要创建的文件
1. `pyproject.toml` - uv配置和项目元数据
2. `src/azuredemo/__init__.py` - 包初始化
3. `src/azuredemo/utils.py` - 核心工具函数
4. `src/azuredemo/main.py` - 主程序入口
5. `tests/test_utils.py` - 单元测试
6. `azure-pipelines.yml` - Azure DevOps Pipeline配置
7. `.gitignore` - Git忽略文件
8. `README.md` - 项目说明

确认后开始创建项目。