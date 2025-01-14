# GPT-SoVITS TTS Demo

这是一个结合了 GPT-SoVITS 和 端脑云（https://cephalon.cloud/） 的文本转语音演示应用。它可以直接将文本转换为语音，也可以先通过 AI 生成文本然后转换为语音。

## 功能特点

- 支持直接文本转语音
- 支持 AI 对话后转语音
- 支持自定义参考音频
- 支持多种语言
- 提供多个预设音色选择

## 安装

1. 克隆仓库：
```bash
git clone https://github.com/nicekate/GPT_SoVITS-demo.git
cd GPT_SoVITS-demo
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 配置环境变量：
   - 复制 `.env.example` 为 `.env`
   - 在 `.env` 文件中填入你的 API Key

## 使用方法

运行应用：
```bash
python app.py
```

### 直接文本转语音
1. 在"直接文本转语音"标签页输入要转换的文本
2. 选择文本语言
3. 选择使用预设音色或上传自定义音频
4. 点击"生成音频"按钮

### AI对话转语音
1. 在"AI对话转语音"标签页输入提示词
2. 点击"生成AI回复"获取 AI 生成的文本
3. 编辑生成的文本（如需要）
4. 选择语音参数
5. 点击"将文本转为语音"按钮

## 注意事项

- 使用自定义音频时，需要提供音频对应的文本
- 音频文件支持 wav、mp3 格式
- 请确保 API Key 配置正确 