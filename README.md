# LP Lab - AI-Assisted Operational Research Platform

**Transform business problems into optimal solutions using AI-powered formulation and industrial-strength solvers**

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://www.python.org)
[![Dash](https://img.shields.io/badge/Dash-2.x-green.svg)](https://dash.plotly.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

## 🚀 Bridging the Gap Between Business Problems and Mathematical Optimization

LP Lab is an innovative two-tier system that democratizes operational research by making linear programming accessible to everyone - from business analysts to OR experts.

### The Two-Tier Approach

```
┌─────────────────────────┐     ┌─────────────────────────┐     ┌─────────────────────────┐
│   Plain English         │     │   AI Formulation        │     │   Optimal Solution      │
│   Business Problem      │ --> │   (Powered by Gemini)   │ --> │   (PuLP/HiGHS Solver)   │
│                         │     │                         │     │                         │
│ "We need to minimize    │     │ Min Z = 2x₁ + 3x₂       │     │ x₁ = 45.0               │
│  shipping costs while   │     │ s.t. x₁ + x₂ ≥ 100      │     │ x₂ = 55.0               │
│  meeting all demands"   │     │      x₁ ≤ 60, x₂ ≤ 80   │     │ Min Cost = $255         │
└─────────────────────────┘     └─────────────────────────┘     └─────────────────────────┘
       TIER 1: AI                    FORMULATION                  TIER 2: SOLVER
```

## ✨ Why AI-Assisted Operational Research?

### For Business Users
- **No Math Required**: Describe your problem in plain English
- **Instant Formulation**: AI converts your description into proper LP format
- **Clear Explanations**: Understand what each constraint means
- **Real-World Examples**: Learn from production, diet, transportation, and portfolio problems

### For OR Professionals
- **Rapid Prototyping**: Quickly test different problem formulations
- **Focus on Insights**: Spend less time on syntax, more on analysis
- **Educational Tool**: Help stakeholders understand OR concepts
- **Extensible Platform**: Easy to add new solvers or algorithms

## 🎯 Key Features

### 🤖 AI-Powered Problem Formulation (Tier 1)
- **Natural Language Input**: Describe optimization problems in plain English
- **Intelligent Parsing**: AI identifies variables, objectives, and constraints
- **Contextual Understanding**: Handles domain-specific terminology
- **Formulation Explanation**: Get detailed explanations for each component

### 🔧 Industrial-Strength Solving (Tier 2)
- **Multiple Solvers**: PuLP (CBC) and HiGHS support
- **Robust Solutions**: Battle-tested algorithms for reliable results
- **Performance Insights**: Detailed solver logs and statistics
- **Scalable**: Handles problems from simple to complex

### 📊 Visualization & Analysis
- **Interactive Graphs**: Visualize feasible regions and optimal points (2D problems)
- **Solution Analysis**: Clear display of variable values and objective function
- **Export Options**: Save visualizations as SVG or PNG
- **Sensitivity Reports**: Understand solution robustness

## 🚀 Quick Start

### Prerequisites
- Python 3.13 or higher
- Git (for cloning the repository)
- Optional: UV package manager (recommended for faster installation)

## 📦 Installation & Setup

Choose one of the following methods:

### Method 1: Using UV (Recommended)

UV is a fast Python package installer and resolver. It's the recommended way to set up this project.

```bash
# 1. Clone the repository
git clone https://github.com/your-username/lp-lab.git
cd lp-lab

# 2. Install UV if you haven't already
pip install uv

# 3. Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv sync

# 4. Set up environment variables
cp .env.example .env
# Edit .env and add your Gemini API key (get it from https://aistudio.google.com/apikey)

# 5. Run the application
uv run python main.py
# Or simply:
python main.py
```

### Method 2: Using Standard Python/pip

```bash
# 1. Clone the repository
git clone https://github.com/your-username/lp-lab.git
cd lp-lab

# 2. Create a virtual environment
python -m venv venv
# Or use python3 if python points to Python 2.x
python3 -m venv venv

# 3. Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# 4. Upgrade pip and install dependencies
pip install --upgrade pip
pip install -e .

# 5. Set up environment variables
cp .env.example .env
# Edit .env and add your Gemini API key (get it from https://aistudio.google.com/apikey)

# 6. Run the application
python main.py
```

### Method 3: Using Docker

Docker provides a containerized environment, ensuring consistency across different systems.

```bash
# 1. Clone the repository
git clone https://github.com/your-username/lp-lab.git
cd lp-lab

# 2. Build the Docker image
docker build -t lp-lab .

# 3. Run the container
# With environment variable:
docker run -p 8050:8050 -e GEMINI_API_KEY=your-api-key-here lp-lab

# Or with .env file:
docker run -p 8050:8050 --env-file .env lp-lab
```

### 🔧 Troubleshooting

**Python Version Issues:**
- Ensure you have Python 3.13 or higher: `python --version`
- If not, install from [python.org](https://www.python.org/downloads/)

**Virtual Environment Not Activating:**
- On macOS/Linux, ensure you're using the correct shell (bash/zsh)
- On Windows, you may need to enable script execution: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

**Missing Dependencies:**
- If `uv sync` fails, try `uv pip install -e .`
- For pip users, if `-e .` fails, try `pip install dash dash-mantine-components dash-iconify plotly pandas numpy scipy pulp sympy python-dotenv google-genai`

**Port Already in Use:**
- If port 8050 is busy, modify `main.py` to use a different port
- Or find and stop the process using port 8050

### ✅ Verify Installation

After setup, verify everything is working:

1. Open your browser to `http://localhost:8050`
2. You should see the LP Lab interface
3. Try the "Production Planning" example from the dropdown
4. If using AI features, test the "AI Assistant" tab

## 📖 How It Works

### Step 1: Describe Your Problem
Write a natural language description of your optimization challenge:

```
"A factory produces two products using two machines. Each unit of Product A 
requires 50 minutes on Machine 1 and 30 minutes on Machine 2. Product B needs 
24 minutes on Machine 1 and 33 minutes on Machine 2. We have 40 hours available 
on Machine 1 and 35 hours on Machine 2. We need to meet minimum demands of 45 
units for Product A and 5 units for Product B. How do we maximize production?"
```

### Step 2: AI Formulation
The AI analyzes your description and generates:

**Variables:**
- `x = units of Product A to produce`
- `y = units of Product B to produce`

**Objective:**
- `Maximize Z = x + y`

**Constraints:**
- `50x + 24y ≤ 2400` (Machine 1 capacity)
- `30x + 33y ≤ 2100` (Machine 2 capacity)
- `x ≥ 45` (Product A demand)
- `y ≥ 5` (Product B demand)

### Step 3: Optimal Solution
The solver finds the best solution:
- `x = 45.0 units of Product A`
- `y = 6.25 units of Product B`
- `Maximum production = 51.25 units`

## 🏭 Real-World Applications

LP Lab helps solve optimization problems across industries:

- **📦 Supply Chain**: Minimize transportation costs, optimize inventory
- **🏭 Manufacturing**: Production planning, resource allocation
- **💰 Finance**: Portfolio optimization, risk management
- **🥗 Healthcare**: Diet planning, staff scheduling
- **🚚 Logistics**: Route optimization, fleet management
- **⚡ Energy**: Power generation planning, grid optimization

## 📚 Example Problems

The platform includes pre-loaded examples:

1. **Production Planning**: Maximize output with limited machine time
2. **Diet Problem**: Minimize cost while meeting nutritional requirements
3. **Transportation**: Minimize shipping costs across warehouses
4. **Portfolio Optimization**: Maximize returns within risk constraints

## 🔄 Workflow Modes

### AI Assistant Mode (Recommended)
1. Click the "AI Assistant" tab
2. Describe your problem in natural language
3. Review the AI-generated formulation
4. Click "Use in Manual Input" to solve

### Manual Input Mode
1. Enter objective function directly
2. Add constraints line by line
3. Solve and analyze results

## 🛠️ Technical Stack

- **Frontend**: Dash + Dash Mantine Components
- **AI Engine**: Google Gemini API
- **LP Solvers**: PuLP (CBC), HiGHS
- **Visualization**: Plotly
- **Server**: Gunicorn

## 🚀 Deployment

### Docker
```bash
docker build -t lp-lab .
docker run -p 8050:8050 -e GEMINI_API_KEY=your-key lp-lab
```

### Cloud Platforms
- **Render**: Use included `render.yaml`
- **Fly.io**: Use included `fly.toml`

## 🌟 Future Enhancements

- [ ] Support for integer programming
- [ ] Multi-objective optimization
- [ ] Sensitivity analysis reports
- [ ] Problem templates library
- [ ] Collaboration features
- [ ] API endpoints for programmatic access

## 🤝 Contributing

We welcome contributions! Areas of interest:
- New solver integrations
- Additional AI models
- Industry-specific templates
- Visualization improvements

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details

---

<div align="center">

**Making Operational Research Accessible to Everyone**

[Report Issue](https://github.com/your-repo/issues) • [Documentation](docs/) • [Examples](examples/)

</div>