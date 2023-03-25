'''
环境依赖
pip install ttkthemes
pip install aliyun-python-sdk-core
pip install aliyun-python-sdk-nlp-automl
基于SER/SA的情感分析程序的设计与实现 通过文本识别情感 
利用阿里云AI情感识别服务（英文）API，实现一个简单的情感分析程序。
输入文本，调用情感分析服务API，输出情感分析结果；
情感分析结果包括正面情感、负面情感和中性情感。

'''
import json
import tkinter as tk
from tkinter import ttk
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdknlp_automl.request.v20191111 import RunPreTrainServiceRequest
from ttkthemes import ThemedTk
# Initialize AcsClient instance
client = AcsClient(
  "AccessKeyID",
  "AccessKeyecret",
  "cn-hangzhou"
)

def analyze_sentiment():
    text = input_text.get(1.0, "end-1c").strip() # Get input text from Text widget
    if not text:
        # If input text is empty, show a warning message
        sentiment_label.configure(text="请输入要分析的文本", foreground="#b6b764")#灰色
        return 
    
    messages=[text]
    content ={"messages": messages} # Set input text
    request = RunPreTrainServiceRequest.RunPreTrainServiceRequest() # Initialize request
    request.set_ServiceName('NLP-En-Sentiment-Analysis') # Set service name
    request.set_PredictContent(json.dumps(content)) # Set input text

    # Call API and get response
    try:
        response = client.do_action_with_exception(request)
        print(f"Response type: {type(response)}")
        print(f"Response content: {response}")

    # Parse response
        resp_obj = json.loads(response)
        predict_result = json.loads(resp_obj['PredictResult'])
        print(f"Predict result type: {type(predict_result)}")
        print(f"Predict result: {predict_result}")

    # Process prediction result
        if "predictions" in predict_result:
            if "positive" in predict_result["predictions"]:
                sentiment = "正面语句"
                color = "#b6b764"
            elif "negative" in predict_result["predictions"]:
                sentiment = "中立语句"
                color = "#b6b764"
            elif "neutral" in predict_result["predictions"]:
                sentiment = "负面语句"
                color = "#b6b764"
            else:
                sentiment = "语句错误无法识别情绪"
                color = "#b6b764"
                sentiment_label.configure(text=sentiment, foreground=color)
            # Update GUI
            result_label.configure(text=sentiment, foreground=color)
            sentiment_label.configure(text="")
        else:
            sentiment_label.configure(text="")
            sentiment = "语句错误无法识别情绪"
            color = "#b6b764"
    except Exception as e:
        sentiment_label.configure(text="")
        
    # Update GUI
        result_label.configure(text=sentiment, foreground=color)
        sentiment_label.configure(text=sentiment, foreground=color)
  
# Create the main window
root = tk.Tk()

style = ttk.Style()# Create a Style object
style.theme_use("clam")# Set the theme for the window
style.configure(".", font=("Helvetica", 12))# Set the font for all widgets
# Set the window title
root.title("基于阿里云AI的文本情感分析程序(英文)")

# Set the window size
root.geometry("745x500")

# Create the input Text widget
input_text = tk.Text(root, height=12, font=("Arial", 12),bg="#67633c", fg="#b6b764",insertbackground="#b6b764")
input_text.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W + tk.E)

# Create the button to analyze sentiment
analyze_button = ttk.Button(root, text="进行情感分析", command=analyze_sentiment)
analyze_button.grid(row=1, column=0, pady=10)

# Set the color scheme
style.configure("TLabel", foreground="#b6b764", background="#656248")
style.configure("TEntry", foreground="#656248", background="#656248")
style.configure("TButton", foreground="#b6b764", background="#3a3825")
# Remove button border
style.configure("TButton", relief="flat")


# Set button background color
style.map("TButton",
          background=[("active", "#b6b764"), ("pressed", "#516548")])

# Create a label with the style
label = ttk.Label(root)
entry = ttk.Entry(root)


# Create a button with the style
button = ttk.Button(root, text="Submit")


# Create the label to display sentiment result
result_label = ttk.Label(root, text="", font=("Arial", 24, "bold"))
result_label.grid(row=2, column=0, pady=10)

# Set the window background color
root.config(bg="#656248")

# Create the label to display sentiment result
sentiment_label = ttk.Label(root, text="", font=("Arial", 24, "bold"))
sentiment_label.grid(row=2, column=0, pady=10)

# Start the GUI event loop
root.mainloop()
