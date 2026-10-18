# Experiment 01: Hybrid Images

混合图像实验：分别提取两张图像的低频和高频信息，再生成混合图像。

## 文件说明

- `hybrid.py`：核心图像处理逻辑
- `gui3.py`：Python 3 图形界面入口
- `test.py`：实验测试
- `pyuiutils/`：本实验使用的 GUI 工具模块
- `resources/`：输入图片和配置模板
- `results/`：实验输出和报告

## 运行

请从当前实验目录运行，代码中的配置和资源路径以该目录为基准：

```powershell
Set-Location experiments\01-hybrid-images
python gui3.py
python test.py
```

依赖安装方式见仓库根目录的 `README.md`。