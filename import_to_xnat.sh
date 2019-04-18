    
#!/bin/bash

# Send in one raw_zip subject directory and this script does the following
# 1. Figure out who the subject is
# 2. Reorganize the directory structure in a temp directory
# 3. Rename sub directories to match PPMI event codes (Baseline ==> BL)
# 4. Upload to Nunda (XNAT)

set -x

# Put your own username
XNAT_USER="mayankmalik01"

# Put your own password
XNAT_PASS=''

XNAT_ROOT='https://nunda.northwestern.edu:8443/nunda'

SUBJECT_DATA_DIR=$1

if [ -d "$1" ]; then
  SUBJECT=$(basename $SUBJECT_DATA_DIR)
  if [[ $SUBJECT =~ ^[0-9]+$ ]]; then 
    echo "SUBJECT_DATA_DIR=$SUBJECT_DATA_DIR, SUBJECT=$SUBJECT"
  else 
    echo "Could not extract a numerical value for SUBJECT from $SUBJECT_DATA_DIR"
  fi

else
  echo "$SUBJECT_DATA_DIR is not a directory"
  exit
fi

# Create Subject
echo "Creating subject: $SUBJECT"
curl -u ${XNAT_USER}:${XNAT_PASS} -X PUT "${XNAT_ROOT}/data/projects/PPMI_SWEDD_DL/subjects/${SUBJECT}" 

# Create tmp directory and zip files with correct structure into this directory
TMPDIR=$(mktemp -d)
trap "rm -r $TMPDIR" EXIT
cd ${TMPDIR}

for session_dir in ${SUBJECT_DATA_DIR}/*
do
  session=${session_dir##*/} 
  code="BL"
  if [ ${code} ]; then
    echo "Session=$session, Code=$code"
    echo "Starting to zip"
    # copy the zip files with all sessions into the temp directory
    cp -r "${session_dir}" ${TMPDIR}/${code}
    ZIP_SESSION_FILE="${TMPDIR}/${SUBJECT}_${code}.zip"
    zip -r ${ZIP_SESSION_FILE} "${code}"
    ls -al $ZIP_SESSION_FILE
    echo "Ready to upload zipped session file"
    curl -u ${XNAT_USER}:${XNAT_PASS} -X POST --form project=PPMI_SWEDD_DL \
    	--form subject=${SUBJECT} \
    	--form session=${SUBJECT}_${code} \
    	--form image_archive=@${ZIP_SESSION_FILE} \
    	"${XNAT_ROOT}/data/services/import"
    echo "Uploaded zipped session file"
  else
       echo "Unknown code for ${session_dir}. Skipping..."
  fi
done
