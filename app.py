import os
import logging
from flask import Flask, request, jsonify, render_template, send_from_directory
from PIL import Image
import torch
import torch.nn.functional as F
from torchvision import transforms
from torchvision.models import resnet50, ResNet50_Weights

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load the model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = resnet50(weights=ResNet50_Weights.DEFAULT).to(device)
model.eval()

# Image preprocessing
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Template sentences for social media style captions
caption_templates = [
    "Capturing moments of {} in perfect detail! 📸",
    "Living for this amazing {} moment! ✨",
    "When you spot the perfect {} 👀",
    "Just vibing with this beautiful {} 🌟",
    "Can't get enough of this {} aesthetic 💫",
    "Found this incredible {} and had to share! 🎯",
    "Major {} energy right here! 🔥",
    "This {} is everything! 💯",
    "POV: You just discovered the most amazing {} ⭐",
    "Main character energy with this {} 🌈"
]

def generate_caption(image_path):
    try:
        # Load and process the image
        image = Image.open(image_path)
        if image.mode != "RGB":
            image = image.convert(mode="RGB")

        # Prepare inputs
        input_tensor = preprocess(image)
        input_batch = input_tensor.unsqueeze(0).to(device)

        # Generate predictions
        with torch.no_grad():
            output = model(input_batch)
            probabilities = F.softmax(output[0], dim=0)
            top5_prob, top5_catid = torch.topk(probabilities, 5)

        # Get class names
        class_names = ResNet50_Weights.DEFAULT.meta["categories"]
        
        # Get the most confident prediction
        main_object = class_names[top5_catid[0]].split(',')[0].strip()
        
        # Generate a social media style caption
        import random
        caption_template = random.choice(caption_templates)
        caption = caption_template.format(main_object)
        
        # Generate hashtags
        hashtags = [f"#{name.split(',')[0].strip().replace(' ', '')}" for name in [class_names[idx] for idx in top5_catid]]
        hashtags = ' '.join(hashtags[:5])  # Limit to 5 hashtags

        return f"{caption}\n\n{hashtags}"

    except Exception as e:
        logger.error(f"Error processing image {image_path}: {str(e)}")
        raise

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/generate_caption', methods=['POST'])
def generate_caption_endpoint():
    if 'image' not in request.files:
        logger.warning("No image file in request")
        return jsonify({'error': 'No image provided'}), 400
    
    file = request.files['image']
    if file.filename == '':
        logger.warning("Empty filename in request")
        return jsonify({'error': 'No selected file'}), 400

    if file:
        try:
            # Save the uploaded file
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)
            logger.info(f"File saved successfully: {filename}")

            # Generate caption
            caption = generate_caption(filename)
            logger.info(f"Caption generated successfully: {caption}")

            return jsonify({
                'caption': caption,
                'image_url': f'/uploads/{file.filename}'
            })
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 