# asn2cpp

`asn2cpp` is a command-line generator that turns ASN.1 modules into pairs of C++ headers and source files. It is built on top of the ANTLR4-generated lexer and parser shipped with the repository and emits modern C++17 structures ready for custom `encode` and `decode` implementations.

## Highlights

- Parses ASN.1 grammars and produces strongly-typed C++17 structs, enums, and `std::variant`-based CHOICE wrappers.
- Preserves existing `.cpp` implementations by default so manual logic in `encode`/`decode` functions is not overwritten.
- Supports header-only generation and configurable output directories to fit a variety of build layouts.

## Requirements

- Python 3.8 or newer
- `pip`
- Recommended: a Python virtual environment (`venv`) to isolate dependencies

Install the runtime dependencies once the virtual environment is active:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Setting up the environment

```bash
# Clone the repository
git clone https://github.com/gvtret/asn2cpp.git
cd asn2cpp

# Create and activate the virtual environment
python3 -m venv .venv
source .venv/bin/activate            # Linux / macOS
# .venv\Scripts\activate             # Windows PowerShell or CMD

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

To deactivate the environment later, run `deactivate`.

## Usage

The generator accepts a single ASN.1 module and writes C++ outputs alongside the module by default:

```bash
python asn2cpp.py asn/COSEMpdu.asn
```

Provide the `--output-dir` option to redirect the generated files elsewhere:

```bash
python asn2cpp.py asn/COSEMpdu.asn --output-dir build/generated
```

If you only need the header definitions and prefer to keep your own implementations, add `--header-only`:

```bash
python asn2cpp.py asn/COSEMpdu.asn --header-only
```

Existing implementation files are preserved unless `--overwrite-cpp` is specified.

## CLI reference

| Flag | Description |
| ---- | ----------- |
| `-o`, `--output-dir <path>` | Write generated `.hpp`/`.cpp` files to the specified directory (created if missing). |
| `--header-only` | Generate only header files. Existing `.cpp` files remain untouched. |
| `--overwrite-cpp` | Recreate the `.cpp` implementation even if it already exists. Ignored when `--header-only` is present. |
| `-h`, `--help` | Show the built-in help message with the complete option list. |

## Updating dependencies

When adding packages, update `requirements.txt` so teammates can reproduce the environment:

```bash
pip install <package>
pip freeze > requirements.txt
```

## Useful commands

```bash
pip list                 # List installed packages
pip list --outdated      # Check for updates
pip uninstall <package>  # Remove a package
```

## Author

asn2cpp was created and is maintained by Tretelnitskiy G. V. (aka "trgv").

