# CF-Analyzer

CF-Analyzer is a Python-based tool that provides detailed analytics and visualizations for Codeforces user profiles. It analyzes problem-solving patterns, submission statistics, and rating history to give users comprehensive insights into their Codeforces performance.

## Features

- **Problem Analysis**
  - Distribution of problem ratings
  - Problem tags frequency analysis
  - Submission verdict statistics (AC, WA, TLE, etc.)
  - Time and memory consumption patterns

- **Performance Metrics**
  - Overall success rate
  - Programming language preferences
  - Problem-solving patterns by difficulty index
  - Rating history visualization

## Requirements

- Python 3.8+
- Required Python packages:
  ```
  pandas
  numpy
  seaborn
  matplotlib
  requests
  ```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Al-mizan/CF-Analyzer.git
cd CF-Analyzer
```

2. Install required packages.

## Usage

1. Run the main script with your Codeforces handle:
```python
python main.py
```

2. The script will generate various visualizations including:
   - Tag frequency distribution
   - Memory consumption distribution
   - Time consumption distribution
   - Time vs Memory scatter plot
   - Problem rating distribution
   - Verdict distribution
   - Solving time distribution
   - Problems solved by index

## Visualizations

The tool generates several types of visualizations:

1. **Tag Distribution**: Bar plot showing the frequency of different problem tags
2. **Memory Usage**: Pie chart showing the distribution of memory consumption
3. **Time Analysis**: Pie chart and histogram showing time consumption patterns
4. **Performance Analysis**: Various plots showing:
   - Rating distribution
   - Verdict distribution
   - Solving time patterns
   - Problem index distribution

## Project Structure

```
CF-Analyzer/
├── main.py                    # Main script
├── codeforces_problems.py     # Problem data fetching
├── codeforces_rating_history.py # Rating history functionality
└── README.md                 # Project documentation
```

## Data Collection

The tool uses the Codeforces API to collect:
- User submission data
- Problem information
- Rating history
- Contest participation details

## Data Processing

1. **Data Cleaning**
   - Removes duplicate submissions
   - Handles missing values
   - Standardizes data formats

2. **Feature Engineering**
   - Creates memory consumption categories
   - Creates time consumption categories
   - Processes problem tags

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Codeforces for providing the API
- Contributors to the Python data science ecosystem

## Contact

For any queries or suggestions, please open an issue in the repository.