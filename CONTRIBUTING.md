# Contributing to SWOT Water Depth Analysis

Thank you for your interest in contributing to this project! This document provides guidelines and instructions for contributing.

## How to Contribute

### 1. Report Issues

Found a bug? Have a suggestion? Please open an issue on GitHub:
- Clearly describe the problem
- Include error messages or screenshots
- Provide steps to reproduce the issue
- Mention your Python version and OS

### 2. Suggest Enhancements

We welcome feature requests and improvements:
- Describe the enhancement and why it would be useful
- Provide examples of how it would be used
- Reference relevant papers or external resources

### 3. Submit Code Changes

#### Fork & Clone
```bash
# Fork the repository on GitHub
# Clone your fork
git clone https://github.com/YOUR_USERNAME/SWOT_CooperFlood.git
cd SWOT_CooperFlood
```

#### Create a Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

#### Make Your Changes
- Write clear, documented code
- Add comments for complex logic
- Follow PEP 8 style guide
- Test your changes before submitting

#### Commit & Push
```bash
git add your_changes
git commit -m "Clear description of changes"
git push origin feature/your-feature-name
```

#### Create a Pull Request
- Go to GitHub and create a pull request
- Describe your changes clearly
- Reference any related issues
- Ensure tests pass before submitting

## Code Standards

### Python Style
- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep lines under 100 characters

### Jupyter Notebooks
- Add markdown cells to explain each processing step
- Use descriptive variable names
- Comment complex calculations
- Include print statements for key results
- Clean up cell outputs before committing

### Documentation
- Update README.md if functionality changes
- Add docstrings to new functions
- Document parameter types and return values
- Include usage examples

## Development Setup

### Prerequisites
- Python 3.8+
- Git
- NASA Earthdata account (for SWOT data)
- Google Earth Engine account (for Sentinel-2 data)

### Installation for Development
```bash
# Clone repository
git clone https://github.com/akr706/SWOT_CooperFlood.git
cd SWOT_CooperFlood

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install numpy pandas geopandas shapely xarray rasterio earthengine-api geemap earthaccess pyproj matplotlib scipy netCDF4

# Authentication
# Add NASA credentials to ~/.netrc (chmod 600)
# Place GEE service account JSON in repository
```

## Testing

Before submitting a PR, please test:
1. Run the full notebook sequentially
2. Check for kernel crashes or errors
3. Verify output files are created correctly
4. Validate depth values are reasonable
5. Test with different study areas if possible

## Documentation

When adding new features:
1. Add docstrings to functions
2. Update README.md with new parameters or functionality
3. Add usage examples in comments
4. Update CHANGELOG.md

Example docstring:
```python
def your_function(param1, param2):
    """
    Brief description of function.
    
    Parameters
    ----------
    param1 : type
        Description of param1
    param2 : type
        Description of param2
    
    Returns
    -------
    output : type
        Description of output
    
    Examples
    --------
    >>> result = your_function(value1, value2)
    """
    # Implementation
    pass
```

## Reporting Bugs

Include:
- Descriptive title
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Error message (full traceback if available)
- Python version
- Operating system
- Relevant dependencies versions

## Feature Requests

Include:
- Clear title
- Detailed description
- Motivation and use case
- Suggested implementation (optional)
- Related papers or references

## Questions?

- Check existing issues and discussions
- Review the README.md for common questions
- Ask on GitHub discussions (if available)
- Contact maintainers if needed

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Acknowledgments

Thank you for contributing to improve this project!

---

**Repository**: https://github.com/akr706/SWOT_CooperFlood  
**Maintainer**: akr706
