# Local-RAG 🍎

Local-RAG is a nutrition analysis and information app that helps you understand the nutritional content of foods and get personalized nutrition advice through a conversational AI assistant.

## Features

- **Nutrition Analysis**: Get detailed nutritional information for thousands of foods
- **Custom Quantity Measurement**: Adjust portion sizes to see scaled nutrition values
- **Visualization**: View nutritional data in easy-to-understand charts
- **AI-Powered Conversation**: Ask nutrition-related questions and get informed responses
- **Search Foods**: Browse through a comprehensive database of common foods

## How It Works

Local-RAG combines structured data retrieval with local AI processing to provide nutrition information without dependency on cloud-based LLMs:

1. **Data Retrieval Layer**: 
   - Uses the USDA FoodData Central API to fetch accurate nutritional data
   - Organizes foods by categories for easy browsing
   - Scales nutrient values based on user-specified quantities

2. **Local AI Processing**:
   - Leverages Ollama to run a smaller, efficient LLM (llama3.2:1b) locally on your machine
   - Processes natural language queries about nutrition
   - Maintains context about previously analyzed foods
   - Generates responses based on scientific nutrition knowledge
   - Works completely offline once set up

3. **Interactive UI**:
   - Built with Streamlit for an intuitive, responsive interface
   - Provides both structured analysis and conversational modes
   - Visualizes nutrition data through interactive charts
   - Maintains conversation history for contextual responses

4. **Contextual Understanding**:
   - Remembers last analyzed food and quantity for follow-up questions
   - Uses system prompts to guide the AI toward nutrition-focused responses
   - Maintains conversation state between interactions

## Demo


![image](https://github.com/user-attachments/assets/9bd8ba7e-f62b-4de0-b7fb-14dde31b4784)
![image](https://github.com/user-attachments/assets/02ca334a-d70e-48d4-9829-07407bafcf0a)
![image](https://github.com/user-attachments/assets/c7101be1-3432-4488-9949-50b8a859bedc)
![image](https://github.com/user-attachments/assets/b566bbe7-66e9-4a84-a486-7953bffab0b2)
![image](https://github.com/user-attachments/assets/d0168988-65be-45f3-bb80-80c766dda8ea)




## Getting Started

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- USDA API Key (free to obtain)

### Installation

1. Clone this repository:
   ```
   git clone https://github.com/your-username/local-rag.git
   cd local-rag
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Get a USDA API Key:
   - Visit [USDA FoodData Central API](https://fdc.nal.usda.gov/api-key-signup.html) to sign up for free
   - Copy your API key

4. Add your API key to the project:
   - Open `main.py` in your preferred text editor
   - Replace the empty `API_KEY = ""` with your key: `API_KEY = "your-api-key-here"`

5. Install Ollama:
   - Follow the instructions at [Ollama's official website](https://ollama.ai/) to install Ollama
   - Pull the required model:
     ```
     ollama pull llama3.2:1b
     ```

### Running the App

Start the application with:
```
streamlit run main.py
```

The app should open automatically in your default web browser at `http://localhost:8501`.

## How to Use

### Nutrition Analysis Mode

1. Select "Nutrition Analysis" from the sidebar
2. Choose between "Select from List" or "Custom Food/Recipe"
3. For "Select from List", pick a food from the dropdown
4. For "Custom Food/Recipe", type the name of your food or dish
5. Adjust the quantity as needed (default is 1 serving)
6. Click "Analyze Nutrition" to see detailed information

### Conversational Mode

1. Select "Conversational Mode" from the sidebar
2. Type your nutrition-related questions in the chat input
3. Get AI-generated responses based on nutrition science
4. Previous conversations will be displayed above
5. Click "Clear Conversation" in the sidebar to start fresh

## Tips for Best Results

- Use specific food names for more accurate analysis
- When asking questions, be specific about the food or nutrient you're interested in
- Adjust quantities to match your actual portions
- Try comparing different foods by running multiple analyses

## Troubleshooting

**Error: API Key Invalid**
- Make sure you've correctly added your USDA API key to the code

**No Results Found**
- Try using more general terms (e.g., "apple" instead of "granny smith apple")
- Check your spelling

**Ollama Model Not Loading**
- Ensure Ollama is running in the background
- Verify you've pulled the correct model (`llama3.2:1b`)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- USDA FoodData Central for providing the nutrition database
- Streamlit for the web application framework
- Ollama for the local LLM capabilities
