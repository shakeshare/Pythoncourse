# Python Course

Python 课程实验与项目代码。

## 目录结构

```text
experiments/
  01-hybrid-images/    混合图像实验
common/                可复用的公共模块
docs/                  课程笔记与实验说明
```

## 环境准备

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## 运行实验

```powershell
Set-Location experiments\01-hybrid-images
python gui3.py
python test.py
```

实验的详细说明位于对应实验目录的 `README.md`。