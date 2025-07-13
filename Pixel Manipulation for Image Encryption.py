from PIL import Image
import numpy as np
import io
import base64
import IPython.display
import ipywidgets as widgets
from IPython.display import display

file_upload = widgets.FileUpload(accept='image/*', multiple=False)
key_input = widgets.BoundedIntText(value=0, min=0, max=255, description="Key (0–255)")
seed_input = widgets.IntText(value=0, description="Shuffle Seed (int)")
encrypt_button = widgets.Button(description="Encrypt Image")

ui = widgets.VBox([file_upload, key_input, seed_input, encrypt_button])
display(ui)

def encrypt_image(image_data, key, seed):
    image = Image.open(io.BytesIO(image_data))
    arr = np.array(image)
    flat = arr.reshape(-1, arr.shape[-1])
    np.random.seed(seed)
    indices = np.arange(flat.shape[0])
    np.random.shuffle(indices)
    shuffled = flat[indices].astype('int16')
    shuffled = (shuffled + key) % 256
    encrypted_arr = shuffled.reshape(arr.shape).astype('uint8')
    encrypted_img = Image.fromarray(encrypted_arr)
    output_path = "encrypted_image.png"
    encrypted_img.save(output_path)
    with open(output_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    link = widgets.HTML(f'<a download="encrypted_image.png" href="data:image/png;base64,{encoded}" target="_blank">Download Encrypted Image</a>')
    display(widgets.HTML("<b>Download</b>"))
    display(link)

def handle_encrypt(b):
    if not file_upload.value:
        print("No image uploaded.")
        return
    uploaded_file = next(iter(file_upload.value.values()))
    key = key_input.value
    seed = seed_input.value
    encrypt_image(uploaded_file['content'], key, seed)

encrypt_button.on_click(handle_encrypt)
