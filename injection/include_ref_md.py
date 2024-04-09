from pathlib import Path
import re
import sys
import logging


def process_file(input_file: Path, output_file: Path, partials_dir: Path):
    """
    Process the specified input file, replacing render tags with referenced content
    and saving the modified content to the output file.

    Parameters:
        input_file (Path): Path to the input file to be processed.
        output_file (Path): Path to the output file to save the processed content.
        partials_dir (Path): Path to the directory containing partial files referenced in the input file.
    """
    # Read the content of the file
    with open(input_file, 'r') as file:
        content = file.read()

    # Define a regular expression pattern to match '{{<render file="filename.md">}}' format
    pattern = r'{{<render file="([^"]+)"\>}}'

    # Find all matches of the pattern in the content
    matches = re.findall(pattern, content)

    # Replace each match with the content of the referenced file
    for match in matches:
        referenced_file_path = partials_dir / match

        if not referenced_file_path.exists():
            logging.warning(f"Referenced file '{referenced_file_path}' not found for '{input_file}'. Skipping...")
            continue

        with open(referenced_file_path, 'r') as referenced_file:
            referenced_content = referenced_file.read()
            content = content.replace('{{<render file="%s">}}' % match, referenced_content)

    # Remove content between opening and closing curly brackets
    content = re.sub(r'{{[^}]*}}', '', content)

    # Define the patterns for each block to remove
    block_patterns = [
        r'(-{3}\n)(title|pcx_content_type|_build|filename)(.|\s)*?-{3}'
    ]

    # Remove each block from the content
    for pattern in block_patterns:
        content = re.sub(pattern, '', content, flags=re.DOTALL)

    # Remove remaining horizontal lines
    content = re.sub(r'\n---\n', '', content)

    # Remove extra new lines
    content = re.sub(r'\n+', '\n', content).strip()

    # Create the output directory if it doesn't exist
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Write the modified content to the new file
    with open(output_file, 'w') as new_file:
        new_file.write(content)

    logging.info(f"File '{input_file}' processed successfully. New file saved as '{output_file}'.")


def process_directory(input_path: Path, output_path: Path, exclude_directories: list, partials_dir: Path):
    """
    Recursively process the specified directory, processing each file within it.

    Parameters:
        input_path (Path): Path to the directory to be processed.
        output_path (Path): Path to the output directory to save the processed files.
        exclude_directories (list): List of directories to be excluded from processing.
        partials_dir (Path): Path to the directory containing partial files referenced in the input files.
    """
    for source in input_path.rglob('*.md'):
        subpath = source.relative_to(input_path)
        # Check if the first part of the subpath matches any excluded directory
        if any(part == exclude_dir for exclude_dir in exclude_directories for part in subpath.parts):
            logging.info(f"Skipping directory: {subpath}")
            continue

        destination = output_path / subpath
        process_file(source, destination, partials_dir)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    if len(sys.argv) < 3:
        print("Usage: python replace_render_tags.py <input_path> <output_path> [exclude_directories...]")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    # List of directories to exclude
    exclude_directories = sys.argv[3:]

    # Default directories to exclude
    default_exclude_directories = ["_partials", "scripts", "platform", "tutorials"]

    # Always include output_path in the list of excluded directories
    exclude_directories.append(str(output_path))

    # Combine default and additional exclude directories
    exclude_directories += default_exclude_directories

    # Traverse the input_path to find the _partials directory
    partials_dir = None
    for item in input_path.iterdir():
        if item.is_dir() and item.name == '_partials':
            partials_dir = item
            break

    if not partials_dir:
        logging.warning("'_partials' directory not found within the input path. Exiting...")
#         sys.exit(1)

    if input_path.is_file():
        process_file(input_path, output_path, partials_dir)
    else:
        process_directory(input_path, output_path, exclude_directories, partials_dir)
