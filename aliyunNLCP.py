'''基于SER/SA的情感分析程序的设计与实现
利用阿里云AI情感识别服务API，实现一个简单的情感分析程序。
输入文本，调用情感分析服务API，输出情感分析结果；
情感分析结果包括正面情感、负面情感和中性情感。
'''
import json
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdknlp_automl.request.v20191111 import RunPreTrainServiceRequest
# Initialize AcsClient instance
client = AcsClient( # Access-Key-Id, Access-Key-Secret, Region-ID
  "LTAI5tGS5Q4TwDdc8LdNVgkS",
  "lJePKSHhZBq7ouvhJxjf1LtpAFQXem",
  "cn-hangzhou"
);
messages=["It has been a pleasure working with you!"] # Input text
content ={"messages": messages} # Set input text
# Initialize a request and set parameters
request = RunPreTrainServiceRequest.RunPreTrainServiceRequest() # Initialize request
request.set_ServiceName('NLP-En-Sentiment-Analysis') # Set service name
request.set_PredictContent(json.dumps(content)) # Set input text
# Print response
response = client.do_action_with_exception(request) # Call API
resp_obj = json.loads(response) # Get response
predict_result = json.loads(resp_obj['PredictResult']) # Get result
print(predict_result['predictions']) # Output result
#为程序添加GUI窗口界面