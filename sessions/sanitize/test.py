import re

def sanitize_filename_v2(filename):
    # Replace spaces with a dash
    filename = filename.replace(' ', '-')
    # Remove any character that is not a-z, 0-9, dash, or period
    filename = re.sub(r'[^a-zA-Z0-9-.]', '', filename)
    return filename

# Define test cases
test_cases = [
    "normalfilename.txt",
    "file name with spaces.txt",
    "file-name-with-dashes.txt",
    "FILE NAME WITH UPPERCASE.TXT",
    "file_name_with_underscores.txt",
    "file-name-with-special-characters!@#$%^&*().txt",
    "1234567890.txt",
    "file   with   multiple   spaces.txt",
    "<>:\"/\\|?*filewithillegalchars.txt"
]

# Apply the updated sanitize_filename function to each test case
Ho
# Print the sanitized filenames
for original, sanitized in sanitized_filenames_v2.items():
    print(f"Original: {original} -> Sanitized: {sanitized}")
