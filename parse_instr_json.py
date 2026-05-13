import json
import pprint

file_name = input("Enter file name: ")

with open(file_name, "r") as f:
    data = json.load(f)

field_names = []
for i in data:
    field_names.append(i)

# unique extensions
extensions = []
for i in field_names:
    if (data[i]["extension"]) not in extensions:
        extensions.append(data[i]["extension"])

# print(extensions)

# categorise extensions
extensions_instr = []
for i in extensions:
    container = []
    for j in field_names:
        if i == data[j]["extension"]:
            # print(j)
            container.append(j)
    extensions_instr.append(container)

# print(store_extensions)
# with open("raw_text.txt","w") as raw_file:
#    for i in range(0, len(store)):
#        raw_file.write(f"{store[i]} | {len(store_extensions[i])} instructions | {store_extensions[i][0]}")


def print_riscv_table_strict(data):
    """Print perfectly aligned table with strict spacing"""

    if isinstance(data, str):
        lines = [line.strip() for line in data.strip().split("\n") if line.strip()]
    else:
        lines = data

    # Parse rows
    rows = []
    for line in lines:
        parts = [x.strip() for x in line.split("|")]
        if len(parts) == 3:
            rows.append((parts[0], parts[1], parts[2]))

    if not rows:
        print("No data to display.")
        return

    # Calculate maximum widths
    max_ext = max(len(row[0]) for row in rows)
    max_count = max(len(row[1]) for row in rows)
    max_inst = max(len(row[2]) for row in rows)

    # Set strict minimum widths for good looks
    col1 = max(max_ext, 55)  # Extensions
    col2 = max(max_count, 6) + 2  # Count
    col3 = max(max_inst, 12)  # Instruction

    # Header
    header = f"{'Extensions':<{col1}} {'Count':<{col2}} {'Instruction':<{col3}}"
    separator = "-" * len(header)

    print("\n" + separator)
    print(header)
    print(separator)

    # Data rows with strict formatting
    for ext, count, inst in rows:
        print(f"{ext:<{col1}} {count:<{col2}} {inst:<{col3}}")

    print(separator)
    print(f"Total Extension categories: {len(rows)}\n")


raw_file = []
for i in range(0, len(extensions)):
    raw_file.append(
        f"{extensions[i]} |{len(extensions_instr[i])} | {extensions_instr[i][0]}\n"
    )

# print_riscv_table_strict(raw_file)

# print(field_names)

# print(extensions_instr)
# print(len(field_names))


# determine instructions with more than one extension
def multiple_extensions():
    # inst with multiple extensions
    mul_ext = []
    combinations = []
    for i in field_names:
        if len(data[i]["extension"]) > 1:
            mul_ext.append(i)
            combinations.append((i, data[i]["extension"]))
    return mul_ext, combinations


mul_ext, combinations = multiple_extensions()
print(mul_ext)
pprint.pprint(combinations)
