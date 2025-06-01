$(document).ready(function() {
    const uploadForm = $('#upload-form');
    const imageUpload = $('#image-upload');
    const generateBtn = $('#generate-btn');
    const previewContainer = $('#preview-container');
    const previewImage = $('#preview-image');
    const loading = $('#loading');
    const result = $('#result');
    const captionText = $('#caption-text');
    const error = $('#error');

    // Prevent form submission
    uploadForm.on('submit', function(e) {
        e.preventDefault();
        return false;
    });

    // Handle file selection
    imageUpload.on('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            // Show preview
            const reader = new FileReader();
            reader.onload = function(e) {
                previewImage.attr('src', e.target.result);
                previewContainer.removeClass('hidden');
                generateBtn.prop('disabled', false);
                result.addClass('hidden');
                error.addClass('hidden');
            };
            reader.readAsDataURL(file);
        }
    });

    // Handle generate button click
    generateBtn.on('click', function() {
        const file = imageUpload[0].files[0];
        if (!file) return;

        // Show loading state
        loading.removeClass('hidden');
        generateBtn.prop('disabled', true);
        result.addClass('hidden');
        error.addClass('hidden');

        // Create form data
        const formData = new FormData();
        formData.append('image', file);

        // Send request
        $.ajax({
            url: '/generate_caption',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                loading.addClass('hidden');
                result.removeClass('hidden');
                
                // Split caption and hashtags
                const [caption, hashtags] = response.caption.split('\n\n');
                
                // Format caption with hashtags
                captionText.html(
                    caption + '<br><br><span class="text-blue-500">' + hashtags + '</span>'
                );
            },
            error: function(xhr, status, errorThrown) {
                loading.addClass('hidden');
                generateBtn.prop('disabled', false);
                error.removeClass('hidden').text('Error: ' + (xhr.responseJSON?.error || 'Failed to generate caption'));
            }
        });
    });

    // Handle drag and drop
    const dropZone = $('label[for="image-upload"]');
    
    dropZone.on('dragover', function(e) {
        e.preventDefault();
        $(this).addClass('border-blue-600');
    });

    dropZone.on('dragleave', function(e) {
        e.preventDefault();
        $(this).removeClass('border-blue-600');
    });

    dropZone.on('drop', function(e) {
        e.preventDefault();
        $(this).removeClass('border-blue-600');
        
        const file = e.originalEvent.dataTransfer.files[0];
        if (file && file.type.startsWith('image/')) {
            imageUpload[0].files = e.originalEvent.dataTransfer.files;
            imageUpload.trigger('change');
        }
    });
}); 