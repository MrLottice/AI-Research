from flask import Flask, render_template, request, jsonify, send_file, Response
import requests
import json
import os
from datetime import datetime
from docx import Document
from docx.shared import Pt
import markdown
import io
import subprocess
import webbrowser
from flask_cors import CORS  # 导入CORS扩展


# 创建Flask应用实例
app = Flask(__name__)
# 添加CORS支持
CORS(app, resources={r"/*": {"origins": "*"}})

# 全局变量存储当前文档
current_doc = None
current_filename = None

# Dify API配置
DIFY_API_URL = "http://127.0.0.1/v1/workflows/run"  # 工作流API地址
DIFY_API_KEY_MASTER_THESIS = "app-kSen0waSQPEPOnA2UzLMx6Rq"  # 硕士论文全文
DIFY_API_KEY_MASTER_THESIS_PROPOSAL = "app-E1DJgX17BuUgg05Ir3vUjzRS"  # 硕士论文开题报告
DIFY_API_KEY_SCI_PAPER = "app-mO9dbv8X9aURZsfm6JKJjiqy" # nature论文
DIFY_API_KEY_REVIEW = "app-wx9y0mYWgTkWKe2XYJbkPJHk" # 综述写作
DIFY_API_KEY_PROJECTREVIEW = "app-RpWORxhGfQgKNvc4ih6h3AOK" # 项目审查
DIFY_API_KEY_FUNDWRITING = "app-YfE5tb12K5R655nonYiA2Qbu"  # 基金申请书
DIFY_UPLOAD_URL = "http://127.0.0.1/v1/files/upload"  # Dify文件上传API地址


# 路由：首页
@app.route('/test', methods=['GET'])
def home():
    return 'test'

@app.route('/dify_api', methods=['POST'])
def dify_api():
    try:
        # 获取请求数据
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()
            
        if not data:
            return jsonify({
                'message': 'error',
                'status': '请求数据不能为空'
            }), 400

        # 获取主题参数
        theme = data.get('theme', 'master_thesis')  # 默认为硕士论文全文

        # 根据主题验证必要字段
        if theme == 'fund_writing':
            if 'paragraph' not in data or 'content' not in data:
                return jsonify({
                    'message': 'error',
                    'status': '基金写作需要包含 paragraph 和 content 字段'
                }), 400
        else:
            if 'title' not in data:
                return jsonify({
                    'message': 'error',
                    'status': '请求数据格式错误，必须包含title字段'
                }), 400
            
        # 根据主题选择不同的API key
        api_key = ""
        if theme == 'master_thesis':
            api_key = DIFY_API_KEY_MASTER_THESIS
            print(f"使用硕士论文全文API key")
        elif theme == 'master_thesis_proposal':
            api_key = DIFY_API_KEY_MASTER_THESIS_PROPOSAL
            print(f"使用硕士论文开题报告API key")
        elif theme == 'sci_paper':
            api_key = DIFY_API_KEY_SCI_PAPER
            print(f"使用sci论文API key")
        elif theme == 'review':
            api_key = DIFY_API_KEY_REVIEW
            print(f"使用综述写作API key")
        elif theme == 'project_review':
            api_key = DIFY_API_KEY_PROJECTREVIEW
            print(f"使用项目申请书API key")
        elif theme == 'fund_writing':
            api_key = DIFY_API_KEY_FUNDWRITING
            print(f"使用基金申请书API key")
        else:
            return jsonify({
                'message': 'error',
                'status': f'不支持的主题: {theme}'
            }), 400

        # 构建符合Dify API规范的请求体
        dify_payload = {
            'inputs': {},
            'response_mode': 'streaming',  # 改为流式模式
            'user': 'user_' + datetime.now().strftime('%Y%m%d%H%M%S')
        }

        # 如果不是 fund_writing 主题，添加 title 字段
        if theme != 'fund_writing':
            dify_payload['inputs']['title'] = data.get('title', '').strip('"')  # 移除可能的引号

        # 如果是 fund_writing 主题，添加 paragraph 和 content 字段
        if theme == 'fund_writing':
            dify_payload['inputs']['paragraph'] = data.get('paragraph', '')
            dify_payload['inputs']['content'] = data.get('content', '')
            print(f"基金申请书参数：")
            print(f"paragraph: {data.get('paragraph', '')}")
            print(f"content: {data.get('content', '')}")

        # 如果是 sci_paper 主题，添加 type 字段
        if theme == 'sci_paper':
            dify_payload['inputs']['type'] = data.get('type', '')  # 从请求中获取 type 字段

        # 添加examples字段，如果在请求中提供了这个字段
        if 'examples' in data:
            dify_payload['inputs']['examples'] = data.get('examples')
        
        print("\n=== 发送请求到Dify ===")
        print(f"请求格式: {'JSON' if request.is_json else 'form-data'}")
        print(f"主题: {theme}")
        print(f"文章名称: {data.get('title', '')}")
        if 'examples' in data:
            print(f"示例数据: {data.get('examples', '')}")
        print(f"请求体: {json.dumps(dify_payload, ensure_ascii=False, indent=2)}")

        # 准备发送到Dify的请求
        dify_headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }

        # 发送请求到Dify并获取流式响应
        dify_response = requests.post(
            DIFY_API_URL,
            headers=dify_headers,
            json=dify_payload,
            stream=True  # 启用流式传输
        )

        # 检查Dify响应
        if dify_response.status_code != 200:
            print(f"Dify API错误: {dify_response.status_code}")
            print(f"错误信息: {dify_response.text}")
            return jsonify({
                'message': 'error',
                'status': f'Dify API错误: {dify_response.status_code}',
                'error_detail': dify_response.text
            }), 500

        def generate():
            try:
                full_text = ""  # 用于存储完整的文本
                print("\n=== 开始生成文本 ===")  # 开始提示
                for line in dify_response.iter_lines():
                    if line:
                        line = line.decode('utf-8')
                        if line.startswith('data: '):
                            try:
                                data = json.loads(line[6:])  # 去掉'data: '前缀
                                if data.get('event') == 'text_chunk' and 'data' in data and 'text' in data['data']:
                                    text_chunk = data['data']['text']
                                    full_text += text_chunk  # 拼接文本
                                    # 打印到控制台
                                    print(text_chunk, end='', flush=True)
                                    # 构造返回给前端的数据
                                    response_data = {
                                        'type': 'text',
                                        'content': text_chunk,
                                        'full_text': full_text
                                    }
                                    yield f"data: {json.dumps(response_data, ensure_ascii=False)}\n\n"
                                elif data.get('event') == 'done':
                                    # 发送完成事件
                                    response_data = {
                                        'type': 'done',
                                        'full_text': full_text
                                    }
                                    yield f"data: {json.dumps(response_data, ensure_ascii=False)}\n\n"
                                else:
                                    # 其他类型的事件直接转发
                                    yield f"data: {json.dumps(data, ensure_ascii=False)}\n\n"
                            except json.JSONDecodeError as e:
                                print(f"\nJSON解析错误: {str(e)}")
                                continue
                print("\n=== 文本生成完成 ===")  # 生成完成后打印换行
            except Exception as e:
                print(f"\n流式处理错误: {str(e)}")
                error_data = {
                    'type': 'error',
                    'message': str(e)
                }
                yield f"data: {json.dumps(error_data, ensure_ascii=False)}\n\n"

        return Response(generate(), mimetype='text/event-stream')

    except Exception as e:
        print(f"\n发生错误: {str(e)}")
        import traceback
        print("错误详情:")
        print(traceback.format_exc())
        return jsonify({
            'message': 'error',
            'status': str(e)
        }), 500

@app.route('/upload_and_analyze', methods=['POST'])
def upload_and_analyze():
    try:
        if 'file' not in request.files:
            return jsonify({
                'message': 'error',
                'status': '没有文件'
            }), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({
                'message': 'error',
                'status': '没有选择文件'
            }), 400

        # 获取主题参数
        theme = request.form.get('theme', 'project_review')  # 默认为项目申请书
        
        # 根据主题选择不同的API key
        api_key = ""
        if theme == 'project_review':
            api_key = DIFY_API_KEY_PROJECTREVIEW
            print(f"使用项目申请书API key")
        else:
            return jsonify({
                'message': 'error',
                'status': f'不支持的主题: {theme}'
            }), 400

        # 准备发送到Dify的请求头
        dify_headers = {
            'Authorization': f'Bearer {api_key}'
        }

        # 生成用户标识
        user_id = 'user_' + datetime.now().strftime('%Y%m%d%H%M%S')
        
        # 第一步：上传文件
        print("\n=== 上传文件到Dify ===")
        print(f"文件名: {file.filename}")
        print(f"主题: {theme}")
        
        # 确保文件流位于开始位置
        file.seek(0)
        
        files = {
            'file': (file.filename, file.stream, file.content_type)
        }
        
        # 添加user参数到form data
        form_data = {
            'user': user_id,
            'type': 'DOCX'  # 设置文件类型
        }
        
        upload_response = requests.post(
            DIFY_UPLOAD_URL,
            headers=dify_headers,
            files=files,
            data=form_data
        )

        if upload_response.status_code not in [200, 201]:
            print(f"Dify文件上传错误: {upload_response.status_code}")
            print(f"错误信息: {upload_response.text}")
            return jsonify({
                'message': 'error',
                'status': f'文件上传失败: {upload_response.status_code}'
            }), 500

        # 解析上传响应
        upload_data = upload_response.json()
        file_id = upload_data.get('id')
        
        print(f"文件上传成功，ID: {file_id}")

        # 第二步：发送分析请求
        dify_headers['Content-Type'] = 'application/json'
        
        analysis_payload = {
            'inputs': {
                'files': [{
                    'transfer_method': 'local_file',
                    'upload_file_id': file_id,
                    'type': 'document'
                }]
            },
            'response_mode': 'streaming',
            'user': user_id
        }

        print("\n=== 发送分析请求到Dify ===")
        print(f"分析请求体: {json.dumps(analysis_payload, ensure_ascii=False, indent=2)}")

        def generate():
            try:
                analysis_response = requests.post(
                    DIFY_API_URL,
                    headers=dify_headers,
                    json=analysis_payload,
                    stream=True
                )

                if analysis_response.status_code != 200:
                    error_data = {
                        'type': 'error',
                        'message': f'分析请求失败: {analysis_response.status_code}'
                    }
                    yield f"data: {json.dumps(error_data, ensure_ascii=False)}\n\n"
                    return

                full_text = ""
                print("\n=== 开始生成分析结果 ===")
                for line in analysis_response.iter_lines():
                    if line:
                        line = line.decode('utf-8')
                        if line.startswith('data: '):
                            try:
                                data = json.loads(line[6:])
                                if data.get('event') == 'text_chunk' and 'data' in data and 'text' in data['data']:
                                    text_chunk = data['data']['text']
                                    full_text += text_chunk
                                    print(text_chunk, end='', flush=True)
                                    response_data = {
                                        'type': 'text',
                                        'content': text_chunk,
                                        'full_text': full_text
                                    }
                                    yield f"data: {json.dumps(response_data, ensure_ascii=False)}\n\n"
                                elif data.get('event') == 'done':
                                    response_data = {
                                        'type': 'done',
                                        'full_text': full_text
                                    }
                                    yield f"data: {json.dumps(response_data, ensure_ascii=False)}\n\n"
                                else:
                                    yield f"data: {json.dumps(data, ensure_ascii=False)}\n\n"
                            except json.JSONDecodeError as e:
                                print(f"\nJSON解析错误: {str(e)}")
                                continue
                print("\n=== 分析完成 ===")
            except Exception as e:
                print(f"\n流式处理错误: {str(e)}")
                error_data = {
                    'type': 'error',
                    'message': str(e)
                }
                yield f"data: {json.dumps(error_data, ensure_ascii=False)}\n\n"

        return Response(generate(), mimetype='text/event-stream')

    except Exception as e:
        print(f"\n发生错误: {str(e)}")
        import traceback
        print("错误详情:")
        print(traceback.format_exc())
        return jsonify({
            'message': 'error',
            'status': str(e)
        }), 500


# 错误处理
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({
        'message': 'Resource not found',
        'status': 'error'
    }), 404

if __name__ == '__main__':
    app.run(debug=True) 