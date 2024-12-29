import streamlit as st
import pydicom
from pydicom.errors import InvalidDicomError

# Set up the Streamlit app
def main():
    st.title("DICOMDIR Viewer")

    st.write("Upload a DICOMDIR file to view its contents.")

    # File uploader
    uploaded_file = st.file_uploader("Choose a DICOMDIR file", type=["DICOMDIR"])

    if uploaded_file is not None:
        try:
            # Read the DICOMDIR file
            dicomdir = pydicom.dcmread(uploaded_file, force=True)

            # Display metadata
            st.subheader("DICOMDIR Metadata")
            metadata = {tag: dicomdir[tag].value for tag in dicomdir.dir() if tag in dicomdir}
            st.json(metadata)

            # Display patient and study information
            if hasattr(dicomdir, "DirectoryRecordSequence"):
                st.subheader("Directory Records")
                records = []
                for record in dicomdir.DirectoryRecordSequence:
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
            st.error("The uploaded file is not a valid DICOMDIR file.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
