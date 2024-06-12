import os
import re
import sys

# Walks through the directory, deletes certain lines of code in Java source files 
# that contains Controller.java, Impl.java in the file name

directory = sys.argv[1]

pattern0 = r"import org.slf4j.Logger;\nimport org.slf4j.LoggerFactory;"
pattern1 = r"[^;{}]*\b(LOGGER.info|logger.info)\b.*?"
pattern2 = r"(?s)(?<=\b(LOGGER.info|logger.info)\b)[^;]*?;"
pattern3 = r"[^;{]*?\b(LOGGER|logger)\b(?!\.)\b.*?"
pattern4 = r"(?s)(?<=\b(LOGGER|logger)\b)(?!\.)(?![.\w])[^;]*?;"


for root, dirs, files in os.walk(directory):
    for file_name in files:
        file_path = os.path.join(root, file_name)
        # Delete the Controller and Impl
        if (all(keyword in file_name for keyword in ["Controller.java"]) or all(keyword in file_name for keyword in ["Impl.java"])) and \
            all(keyword not in file_name for keyword in ["Test"]): 

                with open(file_path, "r") as f:
                    content = f.read()

                modified_content = re.sub(pattern0, "", content, flags=re.DOTALL)
                modified_content = re.sub(pattern2, "", modified_content, flags=re.DOTALL)
                modified_content = re.sub(pattern1, "", modified_content, flags=re.DOTALL)
                modified_content = re.sub(pattern4, "", modified_content, flags=re.DOTALL)
                modified_content = re.sub(pattern3, "", modified_content, flags=re.DOTALL)

                with open(file_path, "w") as f:
                    f.write(modified_content)

print("Deletion completed!")

