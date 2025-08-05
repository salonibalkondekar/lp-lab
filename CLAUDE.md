# LP Lab - AI-Assisted Operational Research Platform

## Project Overview

LP Lab is an innovative platform that democratizes linear programming by bridging the gap between business problems described in plain English and optimal mathematical solutions. The platform implements a unique two-tier approach that makes linear programming accessible to both business users and OR professionals.

**Latest Updates**:
- Fixed constraint parser to handle variables on both sides of inequalities
- Updated README with comprehensive installation instructions for UV, pip, and Docker
- Fixed Dockerfile UV command for proper dependency installation
- Added detailed troubleshooting guide for common setup issues

### Development Environment
- **Package Manager**: uv (fast Python package manager)
- **Virtual Environment**: `.venv` directory
- **Activation**: Use alias `act` for `source .venv/bin/activate`
- **Run Command**: `uv run main.py`
- **Access URL**: `http://0.0.0.0:8050/`

### Core Functionality

**Two-Tier Optimization System:**
1. **Tier 1 (AI Formulation)**: Converts natural language problem descriptions into proper Linear Programming format using Google's Gemini AI
2. **Tier 2 (Industrial Solving)**: Solves the formulated problems using industrial-strength solvers (PuLP/CBC and HiGHS)

## Technology Stack

### Frontend & UI
- **Dash 3.1+** - Python web application framework
- **Dash Mantine Components 2.1+** - Modern UI component library
- **Dash Iconify** - Icon system for intuitive UI
- **Plotly** - Interactive data visualization

### AI Integration
- **Google Gemini 2.5-pro** - AI model for problem formulation
- **Pydantic** - Data validation and structured output
- Custom prompt engineering with example-based learning

### Optimization Solvers
- **PuLP 3.2+** - Python Linear Programming library (uses CBC solver)
- **HiGHS** - High-performance optimization solver (via SciPy)
- **SciPy** - Scientific computing library

### Core Python Stack
- **Python 3.13+** - Modern Python runtime
- **NumPy & Pandas** - Numerical computing and data manipulation
- **SymPy** - Symbolic mathematics
- **python-dotenv** - Environment variable management

### Deployment & DevOps
- **Docker** - Containerization with Python 3.13-slim base
- **Gunicorn** - Production WSGI server
- **uv** - Fast Python package manager

## Project Architecture

```
lp-lab/
├── main.py                     # Application entry point
├── lp_optimizer/              # Main application package
│   ├── app.py                 # Dash application and routing
│   ├── config.py              # Configuration constants
│   ├── ai/                    # AI formulation system
│   │   ├── gemini_formulator.py  # Gemini integration
│   │   └── prompts.py         # AI prompt templates
│   ├── components/            # UI components
│   │   ├── input_panel.py     # Manual input interface
│   │   ├── nl_input_panel.py  # Natural language input
│   │   ├── results_panel.py   # Solution display
│   │   └── visualization_panel.py  # Graphical plotting
│   ├── solvers/               # Optimization engines
│   │   ├── pulp_solver.py     # PuLP/CBC solver
│   │   └── highs_solver.py    # HiGHS solver
│   ├── visualization/         # Plotting utilities
│   │   └── plotter.py         # Feasible region visualization
│   ├── utils/                 # Utility functions
│   │   ├── parser.py          # LP problem parsing (handles constants)
│   │   └── logger.py          # Centralized color-coded logging
│   └── examples/              # Problem library
│       └── problems.py        # Pre-defined examples
├── tests/                     # Comprehensive test suite
└── deployment configs         # Docker, Fly.io, Render
```

## Key Features

### 1. AI-Powered Problem Formulation
- Natural language problem description input
- Google Gemini AI converts text to mathematical formulation
- Contextual understanding of domain-specific terminology
- Structured output with variable descriptions and constraint explanations
- Handles complex problems with demand forecasting and penalties

### 2. Dual Solver Support
- **PuLP Solver**: Uses CBC (COIN-OR Branch and Cut) solver
- **HiGHS Solver**: High-performance optimization via SciPy
- Both solvers now properly handle constant terms in objective functions
- Comparative solving with consistent result format
- Detailed solver logs and performance metrics

### 3. Interactive Visualization
- 2D feasible region plotting for two-variable problems
- Shows optimal solution point
- Currently simplified (constraint visualization pending improvement)
- SVG/PNG export capabilities

### 4. Comprehensive UI Components
- **Manual Input Mode**: Direct objective function and constraint entry
- **AI Assistant Mode**: Natural language problem description
- **Example Library**: Pre-loaded problems (production, diet, transportation, portfolio)
- **Results Panel**: Solution display with variable values
- **Solver Log Panel**: Detailed optimization process output

### 5. Example Problem Library
- Production Planning (manufacturing optimization)
- Diet Problem (nutritional requirement minimization)
- Transportation Problem (shipping cost optimization)
- Portfolio Optimization (investment return maximization)
- Custom problem template

## Development Guidelines

### General Guidelines
- Follow consistent naming conventions
- Write self-documenting code with clear variable and function names
- Prefer composition over inheritance
- Use meaningful comments for complex business logic

### Code Style
- Use 2 spaces for indentation
- Use semicolons where appropriate
- Use double quotes for strings
- Use trailing commas in multi-line objects and arrays

### Architecture Principles
- Organize code by feature, not by file type
- Keep related files close together
- Use dependency injection for better testability
- Implement proper error handling
- Follow single responsibility principle

## Deployment Configuration

### Environment Variables
- `GEMINI_API_KEY` or `GOOGLE_API_KEY` - Required for AI features
- `PORT` - Application port (default: 8050)
- `DASH_DEBUG` - Development mode flag
- `LOG_LEVEL` - Logging level (default: DEBUG)
- `LOG_FILE` - Optional log file path

### Container Deployment
- Base image: Python 3.13-slim
- System dependencies: coinor-cbc solver for PuLP
- Package manager: uv for fast dependency resolution
- Production server: Gunicorn
- **Dockerfile Updated**: Fixed UV installation command from `uv pip install --system -r pyproject.toml` to `uv pip install --system .`
- Properly copies `lp_optimizer/` directory for all application code

## Testing Infrastructure

Comprehensive test suite covering:
- Unit tests for both solvers (PuLP and HiGHS)
- Integration tests for the Dash application
- Solver consistency comparison tests
- Error handling for malformed inputs
- Multi-variable problem testing
- Infeasible and unbounded problem scenarios

## Recent Fixes & Improvements

### Constraint Parser - Variables on Both Sides (Fixed - Latest)
**Problem**: Parser failed with "could not convert string to float: '3x1'" when constraints had variables on the right-hand side (e.g., "x2 >= 3x1")

**Solution**:
1. Updated `parse_constraint()` in `parser.py` to handle variables on both sides
2. Parser now moves all variables to the left-hand side automatically
3. Example: "x2 >= 3x1" is converted to "-3x1 + x2 >= 0"
4. Successfully handles carpenter problem with constraint "x2 >= 3x1"

### Objective Function Constants (Fixed)
**Problem**: Solver was ignoring constant terms in objective functions (e.g., "13x1 + 5x2 - 125" returned 468 instead of 343)

**Solution**:
1. Updated `parse_objective()` in `parser.py` to extract and return constant terms
2. Modified both HiGHS and PuLP solvers to add the constant back to the final objective value
3. Now correctly handles objectives like "Maximize 13x1 + 5x2 - 125"

### AI Formulation Error (Fixed)
**Problem**: "cannot access local variable 'json' where it is not associated with a value" error

**Solution**:
1. Removed duplicate `import json` statement inside method
2. Added comprehensive logging to track formulation process
3. Improved error handling with specific JSON parsing error messages

### JSON Serialization & Dynamic Components (Fixed)
**Problems**: 
1. "copy-to-manual-button" component not found in initial layout
2. Non-JSON serializable data (numpy types and MockProblem object) causing crashes

**Solutions**:
1. Added `suppress_callback_exceptions=True` to Dash app initialization
2. Created `convert_to_native()` function to convert numpy types
3. Removed non-serializable objects from solution data

### Duplicate Callback Outputs (Fixed)
**Problem**: Multiple callbacks trying to write to same outputs

**Solution**: 
1. Refactored to use central `solution-store` for data flow
2. Individual callbacks now listen to store changes
3. Follows proper Dash pattern

### UI Button Click Issue (Fixed)
**Problem**: Buttons were unclickable due to duplicate component IDs

**Solution**: Removed duplicate `ai-formulation-store` from `nl_input_panel.py`

## Known Issues & TODO

### Completed Recently
✅ **Constraint Parser Enhancement**: Now handles variables on both sides of inequalities
✅ **README Documentation**: Added comprehensive setup instructions for all installation methods  
✅ **Dockerfile Fix**: Corrected UV installation command and added missing directory copy
✅ **Objective Function Constants**: Solvers now properly handle constant terms

### High Priority
1. **Loading Indicator for AI Formulation**: Currently no visual feedback during AI processing
   - Button loading state exists but doesn't show during synchronous callback
   - Consider implementing background callbacks or progress indicators

2. **Visualization Improvements**: 
   - Currently only shows optimal point, not full feasible region
   - Need to restore constraint line visualization
   - Add objective function gradient direction

### Medium Priority
1. **Integer Programming Support**: Add support for integer/binary variables
2. **Sensitivity Analysis**: Add post-optimal analysis features
3. **Multi-objective Optimization**: Support for multiple objectives
4. **Better Error Messages**: More user-friendly error messages for constraint parsing failures

### Low Priority
1. **Export Features**: Add ability to export problems and solutions
2. **Problem Templates**: Expand library of example problems
3. **Collaboration Features**: Allow sharing of problems and solutions
4. **Performance Metrics**: Add detailed timing and memory usage statistics

## Installation & Setup

### Method 1: Using UV (Recommended)
```bash
# Clone the repository
git clone https://github.com/your-username/lp-lab.git
cd lp-lab

# Install UV if needed
pip install uv

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv sync

# Set up environment variables
cp .env.example .env
# Edit .env and add your Gemini API key

# Run the application
uv run python main.py
# Or simply: python main.py
```

### Method 2: Using Standard Python/pip
```bash
# Clone and enter directory
git clone https://github.com/your-username/lp-lab.git
cd lp-lab

# Create virtual environment
python -m venv venv  # or python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -e .

# Set up environment and run
cp .env.example .env
python main.py
```

### Method 3: Using Docker
```bash
# Clone repository
git clone https://github.com/your-username/lp-lab.git
cd lp-lab

# Build and run
docker build -t lp-lab .
docker run -p 8050:8050 -e GEMINI_API_KEY=your-api-key lp-lab
# Or with .env file:
docker run -p 8050:8050 --env-file .env lp-lab
```

### Quick Run (if already set up)
```bash
# Activate virtual environment
source .venv/bin/activate  # or use alias: act

# Run with uv
uv run main.py

# Access at
http://localhost:8050
```

### AI Formulation Tips
- Provide clear problem descriptions with all constraints
- Specify units and relationships clearly
- Include all penalty costs and demand constraints
- The AI handles complex formulations including demand forecasting

### Solver Selection
- **HiGHS**: Generally faster for larger problems
- **PuLP/CBC**: More detailed logging and diagnostics
- Both now correctly handle constant terms in objectives
- Both support constraints with variables on either side of inequalities

### Common Troubleshooting

**Python Version Issues**:
- Ensure Python 3.13+ is installed: `python --version`
- Download from [python.org](https://www.python.org/downloads/) if needed

**Virtual Environment Problems**:
- Windows: Enable script execution with `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
- macOS/Linux: Check shell compatibility (bash/zsh)

**Dependency Installation Failures**:
- UV: Try `uv pip install -e .` if `uv sync` fails
- pip: Install packages individually if batch install fails

**Port Conflicts**:
- Default port 8050 can be changed in main.py
- Find process using port: `lsof -i :8050` (macOS/Linux) or `netstat -ano | findstr :8050` (Windows)

## Logging System

Comprehensive color-coded logging system implemented in `utils/logger.py`:
- **Colors by Level**: DEBUG (Cyan), INFO (Green), WARNING (Yellow), ERROR (Red)
- **Component Colors**: Different colors for APP, UI, CALLBACK, SOLVER, AI modules
- **Features**: Timestamps, component tracking, function entry/exit logging
- **Configuration**: Set `LOG_LEVEL` and `LOG_FILE` environment variables

## Real-World Applications

The platform addresses optimization problems across multiple industries:
- **Supply Chain**: Transportation cost minimization, inventory optimization
- **Manufacturing**: Production planning with demand penalties, resource allocation
- **Finance**: Portfolio optimization, risk management
- **Healthcare**: Diet planning, staff scheduling
- **Logistics**: Route optimization, fleet management
- **Energy**: Power generation planning, grid optimization
