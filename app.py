import gradio as gr
import requests
import tempfile
import os
import json
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 常量定义
MODEL_ID = "1864244127731589120"

# 从环境变量获取配置
API_KEY = os.getenv('API_KEY')
if not API_KEY:
    raise ValueError("请确保 .env 文件中设置了 API_KEY")

def qwen_generate(prompt):
    url = "https://cephalon.cloud/user-center/v1/model/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }
    
    data = {
        "model": "Qwen2.5-72B-Instruct-AWQ",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "stream": False
    }
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        raise gr.Error(f"Qwen生成失败: {response.text}")

def tts_generate(text, text_lang, ref_audio_path, prompt_lang, prompt_text, custom_audio=None):
    url = "https://cephalon.cloud/user-center/v1/model/tts"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Model-Id": MODEL_ID
    }
    
    files = {
        "text": (None, text),
        "text_lang": (None, text_lang),
        "prompt_lang": (None, prompt_lang),
        "prompt_text": (None, prompt_text),
        "top_k": (None, "5"),
        "top_p": (None, "1"),
        "temperature": (None, "1"),
        "text_split_method": (None, "cut5"),
        "batch_size": (None, "10"),
        "batch_threshold": (None, "0.75"),
        "split_bucket": (None, "true"),
        "speed_factor": (None, "1.0"),
        "fragment_interval": (None, "0.3"),
        "seed": (None, "-1"),
        "media_type": (None, "wav"),
        "streaming_mode": (None, "false"),
        "parallel_infer": (None, "true"),
        "repetition_penalty": (None, "1.35")
    }
    
    # 如果有上传的音频文件，使用上传的文件
    if custom_audio is not None:
        files["audio_file"] = ("reference.wav", open(custom_audio, "rb"), "audio/wav")
    else:
        files["ref_audio_path"] = (None, ref_audio_path)

    response = requests.post(url, headers=headers, files=files)
    
    if response.status_code == 200:
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        temp_file.write(response.content)
        temp_file.close()
        return temp_file.name
    else:
        raise gr.Error(f"TTS生成失败: {response.text}")

# 创建Gradio界面
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# GPT-SoVITS TTS Demo")
    
    with gr.Tabs():
        with gr.TabItem("直接文本转语音"):
            with gr.Row():
                with gr.Column():
                    text_input1 = gr.Textbox(label="输入文本", value="先帝创业未半而中道崩殂，今天下三分，益州疲弊，此诚危急存亡之秋也")
                    text_lang1 = gr.Dropdown(
                        choices=["zh", "ja", "en", "ko", "yue", "auto", "auto_yue", "all_zh", "all_ja", "all_yue", "all_ko"],
                        value="zh",
                        label="文本语言"
                    )
                    with gr.Row():
                        with gr.Column():
                            use_custom_audio1 = gr.Checkbox(label="使用自定义音频", value=False)
                            custom_audio1 = gr.Audio(label="上传参考音频", type="filepath", visible=False)
                            custom_prompt_text1 = gr.Textbox(label="参考音频对应的文本", visible=False)
                        with gr.Column():
                            ref_audio1 = gr.Dropdown(
                                choices=["Krira", "gakki", "jok", "keli", "ynaifa", "Sadness", "Angry", "Butcher", "feiyan", "enboy", "Cantonese"],
                                value="jok",
                                label="预设参考音频"
                            )
                            preset_prompt_text1 = gr.Textbox(label="预设提示文本", value="说得好像您带我以来我考好过几次一样")
                    prompt_lang1 = gr.Dropdown(
                        choices=["zh", "ja", "en", "ko", "yue"],
                        value="zh",
                        label="提示文本语言"
                    )
                    submit_btn1 = gr.Button("生成音频")
                
                with gr.Column():
                    audio_output1 = gr.Audio(label="生成的音频")
        
        with gr.TabItem("AI对话转语音"):
            with gr.Row():
                with gr.Column():
                    prompt_input = gr.Textbox(label="输入提示词", value="用简短的话介绍一下你自己", lines=3)
                    generate_text_btn = gr.Button("生成AI回复")
                    generated_text = gr.Textbox(label="AI生成的文本(可编辑)", lines=5)
                    
                    with gr.Row():
                        text_lang2 = gr.Dropdown(
                            choices=["zh", "ja", "en", "ko", "yue", "auto", "auto_yue", "all_zh", "all_ja", "all_yue", "all_ko"],
                            value="zh",
                            label="文本语言"
                        )
                        with gr.Column():
                            use_custom_audio2 = gr.Checkbox(label="使用自定义音频", value=False)
                            custom_audio2 = gr.Audio(label="上传参考音频", type="filepath", visible=False)
                            custom_prompt_text2 = gr.Textbox(label="参考音频对应的文本", visible=False)
                            ref_audio2 = gr.Dropdown(
                                choices=["Krira", "gakki", "jok", "keli", "ynaifa", "Sadness", "Angry", "Butcher", "feiyan", "enboy", "Cantonese"],
                                value="jok",
                                label="预设参考音频"
                            )
                            preset_prompt_text2 = gr.Textbox(label="预设提示文本", value="说得好像您带我以来我考好过几次一样")
                    with gr.Row():
                        prompt_lang2 = gr.Dropdown(
                            choices=["zh", "ja", "en", "ko", "yue"],
                            value="zh",
                            label="提示文本语言"
                        )
                    
                    generate_audio_btn = gr.Button("将文本转为语音")
                
                with gr.Column():
                    audio_output2 = gr.Audio(label="生成的音频")
    
    # 处理音频上传组件的显示/隐藏
    def toggle_audio_upload1(use_custom):
        return {
            custom_audio1: gr.update(visible=use_custom),
            custom_prompt_text1: gr.update(visible=use_custom),
            ref_audio1: gr.update(visible=not use_custom),
            preset_prompt_text1: gr.update(visible=not use_custom)
        }
    
    def toggle_audio_upload2(use_custom):
        return {
            custom_audio2: gr.update(visible=use_custom),
            custom_prompt_text2: gr.update(visible=use_custom),
            ref_audio2: gr.update(visible=not use_custom),
            preset_prompt_text2: gr.update(visible=not use_custom)
        }
    
    use_custom_audio1.change(fn=toggle_audio_upload1, inputs=use_custom_audio1, 
                           outputs=[custom_audio1, custom_prompt_text1, ref_audio1, preset_prompt_text1])
    use_custom_audio2.change(fn=toggle_audio_upload2, inputs=use_custom_audio2, 
                           outputs=[custom_audio2, custom_prompt_text2, ref_audio2, preset_prompt_text2])
    
    # 直接文本转语音的事件绑定
    def tts_generate_with_audio_choice(text, text_lang, ref_audio, prompt_lang, use_custom, custom_audio, custom_prompt, preset_prompt):
        prompt_text = custom_prompt if use_custom else preset_prompt
        if use_custom and custom_audio is not None:
            return tts_generate(text, text_lang, None, prompt_lang, prompt_text, custom_audio)
        else:
            return tts_generate(text, text_lang, ref_audio, prompt_lang, prompt_text)
    
    submit_btn1.click(
        fn=tts_generate_with_audio_choice,
        inputs=[text_input1, text_lang1, ref_audio1, prompt_lang1, use_custom_audio1, custom_audio1, 
                custom_prompt_text1, preset_prompt_text1],
        outputs=audio_output1
    )
    
    # AI对话转语音的事件绑定（分两步）
    generate_text_btn.click(
        fn=qwen_generate,
        inputs=prompt_input,
        outputs=generated_text
    )
    
    generate_audio_btn.click(
        fn=tts_generate_with_audio_choice,
        inputs=[generated_text, text_lang2, ref_audio2, prompt_lang2, use_custom_audio2, custom_audio2,
                custom_prompt_text2, preset_prompt_text2],
        outputs=audio_output2
    )

if __name__ == "__main__":
    demo.launch() 