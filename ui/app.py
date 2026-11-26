import os

import requests
import streamlit as st

# Inside Docker Compose the API is reachable by its service name
API_URL = os.getenv("API_URL", "http://api:8000").rstrip("/")


def predict(features: list[float]) -> str:
    """Send the four measurements to the API and return the species name."""
    response = requests.post(
        f"{API_URL}/predict",
        json={"feature_array": features},
        timeout=10,
    )
    response.raise_for_status()
    return response.json()["prediction"]["class_name"]


st.set_page_config(page_title="Iris Classifier", page_icon="🌸")
st.title("🌸 Iris Species Classifier")
st.write("Enter the flower measurements in centimetres, then press **Predict**.")

with st.form("measurements"):
    left, right = st.columns(2)
    sepal_length = left.number_input(
        "Sepal length (cm)", min_value=0.0, value=5.1, step=0.1
    )
    sepal_width = right.number_input(
        "Sepal width (cm)", min_value=0.0, value=3.5, step=0.1
    )
    petal_length = left.number_input(
        "Petal length (cm)", min_value=0.0, value=1.4, step=0.1
    )
    petal_width = right.number_input(
        "Petal width (cm)", min_value=0.0, value=0.2, step=0.1
    )
    submitted = st.form_submit_button("Predict")

if submitted:
    try:
        with st.spinner("Predicting..."):
            # The API expects the values in exactly this order
            species = predict(
                [sepal_length, sepal_width, petal_length, petal_width]
            )
    except requests.ConnectionError:
        st.error(
            f"Cannot connect to the API at {API_URL}. "
            "Check that the API service is running, then try again."
        )
    except requests.Timeout:
        st.error(f"The API at {API_URL} took too long to respond. Try again.")
    except requests.HTTPError as error:
        st.error(
            f"The API returned an error (HTTP {error.response.status_code}). "
            "Check the API logs for details."
        )
    except (requests.RequestException, ValueError, KeyError, TypeError) as error:
        st.error(f"Could not get a prediction from the API: {error}")
    else:
        st.success(f"Predicted species: **{species}**")
