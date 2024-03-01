#!/usr/bin/env bash

SCRIPTS_PATH=$(realpath "$0")
SCRIPTS_DIR=$(dirname "${SCRIPTS_PATH}")

SCRIPT="python3 ${SCRIPTS_DIR}/mongo-crud-cats.py --dotenv ${SCRIPTS_DIR}/.env"

function get_first_id_by_name() {
    local name=$1
    local id=$(${SCRIPT} --action read --name "${name}" \
                        | awk -F ',' 'NR == 1 {print $1}' \
                        | awk -F"'" '{print $4}')
    echo ${id}
}

echo "[*] Create cat Marquise..."
${SCRIPT} --action create --name "Marquise" --age 3 --features "black and white" "smart and cute"

echo "[*] Create cat Timka..."
${SCRIPT} --action create --name "Timka" --age 7 --features "ginger and white" "smart and fluffy"

echo "[*] Create cat Kuzia..."
${SCRIPT} --action create --name "Kuzia" --age 10 --features "tiger coloring" "smart and fluffy"

echo "[*] Read cat Marquise..."
${SCRIPT} --action read --name "Marquise"

echo "[*] Read cat Timka..."
${SCRIPT} --action read --name "Timka"

echo "[*] Read cat Kuzia..."
${SCRIPT} --action read --name "Kuzia"

echo "[*] Read all cats..."
${SCRIPT} --action read

echo "[*] Update cat Marquise..."
${SCRIPT} --action update --id $(get_first_id_by_name "Marquise") --age 4 --features "wise and perfect character"

echo "[*] Update cat Timka..."
${SCRIPT} --action update --id $(get_first_id_by_name "Timka") --age 8 --features "cute and ginger daredevil"

echo "[*] Update cat Kuzia..."
${SCRIPT} --action update --id $(get_first_id_by_name "Kuzia") --age 11 --features "wise and fluffy"

echo "[*] Read all cats again..."
${SCRIPT} --action read

echo "[*] Delete cat Marquise..."
${SCRIPT} --action delete --id $(get_first_id_by_name "Marquise")

echo "[*] Read all cats again..."
${SCRIPT} --action read

echo "[*] Delete all records..."
${SCRIPT} --action delete-all

echo "[*] Read all cats..."
${SCRIPT} --action read
