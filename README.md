# Social Media Style Image Caption Generator

A Flask web application that generates engaging social media style captions for images using AI. The application uses ResNet50 for image recognition and combines the results with creative templates to generate captions that are perfect for social media posts.

## Features

- Upload images through a modern web interface
- Generate social media style captions automatically
- Add relevant hashtags based on image content
- Real-time image preview
- Mobile-responsive design
- Instagram-like post preview

## Tech Stack

- Python 3.13
- Flask 3.0.2
- PyTorch
- TorchVision
- Pillow
- HTML/CSS/JavaScript
- Tailwind CSS

## Installation

1. Clone the repository:
```bash
git clone https://github.com/sachinnegi01/social-media-caption-generator.git
cd social-media-caption-generator
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

5. Open your browser and navigate to `http://127.0.0.1:5000`

## Usage

1. Click the "Select an image" button or drag and drop an image
2. Wait for the caption to be generated
3. The result will be displayed in an Instagram-like post format
4. Copy and use the generated caption and hashtags for your social media posts

## Project Structure

```
social-media-caption-generator/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── static/               # Static files
│   ├── css/             # CSS files
│   └── js/              # JavaScript files
├── templates/           # HTML templates
│   └── index.html      # Main page template
└── uploads/            # Uploaded images directory
```

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add new feature'`)
5. Push to the branch (`git push origin feature/improvement`)
6. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 