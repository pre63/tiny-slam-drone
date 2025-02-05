#!/usr/bin/env python3
import os
import sys
import json
import subprocess
import time
from openai import OpenAI

def approximate_token_count(text):
    return len(text) // 4

def truncate_text(text, max_tokens):
    max_chars = max_tokens * 4
    if len(text) > max_chars:
        return text[:max_chars] + "\n... (truncated)"
    return text

def get_project_tree():
    tree_lines = []
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    for dirpath, dirnames, filenames in os.walk(root_dir):
        rel_dir = os.path.relpath(dirpath, root_dir)
        if rel_dir.split(os.sep)[0] == "autocoder" or rel_dir.startswith("."):
            continue
        indent = "  " * (rel_dir.count(os.sep) if rel_dir != "." else 0)
        tree_lines.append(f"{indent}{os.path.basename(dirpath)}/")
        for filename in filenames:
            if filename.startswith("."):
                continue
            tree_lines.append(f"{indent}  {filename}")
    return "\n".join(tree_lines)

def read_file_contents(file_path, max_tokens=1024):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return truncate_text(content, max_tokens)
    except Exception:
        return ""

def read_readme():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    for name in ['README.md', 'README']:
        path = os.path.join(root_dir, name)
        if os.path.isfile(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return f.read()
            except Exception:
                return ""
    return ""

def call_llm(prompt, config):
    client = OpenAI(
        base_url=config.get("api_url", "http://localhost:8080/v1"),
        api_key=config.get("api_key", "sk-no-key-required")
    )
    payload = {
        "model": config.get("model", "LLaMA_CPP"),
        "messages": [
            {"role": "system", "content": config.get(
                "system_prompt",
                "You are an autonomous coding assistant whose goal is to fix issues and complete the project as specified in the README."
            )},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": config.get("max_tokens", 2048)
    }
    print("DEBUG: Sending payload:")
    print(json.dumps(payload, indent=2))
    try:
        response = client.chat.completions.create(**payload)
        print("DEBUG: Received response:")
        print(json.dumps(response, indent=2))
        return response.choices[0].message.content
    except Exception as e:
        print("DEBUG: Exception during LLM call:")
        print(str(e))
        return f"Error: {str(e)}"

def parse_plan(plan_text):
    commands = []
    edits = []
    for line in plan_text.splitlines():
        line = line.strip()
        if line.startswith("CMD:"):
            commands.append(line[4:].strip())
        elif line.startswith("EDIT:"):
            parts = line[5:].strip().split(maxsplit=1)
            if len(parts) == 2:
                edits.append((parts[0], parts[1]))
    return commands, edits

def parse_requested_files(response_text):
    files = []
    for line in response_text.splitlines():
        line = line.strip()
        if line:
            files.append(line)
    return files

def read_requested_files(file_list):
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    contents = {}
    for rel_path in file_list:
        full_path = os.path.join(root_dir, rel_path)
        if os.path.isfile(full_path):
            contents[rel_path] = read_file_contents(full_path, max_tokens=1024)
    return contents

def build_file_contents_message(requested_files_contents):
    lines = []
    for rel_path, content in requested_files_contents.items():
        lines.append(f"File: {rel_path}\n{content}\n")
    return "\n".join(lines)

def execute_commands(commands):
    for cmd in commands:
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(result.stderr)
        except Exception as e:
            print(f"Command error: {str(e)}")

def apply_edits(edits):
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    for filepath, instruction in edits:
        full_path = os.path.join(root_dir, filepath)
        if not os.path.isfile(full_path):
            continue
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            content += f"\n# TODO: {instruction}\n"
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            print(f"Edit error in {filepath}: {str(e)}")

def generate_commit_message(config):
    # Get the git patch for staged changes.
    diff_result = subprocess.run("git diff --cached", shell=True, capture_output=True, text=True)
    diff_output = diff_result.stdout.strip()
    if not diff_output:
        return None
    # Ask the LLM to generate an informative commit message based on the git patch.
    prompt = "Based on the following git diff patch, generate an informative commit message:\n" + diff_output
    commit_message = call_llm(prompt, config)
    return commit_message.strip()

def git_commit(config):
    subprocess.run("git add .", shell=True, capture_output=True, text=True)
    commit_message = generate_commit_message(config)
    if not commit_message:
        print("DEBUG: No changes to commit.")
        return
    print(f"DEBUG: Generated commit message: {commit_message}")
    try:
        subprocess.run(f'git commit -m "{commit_message}"', shell=True, capture_output=True, text=True)
    except Exception as e:
        print(f"Git error: {str(e)}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 script.py <api_config_file>")
        sys.exit(1)
    config_file = sys.argv[1]
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except Exception as e:
        print(f"Error loading config file: {str(e)}")
        sys.exit(1)
    iteration = 0
    max_prompt_tokens = config.get("max_prompt_tokens", 1024)
    while True:
        iteration += 1
        print(f"\n--- Iteration {iteration} ---")
        project_tree = get_project_tree()
        tree_message = f"Project tree:\n{project_tree}"
        # Ask LLM which files it needs.
        request_prompt = tree_message + "\n\nGoal: List the relative file paths you need to see to complete the project. Provide one file per line."
        file_request_response = call_llm(request_prompt, config)
        print("DEBUG: LLM file request response:")
        print(file_request_response)
        requested_files = parse_requested_files(file_request_response)
        print("DEBUG: Parsed requested files:")
        print(requested_files)
        # Read requested files' contents.
        requested_files_contents = read_requested_files(requested_files)
        file_contents_message = build_file_contents_message(requested_files_contents)
        readme = read_readme()
        # Build a fresh prompt with the project tree, file contents, and README.
        final_prompt = (
            tree_message +
            "\n\nFile contents provided as requested:\n" + file_contents_message +
            "\n\nREADME:\n" + readme +
            "\n\nGoal: Based on the provided project tree, file contents, and README, produce a plan with commands (prefixed with CMD:) and edits (prefixed with EDIT: <filepath> <instruction>). If the plan is too ambitious, include TODO comments for later completion."
        )
        token_count = approximate_token_count(final_prompt)
        print(f"DEBUG: Approximate token count of final prompt: {token_count}")
        final_prompt = truncate_text(final_prompt, max_prompt_tokens)
        plan = call_llm(final_prompt, config)
        print("Plan:\n", plan)
        commands, edits = parse_plan(plan)
        if commands:
            execute_commands(commands)
        if edits:
            apply_edits(edits)
        # After applying changes, ask the LLM for an informative commit message using the git patch.
        git_commit(config)
        time.sleep(10)

if __name__ == "__main__":
    main()
