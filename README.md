# Polypharmic Risk Score Analysis with Falcon LLM

<br />
<div align="center">
    <img src="assets/header.png" alt="Logo" >
</div>


## Overview

This Streamlit application leverages the Falcon LLM model to develop and demonstrate the "Polypharmic Risk Score," a novel metric aimed at integrating with polygenic risk scores to provide a more precise healthcare analysis. The Polypharmic Risk Score evaluates the potential risks and adverse health implications associated with over-the-counter medications taken over time.

## Features

- **Polypharmic Risk Score Calculation**: Analyzes the risk associated with common over-the-counter medications and their potential health impacts.
- **Falcon LLM Integration**: Utilizes the Falcon LLM model to process and analyze data.
- **AI71 API Key**: Integrated into the application for accessing Falcon LLM services.
- **Current Data Limitations**: Application is currently based on a limited set of common over-the-counter medications and illnesses.

## Future Enhancements

- **Expanded Data**: Future versions will include comprehensive medication-related data and patient-specific information to improve accuracy.
- **Broader Medication Coverage**: Plans to incorporate a wider range of over-the-counter medications and illnesses.

## Installation

To run this application locally, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/mstatt/phrs
   ```

2. **Navigate to the Project Directory**:
   ```bash
   cd polypharmic-risk-score-app
   ```

3. **Install Dependencies**:
   Make sure you have Python 3.8 or higher installed. Then, install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up API Key**:
   Replace `AI71_API_KEY = ""` in the `app.py` file with your AI71 API key.

5. **Run the Application**:
   ```bash
   streamlit run app.py
   ```

## Usage

1. Open the application in your browser at `http://localhost:8501`.
2. Select the initial the medication and the 2nd medication from the dropdowns.
3. Review the calculated Polypharmic Risk Score and the associated analysis.

## Limitations

- The current version of the application is limited by the healthcare data available and the scope of over-the-counter medications included.
- Access to more comprehensive healthcare data is required for enhanced accuracy and broader analysis.

## Contributing

Contributions are welcome! If you have suggestions or improvements, please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
