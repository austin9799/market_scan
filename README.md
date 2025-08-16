# MarketMunch: Restaurant Market Analyzer

A powerful AI-powered tool for analyzing restaurant market opportunities using Google's Gemini AI and web search capabilities.

## Features

- 🍽️ Comprehensive market analysis for restaurant concepts
- 🔍 Real-time web search integration
- 📊 Detailed financial modeling and cost analysis
- 🌍 Multi-region support with local market insights
- 📱 Streamlit-based web interface

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configuration

The application requires an LLM API key to function. Follow these steps:

1. **Copy the template configuration:**

   ```bash
   cp src/constants/config_template.py src/constants/config.py
   ```

2. **Edit the configuration file:**

   ```bash
   # Open src/constants/config.py and replace:
   LLM_API_KEY = "YOUR_LLM_API_KEY_HERE"
   # with your actual API key
   ```

3. **Get your API key:**
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Copy the key to your `config.py` file

### 3. Run the Application

```bash
streamlit run main.py
```

## Usage

1. Enter your cuisine type and city (e.g., "Italian in New York")
2. The AI will analyze:

   - Dining culture and preferences
   - Regulatory requirements
   - Supply chain feasibility
   - Customer segments and pricing
   - Financial modeling data
   - Risks and recommendations

3. Download your analysis report as HTML

## Architecture

- **Frontend**: Streamlit web interface
- **AI Backend**: Google Gemini 2.0 Flash with web search
- **Configuration**: Centralized config management
- **Modular Design**: Separated concerns for maintainability

## Security Notes

- The `config.py` file is gitignored to prevent API key exposure
- Never commit your actual API keys to version control
- Use environment variables in production deployments

## Requirements

- Python 3.8+
- Streamlit
- Google GenAI
- Markdown