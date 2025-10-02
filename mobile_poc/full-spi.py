import requests
from urllib.parse import urlencode

# Wolfram|Alpha Full Results API 配置
APPID = "YOUR_APP_ID_HERE"  # 请替换为您的AppID
BASE_URL = "https://api.wolframalpha.com/v2/query"

s = requests.Session()

def query_wolfram(input_text, **kwargs):
	"""
	使用Wolfram|Alpha Full Results API进行查询
	
	@input_text: 查询文本
	@kwargs: 其他API参数，如format, includepodid等
	"""
	params = {
		'appid': APPID,
		'input': input_text
	}
	
	# 添加其他参数
	params.update(kwargs)
	
	# 构建完整URL
	url = f"{BASE_URL}?{urlencode(params)}"
	
	try:
		response = s.get(url)
		response.raise_for_status()
		return response.text
	except requests.exceptions.RequestException as e:
		raise Exception(f"API请求失败: {e}")

def query_with_format(input_text, format_type="xml", **kwargs):
	"""
	指定输出格式的查询函数
	
	@input_text: 查询文本
	@format_type: 输出格式 (xml, json, plaintext等)
	@kwargs: 其他API参数
	"""
	return query_wolfram(input_text, format=format_type, **kwargs)

def query_specific_pod(input_text, pod_id, format_type="xml"):
	"""
	查询特定pod的结果
	
	@input_text: 查询文本
	@pod_id: pod ID (如 "Result", "Input" 等)
	@format_type: 输出格式
	"""
	return query_wolfram(input_text, includepodid=pod_id, format=format_type)

def validate_query(input_text):
	"""
	验证查询是否有效（使用validatequery函数）
	
	@input_text: 查询文本
	"""
	validate_url = "https://api.wolframalpha.com/v2/validatequery"
	params = {
		'appid': APPID,
		'input': input_text
	}
	
	url = f"{validate_url}?{urlencode(params)}"
	
	try:
		response = s.get(url)
		response.raise_for_status()
		return response.text
	except requests.exceptions.RequestException as e:
		raise Exception(f"验证查询失败: {e}")

def query_with_assumptions(input_text, assumption_input):
	"""
	使用假设进行查询
	
	@input_text: 查询文本
	@assumption_input: 假设输入
	"""
	return query_wolfram(input_text, assumption=assumption_input)

if __name__ == "__main__":
	# 示例1: 基本查询
	print("=== 基本查询示例 ===")
	try:
		result = query_wolfram("population of France")
		print("法国人口查询结果:")
		print(result[:500] + "..." if len(result) > 500 else result)
	except Exception as e:
		print(f"查询失败: {e}")
	
	print("\n=== 指定格式查询示例 ===")
	try:
		# 示例2: 指定输出格式为JSON
		result_json = query_with_format("population of France", format_type="json")
		print("JSON格式结果:")
		print(result_json[:500] + "..." if len(result_json) > 500 else result_json)
	except Exception as e:
		print(f"JSON查询失败: {e}")
	
	print("\n=== 特定Pod查询示例 ===")
	try:
		# 示例3: 只获取Result pod
		result_pod = query_specific_pod("population of France", "Result", "plaintext")
		print("Result Pod结果:")
		print(result_pod)
	except Exception as e:
		print(f"Pod查询失败: {e}")
	
	print("\n=== 数学查询示例 ===")
	try:
		# 示例4: 数学查询
		math_result = query_wolfram("y' = y/(x+y^3)", format="plaintext")
		print("微分方程查询结果:")
		print(math_result)
	except Exception as e:
		print(f"数学查询失败: {e}")