import re
import os

def getCode(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            code = file.read()
            return code
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return
    except IOError as e:
        print(f"Error reading file: {e}")
        return


def find_mappings(file_content):
    mapping_with_value_regex = re.compile(
        r'@(GetMapping|PostMapping|PutMapping|DeleteMapping|RequestMapping)\s*\((?:[^)]*\bvalue\b\s*=\s*\{?\s*"([^"]+)"\s*\}?[^)]*)\)'
    )
    mapping_without_value_regex = re.compile(
        r'@(GetMapping|PostMapping|PutMapping|DeleteMapping|RequestMapping)\s*\(\s*\{?\s*\"([^\"]+)\"\s*\}?\s*\)'
    )

    mappings_with_value = mapping_with_value_regex.findall(file_content)
    mappings_without_value = mapping_without_value_regex.findall(file_content)

    all_mappings = mappings_with_value + mappings_without_value
    return all_mappings

def checkPublic(file_path):
    code = getCode(file_path)
    match_beofre = re.match(r'(.*?)public', code, re.DOTALL)
    match_after = re.search(r'public(.*)', code, re.DOTALL)

    if match_beofre:
        code_before_public = match_beofre.group(1)
        code_after_public = match_after.group(1)
    else:
        code_after_public = code
        code_before_public = code
    mappings = find_mappings(code_after_public)
    mapping_before = find_mappings(code_before_public)
    if len(mapping_before) == 1 :
        for mapping in mappings:
            if mapping[1].startswith("/"):
                new_pattern = mapping_before[0][1] + mapping[1]
            else:
                new_pattern = mapping_before[0][1] + "/" + mapping[1]
            print(new_pattern)
    else:
        for mapping in mappings:
            pass
            print(mapping[1])

def findFile(project_dir):
    for root, dirs, files in os.walk(project_dir):
        for file in files:
            # print(file)
            if file.endswith('.java'):
                file_path = os.path.join(root, file)
                checkPublic(file_path)


if __name__ == "__main__":
    project_dir = "文件目录"
    restful = findFile(project_dir)
