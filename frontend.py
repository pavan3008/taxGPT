from gpt import process
import streamlit as st
import base64
import os


st.set_page_config(page_title= "UncleSamTax" , page_icon= "💰" , layout="wide")


def save_uploaded_file(uploaded_file, directory):
    if uploaded_file is not None:
        os.makedirs(directory, exist_ok=True)
        with open(os.path.join(directory, uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())
        return os.path.join(directory, uploaded_file.name)
    return None


def displayImage(image_path):
    # Check if the image exists
    if not os.path.exists(image_path):
        print(image_path)
        st.info("Give us your info so we can display it here.")
        return

    # Display the image
    st.image(image_path, width=700)
    
def display_images_from_folder(folder_path):
    images = os.listdir(folder_path)
    for image_name in images:
        image_path = os.path.join(folder_path, image_name)
        st.image(image_path, caption=image_name, use_column_width=True)


def displayPDF(uploaded_file):
    # Read file as bytes:
    bytes_data = uploaded_file.getvalue()
    # Convert to utf-8
    base64_pdf = base64.b64encode(bytes_data).decode("utf-8")
    # Embed PDF in HTML
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="300" type="application/pdf"></iframe>'
    # Display file
    st.markdown(pdf_display, unsafe_allow_html=True)


def main():
    image_path = 'final'
    st.header("💰_Uncle Sam Tax_  💰", divider="rainbow", help="Help?", anchor=False)
    # st.title( )
    # Split the window into two columns
    col1, col2 = st.columns(2)
    # Col1
    with col1:
        st.header("1️⃣: Hey, give me your info 🫵 ", anchor=False)
        tab1, tab2 = st.tabs(["Input", "Preview"])

        with tab1:
            st.subheader("How much money did you make? (W2 form)")
            st.caption('Your employer should have given it to you!')
            uploaded_file_w2 = st.file_uploader(
                "Choose Files",
                type="pdf",
                accept_multiple_files=True,
                help="Please submit your W-2",
                label_visibility="hidden",
            )
            st.subheader("Upload your last year's return (1040)")
            st.caption('Skip if you did not file taxes. Shame on you!')
            uploaded_file_1040 = st.file_uploader(
                "Choose Files",
                type="pdf",
                accept_multiple_files=True,
                help="Please submit 1040 from the previous year",
                label_visibility="hidden",
            )

            if st.button("Submit"):
                # print(uploaded_file_w2, uploaded_file_1040)
                file_paths = []
                if uploaded_file_w2:
                    for file in uploaded_file_w2:
                        uploaded_w2_path = save_uploaded_file(file, "w2_forms")
                        file_paths.append(uploaded_w2_path)
                if uploaded_file_1040:
                    for file in uploaded_file_1040:
                        uploaded_1040_path = save_uploaded_file(file, "past_1040_forms")
                        file_paths.append(uploaded_1040_path)
                        
                # Final Run:
                process()

        with tab2:
            st.header("Preview of your uploaded forms")
            if uploaded_file_w2:
                for file in uploaded_file_w2:
                    print(file)
                    displayPDF(file)

            if uploaded_file_1040:
                for file in uploaded_file_1040:
                    displayPDF(file)

    # Col2
    with col2:
        st.header("2️⃣: Now, file your taxes💰", anchor=False)
        tab3, tab4 = st.tabs(["Filled Form", "Download/E-File"])

        with tab3:
            st.subheader("Preview of your prepared tax form.")
            st.caption('Double check and dont mess up. Uncle sam will come after you')
            # displayImage(image_path)
            display_images_from_folder(image_path)


        with tab4:
            st.header("Use us to E-File for you")
            st.button("Download to SnailMail it")
            st.button("E-File Now")


if __name__ == "__main__":
    main()