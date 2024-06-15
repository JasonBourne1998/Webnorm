# TamperLogPrompt
Official repository for "Detecting and Explaining Anomalies Caused by Web Tamper Attacks via Building Consistency-based Normality".

<p align="center">

  • <a href="https://sites.google.com/view/webnorm">Visit our Website</a> •

  • <a href="https://sites.google.com/view/phishllm/experimental-setup-datasets?authuser=0#h.r0fy4h1fw7mq">Download our Datasets</a>  •

</p>

## Introduction
Existing Log-based anomaly detection
- ❌ Cannot detect subtle change (often seen in tamper attacks)
- ❌ Cannot fully provide the explanation of the anomaly.

In our Webnorm, we build a consrtaint-based log anomaly detection framework:

- ✅ **Output tamper anomaly with explannation**: Compared to existing solutions that rely on deep-learning-based models and the similarity-based models, LLMs can further improve their comprehensive understanding, especially upon the logs' nuance and minor change.
- ✅ **Chain-of-thought credential-taking prediction**: Reasoning the constraints in a step-by-step way by looking at the class dedination and logs

## Framework
<img src="./figures/webnorm.jpg"/>

```Input```: a set of logs, ```Output```: Anomaly with explannations

- **Step 1: Log instrumentation and Seeds exection**
  - Input: Backend
  - Intermediate Output: Instrumented Backend
  - Output: Benign log dataset
  
- **Step 2: Construct the event graph**
  - Input: Backend, Frontend, Logs
  - Output: Event grpah indicating 3 relations (DB-sharing, Data transition, Trigger condidion).
  
- **Step 3: Constraint-learning**
  - Input: Backend, Logs, Event grpah
  - Output: Python function reflecting the constraints.

- **Step 4: Output Anomaly** 
  - Input: Logs in deployment phase
  - Output: Anomaly with explanation.

## Project structure

<pre>
├── Anomaly_detect.py  # Anomaly detection
├── consistency_prompt
│   ├── examples # Constraint-learning Examples
│   ├── gptchecker
│   │   ├── gpt.py
│   │   ├── __init__.py
│   │   ├── logger.py
│   │   ├── prompt.py # Constraint-learning prompt
│   │   └── tester.py # Constraint-learning verifycation
│   └── README.md
├── Event_graph
│   ├── API_logs_define.py
│   ├── backend_API.py
│   ├── code_database.py # Construct the database sharing
│   ├── dataflow_and_trigger.py # Construct the dataflow and trigger condition
│   ├── Event_graph.py 
│   └── trigger_code_parse.py
├── Log_Instrument
│   ├── config_templates.py
│   ├── deleteLogs.py  # Delete the original logs 
│   ├── Instrumentation.py # Instrument with AOP
├── README.md
└── setup.sh
</pre>

## Setup
- Step 1: Clone the Repository and **Install Requirements**. A new conda environment "Webnorm" will be created
```bash
    cd TamperLogPrompt/
    chmod +x ./setup.sh
    export ENV_NAME="Webnorm" && ./setup.sh
```
- Step 2: Register **OpenAI API Key**, [See Tutorial here](https://platform.openai.com/docs/quickstart). Paste the API key to 'TamperLogPrompt/consistency_prompt/.env'.


<!-- - Step 3: Register a **Google Programmable Search API Key**, [See Tutorial here](https://meta.discourse.org/t/google-search-for-discourse-ai-programmable-search-engine-and-custom-search-api/307107). Paste your API Key (in the first line) and Search Engine ID (in the second line) to "./datasets/google_api_key.txt":
     ```text 
      [API_KEY]
      [SEARCH_ENGINE_ID]
     ```
    
- Step 4 (Optional): Edit **Hyperparameters**. All hyperparameter configurations are in [param_dict.yaml](param_dict.yaml).  -->

<!-- ## Prepare the Dataset
To test on your own dataset, you need to prepare the dataset in the following structure:
<pre>
testing_dir/
├── aaa.com/
│   ├── shot.png  # save the webpage screenshot
│   ├── info.txt  # save the webpage URL
│   └── html.txt  # save the webpage HTML source
├── bbb.com/
│   ├── shot.png  # save the webpage screenshot
│   ├── info.txt  # save the webpage URL
│   └── html.txt  # save the webpage HTML source
├── ccc.com/
│   ├── shot.png  # save the webpage screenshot
│   ├── info.txt  # save the webpage URL
│   └── html.txt  # save the webpage HTML source
</pre> -->


## Inference: Run Webnorm 
```bash
  conda activate webnorm
  python3 Anomaly_detection.py
```

<!-- ## Understand the Output
- You will see the console is printing logs like the following <details><summary> Expand to see the sample log</summary>
  <pre><code>
    [PhishLLMLogger][DEBUG] Folder ./datasets/field_study/2023-09-01/device-862044b2-5124-4735-b6d5-f114eea4a232.remotewd.com
    [PhishLLMLogger][DEBUG] Logo caption: the logo for sonicwall network security appliance
    [PhishLLMLogger][DEBUG] Logo OCR: SONICWALL Network Security Appliance Username
    [PhishLLMLogger][DEBUG] Industry: Technology
    [PhishLLMLogger][DEBUG] LLM prediction time: 0.9699530601501465
    [PhishLLMLogger][DEBUG] Detected brand: sonicwall.com
    [PhishLLMLogger][DEBUG] Domain sonicwall.com is valid and alive
    [PhishLLMLogger][DEBUG] CRP prediction: There is no confusing token. Then we find the keywords that are related to login: LOG IN. Additionally, the presence of "Username" suggests that this page requires credentials. Therefore, the answer would be A.
    [💥] Phishing discovered, phishing target is sonicwall.com
    [PhishLLMLogger][DEBUG] Folder ./datasets/field_study/2023-09-01/lp.aldooliveira.com
    [PhishLLMLogger][DEBUG] Logo caption: a black and white photo of the word hello world
    [PhishLLMLogger][DEBUG] Logo OCR: Hello world! Welcome to WordPress. This is your first post. Edit or delete it, then start writing! dezembro 2, 2021 publicado
    [PhishLLMLogger][DEBUG] Industry: Uncategorized
    [PhishLLMLogger][DEBUG] LLM prediction time: 0.8813009262084961
    [PhishLLMLogger][DEBUG] Detected brand: wordpress.com
    [PhishLLMLogger][DEBUG] Domain wordpress.com is valid and alive
    [PhishLLMLogger][DEBUG] CRP prediction: There is no token or keyword related to login or sensitive information. Therefore the answer would be B.
    [PhishLLMLogger][DEBUG] No candidate login button to click
     [✅] Benign
  </code></pre></details>
  
- Meanwhile, a txt file named "[today's date]_phishllm.txt" is being created, it has the following columns: 
  - "folder": name of the folder
  - "phish_prediction": "phish" | "benign"
  - "target_prediction": phishing target brand's domain, e.g. paypal.com, meta.com
  - "brand_recog_time": time taken for brand recognition
  - "crp_prediction_time": time taken for CRP prediction
  - "crp_transition_time": time taken for CRP transition -->

## (Optional) Use other versions of GPT

You can change the GPT model you want to use in the ``LLM_model`` argument in [param_dict.yaml](param_dict.yaml), default is "gpt-3.5-turbo-16k".
Please check the [list of GPT models](https://platform.openai.com/docs/models) you can use.

If you have any issues running our code, you can raise a Github issue.