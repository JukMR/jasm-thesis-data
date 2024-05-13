import yaml


def load_yaml(filepath: str):
    with open(filepath, "r") as file:
        data = yaml.safe_load(file)
    return data


def generate_latex_table(data):
    id_to_filename = {
        "0.01": "logging_config.py",
        "0.02": "measure_performance.py",
        "0.03": "global_definitions.py",
        "1.01": "regex/yaml2regex.py",
        "1.02": "regex/file2regex.py",
        "1.03": "regex/tree_generators/deref_classes.py",
        "1.04": "regex/tree_generators/pattern_node_builder.py",
        "1.05": "regex/tree_generators/capture_group_index.py",
        "1.06": "regex/tree_generators/pattern_node_abstract.py",
        "1.07": "regex/tree_generators/pattern_node_tmp_untyped.py",
        "1.08": "regex/tree_generators/shared_context.py",
        "1.09": "regex/tree_generators/capture_manager.py",
        "1.10": "regex/tree_generators/pattern_node_type_builder/special_register_capture_group_type_builder.py",
        "1.11": "regex/tree_generators/pattern_node_type_builder/register_capture_group_builder.py",
        "1.12": "regex/tree_generators/pattern_node_type_builder/pattern_node_type_builder.py",
        "1.13": "regex/tree_generators/pattern_node_type_builder/capture_group_interface.py",
        "1.14": "regex/tree_generators/pattern_node_type_builder/operand_capture_group_builder.py",
        "1.15": "regex/tree_generators/pattern_node_implementations/time_type_builder.py",
        "1.16": "regex/tree_generators/pattern_node_implementations/node_branch_root.py",
        "1.17": "regex/tree_generators/pattern_node_implementations/deref.py",
        "1.18": "regex/tree_generators/pattern_node_implementations/mnemonic_and_operand/mnemonic_and_operand.py",
        "1.19": "regex/tree_generators/pattern_node_implementations/capture_group/capture_group_register.py",
        "1.20": "regex/tree_generators/pattern_node_implementations/capture_group/capture_group_instruction.py",
        "1.21": "regex/tree_generators/pattern_node_implementations/capture_group/capture_group_operand.py",
        "1.22": "regex/macro_expander/args_mapping_generator.py",
        "1.23": "regex/macro_expander/macro_args_resolver.py",
        "1.24": "regex/macro_expander/macro_expander.py",
        "2.01": "match/match.py",
        "2.02": "match/implementations/stream_consumer.py",
        "2.03": "match/implementations/consumer_builder.py",
        "2.04": "match/implementations/instruction_observer_consumer.py",
        "2.05": "match/implementations/matched_observers.py",
        "2.06": "match/implementations/complete_consumer.py",
        "2.07": "match/abstracts/i_matched_observer.py",
        "2.08": "match/abstracts/i_consumer.py",
        "3.01": "stringify_asm/implementations/observers.py",
        "3.02": "stringify_asm/implementations/shell_disassembler.py",
        "3.03": "stringify_asm/implementations/producer_builder.py",
        "3.04": "stringify_asm/implementations/null_disassembler.py",
        "3.05": "stringify_asm/implementations/composable_producer.py",
        "3.06": "stringify_asm/implementations/gnu_objdump/asm_manual_parser_w_regex.py",
        "3.07": "stringify_asm/implementations/gnu_objdump/gnu_objdump_disassembler.py",
        "3.08": "stringify_asm/implementations/gnu_objdump/gnu_objdump_parser_manual.py",
        "3.09": "stringify_asm/implementations/llvm_objdump/llvm_objdump_disassembler.py",
        "3.10": "stringify_asm/implementations/llvm_objdump/llvm_objdump_parser.py",
        "3.11": "stringify_asm/abstracts/asm_parser.py",
        "3.12": "stringify_asm/abstracts/disassembler.py",
        "3.13": "stringify_asm/abstracts/i_instruction_observer.py",
    }

    table1_rows = []
    table2_rows = []

    for file_path, metrics in data.items():
        # Raise error if any __init__ file
        if "__init__.py" in file_path:
            raise ValueError(f"File path {file_path} is an __init__.py file")

        # Remove `src/jasm/` from the file path
        if file_path.startswith("src/jasm/"):
            file_path = file_path[9:]

        file_id = get_file_id_from_path(file_path, id_to_filename)
        table1_rows.append(f'{file_id} & {" & ".join(map(lambda x: str(round(x, 2)), metrics.values()))} \\\\')
        table2_rows.append(f"{file_id} & {file_path} \\\\")

    line_break = "\n"
    table1 = (
        "\\begin{table}[H]\n"
        "    \\centering\n"
        "    \\tiny\n"
        "    \\begin{tabular}{\n"
        "    >{\\centering\\arraybackslash}p{0.3cm}| % ID column\n"
        "    *{4}{>{\\centering\\arraybackslash}p{0.3cm}}| % First 4 columns with adjusted width\n"
        "    *{8}{>{\\centering\\arraybackslash}p{1.3cm}} % Remaining columns\n"
        "    }\n"
        "    \\textbf{ID} & \\textbf{h1} & \\textbf{h2} & \\textbf{N1} & \\textbf{N2} & \\textbf{vocabulary} & \\textbf{length} & \\textbf{calculated length} & \\textbf{volume} & \\textbf{difficulty} & \\textbf{effort} & \\textbf{time} & \\textbf{bugs} \\\\ \\hline\n"
        f"    {f'{line_break}    '.join(table1_rows)}\n"
        "    \\end{tabular}\n"
        "    \\caption{Halstead: Métricas por IDs}\n"
        "    \\label{table:halstead_metrics_by_id}\n"
        "\\end{table}"
    )

    table2 = (
        "\\begin{table}[H]\n"
        "    \\centering\n"
        "    \\tiny\n"
        "    \\begin{tabular}{c|l}\n"
        "    \\textbf{ID} & \\textbf{Nombre de archivo} \\\\ \\hline\n"
        f"    {f'{line_break}'.join(table2_rows)}\n"
        "    \\end{tabular}\n"
        "    \\caption{Halstead: Mapeo entre Nombre de Archivos e ID}\n"
        "    \\label{table:halstead_id_to_filename}\n"
        "\\end{table}"
    )

    return table1, table2


def get_file_id_from_path(file_path: str, id_to_filename: dict[str, str]) -> str:

    assert "src/jasm/" not in file_path, f'File path {file_path} should not contain "src/jasm/" prefix'

    for elem in id_to_filename:
        if id_to_filename[elem] == file_path:
            return elem

    raise ValueError(f"File path {file_path} not found in id_to_filename")


def main():
    filepath = "hal_metrics.yml"
    data = load_yaml(filepath)
    table1, table2 = generate_latex_table(data)

    print(table1)
    print()
    print(table2)


if __name__ == "__main__":
    main()
