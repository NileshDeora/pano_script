def validate_object(obj):
    # Define the required keys and their expected file extensions
    required_keys = {
        'main_vw': ['.jpg', '.jpeg', '.png','.webp','.mp4'],
        'other_vw1': ['.jpg', '.jpeg', '.png','.webp','.mp4']
    }

    # Check if all required keys are in the object
    if not all(key in obj for key in required_keys):
        raise ValueError("Object is missing one or more required parameters.")

    # Validate each field against its expected file extensions
    for key, extensions in required_keys.items():
        if not any(obj[key].lower().endswith(ext) for ext in extensions):
            raise ValueError(f"The '{key}' field does not have a valid file extension: {extensions}")

    return True

    