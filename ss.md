# Tool Documentation: `write_files_from_snapshot`

## Overview

The `write_files_from_snapshot` tool is a powerful utility designed to write multiple files and their content to the filesystem from a single, formatted string. This string, referred to as a "snapshot," contains both the file paths and the line-by-line content for each file.

This tool is located in `swe_tools/codebase_restorer.py`. Its primary function is to allow the AI to perform batch file creation or modification operations efficiently. When executed, it parses the snapshot string, creates any necessary directories, and then writes the content to the specified files.

**CRITICAL:** This tool performs a complete overwrite. If a file specified in the snapshot already exists, its current content will be **entirely replaced**. If the file does not exist, it will be created. This is a destructive operation and should be used with caution.

## How it Works

The tool takes a single string (`input_snapshot_content`) as its main input. This string is parsed by a utility function (`parse_multiline_commands`) which extracts the file paths and their corresponding content.

For each file in the parsed snapshot:
1.  It constructs the full destination path.
2.  It ensures the parent directory for the file exists, creating it if necessary.
3.  It opens the file in write mode (`'w'`), erasing any existing content.
4.  It writes the new content line by line into the file.
5.  It compiles a report detailing which files were written successfully and which failed.

## Input Parameters

-   **`input_snapshot_content`** (string, required): The snapshot string containing the file data. The format is very specific and must be followed exactly.
-   **`output_directory`** (string, optional): The base directory where files will be written. It defaults to the project's root directory (`.`).

## Snapshot Input Format

The `input_snapshot_content` string has a strict format that must be adhered to for the tool to work correctly.

-   Each file's section must begin with a line starting with a dollar sign (`$`) followed immediately by the file path (e.g., `$path/to/your/file.py`).
-   The subsequent lines contain the content for that file. Each line must start with a line number, followed by a colon (`:`), a space, and then the actual line content.
-   The line numbering should be sequential for each file.

### Format Template

```
$path/to/first_file.ext
1: content for line 1 of the first file
2: content for line 2 of the first file
...
$path/to/second_file.ext
1: content for line 1 of the second file
2: content for line 2 of the second file
...
```

---

## Usage and Scenarios

### Scenario 1: Creating Multiple New Files

This example shows how to create two new Python files, `greetings.py` and `main.py`, inside a new `app` directory.

**Example `input_snapshot_content`:**

```python
input_content = """
$app/greetings.py
1: def say_hello(name):
2:     return f"Hello, {name}!"
3: 
4: def say_goodbye(name):
5:     return f"Goodbye, {name}."
$app/main.py
1: from greetings import say_hello
2: 
3: if __name__ == "__main__":
4:     print(say_hello("World"))
"""

# Tool call by the AI
write_files_from_snapshot(input_snapshot_content=input_content)
```

**Explanation:**

-   The tool will first parse the `input_content` string.
-   It will identify two files to be created: `app/greetings.py` and `app/main.py`.
-   It will create the `app/` directory because it doesn't exist.
-   It will then create `greetings.py` and write the 5 lines of specified content into it.
-   Finally, it will create `main.py` and write its 4 lines of content.

### Scenario 2: Modifying an Existing File and Creating a New One

This example shows how to overwrite an existing configuration file and add a new script.

**Example `input_snapshot_content`:**

```python
input_content = """
$config/settings.json
1: {
2:   "theme": "dark",
3:   "notifications": "enabled"
4: }
$scripts/deploy.sh
1: #!/bin/bash
2: echo "Deploying application..."
3: # Add deployment commands here
"""

# Tool call by the AI
write_files_from_snapshot(input_snapshot_content=input_content)
```

**Explanation:**

-   The tool will parse the string.
-   It will find the existing file `config/settings.json` and **completely replace its content** with the new JSON structure.
-   It will then create a new directory `scripts/` and a new file `deploy.sh` inside it with the specified shell script content.

### Scenario 3: Error Handling

If the input string is malformed or an error occurs during file writing, the tool will report it.

**Example of invalid input:**

```python
# Missing the '$' prefix for the file path
input_content = """
path/to/file.txt
1: This will fail.
"""

# Tool call
write_files_from_snapshot(input_snapshot_content=input_content)
```

**Potential Output:**

```
"Restorer finished. Created/modified 0 files.
Error writing file path/to/file.txt: [Some specific OS error]"
```
Or, depending on the parser's implementation:
```
"Error: Input snapshot content is empty or invalid."
```