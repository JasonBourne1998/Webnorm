import re

def filter_logs(input_file, output_file):
    # 定义需要查找的字符串和时间格式的正则表达式
    required_text = "LoggingAspect: Execution of"
    Enter_text = "Entering in Method"
    time_pattern = r"\d{2}/[a-zA-Z]{3}/\d{4}:\d{2}:\d{2}:\d{2} \+\d{4}\.\d{10}"

    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            with open(output_file, 'w', encoding='utf-8') as output:
                for line in file:
                    # 检查是否含有指定的字符串和符合时间格式的文本
                    if required_text in line or Enter_text in line:
                        pattern = r"Request Headers: \{[^}]*\}"
                        new_line = re.sub(pattern, '', line)
                        output.write(new_line)
                    else:
                        if re.search(time_pattern, line) and ("/api/v1" in line ):
                            output.write(line)           
        print(f"Filtered logs have been written to {output_file}")
    except FileNotFoundError:
        print(f"Error: The file {input_file} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    input_file_path = '11.txt'
    output_file_path = '11_Filter.txt'

    filter_logs(input_file_path, output_file_path)
