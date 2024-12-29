import streamlit as st

try:
    import pydicom
    from pydicom.errors import InvalidDicomError
except ModuleNotFoundError:
    st.error("The pydicom library is not installed. Please install it using 'pip install pydicom' and restart the app.")

# Set up the Streamlit app
def main():
    st.title("DICOM Viewer")

    st.write("Upload a DICOM (.dcm or DICOMDIR) file to view its contents.")

    # File uploader
    uploaded_file = st.file_uploader("Choose a DICOM file", type=["dcm", "DICOMDIR"])

    if uploaded_file is not None:
        try:
            # Read the DICOM file
            dicom_file = pydicom.dcmread(uploaded_file, force=True)

            # Display metadata
            st.subheader("DICOM Metadata")
            metadata = {tag: dicom_file[tag].value for tag in dicom_file.dir() if tag in dicom_file}
            st.json(metadata)

            # If the file is a DICOMDIR, display patient and study information
            if hasattr(dicom_file, "DirectoryRecordSequence"):
                st.subheader("Directory Records")
                records = []
                for record in dicom_file.DirectoryRecordSequence:
                    record_info = {
                        "Patient Name": getattr(record, "PatientName", "N/A"),
                        "Study Date": getattr(record, "StudyDate", "N/A"),
                        "Modality": getattr(record, "Modality", "N/A"),
                        "SOP Class UID": getattr(record, "SOPClassUID", "N/A"),
                        "File Name": getattr(record, "ReferencedFileID", "N/A"),
                    }
                    records.append(record_info)
                st.write(records)

        except InvalidDicomError:
            st.error("The uploaded file is not a valid DICOM file.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
