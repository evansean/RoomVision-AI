import streamlit as st
import json
import base64
import requests
import hydralit_components as hc
import time

server_url = "https://a477be354b1a4a1484.gradio.live"


def sketch(prompt, base64_image):
    
    url = server_url + "/sdapi/v1/img2img"

    headers = {
        'Content-Type': 'application/json',
    }

    payload = json.dumps({
        "prompt": prompt,
        "negative_prompt": "text, close up, cropped, out of frame, worst quality, low quality, jpeg artifacts, ugly, duplicate, morbid, mutilated, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, deformed, blurry, dehydrated, bad anatomy, bad proportions, extra limbs, cloned face, disfigured, gross proportions, malformed limbs, missing arms, missing legs, extra arms, extra legs, fused fingers, too many fingers, long neck, watermark",
        "init_images": [base64_image],
        "sampler_name": "DPM++ 2M Karras",
        "steps": 20,
        "cfg_scale": 7,
        "width": 512,
        "height": 512,
        "batch_size": 4,
        "seed": 10948394,
        "denoising_strength": 0.75,
        "override_settings": {
            "sd_model_checkpoint": "realisticVisionV51_v20Novae.safetensors [c0d1994c73]"
        },
        "alwayson_scripts": {
            "controlnet": {
                "args": [
                    {
                        "input_image": base64_image,
                        "module": "mlsd",
                        "model": "control_v11p_sd15_mlsd [aca30ff0]",
                        "weight": 1.0,
                        "guidance_start": 0.0,
                        "guidance_end": 1.0,
                        "control_mode": 0
                    }
                ]
            }
        }
    })

    response = requests.request("POST", url, data=payload, headers=headers)

    images = response.json()["images"]

    print(response)
    print(response.json()['info'])

    return images

def interior(prompt, base64_image):

    url = server_url + "/sdapi/v1/img2img"

    headers = {
        'Content-Type': 'application/json',
    }

    payload = json.dumps({
        "prompt": prompt,
        "negative_prompt": "text, close up, cropped, out of frame, worst quality, low quality, jpeg artifacts, ugly, duplicate, morbid, mutilated, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, deformed, blurry, dehydrated, bad anatomy, bad proportions, extra limbs, cloned face, disfigured, gross proportions, malformed limbs, missing arms, missing legs, extra arms, extra legs, fused fingers, too many fingers, long neck, watermark",
        "init_images": [base64_image],
        "sampler_name": "DPM++ 2M Karras",
        "steps": 20,
        "cfg_scale": 7,
        "width": 512,
        "height": 512,
        "batch_size": 4,
        "seed": -1,
        "denoising_strength": 0.75,
        "override_settings": {
            "sd_model_checkpoint": "realisticVisionV51_v20Novae.safetensors [c0d1994c73]"
        },
        "alwayson_scripts": {
            "controlnet": {
                "args": [
                    {
                        "input_image": base64_image,
                        "module": "segmentation",
                        "model": "control_v11p_sd15_seg [e1f51eb9]",
                        "weight": 1.0,
                        "guidance_start": 0.0,
                        "guidance_end": 1.0,
                        "control_mode": 0
                    },
                    {
                        "input_image": base64_image,
                        "module": "mlsd",
                        "model": "control_v11p_sd15_mlsd [aca30ff0]",
                        "weight": 1.0,
                        "guidance_start": 0.0,
                        "guidance_end": 1.0,
                        "control_mode": 0
                    }
                ]
            }
        }
    })

    response = requests.request("POST", url, data=payload, headers=headers)

    images = response.json()["images"]

    print(response)
    print(response.json()['info'])

    return images



st.set_page_config(layout="wide",page_title="AI Interior Designer")


st.title("AI Interior Designer")

def display_generated_images(image_urls):
    image_url = image_urls[0]
    if image_url.endswith(".png"):
        with col2:
            # st.write("Generated Designs")
            genupp_container, genlow_container = st.columns(2)
            
            # Display images in a grid
            with genupp_container:
                st.image(image_urls[0], use_column_width=True)
                st.image(image_urls[1], use_column_width=True)

            with genlow_container:
                st.image(image_urls[2], use_column_width=True)
                st.image(image_urls[3], use_column_width=True)

    else:
        with col2:
            # st.write("Generated Designs")
            genupp_container, genlow_container = st.columns(2)
            
            # Display images in a grid
            with genupp_container:
                st.image(f"data:image/png;base64,{image_urls[0]}", use_column_width=True)
                st.image(f"data:image/png;base64,{image_urls[1]}", use_column_width=True)

            with genlow_container:
                st.image(f"data:image/png;base64,{image_urls[2]}", use_column_width=True)
                st.image(f"data:image/png;base64,{image_urls[3]}", use_column_width=True)



upper_container = st.container()
lower_container = st.container()


with lower_container:
    col1, col2 = st.columns(2)
    pictype = ""
    with col1:
        image_type = st.radio("Input type", ["Sketch","Image of an interior"])
        if image_type == "Sketch":
            pictype = "a sketch"
        else:
            pictype = "an image of an interior"    
        uploaded_image = st.file_uploader(f"Upload {pictype}", type=["jpg", "png", "jpeg"], disabled=False,label_visibility="visible")
        if uploaded_image is not None:
            st.image(uploaded_image, use_column_width=True)
         
    # Initial image URLs
    image_urls = [
        "https://designclinic.sg/wp-content/uploads/2017/02/Untitled-design-23.png",
        "https://designclinic.sg/wp-content/uploads/2017/02/Untitled-design-23.png",
        "https://designclinic.sg/wp-content/uploads/2017/02/Untitled-design-23.png",
        "https://designclinic.sg/wp-content/uploads/2017/02/Untitled-design-23.png"
    ]

    # Display initial images
    # display_generated_images(image_urls)

    with col2:
        st.header("Generated Designs")
        

with upper_container:
    input_col, button_col = st.columns([0.6,0.4])
    
    with input_col:
        prompt = st.text_input("What are your desired design requirements?", placeholder="Bohemian interior design style with a hint of greenery")

    with button_col:
        fil_col, but_col = st.columns([0.7,0.3])
        with but_col:
            if st.button("Generate", type="primary"):
                if uploaded_image is not None:
                    image_content = uploaded_image.getvalue()
                    base64_image = base64.b64encode(image_content).decode("utf-8")
                    if image_type == "Sketch":
                        image_urls = sketch(prompt, base64_image)
                    else:
                        image_urls = interior(prompt, base64_image)
                    # Refresh images after clicking "Generate"
                    display_generated_images(image_urls)
                else:
                    st.error('Please upload an image', icon="🚨")

                    print("Please upload an image")

def refinePrompt(prompt):
    refinedPrompt = ""
    
    return refinedPrompt